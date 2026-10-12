# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrJob(models.Model):
    _inherit = 'hr.job'

    parent_id = fields.Many2one(
        'hr.job', string='Reports To',
        domain="[('id', '!=', id)]",
        help='The job position this position reports to, independent of the department hierarchy.',
    )
    child_ids = fields.One2many('hr.job', 'parent_id', string='Direct Reports')
    color = fields.Integer(string='Color Index', default=0)
    is_available = fields.Boolean(
        string='Available',
        help='Marked positions are highlighted light yellow on the Positional Structure org chart.',
    )
    is_ceo_office = fields.Boolean(
        string='CEO Office',
        help='Marked positions are colored grey on the Positional Structure org chart, '
             'same grey as a Committee department, regardless of their level in the '
             'Reports-To chain. Available still takes priority over this if both are checked.',
    )
    chart_layout = fields.Selection(
        selection=[
            ('normal', 'Horizontal'),
            ('hanging', 'Vertical'),
        ],
        string='Chart Layout',
        help="How this position's direct reports are arranged in the Positional Structure "
             "org chart.\nHorizontal: they sit side by side in the row below.\n"
             "Vertical: they are stacked and progressively indented under this box, and "
             "so is everything further below them, unless one of them is set back to "
             "Horizontal.\nLeft blank: follows whatever the nearest ancestor above it "
             "set (Highcharts' own inheritance) -- deliberately not defaulted to "
             "Horizontal, which would block that inheritance for every node.",
    )

    hierarchy_level = fields.Integer(
        string='Hierarchy Level', compute='_compute_hierarchy_level', store=True,
        help='Depth in the Reports-To chain: 0 for a position with no parent, '
             'parent\'s level + 1 otherwise.',
    )
    chart_color_class = fields.Char(
        string='Chart Color Class', compute='_compute_chart_color_class', store=True,
        help='CSS class for the Positional Structure org chart card, derived from '
             'hierarchy_level (capped at 4, so anything 4 levels below a root shares '
             'the deepest color band).',
    )
    needed_employees = fields.Integer(
        string='Needed Employees', compute='_compute_needed_employees', store=True,
        help='Target minus the current number of employees in this position. '
             'Negative when there are more employees than the target.',
    )

    @api.depends('no_of_recruitment', 'no_of_employee')
    def _compute_needed_employees(self):
        for job in self:
            job.needed_employees = (job.no_of_recruitment or 0) - (job.no_of_employee or 0)

    @api.depends('parent_id', 'parent_id.hierarchy_level')
    def _compute_hierarchy_level(self):
        for job in self:
            job.hierarchy_level = (job.parent_id.hierarchy_level + 1) if job.parent_id else 0

    @api.depends('hierarchy_level')
    def _compute_chart_color_class(self):
        for job in self:
            level = min(job.hierarchy_level or 0, 4)
            job.chart_color_class = f'o_org_job_level_{level}'

    @api.constrains('parent_id')
    def _check_parent_id_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create a recursive hierarchy of job positions.'))

    def action_view_job_employees(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Employees'),
            'res_model': 'hr.employee',
            'view_mode': 'kanban,list,form',
            'domain': [('job_id', '=', self.id)],
            'context': {'default_job_id': self.id, 'default_department_id': self.department_id.id},
        }
