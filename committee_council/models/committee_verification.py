# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeVerification(models.Model):
    _name = "committee.verification"
    _description = "Committee Verification Checklist Item"
    _order = "sequence, id"

    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    name = fields.Char(string="Item", required=True)
    sequence = fields.Integer(default=10)
    verified = fields.Boolean(string="Verified")
    verification_date = fields.Date(string="Verification Date")
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")
    notes = fields.Char(string="Notes")
