# -*- coding: utf-8 -*-
{
    'name': "HR Attendance Sheet And Policies For Odoo Community",

    'summary': """Managing  Attendance Sheets for Employees for odoo community
        """,
    'description': """
        Employees Attendance Sheet Management  For Odoo Community  
    """,
    'author': "CDS Solutions SRL,Ramadan Khalil",
    'website': "www.cdsegypt.com",
    'contributors': [
        'Ramadan Khalil <rkhalil1990@gmail.com>',
    ],
    'price': 120,
    'currency': 'USD',

    'category': 'hr',
    'version': '17.0',
    'images': ['static/description/banner.gif'],

    'depends': ['base',
                'hr',
                'hr_contract',
                'hr_payroll_community',
                'hr_holidays',
                'hr_attendance'],
    'data': [
        'data/ir_sequence.xml',
        'data/data.xml',
        'data/ir_cron.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/change_att_data_view.xml',
        'views/hr_attendance_sheet_view.xml',
        'views/hr_attendance_policy_view.xml',
        'views/hr_contract_view.xml',
        'views/hr_public_holiday_view.xml',
        'views/attendance_sheet_batch_view.xml',
        'views/hr_leave_type.xml',
        'views/hr_payslip_view.xml',

    ],

    'license': 'OPL-1',
    'demo': [
        'demo/demo.xml',
    ],
}
