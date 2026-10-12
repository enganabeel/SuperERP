# -*- coding: utf-8 -*-
{
    'name': 'HR Department Org Reference Fields',
    'summary': 'Adds Sector / Executive Department / Function / role-source reference fields to Departments',
    'description': """
HR Department Org Reference Fields
====================================
Extends hr.department (does not replace it) with reference fields carried
over from the organization's master-data spreadsheet, so that data can live
directly on the department record instead of only in a spreadsheet:

- Sector
- Executive Department
- Department (as named in the source master data)
- Function
- Source Type (LOC FTE / Outsource)
- Title - High Level
- Level
- Role Status (Filled / Vacant)
- Line Manager role ID

All fields are shown in a new "Organizational Reference" section on the
Department form view (Employees > Configuration > Departments).
""",
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'author': 'Ejad Tech',
    'website': 'https://ejadtech.sa',
    'license': 'LGPL-3',
    'depends': ['hr'],
    'data': [
        'views/hr_department_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
