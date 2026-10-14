# -*- coding: utf-8 -*-
{
    'name': 'HR Job Hierarchy - Department Structure Report Enhancements',
    'summary': 'Cleaner layout, N-1..N-4 level colours, wider cards and a branded header '
               'for the Department Structure report',
    'description': """
Department Structure report enhancements
=========================================

Extends ``hr_job_hierarchy`` (by inheritance, the base module is not modified):

* Fixes overlapping cards (CEO assistants / committee chains) and misaligned
  connector lines.
* Card colours follow the real level order: N-1 (first level, e.g. Operations),
  then N-2, N-3 and N-4.
* Wider cards (one CSS variable, ``--dsr-grow``).
* Branded header: logo + company name + report title.
""",
    'category': 'Human Resources',
    'version': '18.0.1.0.8',
    'author': 'Ejad Tech',
    'license': 'LGPL-3',
    'depends': ['hr_job_hierarchy'],
    'data': [
        'views/department_structure_report_templates.xml',
        'views/positional_structure_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_job_hierarchy_report_enhance/static/src/css/org_levels.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
