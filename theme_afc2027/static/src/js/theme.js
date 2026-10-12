/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';

/**
 * Toggles the header from transparent (over the hero) to a solid background
 * once the page is scrolled, matching the reference site's nav behaviour.
 */
publicWidget.registry.Afc2027HeaderScroll = publicWidget.Widget.extend({
    selector: '.o_header_afc2027',
    disabledInEditableMode: false,

    /**
     * @override
     */
    start() {
        this._onScroll = this._onScroll.bind(this);
        window.addEventListener('scroll', this._onScroll, { passive: true });
        this._onScroll();
        return this._super(...arguments);
    },

    /**
     * @override
     */
    destroy() {
        window.removeEventListener('scroll', this._onScroll);
        this._super(...arguments);
    },

    _onScroll() {
        const scrolled = window.scrollY > 60;
        this.el.classList.toggle('o_header_afc2027_scrolled', scrolled);
    },
});

/**
 * Wires the hero "play" button to the modal's video player. The source is
 * read, in order of preference, from:
 *   1. data-oe-video-url on the .s_afc_hero_video section (set this if you
 *      want the modal to play a *different*, higher-quality/with-sound cut
 *      than the muted looping background video).
 *   2. the src of the background <video class="hero-video-bg"> itself, so
 *      by default the modal just replays the same file with sound+controls.
 * Pauses and resets the modal video on close so it doesn't keep playing
 * (with sound) off-screen.
 */
publicWidget.registry.Afc2027HeroVideo = publicWidget.Widget.extend({
    selector: '.s_afc_hero_video',
    events: {
        'click .s_afc_video_trigger': '_onPlayClick',
    },

    /**
     * @override
     */
    start() {
        this.modalEl = document.getElementById('afcHeroVideoModal');
        if (this.modalEl) {
            this._onModalHidden = this._onModalHidden.bind(this);
            this.modalEl.addEventListener('hidden.bs.modal', this._onModalHidden);
        }
        return this._super(...arguments);
    },

    /**
     * @override
     */
    destroy() {
        if (this.modalEl) {
            this.modalEl.removeEventListener('hidden.bs.modal', this._onModalHidden);
        }
        this._super(...arguments);
    },

    _onPlayClick() {
        if (!this.modalEl) {
            return;
        }
        const bgVideo = this.el.querySelector('.hero-video-bg');
        const videoUrl = this.el.dataset.oeVideoUrl || (bgVideo && bgVideo.currentSrc);
        const modalVideo = this.modalEl.querySelector('video[data-oe-video-sync]');
        if (videoUrl && modalVideo) {
            modalVideo.src = videoUrl;
            modalVideo.play().catch(() => {});
        }
        // If neither a data-oe-video-url nor a background video source is
        // configured yet, the modal still opens (empty player) rather than
        // blocking the click — swap in a real URL once you have one.
    },

    _onModalHidden() {
        const modalVideo = this.modalEl.querySelector('video[data-oe-video-sync]');
        if (modalVideo) {
            modalVideo.pause();
            modalVideo.removeAttribute('src');
            modalVideo.load();
        }
    },
});

export default {
    Afc2027HeaderScroll: publicWidget.registry.Afc2027HeaderScroll,
    Afc2027HeroVideo: publicWidget.registry.Afc2027HeroVideo,
};
