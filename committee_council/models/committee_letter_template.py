# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeMinutesLetterTemplate(models.Model):
    _name = "committee.minutes.letter.template"
    _description = "Minutes Letter Template"

    name = fields.Char(required=True)
    applies_to = fields.Selection(
        [("minutes", "Minutes")],
        string="Applies On",
        default="minutes",
        required=True,
    )
    subject = fields.Char(string="Subject")
    body = fields.Html(string="Body", sanitize=False)
    active = fields.Boolean(default=True)

    def render_for_minutes(self, minutes):
        self.ensure_one()
        placeholders = {
            "object.committee_id.name": minutes.committee_id.name or "",
            "object.minutes_number": minutes.name or "",
            "object.approval_transfer_date": fields.Date.to_string(minutes.approval_transfer_date or "") or "",
            "object.review_notes": minutes.review_notes or "",
            "object.name": minutes.name or "",
        }
        content = self.body or ""
        for token, value in placeholders.items():
            content = content.replace(token, value)
        return content
