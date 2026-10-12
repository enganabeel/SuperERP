# -*- coding: utf-8 -*-
from odoo import fields, models


class HrDepartmentStructureReportWizard(models.TransientModel):
    _name = 'hr.department.structure.report.wizard'
    _description = 'Department Structure by Sector'

    department_id = fields.Many2one(
        'hr.department', string='Sector', required=True,
        help='A Sector or any other department. The report shows this '
             'department and everything under it.',
    )

    def action_show_report(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/department_structure_report?department_id=%d' % self.department_id.id,
            'target': 'new',
        }
