# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJob(models.Model):
    _inherit = 'hr.job'

    role_type_id = fields.Many2one('hr.job.role.type', string='Role Type')
    role_id = fields.Char(string='Role ID')
    source_type_id = fields.Many2one('hr.job.source.type', string='Source Type')
    role_status = fields.Selection(
        selection=[
            ('onboarded', 'Onboarded'),
            ('not_deployed', 'Not Deployed for Tournament'),
            ('filled', 'Filled'),
            ('vacant', 'Vacant'),
            ('replacement', 'Replacement'),
            ('onboarding', 'Onboarding'),
        ],
        string='Role Status',
    )
    tournament_time_role_id = fields.Many2one('hr.job.tournament.time.role', string='Tournament Time Role')
