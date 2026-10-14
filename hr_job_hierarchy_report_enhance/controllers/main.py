# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from .tree import build_nodes


class PositionalStructureReport(http.Controller):

    @staticmethod
    def _to_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _descendants(root):
        """``root`` plus every job reporting to it, directly or not (cycle safe)."""
        result = root
        frontier = root
        while frontier:
            frontier = request.env['hr.job'].search(
                [('parent_id', 'in', frontier.ids)]) - result
            result |= frontier
        return result

    @http.route('/positional_structure_report', type='http', auth='user')
    def positional_structure_report(self, department_id=None, job_id=None, **kw):
        env = request.env
        job_id = self._to_int(job_id)
        department_id = self._to_int(department_id)

        if job_id:
            # A job: show it and everybody below it, down to the lowest position.
            root_job = env['hr.job'].browse(job_id).exists()
            if not root_job:
                return request.not_found()
            jobs = self._descendants(root_job)
            roots = build_nodes(jobs, lambda j: j.parent_id.id, top=root_job)
        elif department_id:
            # A department: show it with every job of it and of its sub-departments.
            department = env['hr.department'].browse(department_id).exists()
            if not department:
                return request.not_found()
            departments = env['hr.department'].search([('id', 'child_of', department.id)])
            jobs = env['hr.job'].search([('department_id', 'in', departments.ids)])
            roots = [{
                'name': department.name or '',
                'sub': '',
                'css': 'dsr_ceo',
                'children': build_nodes(jobs, lambda j: j.parent_id.id),
            }]
        else:
            return request.not_found()

        return request.render(
            'hr_job_hierarchy_report_enhance.positional_structure_report_page',
            {'roots': roots},
        )
