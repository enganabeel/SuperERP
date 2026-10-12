# theme_afc2027 — build notes

## What this is
An installable Odoo 18 website theme module inspired by the layout of
https://ambitious-beach-0ac119c03.7.azurestaticapps.net/ (an LOC / major
sporting-event corporate site): video hero, "Who We Are" mission block, news
carousel, vendors/partners band, careers CTA, and a contact section — plus a
matching header/footer and a pre-assembled homepage.

## Install
1. Copy the `theme_afc2027` folder into your Odoo 18 `addons` path (or a
   custom addons repo mounted into your instance).
2. Restart Odoo with `-u theme_afc2027` (or Apps > Update Apps List, then
   search "Theme AFC2027 Corporate" and install).
3. Go to the website, refresh — homepage should show the six sections.
4. Open the website builder ("Edit") on the homepage to drag additional
   copies of the six blocks (Hero Video, Who We Are, News Carousel,
   Vendors/Partners, Careers CTA, Contact Split) onto any page.

## Known approximations — replace before going live
Because the reference site could only be read as rendered text/markdown
(no direct access to its CSS/JS bundles or a screenshot), the following are
**best-guess placeholders**, not extracted values:

- **Colors** (`static/src/scss/primary_variables.scss`): deep green / gold /
  near-black palette, chosen as a reasonable approximation for a Saudi
  national sporting-event site. Swap the 6 hex values at the top of that
  file (or via Website > Configuration > Theme once installed) for the real
  brand kit.
- **Fonts**: Barlow Condensed (headings — real brand font, per v1.0.9) +
  Inter (body, still a placeholder pairing) via Google Fonts. To change
  either, edit the fonts URL in `__manifest__.py` and the font variables in
  `primary_variables.scss`.
- **Images**: `static/src/img/hero-bg.jpg`, `stadium-night.jpg`,
  `news-placeholder.jpg`, and `logo-light.svg` are all generated
  placeholders (solid color + label). Replace with real assets.
- **Nav/footer links**: `/about-us`, `/news`, careers portal, vendors page
  etc. are placeholder URLs (`data/theme_data.xml`, `views/layout.xml`).
  Point them at your real pages once built.
- **News carousel**: now dynamic (see Changelog v1.0.6) — it pulls real
  `blog.post` records once the Website Blog app has content. Until you
  publish your first post it still shows 3 static placeholder cards so the
  section never renders empty.

## Structural note — header/footer
Odoo's stock header/footer are swappable "template options" built from
several nested sub-templates whose internal ids can shift between 18.x point
releases. To stay robust, this theme replaces the whole `<header>`/`<footer>`
landmark tags inside `website.layout` (`views/layout.xml`) by tag, rather
than patching internal sub-templates. Trade-off: the builder's built-in
"transparent/boxed/hamburger" header quick-options won't apply to this
custom header — instead everything is controlled by SCSS + the
`website.menu` records in `data/theme_data.xml`. The header/footer text/
images are still editable in place via the normal drag-edit mode.

## Structural note — snippet registration
`views/snippets_registry.xml` registers the six blocks into the builder's
"Blocks" panel via an xpath on `website.snippets` targeting
`#snippet_structure .o_panel_body`. If Odoo 18 has moved/renamed that
container by the point release you're installing against, this view will
fail on load — open `addons/website/views/snippets/snippets.xml` in your
Odoo source, find the current panel container id, and update the xpath
`expr` in that file. The six snippet templates themselves
(`views/snippets/s_*.xml`) don't need to change.

## Changelog
- **v1.0.15** — Wired up self-hosted `@font-face` rules for the real DIN
  Next Arabic (`theme.scss`), ready for whenever licensed font files
  actually show up — no further code change needed once they do:
  - **Drop the files here:** `theme_afc2027/static/src/fonts/` (new
    folder — see the `README.md` inside it for the exact filenames
    expected: `DINNextLTArabic-{Light,Regular,Medium,Bold}.woff2` +
    `.woff` fallbacks).
  - Four `@font-face` blocks declare `'DIN Next Arabic'` at weights
    300/400/500/700, each pointing at the matching filename under that
    folder via a plain URL path
    (`/theme_afc2027/static/src/fonts/DINNextLTArabic-Regular.woff2`,
    etc.) — no manifest asset-list entry needed, Odoo serves any file
    under a module's `static/` automatically.
  - `:lang(ar)`'s font stack is now
    `'DIN Next Arabic', 'Changa', 'Barlow Condensed Fallback', sans-serif`
    — since the font files don't exist yet, each `@font-face` currently
    fails to load 404 and the browser falls through to Changa (the
    v1.0.14 placeholder), so nothing is broken right now. The moment real
    files land at those paths, DIN Next Arabic starts rendering
    automatically, with Changa remaining as the safety fallback for any
    weight the license doesn't cover.
  - If the license only comes as `.ttf`/`.otf` (not converted to
    `.woff2`/`.woff`), either convert them first (e.g. `fonttools`) or
    ask and a `.ttf` `src` entry can be added instead — `@font-face`
    supports raw TrueType/OpenType too, just less optimally compressed.
- **v1.0.14** — Swapped the Arabic typeface from Cairo to Changa, per a
  request to use "DIN Arabic" (DIN Next Arabic). DIN Next Arabic is a
  commercial Monotype font, not available on Google Fonts — confirmed by
  requesting it directly from `fonts.googleapis.com`, which returns
  `400: font family not found` — and no licensed font files were provided
  to self-host. Changa is a free, open-source Google Font with a similar
  geometric/engineered look often used as a DIN stand-in for Arabic,
  swapped in as the interim choice (`__manifest__.py`'s Google Fonts link,
  and the `:lang(ar)` rule in `theme.scss`). **If a real DIN Next Arabic
  license + font files (.woff2/.woff/.ttf) become available**, replace
  Changa with it: drop the files in a new `static/src/fonts/` folder, add
  `@font-face` rules pointing at them in `theme.scss` (instead of the
  Google Fonts `<link>` entry), and update the two `'Changa'` references in
  the `:lang(ar)` block to the real font-family name.
- **v1.0.13** — Added Arabic (RTL) font support. Barlow Condensed and Inter
  (this theme's Latin brand fonts) have no Arabic glyphs, so Arabic text
  would silently fall back to whatever generic Arabic face the visitor's
  OS ships. Added Cairo (weights 400–800) to the Google Fonts `<link>`
  (`__manifest__.py`) and a `:lang(ar) { font-family: 'Cairo', ... }`
  override in `theme.scss` (headings, nav, buttons, and body) so Arabic
  pages get a proper matching Arabic typeface. Note: layout mirroring
  (margins/floats/text-align flipping for RTL) is a *separate* concern
  handled automatically by Odoo core's `rtlcss` asset pipeline — that
  requires the `rtlcss` Node package to be installed on the server
  (`npm install -g rtlcss`; verified against
  `odoo/addons/base/models/assetsbundle.py` on the 18.0 branch, which logs
  a warning and silently falls back to LTR CSS if `rtlcss` isn't on PATH —
  no error, so it's easy to miss). This theme's own custom CSS was audited
  and doesn't fight that pipeline: the few `left`/`right` rules in
  `theme.scss` are all symmetric (full-bleed overlays) or plain
  `margin-right` for icon spacing, which `rtlcss` flips correctly on its
  own; Bootstrap's logical-property utility classes already in use
  (`ms-*`, `me-*`) are RTL-safe by design. No layout CSS changes were
  needed, only this font addition.
- **v1.0.12** — **Fixed a whole-site-down crash** introduced by v1.0.11's
  About Us page. Sequence of events, for the record:
  1. `/about-us` initially rendered blank (200 OK, empty body) — turned out
     the `website.page` record was in a corrupted state (its "Page Title"
     showed garbage like `ir.actions.windows.list` instead of "About Us
     Page").
  2. Deleting that page row via Website > Site > Pages seemed like the
     obvious fix, but `website.page` delegates to `ir.ui.view` via Odoo's
     `_inherits` mechanism — deleting the `website.page` record **also
     deleted its underlying `ir.ui.view` template row**.
  3. Somewhere in the database, Odoo's per-website "theme" tracking still
     held a record whose `theme_template_id` pointed at that now-deleted
     view id. Every subsequent attempt to reload `about_us.xml` re-created
     the `website.page` → `ir.ui.view` delegation link, which re-triggered
     a `write()` in `website/models/theme_models.py` that dereferences
     `theme_template_id.arch` — raising `MissingError` on the deleted id.
  4. Because module data loading is transactional, that exception aborted
     the **entire module load**, not just this one page — which is why
     even `/` started 500ing (`Failed to initialize database`).
  Fix: renamed the page's XML IDs (`page_about_us` → `page_about_us_v2`,
  `page_about_us_page` → `page_about_us_page_v2`). Since these are IDs
  Odoo has never seen before, it creates fresh `ir.ui.view`/`website.page`
  rows with no `theme_template_id` baggage, sidestepping the poisoned
  lineage entirely rather than trying to repair it in place (no direct DB
  access was available to hunt down and fix the dangling reference by
  hand). Also wrapped the `website.page` record in `<data noupdate="1">`,
  matching the pattern Odoo's own `website_data.xml` uses for
  `homepage_page`/`contactus_page`: the record is created once and never
  re-touched by later module upgrades, which both matches upstream
  convention and prevents this exact write-path from firing again on every
  future upgrade.
  **Takeaway for next time**: don't delete a theme-installed
  `website.page` via the UI to "reset" it — if a page record from this
  module ever needs to be reset again, uninstalling and reinstalling the
  whole module is the safe path (or asking for a fresh, differently-named
  XML ID rather than deleting and recreating the same one).
- **v1.0.11** — Added an "About Us" page (`/about-us`, wired to the
  existing "About Us" nav entry). Content and section design copied from
  the reference site's `/about` page. Note: that host
  (`ambitious-beach-0ac119c03.7.azurestaticapps.net`) is blocked by this
  environment's network egress policy (confirmed via the agent-proxy
  status log — a policy-level `403` on the CONNECT, not a site error), so
  this was built from a full-page screenshot the user provided rather than
  a live fetch. New file `views/pages/about_us.xml`, following the same
  `<template> + <record model="website.page">` pattern Odoo itself uses
  for its own default pages (verified against
  `addons/website/data/website_data.xml`, 18.0 branch). Sections, top to
  bottom:
  - Page banner: "Welcome to LOC" eyebrow over "Hosting the Asian Cup
    Saudi Arabia 2027™", on the theme's aerial `hero-bg.jpg` (same overlay
    treatment as the homepage hero).
  - Crest + intro: centered crest image, "AFC Asian Cup Saudi Arabia 2027 /
    Local Organizing Committee" caption, and the LOC mission paragraph,
    copied verbatim from the screenshot.
  - Vision/Mission 2×2 mosaic: tan "Our Vision" text cell, a photo cell, a
    second photo cell, and a dark-green "Our Mission" text cell, with a
    circular crest badge overlapping the center (desktop only).
  - "Our Values" grid: 5 value cards (Leave a Mark, Create the Chance,
    Serve the Squad, Practice Under the Strain, Pass the Ball) with
    Font Awesome icons standing in for the reference site's custom
    line-art icons, text copied verbatim — including "Pass the Ball"
    sharing its body text with "Create the Chance", which is how it
    reads on the reference site itself, not a copy error here.
  - Careers CTA: reused the existing `s_careers_cta` snippet, but rewrote
    its markup/copy and `.s_afc_careers` CSS in `theme.scss` to match the
    reference exactly (centered layout, "Career | Join Us" eyebrow,
    uppercase "Be Part of an Extraordinary Event" heading, pattern-textured
    green background, pill-shaped "Discover all opportunities" button).
    Because this snippet is shared, the **homepage's** careers section
    picks up the same redesign/copy automatically.
  - **Known placeholders needing real assets** (flagged inline in
    `about_us.xml` too): the crest/emblem image reuses the existing gold
    placeholder logo (no real crest file available yet — same situation as
    the header logo); the second Vision/Mission photo cell (a
    celebration/podium shot on the reference site) reuses the theme's
    `stadium-night.jpg` since no matching photo asset exists in this repo
    and the reference host can't be fetched from this environment to
    source one.
- **v1.0.10** — Restyled the blog pages (/blog) as a "Media Center", matching
  the reference site's design (`views/pages/blog.xml` + new SCSS in
  `theme.scss`):
  - Dark-green patterned page banner titled "Media Center" (uses the
    theme's existing `pattern.png`), inserted above the standard blog top
    area via `website_blog.blog_post_short`.
  - Deactivated `website_blog.opt_blog_cover_post` (the stock "Top banner —
    Name / Latest Post" customize option) so the blog's own name/cover row
    doesn't render twice under the new banner. Note: updating the
    `website_blog` module itself may re-activate that option; if a
    duplicate banner ever reappears after an Odoo update, turn it back off
    in the website builder's customize panel or re-update this theme.
  - Replaced the post cards in `website_blog.posts_loop` with the reference
    design: full-image cards with the title + date overlaid on a bottom
    dark gradient, hover zoom, rounded corners. First post spans 2/3 width
    with its neighbour filling the remaining 1/3 (equal height), remaining
    posts alternate at half width. Cover images come from each post's
    `cover_properties` (same source as the homepage carousel), with the
    theme placeholder as fallback. The surrounding search/tag filters,
    "no post yet" empty state, pagination and the designer-only
    published/unpublished toggle are all preserved.
    Trade-off: the customize-menu options that shaped the old cards
    (cards design / list view / teaser / author / stats toggles) no longer
    affect the replaced card markup.
  - Added a "Latest News" heading with a pill-outline "Discover More"
    button (links to the next pager page; hidden when everything fits on
    one page).
  - The banner title is hardcoded (translatable) as "Media Center". The
    blog *record's* name (shown in breadcrumbs, the multi-blog nav and
    post pages) is data, not code — rename it to "Media Center" in
    Website > Configuration > Blogs to match everywhere.
- **v1.0.9** — Switched the heading font to the brand's Barlow Condensed:
  - Replaced Montserrat with Barlow Condensed (weights 400–800) in the
    Google Fonts `<link>` (`__manifest__.py`); Inter stays for body copy.
  - `$font-family-headings` and the Odoo font-picker config
    (`$o-theme-font-configs`) now use
    `'Barlow Condensed', 'Barlow Condensed Fallback', 'Arial Narrow',
    sans-serif` — the "Fallback" name matches the reference site's stack,
    and Arial Narrow is the closest common condensed system face while the
    webfont loads.
  - Also set Bootstrap's `$headings-font-family` (previously unset), so
    every h1–h6 site-wide gets the brand font — including headings rendered
    by other Odoo apps such as blog post titles on `/blog` — not just this
    theme's own snippets, which reference `$font-family-headings` directly.
- **v1.0.8** — Fixed the header/menu bar not appearing at all. Two stacked
  CSS problems:
  - The header had no `z-index`, and since the hero section is a positioned
    element that comes *after* the header in the DOM, the hero painted on
    top of it — the navbar was rendered but completely buried under the
    hero video/overlay. `.o_header_afc2027` now gets `z-index: 1030`
    (Bootstrap's `$zindex-fixed`).
  - The header was `position-absolute`, so it scrolled away with the page
    and the JS "transparent → solid on scroll" behaviour
    (`Afc2027HeaderScroll` in `theme.js`) could never be seen. Switched the
    markup to Bootstrap's `fixed-top` (`views/layout.xml`), which is what
    the transparent-until-scroll pattern needs.
  - Follow-on: the old `.o_afc_has_overlay_header main { margin-top: -76px }`
    rule was dead code (that class sits on the hero *section*, which is
    inside `main`, so the selector never matched anything). Replaced it with
    the inverse guard it was trying to be: on pages that do NOT start with
    the dark hero, `#wrapwrap:not(:has(.o_afc_has_overlay_header))` gives
    the fixed header a solid brand background (white nav links would
    otherwise be invisible on light pages) and pads `main` down 76px so the
    header doesn't cover the top of the content.
- **v1.0.7** — Fixed a crash when the "News Carousel" block is previewed
  from the website builder's block picker (dragging/hovering it in the
  "Add Building Block" panel): `AttributeError: 'Request' object has no
  attribute 'website'` in `theme_afc2027.s_news_carousel`. That preview path
  renders the template through `ir.ui.view.render_public_asset`, a
  lightweight RPC context where `request.website` isn't populated the way
  it is on a normal page render, so calling `request.website.website_domain()`
  raised. Replaced it with `request.env['website'].get_current_website()
  .website_domain()`, which resolves the current website itself and is
  explicitly written to tolerate a missing/partial `request` (confirmed
  against `get_current_website()` in `addons/website/models/website.py`),
  so it works in both normal page renders and this preview context.
- **v1.0.6** — Made the News Carousel dynamic. Added a `website_blog`
  dependency (`__manifest__.py`) and rewired
  `views/snippets/s_news_carousel.xml` to query real `blog.post` records
  instead of always showing 3 static dummy cards:
  - Domain: `request.website.website_domain() + [('post_date', '<=',
    datetime.datetime.now())]`, `order='post_date desc', limit=9` — the same
    base domain/ordering pattern `website_blog`'s own controller uses
    (`addons/website_blog/controllers/main.py`), so unpublished/future posts
    are hidden from regular visitors but still previewable by website
    editors, and posts are scoped to the current website in a multi-website
    setup. No `sudo()` is used, so normal record-rule visibility applies.
  - Posts are chunked into groups of 3 (`range(0, len(posts), 3)`) so each
    group becomes one `carousel-item` slide, matching the existing 3-card
    layout; the prev/next arrows now only render when there are more than 3
    posts (nothing to slide to otherwise).
  - Cover image: parses `json.loads(post.cover_properties)` and reads the
    `background-image` key (the same field/format `website_blog`'s own
    templates use for a post's cover), falling back to the theme's existing
    `news-placeholder.jpg` when a post has no cover set or the JSON value is
    the field's default `"none"`.
  - If the Blog app has no posts yet (fresh install), the section falls back
    to the original 3 static placeholder cards so it never renders empty.
  - Updated the carousel's "View all news" button and the top-nav "News"
    menu entry (`data/theme_data.xml`) from the placeholder `/news` URL to
    the real `/blog` route now that it's backed by actual content.
- **v1.0.5** — Wired up a real full-bleed background video for the hero,
  matching a screenshot of the actual reference site (aerial city footage,
  centered white headline, plain circular play button below it, no inline
  "Watch the welcome message" label). Two fixes:
  - Added the missing `.hero-video-bg` CSS (`theme.scss`): the `<video>` tag
    had no styling at all, so it was rendering as a normal inline element
    instead of a full-bleed absolutely-positioned layer — that's why it
    wasn't "in the same position" as the reference. It's now
    `position: absolute; inset/width/height: 100%; object-fit: cover`,
    sitting behind the gradient overlay and the text (fixed the z-index
    stack: video → gradient → content). Hero text/play button are now
    centered to match the screenshot too.
  - The video modal (opened by the play button) previously contained an
    `<iframe>` meant for a YouTube/Vimeo embed, which doesn't work for a
    direct `.mp4` file. Replaced it with a `<video controls>` element;
    `theme.js`'s `Afc2027HeroVideo` widget now copies the background video's
    source into the modal on click, plays it with sound, and pauses/resets
    it when the modal closes.
  - Added `muted="muted"` to the background `<video>` — it was missing, and
    Chrome/Safari/Firefox all refuse to `autoplay` a video with sound, so
    the "in same position" issue may partly have looked like the video
    wasn't showing at all if autoplay was silently blocked.

  **Hotlinking risk:** the video `src` currently points directly at
  `ambitious-beach-0ac119c03.7.azurestaticapps.net/videos/...mp4` — the
  reference site's own hosting. That's fine for previewing, but is fragile
  long-term (breaks if that site changes/removes the file) and you should
  confirm you actually have the rights to use that specific video before
  shipping it. Once cleared, download it and either add it to
  `static/src/img/` (or a new `static/src/video/`) and ship it in the
  module, or upload it to Odoo's own media library and point `src` at that
  URL instead.
- **v1.0.4** — Proactively fixed the one remaining unverified reference
  flagged in the v1.0.1 note before it caused its own crash:
  `views/layout.xml` called `t-call="website.language_selector"`, which
  isn't the real template id. Checked against actual Odoo 18.0 source
  (`addons/website/views/website_templates.xml`) and every one of Odoo's own
  header variants (`template_header_default`, `template_header_mobile`,
  etc.) calls `t-call="website.placeholder_header_language_selector"`
  instead, setting `_btn_class`/`_dropdown_menu_class`. Updated to match.
- **v1.0.3** — Fixed an install-time crash: `views/snippets_registry.xml`
  targeted `//div[@id='snippet_structure']//div[hasclass('o_panel_body')]`,
  which doesn't exist in Odoo 18
  (`ValueError: Element '<xpath expr="...">' cannot be located in parent
  view`). That guess was based on an older Odoo layout. Odoo 18 rebuilt the
  block picker around a custom `<snippets id="snippet_structure">` element
  with `<t t-snippet="module.xml_id" string="..." group="category"/>`
  entries as direct children — no wrapper divs. This time the fix was
  checked against the real Odoo 18.0 source
  (`addons/website/views/snippets/snippets.xml` on the `18.0` branch)
  instead of guessed from memory, so it should match your instance. Each of
  the six blocks now also has a `group` (intro/content/contact_and_forms)
  and `<keywords>` so they sort into the right category and are searchable
  in the block picker, matching how Odoo's own snippets are registered.
- **v1.0.2** — Fixed a Chrome DevTools "Issue": `@import url(...)` for Google
  Fonts inside `theme.scss` was silently dropped by the browser because Odoo
  concatenates every `web.assets_frontend` file into one bundle, so the
  `@import` was no longer the first rule in the final stylesheet (CSS
  requires `@import` to be first-in-file, or it's ignored — this didn't
  break anything else, it just meant the custom fonts never loaded and the
  page fell back to system fonts). Moved the Google Fonts URL out of the
  SCSS and into `__manifest__.py`'s `web.assets_frontend` list directly —
  Odoo emits external URLs in an asset list as a plain `<link
  rel="stylesheet">` tag instead of trying to concatenate them, which isn't
  subject to the same-file ordering rule.
- **v1.0.1** — Fixed an install-time crash: `s_contact_split.xml` called a
  `website.contactus_form` template that does not actually exist in Odoo 18
  (`ValueError: View 'website.contactus_form' in website 1 not found`) — that
  id was an unverified guess on my part, not something I confirmed against
  Odoo 18 source. Replaced it with a self-contained form built directly on
  Odoo's generic `website_form` mechanism (`<form action="/website/form/"
  data-model_name="mail.mail">` with `name`/`email_from`/`phone`/`subject`/
  `description` fields) — this is the same POST target and field-naming
  convention Odoo's own default Contact Us page uses, and it doesn't depend
  on calling into any core QWeb template by id, so it can't fail the same way.

## If you hit another "not found" / "cannot be located in parent view" error
As of v1.0.4, every core-template reference in this module
(`website.placeholder_header_language_selector` in `views/layout.xml`,
`//snippets[@id='snippet_structure']` in `views/snippets_registry.xml`) has
been checked against the actual Odoo 18.0 source on GitHub
(`odoo/odoo`, `18.0` branch), not just recalled from memory — the two
earlier failures you hit (v1.0.1, v1.0.3) both came from guessing instead of
verifying. If a new instance-specific error still turns up (e.g. you're on a
18.0 point release with local patches, or a different template got
reshuffled), paste the traceback back and it can be checked against the real
source the same way rather than guessed at again.

## Suggested next steps
1. Drop in the real logo, hero video/image, brand colors and fonts.
2. Build out `/about-us`, `/news` (ideally backed by the Website Blog app)
   and a vendors/careers landing page, and confirm this theme's nav/footer
   links against them.
3. Wire the hero "play" button to a real video (YouTube/Vimeo URL or an
   Odoo-hosted MP4) via the `data-oe-video-url` attribute described in
   `static/src/js/theme.js`.
4. Sanity-check the module in a real Odoo 18 instance (install, click
   through every page, test the builder drag-and-drop) — this build was
   authored and validated for XML well-formedness and SCSS/JS syntax
   outside of a running Odoo instance, since one wasn't available in this
   environment.
