/** @odoo-module */
// NOTE: see izi_dashboard_controller_legacy.js - web.AbstractController has
// no Odoo 18 equivalent. Reference-only, not registered in the manifest.
import AbstractController from "@web/legacy/js/views/abstract_controller";

export const IZIAnalysisController = AbstractController.extend({
    init: function (parent, model, renderer, params) {
        params.viewType = "izianalysis";
        this._super.apply(this, arguments);
    },
});

export default IZIAnalysisController;
