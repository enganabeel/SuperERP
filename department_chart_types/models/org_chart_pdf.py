"""Print the org chart exactly as it is previewed on screen.

The chart is a Highcharts organization series whose cards are HTML data
labels layered over the SVG, so neither Highcharts' own SVG export nor a
server-side re-draw reproduces what the user is actually looking at. The
browser therefore rasterises the live, already-filtered chart (html2canvas)
and posts the PNG here; this side only wraps it in a titled, fit-to-page PDF.
"""

import base64
import binascii
import io
import logging
import os
import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_datetime

from reportlab.lib.pagesizes import A0, A1, A2, A3, A4, landscape, portrait
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

from PIL import Image

_logger = logging.getLogger(__name__)

_DATA_URL_RE = re.compile(r'^data:image/png;base64,', re.IGNORECASE)

# The client already caps its capture, but it is the one number a caller could
# push arbitrarily high, so bound it here too.
MAX_IMAGE_BYTES = 32 * 1024 * 1024

# Fit-to-page walks these in order and stops at the first sheet that renders
# the capture at MIN_FIT_RATIO or more of its natural on-screen size - a wide
# chart lands on A2 rather than shrinking to an unreadable smudge on A4.
PAPER_SIZES = {'A4': A4, 'A3': A3, 'A2': A2, 'A1': A1, 'A0': A0}
PAPER_LADDER = ('A4', 'A3', 'A2')
MIN_FIT_RATIO = 0.6

# CSS pixels are 96 per inch, PDF points 72.
PX_TO_PT = 72.0 / 96.0

MARGIN = 12 * mm
HEADER_HEIGHT = 17 * mm
FOOTER_HEIGHT = 8 * mm

# Helvetica is Latin-1 only, which mangles any non-Western department name that
# made it into the title or the filter line. Prefer a wide-coverage TTF when the
# host has one. (Glyph coverage only - reportlab does no Arabic/Indic shaping;
# the chart image itself is browser-rendered, so it is unaffected either way.)
_TTF_CANDIDATES = (
    ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
     '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
    ('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
     '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'),
    ('/usr/share/fonts/dejavu/DejaVuSans.ttf',
     '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf'),
)


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    # ------------------------------------------------------------------
    # Entry point (called over RPC by the org view's "Print PDF" button)
    # ------------------------------------------------------------------

    def action_print_org_chart_pdf(self, image_data, title=None,
                                   filter_description=None, css_width=0,
                                   css_height=0, paper=None, orientation=None):
        """Wrap a client-side capture of the org chart in a PDF and hand it back.

        :param str image_data: PNG data URL (or bare base64) of the chart.
        :param str title: heading for the sheet; defaults to the model name.
        :param str filter_description: the search facets that were active, so
            the printout says which slice of the hierarchy it shows.
        :param int css_width: on-screen size of the captured area, in CSS px.
            Used to scale the capture back to its natural size, independently
            of the pixel ratio the browser rasterised it at.
        :param str paper: 'A4'/'A3'/'A2'/'A1'/'A0', or None to pick one.
        :param str orientation: 'landscape'/'portrait', or None to pick one.
        :return: an ``ir.actions.act_url`` downloading the generated PDF.
        """
        self.check_access('read')

        image = self._org_chart_decode_png(image_data)
        pdf = self._org_chart_render_pdf(
            image,
            title=title or _("Org Chart"),
            filter_description=filter_description,
            css_width=css_width,
            css_height=css_height,
            paper=paper,
            orientation=orientation,
        )

        filename = '%s - %s.pdf' % (
            (title or _("Org Chart")).replace('/', '-'),
            fields.Date.context_today(self),
        )
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'datas': base64.b64encode(pdf),
            'mimetype': 'application/pdf',
            # res_id stays empty on purpose: ir.attachment.check() then limits
            # the attachment to whoever created it, which is exactly right for
            # a one-off download.
            'res_model': self._name,
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }

    # ------------------------------------------------------------------
    # Image
    # ------------------------------------------------------------------

    @api.model
    def _org_chart_decode_png(self, image_data):
        """Validate the posted data URL and return a flattened RGB image."""
        if not image_data or not isinstance(image_data, str):
            raise UserError(_("The chart could not be captured, so there is nothing to print."))

        payload = _DATA_URL_RE.sub('', image_data.strip())
        if len(payload) > MAX_IMAGE_BYTES:
            raise UserError(_(
                "This chart is too large to print in one go. Filter it down "
                "to a smaller part of the hierarchy and try again."
            ))
        try:
            raw = base64.b64decode(payload, validate=True)
            image = Image.open(io.BytesIO(raw))
            image.load()
        except (binascii.Error, ValueError, OSError) as err:
            _logger.warning("Invalid org chart capture posted: %s", err)
            raise UserError(_("The captured chart image could not be read.")) from err

        # html2canvas returns RGBA; flatten onto white so the PDF has no
        # transparency and prints the way the screen looks.
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGBA')
            flattened = Image.new('RGB', image.size, (255, 255, 255))
            flattened.paste(image, mask=image.split()[-1])
            image = flattened
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        return image

    # ------------------------------------------------------------------
    # PDF
    # ------------------------------------------------------------------

    @api.model
    def _org_chart_fonts(self):
        """(regular, bold) font names, registering a TTF pair if one is around."""
        registered = pdfmetrics.getRegisteredFontNames()
        if 'OrgChartSans' in registered:
            return 'OrgChartSans', 'OrgChartSans-Bold'
        for regular_path, bold_path in _TTF_CANDIDATES:
            if not (os.path.exists(regular_path) and os.path.exists(bold_path)):
                continue
            try:
                pdfmetrics.registerFont(TTFont('OrgChartSans', regular_path))
                pdfmetrics.registerFont(TTFont('OrgChartSans-Bold', bold_path))
            except Exception:  # noqa: BLE001 - a broken font must not stop a print
                _logger.warning("Could not register %s for the org chart PDF", regular_path)
                break
            return 'OrgChartSans', 'OrgChartSans-Bold'
        return 'Helvetica', 'Helvetica-Bold'

    @api.model
    def _org_chart_page_setup(self, natural_width, natural_height, paper, orientation):
        """Pick sheet and orientation, then return them with the image box."""
        if orientation not in ('landscape', 'portrait'):
            orientation = 'landscape' if natural_width >= natural_height else 'portrait'
        turn = landscape if orientation == 'landscape' else portrait

        ladder = (paper,) if paper in PAPER_SIZES else PAPER_LADDER
        chosen = ladder[-1]
        for name in ladder:
            page_width, page_height = turn(PAPER_SIZES[name])
            box_width = page_width - 2 * MARGIN
            box_height = page_height - 2 * MARGIN - HEADER_HEIGHT - FOOTER_HEIGHT
            fit = min(box_width / natural_width, box_height / natural_height)
            if fit >= MIN_FIT_RATIO:
                chosen = name
                break

        page_width, page_height = turn(PAPER_SIZES[chosen])
        return page_width, page_height, page_width - 2 * MARGIN, \
            page_height - 2 * MARGIN - HEADER_HEIGHT - FOOTER_HEIGHT

    @api.model
    def _org_chart_render_pdf(self, image, title, filter_description,
                              css_width, css_height, paper, orientation):
        image_width, image_height = image.size

        # Prefer the on-screen CSS size: the browser may have rasterised at 2x
        # for sharpness, and that must not shrink the drawing on the page.
        natural_width = (css_width or image_width) * PX_TO_PT
        natural_height = (css_height or image_height) * PX_TO_PT
        if natural_width <= 0 or natural_height <= 0:
            raise UserError(_("The captured chart image is empty."))

        page_width, page_height, box_width, box_height = self._org_chart_page_setup(
            natural_width, natural_height, paper, orientation)

        fit = min(box_width / natural_width, box_height / natural_height)
        draw_width = natural_width * fit
        draw_height = natural_height * fit

        font, font_bold = self._org_chart_fonts()
        buffer = io.BytesIO()
        pdf = rl_canvas.Canvas(buffer, pagesize=(page_width, page_height))
        pdf.setPageCompression(1)
        pdf.setTitle(title)
        pdf.setCreator('Odoo')

        self._org_chart_draw_header(
            pdf, page_width, page_height, title, filter_description, font, font_bold)
        self._org_chart_draw_footer(pdf, page_width, font)

        pdf.drawImage(
            ImageReader(image),
            MARGIN + (box_width - draw_width) / 2.0,
            MARGIN + FOOTER_HEIGHT + (box_height - draw_height) / 2.0,
            width=draw_width,
            height=draw_height,
            preserveAspectRatio=True,
            anchor='c',
        )

        pdf.showPage()
        pdf.save()
        return buffer.getvalue()

    @api.model
    def _org_chart_fit_text(self, pdf, text, font, size, max_width):
        """Truncate `text` with an ellipsis so it fits `max_width` at `size`."""
        text = (text or '').replace('\n', ' ').strip()
        if not text or pdf.stringWidth(text, font, size) <= max_width:
            return text
        ellipsis = '…'
        while text and pdf.stringWidth(text + ellipsis, font, size) > max_width:
            text = text[:-1]
        return text + ellipsis

    @api.model
    def _org_chart_draw_header(self, pdf, page_width, page_height, title,
                               filter_description, font, font_bold):
        top = page_height - MARGIN
        right_edge = page_width - MARGIN

        stamp = _(
            "Printed %(date)s by %(user)s",
            date=format_datetime(self.env, fields.Datetime.now()),
            user=self.env.user.display_name,
        )
        pdf.setFont(font, 8)
        pdf.setFillGray(0.4)
        stamp_width = pdf.stringWidth(stamp, font, 8)
        pdf.drawRightString(right_edge, top - 9, stamp)

        pdf.setFont(font_bold, 14)
        pdf.setFillGray(0.1)
        pdf.drawString(MARGIN, top - 11, self._org_chart_fit_text(
            pdf, title, font_bold, 14, right_edge - MARGIN - stamp_width - 8 * mm))

        # The whole point of "print what I am previewing": say which slice it is.
        line = filter_description or _("No filter - full hierarchy")
        pdf.setFont(font, 8.5)
        pdf.setFillGray(0.4)
        pdf.drawString(MARGIN, top - 24, self._org_chart_fit_text(
            pdf, line, font, 8.5, right_edge - MARGIN))

        rule = page_height - MARGIN - HEADER_HEIGHT + 4 * mm
        pdf.setStrokeGray(0.8)
        pdf.setLineWidth(0.5)
        pdf.line(MARGIN, rule, right_edge, rule)
        pdf.setFillGray(0)

    @api.model
    def _org_chart_draw_footer(self, pdf, page_width, font):
        pdf.setFont(font, 7.5)
        pdf.setFillGray(0.5)
        pdf.drawString(MARGIN, MARGIN, self.env.company.display_name or '')
        pdf.drawRightString(page_width - MARGIN, MARGIN, _("Page 1 of 1"))
        pdf.setFillGray(0)
