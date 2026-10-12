# -*- coding: utf-8 -*-
{
    'name': 'HR Department Tree Report',
    'summary': 'Printable, styled report of the department hierarchy',
    'description': """
HR Department Tree Report
==========================
Odoo doesn't ship a printable report of the department structure. This
module adds one: select one or more departments (Employees > Departments)
and use Print > Department Tree, or use Employees > Reporting > Department
Tree to print the whole company hierarchy in one go.

Each department is shown nested under its parent with a manager name and
employee headcount, styled as a clean indented org tree rather than a flat
list.
""",
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Ejad Tech',
    'website': 'https://ejadtech.sa',
    'license': 'LGPL-3',
    'depends': ['hr'],
    'data': [
        'reports/hr_department_tree_report.xml',
        'views/hr_department_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
