# -*- coding: utf-8 -*-
import time
import logging
from odoo import api, models, _, fields

class invoice_type(models.Model):
    _inherit = 'account.move'
    is_customs_inv = fields.Boolean()