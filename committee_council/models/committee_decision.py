# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeDecision(models.Model):
    _name = "committee.decision"
    _description = "Committee Decision"
    _order = "date desc, id desc"

    name = fields.Char(string="Subject", required=True)
    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    meeting_id = fields.Many2one("committee.meeting", string="Meeting")
    date = fields.Date(string="Date", default=fields.Date.context_today)
    recipient = fields.Char(string="Recipient")
    stage = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("closed", "Closed"),
        ],
        default="new",
        string="Stage",
    )
    notes = fields.Text(string="Notes")
