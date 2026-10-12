# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2020-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################

from odoo import models, fields, tools, api, exceptions, _

class HRLeaveType(models.Model):
    _inherit = 'hr.leave.type'
    
    unpaid_leave = fields.Boolean(string='Unpaid Leave', default=False)