# -*- coding: utf-8 -*-
from odoo import fields, models


class WhistleblowingCategory(models.Model):
    _name = 'whistleblowing.category'
    _description = 'Whistleblowing Incident Category'
    _order = 'sequence, name'

    name = fields.Char(string='Category', required=True, translate=True)
    sequence = fields.Integer(default=10)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color')
    report_count = fields.Integer(string='Reports', compute='_compute_report_count')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'This incident category already exists.'),
    ]

    def _compute_report_count(self):
        grouped = self.env['whistleblowing.report']._read_group(
            [('category_id', 'in', self.ids)], ['category_id'], ['__count']
        )
        mapped = {category.id: count for category, count in grouped}
        for record in self:
            record.report_count = mapped.get(record.id, 0)
