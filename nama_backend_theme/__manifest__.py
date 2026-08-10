# -*- coding: utf-8 -*-
{
    "name": "Nama Backend Theme",
    "summary": "Applies the نماء visual design (navy/mint palette, Tajawal typography, rounded cards) to Odoo's real backend: sidebar, menus, forms, lists, kanban and login.",
    "version": "18.0.1.0.0",
    "author": "Speed Pro",
    "license": "LGPL-3",
    "category": "Themes/Backend",
    "depends": ["clarity_backend_theme_bits"],
    "data": [],
    "assets": {
        "web.assets_frontend": [
            "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;600;700;800&display=swap",
            "nama_backend_theme/static/src/scss/login.scss",
        ],
        "web.assets_backend": [
            "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;600;700;800&display=swap",
            "nama_backend_theme/static/src/scss/variables.scss",
            "nama_backend_theme/static/src/scss/sidebar.scss",
            "nama_backend_theme/static/src/scss/topbar.scss",
            "nama_backend_theme/static/src/scss/components.scss",
        ],
    },
    "installable": True,
    "application": True,
}
