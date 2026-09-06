# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeStatusUpdate(models.Model):
    _name = "committee.status.update"
    _description = "Committee Periodic Status Update"
    _order = "date desc, id desc"

    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    current_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("archived", "Archived"),
            ("rejected", "Rejected"),
        ],
        string="Current Committee State",
    )
    update_type = fields.Selection(
        [
            ("periodic", "Periodic Update"),
            ("warning", "Warning Notice"),
        ],
        string="Update Type",
        default="periodic",
        required=True,
    )
    statement = fields.Text(string="Statement")
    date = fields.Date(string="Date", default=fields.Date.context_today)
    user_id = fields.Many2one("res.users", string="Updated By", default=lambda self: self.env.user)
