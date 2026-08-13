/** @odoo-module */
// NOTE: see izi_dashboard_controller_legacy.js - web.AbstractRenderer has no
// Odoo 18 equivalent. Reference-only, not registered in the manifest.
import AbstractRenderer from "@web/legacy/js/views/abstract_renderer";
import IZIViewAnalysis from "@izi_dashboard/js/component/main/izi_view_analysis";
import IZIConfigAnalysis from "@izi_dashboard/js/component/main/izi_config_analysis";

export const IZIAnalysisRenderer = AbstractRenderer.extend({
    template: "IZIAnalysis",
    events: Object.assign({}, AbstractRenderer.prototype.events, {}),
    init: function (parent, state, params) {
        var self = this;
        this._super.apply(this, arguments);
        self.parent = parent;
        if (parent.props) self.props = parent.props;
    },
    start: function () {
        var self = this;
        var $viewAnalysis = new IZIViewAnalysis(self);
        self.$viewAnalysis = $viewAnalysis;
        var $configAnalysis = new IZIConfigAnalysis(self, $viewAnalysis);
        self.$configAnalysis = $configAnalysis;
        $configAnalysis.appendTo(self.$el);
        $viewAnalysis.appendTo(self.$el);
    },
    destroy: function () {
        this._super.apply(this, arguments);
    },
});

export default IZIAnalysisRenderer;
