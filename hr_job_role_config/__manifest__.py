# -*- coding: utf-8 -*-
{
    'name': 'HR Job Position - Role Configuration',
    'version': '18.0.1.0.0',
    'summary': 'Add Role Type, Role ID, Source Type, Role Status and Tournament Time Role to Job Positions',
    'category': 'Human Resources/Recruitment',
    'depends': ['hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_job_role_type_views.xml',
        'views/hr_job_source_type_views.xml',
        'views/hr_job_tournament_time_role_views.xml',
        'views/hr_job_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
