# -*- coding: utf-8 -*-
from odoo import fields, models


class WhistleblowingPartyType(models.Model):
    _name = 'whistleblowing.party.type'
    _description = 'Whistleblowing Party Type Involved'
    _order = 'sequence, name'

    name = fields.Char(string='Party Type', required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'This party type already exists.'),
    ]
