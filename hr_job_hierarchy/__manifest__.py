# -*- coding: utf-8 -*-
{
    'name': 'HR Job Hierarchy',
    'summary': 'Reports-To hierarchy between Job Positions, plus interactive and printable tree views (by position and by department)',
    'description': """
HR Job Hierarchy
=================
Adds a "Reports To" field on Job Position so positions can be linked into
a reporting chain, independent of the department tree.

Provides, for both the position-reporting hierarchy and the existing
department hierarchy:
- A native Hierarchy view (Employees > Reporting > Jobs by Parent Job /
  Jobs by Department), same box-and-connector widget as the stock
  Departments Hierarchy view. Requires whatever app/module already
  provides that <hierarchy> view type on this database (it was already
  in use for Departments when this module was written) -- if that is
  ever uninstalled, these two menu items will need to be revisited.
- An interactive, expandable tree page inside Odoo (Employees > Reporting)
  built with plain HTML, as a fallback that needs no extra view type.
- A printable QWeb PDF report, in the same visual style as the Department
  Tree report.

Also adds two "org" (web_org) chart views, colored by hierarchy depth
with an Available (light yellow) override: Positional Structure for Job
Positions, and Department Structure for Departments -- both under
Employees > Reporting, separate from department_chart_types' own
dept_type-colored Departments Org Chart.

And a plain HTML/CSS "Department Structure Report" (no chart widget
involved), built to match the LOC Positional Structure PDF layout:
Committee-typed departments render beside their parent in a sideways
chain instead of below it, everything else is a normal top-down tree
colored by dept_type, using the same "PDF-matched" colors
department_chart_types already defines.
""",
    'version': '18.0.1.0.39',
    'category': 'Human Resources',
    'author': 'Ejad Tech',
    'website': 'https://ejadtech.sa',
    'license': 'LGPL-3',
    'depends': ['hr_recruitment', 'web_org', 'department_chart_types'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_job_views.xml',
        'views/hr_job_hierarchy_templates.xml',
        'views/hr_job_native_hierarchy_views.xml',
        'views/hr_job_org_views.xml',
        'views/hr_job_positional_structure_sector_wizard_views.xml',
        'views/hr_department_org_views.xml',
        'views/hr_department_structure_report_templates.xml',
        'reports/hr_job_hierarchy_report.xml',
        'reports/hr_job_by_department_report.xml',
        'reports/hr_department_structure_report.xml',
        'views/hr_department_structure_report_wizard_views.xml',
        'views/hr_job_hierarchy_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_job_hierarchy/static/src/scss/org_view.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
