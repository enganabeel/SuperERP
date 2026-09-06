/** @odoo-module */
// NOTE: web.AbstractView / web.view_registry were removed from Odoo core
// after 16.0 and have no Odoo 18 equivalent. This file is a
// syntax-modernized reference only (odoo.define -> @odoo-module) and is not
// registered in the manifest. The active Dashboard view type registration
// for Odoo 18 is izi_dashboard_view.js (registry.category("views")).
import AbstractView from "@web/legacy/js/views/abstract_view";
import viewRegistry from "@web/legacy/js/views/view_registry";
import IZIDashboardModel from "@izi_dashboard/js/izi_dashboard_model";
import IZIDashboardController from "@izi_dashboard/js/izi_dashboard_controller_legacy";
import IZIDashboardRenderer from "@izi_dashboard/js/izi_dashboard_renderer";

export const IZIDashboardView = AbstractView.extend({
    template: "IZIDashboard",
    display_name: "IZIDashboard",
    events: {},
    icon: "fa-tachometer",
    config: Object.assign({}, AbstractView.prototype.config, {
        Model: IZIDashboardModel,
        Controller: IZIDashboardController,
        Renderer: IZIDashboardRenderer,
    }),
    viewType: "izidashboard",
    withControlPanel: false,
    withSearchPanel: false,

    init: function () {
        this._super.apply(this, arguments);
    },
});

viewRegistry.add("izidashboard", IZIDashboardView);

export default IZIDashboardView;
