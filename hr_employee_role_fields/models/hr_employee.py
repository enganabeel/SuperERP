# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    role_id = fields.Char(string='Role ID')
    tournament_time_role_id = fields.Many2one('hr.job.tournament.time.role', string='Tournament Time Role')
    role_level = fields.Char(string='Level')
    line_manager_role_id = fields.Char(string='Line Manager Role ID')
    employee_category = fields.Selection(
        selection=[
            ('corporate', 'Corporate'),
            ('tournament_time', 'Tournament Time'),
        ],
        string='Employee Category',
    )
    role_status = fields.Selection(
        selection=[
            ('filled', 'Filled'),
            ('vacant', 'Vacant'),
            ('replacement', 'Replacement'),
            ('onboarding', 'Onboarding'),
        ],
        string='Role Status',
    )
    contractor_type = fields.Selection(
        selection=[
            ('tbp', 'TBP'),
            ('loc', 'LOC'),
            ('freeze', 'Freeze'),
            ('loc_seconded', 'LOC - Seconded'),
            ('secondee', 'Secondee'),
        ],
        string='Contractor',
    )
    emp_id = fields.Char(string='EMP ID')
    secondment_entity = fields.Char(string='Secondment Entity')
    nationality_category = fields.Selection(
        selection=[
            ('saudi', 'Saudi'),
            ('non_saudi', 'Non-Saudi'),
        ],
        string='Nationality Category',
    )
    work_city = fields.Selection(
        selection=[
            ('riyadh', 'Riyadh'),
            ('jeddah', 'Jeddah'),
            ('khobar', 'Khobar'),
            ('roaming', 'Roaming'),
            ('on_hold', 'On Hold'),
        ],
        string='City',
    )
