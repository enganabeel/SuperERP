{
    "name": "Department Chart Types",
    "version": "1.0.1",
    "category": "Tools",
    "summary": "Department hierarchy with chart types, sub-tree filtering, type colors and a PDF printout.",
    "license": "LGPL-3",
    # web_editor ships the html2canvas build the org chart is captured with.
    "depends": ["base", "hr", "web_org", "web_editor"],
    "data": [
        "security/ir.model.access.csv",
        "security/department_security.xml",
        "views/department_views.xml",
        "views/department_search_views.xml",
        "views/department_org_views.xml",
        "views/menus.xml",
        "data/department_types.xml",
    ],
    'assets': {
            'web.assets_backend': [
                'department_chart_types/static/src/scss/org_view.scss',
                'department_chart_types/static/src/org_print/org_print.js',
                'department_chart_types/static/src/org_print/org_print.xml',
            ],
        },
    "installable": True,
    "application": True,
}
