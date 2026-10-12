{
    'name': 'Whistleblowing',
    'version': '18.0.1.0.10',
    'summary': 'Confidential whistleblowing / incident reporting management',
    'description': """
Whistleblowing Management
==========================
Confidentially collect, triage and investigate whistleblowing reports.

Features
--------
* Public / employee submission of whistleblowing reports (with optional anonymity)
* Configurable Incident Categories and Party Types involved
* Full investigation workflow (Draft > Submitted > Under Review > Investigating > Closed / Rejected)
* List, Form, Kanban and Pivot views
* Rich search & filtering on every field
* Confidential access rules restricting visibility to authorized officers only
* Attachments / supporting evidence, chatter & activities
""",
    'category': 'Human Resources/Compliance',
    'author': 'Ejad Tech',
    'website': 'https://www.ejadtech.sa',
    'license': 'LGPL-3',
    'depends': ['mail', 'portal', 'website'],
    'data': [
        'security/whistleblowing_security.xml',
        'security/ir.model.access.csv',
        'data/whistleblowing_sequence.xml',
        'data/whistleblowing_category_data.xml',
        'data/whistleblowing_party_type_data.xml',
        'views/whistleblowing_category_views.xml',
        'views/whistleblowing_party_type_views.xml',
        'views/whistleblowing_report_views.xml',
        'views/whistleblowing_portal.xml',
        'views/whistleblowing_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
