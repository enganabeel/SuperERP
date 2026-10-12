/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { VideoSelector } from "@web_editor/components/media_dialog/video_selector";

patch(VideoSelector.prototype, {
    /**
     * Direct video-file URLs (e.g. a locally uploaded .mp4) aren't a
     * platform /web_editor/video_url/data knows how to resolve -- treat
     * them as their own "local" platform instead of calling that RPC, so
     * both a fresh upload and re-opening the dialog on an already-configured
     * local video work without an "unsupported video" error.
     *
     * @override
     */
    async _getVideoURLData(url, options) {
        if (this._isLocalVideoUrl(url)) {
            return { embed_url: url, video_id: null, params: {}, platform: 'local' };
        }
        return super._getVideoURLData(url, options);
    },

    _isLocalVideoUrl(url) {
        return /\.(mp4|webm|ogv|ogg|mov)(\?|#|$)/i.test(url || '');
    },

    /**
     * Handler for the "Or upload a video file" input added by
     * video_selector_patch.xml: uploads the chosen file, then feeds its URL
     * through the normal update flow exactly as if it had been pasted in
     * the URL field.
     */
    async onUploadLocalVideo(ev) {
        const file = ev.target.files && ev.target.files[0];
        ev.target.value = '';
        if (!file) {
            return;
        }
        this.state.errorMessage = '';
        const formData = new FormData();
        formData.append('video_file', file);
        formData.append('csrf_token', odoo.csrf_token);
        let data;
        try {
            const response = await fetch('/website_local_video_background/upload_video', {
                method: 'POST',
                body: formData,
            });
            data = await response.json();
        } catch (error) {
            this.state.errorMessage = _t("Could not upload the video file.");
            return;
        }
        if (!data || !data.url) {
            this.state.errorMessage = (data && data.error) || _t("Could not upload the video file.");
            return;
        }
        this.state.urlInput = data.url;
        await this.updateVideo();
    },
});
