# -*- coding: utf-8 -*-
from odoo import fields, models


class CommitteeMember(models.Model):
    _name = "committee.member"
    _description = "Committee Member"
    _order = "sequence, id"

    committee_id = fields.Many2one("committee.committee", string="Committee", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", string="Member", required=True)
    role_id = fields.Many2one("committee.member.role", string="Role Classification")
    agency_id = fields.Many2one("committee.agency", string="Agency")
    email = fields.Char(related="user_id.email", readonly=True)
    phone = fields.Char(related="user_id.phone", readonly=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
