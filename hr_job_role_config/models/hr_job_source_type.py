# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJobSourceType(models.Model):
    _name = 'hr.job.source.type'
    _description = 'Job Source Type'
    _order = 'name'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A source type with this name already exists.'),
    ]
