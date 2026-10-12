# -*- coding: utf-8 -*-
from odoo import fields, models


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    org_sector = fields.Char(string='Sector')
    org_executive_department = fields.Char(string='Executive Department')
    org_department = fields.Char(string='Department')
    org_function = fields.Char(string='Function')
    org_source_type = fields.Selection(
        selection=[
            ('loc_fte', 'LOC FTE'),
            ('outsource', 'Outsource'),
            ('secondee', 'Secondee'),
            ('volunteer', 'Volunteer'),
        ],
        string='Source Type',
    )
    org_title_high_level = fields.Char(string='Title - High Level')
    org_level = fields.Char(string='Level')
    org_role_status = fields.Selection(
        selection=[
            ('filled', 'Filled'),
            ('vacant', 'Vacant'),
        ],
        string='Role Status',
    )
    org_line_manager_role_id = fields.Char(string='Line Manager role ID')
