/**
 * "Print PDF" for the department org chart.
 *
 * The chart's cards are Highcharts `useHTML` data labels - real DOM layered
 * over the SVG - so Highcharts' own SVG export comes back with empty boxes.
 * The only thing that reproduces what the user is looking at, filters and all,
 * is rasterising the live chart. html2canvas (already shipped by web_editor)
 * does that; the server just wraps the PNG in a titled, fit-to-page PDF.
 *
 * Known limitations of the capture, all cosmetic: html2canvas ignores
 * box-shadow (the ring around a selected node's card), and it needs every font
 * to be loaded already - which it is by the time the chart has rendered.
 */

import { patch } from "@web/core/utils/patch";
import { loadJS } from "@web/core/assets";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { OrgRenderer } from "@web_org/org_renderer";

const HTML2CANVAS_URL = "/web_editor/static/lib/html2canvas.js";

// The org view is generic, this printout is not: action_print_org_chart_pdf
// lives on hr.department, so the button only belongs on that chart.
const PRINTABLE_MODEL = "hr.department";

// Capture above 1:1 so text stays sharp once the PDF is scaled to the sheet.
const TARGET_CAPTURE_SCALE = 2;
// Browsers refuse to allocate a canvas past roughly 16k px per side, and a
// capture much beyond ~36 megapixels stops being worth the memory it costs.
const MAX_CANVAS_EDGE = 12000;
const MAX_CANVAS_PIXELS = 36e6;
const MIN_CAPTURE_SCALE = 0.25;

patch(OrgRenderer.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state.printing = false;
    },

    get canPrintChartPdf() {
        return this.props.model.resModel === PRINTABLE_MODEL;
    },

    /**
     * Rasterise the chart as it currently stands and download it as a PDF.
     */
    async printChartPdf() {
        if (this.state.printing) {
            return;
        }
        const area = this.containerRef.el;
        if (!area || !this.chart) {
            this.notification.add(_t("There is no chart to print."), { type: "warning" });
            return;
        }

        this.state.printing = true;
        try {
            const { dataUrl, cssWidth, cssHeight } = await this._captureChartPng(area);
            const action = await this.orm.call(
                this.props.model.resModel,
                "action_print_org_chart_pdf",
                [[]],
                {
                    image_data: dataUrl,
                    title: this.chartPrintTitle,
                    filter_description: this.chartPrintFilterDescription,
                    css_width: cssWidth,
                    css_height: cssHeight,
                    // Sheet and orientation are left to the server, which picks
                    // them from the capture's aspect ratio.
                }
            );
            await this.action.doAction(action);
        } catch (error) {
            // A server-side UserError already surfaces on its own; only the
            // capture itself needs translating into something readable.
            if (error?.name === "OrgChartCaptureError") {
                this.notification.add(error.message, { type: "danger" });
            } else {
                throw error;
            }
        } finally {
            this.state.printing = false;
        }
    },

    /** Heading for the printed sheet: the breadcrumb the user is looking at. */
    get chartPrintTitle() {
        return this.env.config?.getDisplayName?.() || this.env.config?.displayName || _t("Org Chart");
    },

    /**
     * The active search facets, spelled out, so the sheet says which slice of
     * the hierarchy it is - "Type & Everything Below: Sector", say.
     */
    get chartPrintFilterDescription() {
        const facets = this.env.searchModel?.facets || [];
        const parts = [];
        for (const facet of facets) {
            const values = (facet.values || []).join(` ${facet.separator || _t("or")} `);
            if (!values) {
                continue;
            }
            parts.push(facet.title ? `${facet.title}: ${values}` : values);
        }
        return parts.join("  •  ");
    },

    /**
     * @param {HTMLElement} area the chart element, sized to the full chart by
     *  the renderer, so this captures all of it and not just the scrolled part.
     */
    async _captureChartPng(area) {
        const fail = (message) => {
            const error = new Error(message);
            error.name = "OrgChartCaptureError";
            return error;
        };

        await loadJS(HTML2CANVAS_URL);
        const html2canvas = window.html2canvas;
        if (!html2canvas) {
            throw fail(_t("The screen capture library could not be loaded."));
        }

        const cssWidth = Math.ceil(area.scrollWidth || area.offsetWidth);
        const cssHeight = Math.ceil(area.scrollHeight || area.offsetHeight);
        if (!cssWidth || !cssHeight) {
            throw fail(_t("The chart has no size to capture yet."));
        }

        let canvas;
        try {
            canvas = await html2canvas(area, {
                backgroundColor: "#ffffff",
                scale: this._captureScale(cssWidth, cssHeight),
                width: cssWidth,
                height: cssHeight,
                // The chart is wider than its scrolling wrapper; cloning it at
                // its own full size is what keeps the off-screen part in.
                windowWidth: cssWidth,
                windowHeight: cssHeight,
                scrollX: 0,
                scrollY: 0,
                useCORS: true,
                logging: false,
            });
        } catch (error) {
            console.error("[department_chart_types] chart capture failed", error);
            throw fail(_t("The chart could not be captured. Try filtering it down to a smaller part of the hierarchy."));
        }

        // A canvas the browser refused to allocate still hands back a canvas -
        // it just serialises to a stub. Catch that here rather than posting it.
        const dataUrl = canvas.toDataURL("image/png");
        if (!dataUrl || dataUrl.length < 1000) {
            throw fail(_t("The chart is too large to capture. Filter it down to a smaller part of the hierarchy and try again."));
        }
        return { dataUrl, cssWidth, cssHeight };
    },

    /**
     * Capture above 1:1 for sharpness, backing off on large charts before the
     * canvas hits a browser limit.
     */
    _captureScale(cssWidth, cssHeight) {
        const scale = Math.min(
            TARGET_CAPTURE_SCALE,
            MAX_CANVAS_EDGE / cssWidth,
            MAX_CANVAS_EDGE / cssHeight,
            Math.sqrt(MAX_CANVAS_PIXELS / (cssWidth * cssHeight))
        );
        return Math.max(scale, MIN_CAPTURE_SCALE);
    },
});
