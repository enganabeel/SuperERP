# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    # Adds to department_chart_types' own dept_type/dept_type_branch
    # Selection (both share the same options list there) -- a department
    # typed CEO Assistant renders beside its parent the same way a
    # Committee does, just mirrored to the other side (left instead of
    # right). dept_type_branch is a computed mirror of dept_type, so it
    # needs the same new option or its compute raises on a CEO Assistant
    # record.
    dept_type = fields.Selection(
        selection_add=[('ceo_assistant', 'CEO Assistant')],
        ondelete={'ceo_assistant': 'set default'},
    )
    dept_type_branch = fields.Selection(
        selection_add=[('ceo_assistant', 'CEO Assistant')],
    )

    job_count = fields.Integer(string='Job Position Count', compute='_compute_job_count')

    hierarchy_level = fields.Integer(
        string='Hierarchy Level', compute='_compute_hierarchy_level', store=True,
        help='Depth in the department tree: 0 for a department with no parent, '
             'parent\'s level + 1 otherwise.',
    )
    chart_color_class = fields.Char(
        string='Chart Color Class', compute='_compute_chart_color_class', store=True,
        help='CSS class for the Department Structure org chart card, derived from '
             'hierarchy_level (capped at 4, so anything 4 levels below a root shares '
             'the deepest color band).',
    )
    is_available = fields.Boolean(
        string='Available',
        help='Marked departments are highlighted light yellow on the Department Structure org chart.',
    )
    job_list_text = fields.Text(
        string='Job Positions (list)', compute='_compute_job_list_text',
        help='Distinct job position titles in this department, with a count for any '
             'title held by more than one job record, one per line. Shown on the '
             '"Jobs by Department" org chart card.',
    )

    @api.depends('parent_id', 'parent_id.hierarchy_level')
    def _compute_hierarchy_level(self):
        for department in self:
            department.hierarchy_level = (
                department.parent_id.hierarchy_level + 1 if department.parent_id else 0
            )

    @api.depends('hierarchy_level')
    def _compute_chart_color_class(self):
        for department in self:
            level = min(department.hierarchy_level or 0, 4)
            department.chart_color_class = f'o_org_dept_level_{level}'

    def _compute_job_count(self):
        job_data = self.env['hr.job']._read_group(
            [('department_id', 'in', self.ids), ('active', '=', True)],
            ['department_id'], ['__count'],
        )
        counts = {department.id: count for department, count in job_data}
        for department in self:
            department.job_count = counts.get(department.id, 0)

    def _compute_job_list_text(self):
        title_data = self.env['hr.job']._read_group(
            [('department_id', 'in', self.ids), ('active', '=', True)],
            ['department_id', 'name'], ['__count'],
        )
        titles_by_dept = {}
        for department, name, count in title_data:
            titles_by_dept.setdefault(department.id, []).append((name or _('(untitled)'), count))
        for department in self:
            titles = sorted(titles_by_dept.get(department.id, []))
            lines = [f'{name} x{count}' if count > 1 else name for name, count in titles]
            department.job_list_text = '\n'.join(f'• {line}' for line in lines)

    def action_view_department_jobs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Job Positions'),
            'res_model': 'hr.job',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }

    def action_apply_committee_layout(self):
        """Manually-triggered (button on the CEO department's form): parents
        every dept_type='committee' department under whichever department is
        dept_type='ceo', and pins each one to its own chart_column row right
        after the CEO's, so they hang in a column beside the CEO instead of
        dropping into its normal (horizontal) children row -- matching the
        LOC Positional Structure PDF layout, purely by Department Type, no
        hardcoded department IDs or names.

        Deliberately a button you click, not something that fires silently
        on every save: re-run it after adding/removing a committee-typed
        department and it recomputes the pins from scratch.
        """
        ceo = self.env['hr.department'].search([('dept_type', '=', 'ceo')], limit=1)
        if not ceo:
            raise UserError(_('No department is set to Department Type "CEO". Set one first.'))

        committees = self.env['hr.department'].search([
            ('dept_type', '=', 'committee'), ('id', '!=', ceo.id),
        ], order='sequence, name')
        if not committees:
            raise UserError(_('No department is set to Department Type "Committee".'))

        committees.write({'parent_id': ceo.id, 'chart_layout': 'normal'})
        if ceo.chart_layout != 'normal':
            ceo.chart_layout = 'normal'

        row = ceo.chart_column or 0
        for committee in committees:
            row += 1
            committee.chart_column = row

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Committee layout applied'),
                'message': _('%(count)s committee department(s) linked to %(ceo)s.', count=len(committees), ceo=ceo.name),
                'type': 'success',
            },
        }
