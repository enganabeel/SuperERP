# -*- coding: utf-8 -*-
import base64
from datetime import datetime
from urllib.parse import quote

from odoo import api, fields, models

try:
    from num2words import num2words
except ImportError:
    num2words = None


def _tlv_encode(tag, value):
    value_bytes = (value or "").encode("utf-8")
    return bytes([tag, len(value_bytes)]) + value_bytes


class AccountMove(models.Model):
    _inherit = "account.move"

    amount_discount_total = fields.Monetary(
        string="Total Discounts",
        compute="_compute_amount_discount_total",
        currency_field="currency_id",
    )
    speed_pro_qr_code = fields.Char(
        string="ZATCA QR Code (base64 TLV)",
        compute="_compute_speed_pro_qr_code",
    )
    speed_pro_qr_code_url = fields.Char(
        string="ZATCA QR Code Image URL",
        compute="_compute_speed_pro_qr_code",
    )
    amount_total_words_en = fields.Char(
        string="Total in Words (English)",
        compute="_compute_amount_total_words",
    )
    amount_total_words_ar = fields.Char(
        string="Total in Words (Arabic)",
        compute="_compute_amount_total_words",
    )

    @api.depends("invoice_line_ids.price_unit", "invoice_line_ids.quantity", "invoice_line_ids.discount")
    def _compute_amount_discount_total(self):
        for move in self:
            lines = move.invoice_line_ids.filtered(lambda l: not l.display_type)
            move.amount_discount_total = sum(
                line.price_unit * line.quantity * (line.discount or 0.0) / 100.0
                for line in lines
            )

    @api.depends("company_id.name", "company_id.vat", "invoice_date", "amount_total", "amount_tax")
    def _compute_speed_pro_qr_code(self):
        for move in self:
            if not move.company_id.vat or not move.invoice_date:
                move.speed_pro_qr_code = False
                move.speed_pro_qr_code_url = False
                continue
            time_val = (move.create_date or fields.Datetime.now()).time()
            timestamp = datetime.combine(move.invoice_date, time_val).strftime("%Y-%m-%dT%H:%M:%SZ")
            tlv = (
                _tlv_encode(1, move.company_id.name)
                + _tlv_encode(2, move.company_id.vat)
                + _tlv_encode(3, timestamp)
                + _tlv_encode(4, "%.2f" % move.amount_total)
                + _tlv_encode(5, "%.2f" % move.amount_tax)
            )
            qr_value = base64.b64encode(tlv).decode()
            move.speed_pro_qr_code = qr_value
            move.speed_pro_qr_code_url = "/report/barcode/QR/%s?width=120&height=120" % quote(qr_value, safe="")

    @api.depends("amount_total", "currency_id")
    def _compute_amount_total_words(self):
        for move in self:
            currency_name_en = "Saudi Riyals" if move.currency_id.name == "SAR" else (move.currency_id.name or "")
            currency_name_ar = "ريالاً سعودياً" if move.currency_id.name == "SAR" else (move.currency_id.name or "")
            integer_part = int(move.amount_total)
            fraction_part = round((move.amount_total - integer_part) * 100)

            words_en = str(integer_part)
            words_ar = str(integer_part)
            if num2words:
                try:
                    words_en = num2words(integer_part, lang="en").replace("-", " ").title()
                except Exception:
                    pass
                try:
                    words_ar = num2words(integer_part, lang="ar")
                except Exception:
                    pass

            text_en = "%s %s only" % (words_en, currency_name_en)
            text_ar = "فقط %s %s لا غير" % (words_ar, currency_name_ar)

            if fraction_part:
                frac_words_en = str(fraction_part)
                if num2words:
                    try:
                        frac_words_en = num2words(fraction_part, lang="en").replace("-", " ").title()
                    except Exception:
                        pass
                text_en = "%s %s and %s Halalas only" % (words_en, currency_name_en, frac_words_en)
                text_ar = "فقط %s %s و%s هللة لا غير" % (words_ar, currency_name_ar, fraction_part)

            move.amount_total_words_en = text_en
            move.amount_total_words_ar = text_ar
