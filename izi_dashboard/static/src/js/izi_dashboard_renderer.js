/** @odoo-module */
// NOTE: see izi_dashboard_controller_legacy.js - web.AbstractRenderer has no
// Odoo 18 equivalent. Reference-only, not registered in the manifest.
import AbstractRenderer from "@web/legacy/js/views/abstract_renderer";
import IZIViewDashboard from "@izi_dashboard/js/component/main/izi_view_dashboard";
import IZIConfigDashboard from "@izi_dashboard/js/component/main/izi_config_dashboard";

export const IZIDashboardRenderer = AbstractRenderer.extend({
    template: "IZIDashboard",
    events: Object.assign({}, AbstractRenderer.prototype.events, {}),
    init: function (parent, state, params) {
        var self = this;
        this._super.apply(this, arguments);
        self.parent = parent;
        if (parent.props) self.props = parent.props;
    },
    start: function () {
        var self = this;
        var $viewDashboard = new IZIViewDashboard(self);
        var $configDashboard = new IZIConfigDashboard(self, $viewDashboard);
        $configDashboard.appendTo(self.$el);
        $viewDashboard.appendTo(self.$el);
    },
    destroy: function () {
        this._super.apply(this, arguments);
    },
});

export default IZIDashboardRenderer;
