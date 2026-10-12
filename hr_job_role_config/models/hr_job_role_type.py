# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJobRoleType(models.Model):
    _name = 'hr.job.role.type'
    _description = 'Job Role Type'
    _order = 'name'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A role type with this name already exists.'),
    ]
