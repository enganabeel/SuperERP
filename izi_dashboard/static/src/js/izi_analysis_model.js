/** @odoo-module */
// NOTE: see izi_dashboard_controller_legacy.js - web.AbstractModel has no
// Odoo 18 equivalent. Reference-only, not registered in the manifest.
import AbstractModel from "@web/legacy/js/views/abstract_model";

export const IZIAnalysisModel = AbstractModel.extend({
    init: function () {
        this._super.apply(this, arguments);
    },
});

export default IZIAnalysisModel;
