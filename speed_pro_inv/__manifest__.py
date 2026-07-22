# -*- coding: utf-8 -*-
{
    "name": "Speed Pro Sales Tax Invoice",
    "summary": "Bilingual (Arabic/English) ZATCA-style sales tax invoice report.",
    "version": "18.0.1.0.0",
    "author": "Speed Pro",
    "license": "LGPL-3",
    "category": "Accounting/Accounting",
    "depends": ["account"],
    "external_dependencies": {
        "python": ["num2words"],
    },
    "data": [
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
        "report/report_invoice.xml",
        "report/report_invoice_template.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "speed_pro_inv/static/src/scss/invoice.scss",
        ],
    },
    "installable": True,
    "application": False,
}
