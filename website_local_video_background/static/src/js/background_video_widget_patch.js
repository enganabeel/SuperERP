/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.backgroundVideo.include({
    /**
     * Stock behaviour always wraps the video source in an <iframe> (built
     * for YouTube/Vimeo/Dailymotion/Instagram embeds). A direct video-file
     * URL (a locally uploaded video) can't autoplay/loop/mute properly
     * inside an iframe -- render a real <video> element for those instead,
     * reusing the same .o_bg_video_container positioning. Anything else
     * (an actual platform embed URL) falls through to the original
     * behaviour unchanged.
     *
     * @override
     */
    _appendBgVideo() {
        if (!this._isLocalVideoSrc(this.videoSrc)) {
            return this._super(...arguments);
        }

        const $oldContainer = this.$bgVideoContainer || this.$('> .o_bg_video_container');

        const videoEl = document.createElement('video');
        videoEl.classList.add('o_bg_video_local');
        videoEl.src = this.videoSrc;
        videoEl.autoplay = true;
        videoEl.muted = true;
        videoEl.loop = true;
        videoEl.playsInline = true;

        const containerEl = document.createElement('div');
        containerEl.classList.add('o_bg_video_container', 'o_bg_video_container_local');
        containerEl.appendChild(videoEl);

        this.$bgVideoContainer = $(containerEl);
        // No iframe in this branch -- _adjustIframe() already no-ops when
        // this.$iframe isn't set, so it stays safe for resize/dropdown/modal
        // handlers that call it.
        this.$iframe = undefined;

        this.$bgVideoContainer.prependTo(this.$el);
        $oldContainer.remove();
    },

    /**
     * @private
     * @param {string} src
     * @returns {boolean}
     */
    _isLocalVideoSrc(src) {
        return /\.(mp4|webm|ogv|ogg|mov)(\?|#|$)/i.test(src || '');
    },
});
