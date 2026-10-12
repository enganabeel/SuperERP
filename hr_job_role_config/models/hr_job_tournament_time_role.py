# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJobTournamentTimeRole(models.Model):
    _name = 'hr.job.tournament.time.role'
    _description = 'Tournament Time Role'
    _order = 'name'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A tournament time role with this name already exists.'),
    ]
