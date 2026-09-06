/** @odoo-module */
// NOTE: web.AbstractView / web.view_registry were removed from Odoo core
// after 16.0 and have no Odoo 18 equivalent. This file is a
// syntax-modernized reference only (odoo.define -> @odoo-module) and is not
// registered in the manifest. The active Analysis view type registration
// for Odoo 18 is izi_analysis_view.js (registry.category("views")).
import AbstractView from "@web/legacy/js/views/abstract_view";
import viewRegistry from "@web/legacy/js/views/view_registry";
import IZIAnalysisModel from "@izi_dashboard/js/izi_analysis_model";
import IZIAnalysisController from "@izi_dashboard/js/izi_analysis_controller_legacy";
import IZIAnalysisRenderer from "@izi_dashboard/js/izi_analysis_renderer";

export const IZIAnalysisView = AbstractView.extend({
    template: "IZIAnalysis",
    display_name: "IZIAnalysis",
    events: {},
    icon: "fa-tachometer",
    config: Object.assign({}, AbstractView.prototype.config, {
        Model: IZIAnalysisModel,
        Controller: IZIAnalysisController,
        Renderer: IZIAnalysisRenderer,
    }),
    viewType: "izianalysis",
    withControlPanel: false,
    withSearchPanel: false,

    init: function () {
        this._super.apply(this, arguments);
    },
});

viewRegistry.add("izianalysis", IZIAnalysisView);

export default IZIAnalysisView;
