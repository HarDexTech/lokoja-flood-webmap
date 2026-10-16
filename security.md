# Security Report — lokoja-flood-webmap

## 2026-10-16 14:36
- **Checked:** static site, no server-side code or dependencies (Leaflet + CARTO basemap loaded from CDN); manual review of `index.html` and data files; `.gitignore` excludes `build/` intermediates.
- **Findings:**
  - **Low — hard-coded CARTO API key** in `index.html` (`...?key=cb1_4mg1_...`). It is a public client-side basemap key by design, but embedding it in a public repo allows reuse. Fix if desired: register a key restricted to the site's domain, or drop the key (CARTO `light_all` works without it under fair-use).
  - No secrets, credentials or personal data in committed files. No injection surface (no user input, no backend).
- **Status:** No high-severity issues. CARTO key noted, left as-is (public by design), no change made.
