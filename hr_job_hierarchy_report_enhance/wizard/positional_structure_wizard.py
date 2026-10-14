# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrJobPositionalReportWizard(models.TransientModel):
    _name = 'hr.job.positional.report.wizard'
    _description = 'Positional Structure By Sector'

    department_id = fields.Many2one('hr.department', string='Department')
    job_id = fields.Many2one('hr.job', string='Job Position')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.job_id = False

    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id:
            self.department_id = False

    def action_show_report(self):
        self.ensure_one()
        if self.job_id:
            url = '/positional_structure_report?job_id=%d' % self.job_id.id
        elif self.department_id:
            url = '/positional_structure_report?department_id=%d' % self.department_id.id
        else:
            raise UserError(_('Please select a department or a job position.'))
        return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new'}
