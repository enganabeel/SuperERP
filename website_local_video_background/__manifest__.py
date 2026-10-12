# -*- coding: utf-8 -*-
{
    'name': 'Website Local Video Background',
    'summary': 'Allow uploading a self-hosted video file as a snippet background video',
    'description': """
Website Local Video Background
===============================
Odoo's stock "Background Video" snippet option (Website Builder > select a
section > Background > Video) only accepts a YouTube, Vimeo, Dailymotion or
Instagram URL -- there is no way to use a locally uploaded video file as a
section's background (e.g. a hero/intro slider).

This module adds an "Or upload a video file" control directly inside that
same video picker dialog. Uploading a file there stores it as a public
attachment and plays it as a real, muted, looping, autoplaying <video>
background. Everything else (YouTube/Vimeo/Dailymotion/Instagram via URL)
keeps working exactly as before -- this only adds a new path, it does not
change the existing one.
""",
    'version': '18.0.1.0.1',
    'category': 'Website',
    'author': 'Ejad Tech',
    'website': 'https://ejadtech.sa',
    'license': 'LGPL-3',
    'depends': ['website'],
    'assets': {
        'web_editor.assets_media_dialog': [
            'website_local_video_background/static/src/js/video_selector_patch.js',
            'website_local_video_background/static/src/xml/video_selector_patch.xml',
        ],
        'web.assets_frontend': [
            'website_local_video_background/static/src/js/background_video_widget_patch.js',
            'website_local_video_background/static/src/scss/background_video_local.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
