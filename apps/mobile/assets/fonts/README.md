# Tricorder fonts

Archivo 400, 700 and 800 and IBM Plex Mono 400 use the same Latin glyphs and normal width as the prototype. These TTF assets were decoded from the pinned WOFF2 files in `docs/ongoing/style/fonts/` using the repository's FontTools and Node's Brotli decoder, without changing glyphs or font metrics. TTF supports Android as well as iOS and web. Both SIL Open Font Licenses are included here; original download URLs and versions are recorded in that source directory's `SOURCES.md`.

The root loads these bundled assets through the already installed `expo-font`. No network font request or native rebuild is required.
