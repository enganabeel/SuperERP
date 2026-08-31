# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeSupportRequest(models.Model):
    _name = "committee.support.request"
    _description = "Committee Support Request"
    _inherit = ["mail.thread"]
    _order = "id desc"

    name = fields.Char(string="Subject", required=True, tracking=True)
    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    assigned_department = fields.Char(string="Assigned Department")
    request_date = fields.Date(string="Request Date", default=fields.Date.context_today)
    description = fields.Html(string="Description")
    state = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        default="new",
        tracking=True,
    )
