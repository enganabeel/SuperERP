# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    building_no = fields.Char(related="partner_id.building_no", readonly=False, store=True)
    district = fields.Char(related="partner_id.district", readonly=False, store=True)
    additional_no = fields.Char(related="partner_id.additional_no", readonly=False, store=True)
