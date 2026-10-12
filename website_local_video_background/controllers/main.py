# -*- coding: utf-8 -*-
import base64
import json
from urllib.parse import quote

from odoo import http
from odoo.http import request


class WebsiteLocalVideoBackgroundController(http.Controller):

    @http.route('/website_local_video_background/upload_video', type='http',
                auth='user', methods=['POST'], website=True)
    def upload_local_background_video(self, video_file=None, **kw):
        """Upload a video file as a public ir.attachment and return its URL,
        for use as a self-hosted snippet background video."""

        def _json(payload, status=200):
            return request.make_response(
                json.dumps(payload),
                headers=[('Content-Type', 'application/json')],
                status=status,
            )

        if not request.env.user.has_group('website.group_website_designer'):
            return _json({'error': 'Access denied.'}, status=403)

        if not video_file:
            return _json({'error': 'No file provided.'}, status=400)

        if not (video_file.content_type or '').startswith('video/'):
            return _json({'error': 'Only video files are allowed.'}, status=400)

        attachment = request.env['ir.attachment'].sudo().create({
            'name': video_file.filename,
            'datas': base64.b64encode(video_file.read()),
            'res_model': 'ir.attachment',
            'public': True,
            'mimetype': video_file.content_type,
        })
        # Include the filename in the URL (Odoo's own
        # /web/content/<id>/<filename> route, see addons/web/controllers/
        # binary.py) so it ends in the real file extension -- both this
        # module's own "is this a local video file" checks and the fact
        # that browsers/players often rely on the extension to guess the
        # format need that, not just the bare /web/content/<id>.
        return _json({
            'url': '/web/content/%s/%s' % (attachment.id, quote(video_file.filename)),
        })
