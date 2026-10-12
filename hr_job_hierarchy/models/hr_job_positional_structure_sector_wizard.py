# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class HrJobPositionalStructureSectorWizard(models.TransientModel):
    _name = 'hr.job.positional.structure.sector.wizard'
    _description = 'Positional Structure by Sector'

    department_id = fields.Many2one(
        'hr.department', string='Sector', required=True,
        help='A Sector or any other department -- its parent included. The '
             'chart opens scoped to this department and everything under it.',
    )

    def action_show_chart(self):
        self.ensure_one()
        departments = self.env['hr.department'].search([('id', 'child_of', self.department_id.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': _('Positional Structure - %s', self.department_id.name),
            'res_model': 'hr.job',
            'view_mode': 'org,kanban,list,form',
            'views': [(self.env.ref('hr_job_hierarchy.hr_job_view_org').id, 'org')],
            'domain': [('department_id', 'in', departments.ids)],
        }
