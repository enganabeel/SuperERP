/** @odoo-module */
// NOTE: web.AbstractController was removed from Odoo core after 16.0 and has
// no direct replacement, so this import cannot resolve on Odoo 18. This file
// is a syntax-modernized reference only (odoo.define -> @odoo-module) and is
// not registered in the manifest. The active Dashboard view for Odoo 18 is
// izi_dashboard_controller.js + izi_dashboard_view.js.
import AbstractController from "@web/legacy/js/views/abstract_controller";

export const IZIDashboardController = AbstractController.extend({
    init: function (parent, model, renderer, params) {
        params.viewType = "izidashboard";
        this._super.apply(this, arguments);
    },
});

export default IZIDashboardController;
