# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CommitteeMinutes(models.Model):
    _name = "committee.minutes"
    _description = "Committee Minutes"
    _inherit = ["mail.thread"]
    _order = "id desc"

    name = fields.Char(string="Minutes No.", copy=False, readonly=True, default="New")
    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    meeting_id = fields.Many2one("committee.meeting", string="Meeting")
    topic_ids = fields.Many2many("committee.topic", string="Topics Discussed")
    recommendations = fields.Html(string="Recommendations")
    signature_ids = fields.One2many("committee.minutes.signature", "minutes_id", string="Member Signatures")
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")

    letter_template_id = fields.Many2one("committee.minutes.letter.template", string="Letter Template")
    body = fields.Html(string="Minutes Body")

    review_authority_id = fields.Many2one("committee.review.authority", string="Review Authority")
    review_notes = fields.Text(string="Review Authority Notes")
    adoption_authority_id = fields.Many2one("committee.adoption.authority", string="Adoption Authority")
    adoption_notes = fields.Text(string="Adoption Authority Notes")
    approval_transfer_date = fields.Date(string="Approval Transfer Date")

    state = fields.Selection(
        [
            ("draft", "New"),
            ("review", "Under Review"),
            ("approved", "Approved"),
        ],
        default="draft",
        tracking=True,
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("committee.minutes") or "New"
        return super().create(vals_list)

    def action_send_for_review(self):
        self.write({"state": "review"})

    def action_approve(self):
        self.write({"state": "approved"})

    def action_reset_draft(self):
        self.write({"state": "draft"})


class CommitteeMinutesSignature(models.Model):
    _name = "committee.minutes.signature"
    _description = "Committee Minutes Signature"

    minutes_id = fields.Many2one("committee.minutes", string="Minutes", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", string="Member", required=True)
    signed = fields.Boolean(string="Signed")
    signed_date = fields.Datetime(string="Signed On")
