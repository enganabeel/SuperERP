# -*- coding: utf-8 -*-
{
    'name': 'Theme AFC2027 Corporate',
    'summary': 'Corporate / sporting-event organizing-committee website theme',
    'description': """
Theme AFC2027 Corporate
========================
A corporate website theme for major-event organizing committees, sports
federations and government-adjacent institutional sites. Inspired by the
layout of large event LOC (Local Organizing Committee) websites: video hero,
mission statement, news carousel, partners/vendors section, careers call to
action and a contact block.

Includes:
- A full color & typography system driven by Odoo's website color presets
  (edit in Website > Configuration > Theme, or in
  static/src/scss/primary_variables.scss).
- Custom header with transparent-to-solid scroll behaviour and an external
  "micro-site" nav link pattern.
- Custom footer with legal links and social icons.
- Six ready-to-use building-block snippets you can drag onto any page:
  Hero Video, Who We Are, News Carousel, Partners/Vendors, Careers CTA,
  Contact Split.
- A pre-assembled homepage using all of the above.

NOTE: Brand colors, fonts and imagery in this build are placeholders
approximated from a reference site and MUST be replaced with the real
brand kit (see NOTES.md in the module root) before going live.
""",
    'version': '18.0.1.0.15',
    'category': 'Theme/Corporate',
    'author': 'Ejad Tech',
    'website': 'https://ejadtech.sa',
    'license': 'LGPL-3',
    'depends': ['website', 'website_blog'],
    'data': [
        'views/snippets/s_hero_video.xml',
        'views/snippets/s_who_we_are.xml',
        'views/snippets/s_news_carousel.xml',
        'views/snippets/s_vendors.xml',
        'views/snippets/s_careers_cta.xml',
        'views/snippets/s_contact_split.xml',
        'views/snippets_registry.xml',
        'views/layout.xml',
        'views/pages/homepage.xml',
        'views/pages/blog.xml',
        'views/pages/about_us.xml',
        'data/theme_data.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'theme_afc2027/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=Changa:wght@400;500;600;700;800&display=swap',
            'theme_afc2027/static/src/scss/theme.scss',
            'theme_afc2027/static/src/js/theme.js',
        ],
    },
    'images': [
        'static/description/cover.png',
    ],
    'application': False,
    'installable': True,
}
