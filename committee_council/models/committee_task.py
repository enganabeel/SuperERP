# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeTask(models.Model):
    _name = "committee.task"
    _description = "Committee Task"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, id"

    name = fields.Char(string="Task Name", required=True, tracking=True)
    sequence = fields.Integer(default=10)
    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    assigned_user_id = fields.Many2one("res.users", string="Assigned To", tracking=True)
    deadline = fields.Date(string="Deadline")
    priority = fields.Selection(
        [("0", "Normal"), ("1", "Low"), ("2", "High"), ("3", "Urgent")], default="0", string="Priority"
    )
    stage = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("review", "Under Review"),
            ("done", "Done"),
        ],
        default="new",
        tracking=True,
        copy=False,
    )
    description = fields.Html(string="Description")
    notes = fields.Text(string="Notes")
