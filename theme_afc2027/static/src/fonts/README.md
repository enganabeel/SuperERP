# DIN Next Arabic font files go here

Drop the licensed **DIN Next Arabic** webfont files into this folder using
these exact names (the CSS in `../scss/theme.scss` already points at them —
nothing else needs to change once they're here):

| Weight  | Files to add                                                          |
|---------|------------------------------------------------------------------------|
| Light   | `DINNextLTArabic-Light.woff2`, `DINNextLTArabic-Light.woff`            |
| Regular | `DINNextLTArabic-Regular.woff2`, `DINNextLTArabic-Regular.woff`        |
| Medium  | `DINNextLTArabic-Medium.woff2`, `DINNextLTArabic-Medium.woff`          |
| Bold    | `DINNextLTArabic-Bold.woff2`, `DINNextLTArabic-Bold.woff`              |

- `.woff2` is the one browsers actually use; `.woff` is only a fallback for
  very old browsers. If you only have `.ttf`/`.otf` files from the license,
  convert them to `.woff2`/`.woff` first (e.g. with `fonttools` or an online
  converter) — raw `.ttf` will work in `@font-face` too if you'd rather skip
  conversion, just tell me and I'll add a `.ttf` `src` entry instead.
- If your license only includes some of these four weights, that's fine —
  drop in whichever ones you have and delete the unused `@font-face` blocks
  in `theme.scss` (search for `DIN Next Arabic`), or ask and I'll trim them.
- Until these files exist, Arabic pages keep using Changa (the interim
  placeholder font) automatically — nothing breaks in the meantime, this
  swap is designed to activate itself the moment the real files land.

This file itself isn't a font asset — delete it once the real files are in
place, or leave it, it won't affect anything either way.
