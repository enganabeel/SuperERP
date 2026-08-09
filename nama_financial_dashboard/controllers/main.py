# -*- coding: utf-8 -*-
import os

from odoo import http
from odoo.http import request

_DASHBOARD_HTML_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "static", "src", "dashboard.html"
)


class NamaFinancialDashboardController(http.Controller):

    @http.route("/nama/dashboard", type="http", auth="user")
    def dashboard(self, **kwargs):
        with open(_DASHBOARD_HTML_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return request.make_response(content, headers=[("Content-Type", "text/html; charset=utf-8")])
