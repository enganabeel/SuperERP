# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    building_no = fields.Char(string="Building No.")
    district = fields.Char(string="District")
    additional_no = fields.Char(string="Additional No.")
