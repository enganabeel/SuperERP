# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJob(models.Model):
    _inherit = 'hr.job'

    level = fields.Selection(
        [('1', 'N-1'), ('2', 'N-2'), ('3', 'N-3'), ('4', 'N-4'),
         ('ceo_office', 'N-CEO-Office')],
        string='Level',
        help="Drives the card colour in the Positional Structure By Sector report.",
    )
