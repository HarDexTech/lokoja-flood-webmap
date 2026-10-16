# Security Report — lokoja-flood-webmap

## 2026-10-16 14:36
- **Checked:** static site, no server-side code or dependencies (Leaflet + CARTO basemap loaded from CDN); manual review of `index.html` and data files; `.gitignore` excludes `build/` intermediates.
- **Findings:**
  - **Low — hard-coded CARTO API key** in `index.html` (`...?key=cb1_4mg1_...`). It is a public client-side basemap key by design, but embedding it in a public repo allows reuse. Fix if desired: register a key restricted to the site's domain, or drop the key (CARTO `light_all` works without it under fair-use).
  - No secrets, credentials or personal data in committed files. No injection surface (no user input, no backend).
- **Status:** No high-severity issues. CARTO key noted, left as-is (public by design), no change made.

## 2026-10-16 16:01
- **Checked:** changes in this update — `index.html` (minZoom), `fix_stats.py` (source raster path), regenerated `data/stats.json`, `data/accuracy_points.geojson`, and rebuilt tile pyramids. Manual review only; no new dependencies, no server-side code, no user input.
- **Findings:** No issues found. Tile change only alters which raster is rendered (masked vs unmasked); no new data exposure. CARTO key still present and still public-by-design (see 14:36 entry) — unchanged.
- **Status:** No high-severity issues; nothing to fix.

## 2026-10-16 16:07
- **Checked:** new client-side code in `index.html` (map click handler, tile pixel sampling via canvas, clipboard copy).
- **Findings:** No issues. Sampling draws same-origin tiles to a canvas (no cross-origin data leak; `crossOrigin='anonymous'` set). Clipboard use is user-initiated copy of a coordinate string only; no sensitive data. Popup content is built from numeric coordinates and fixed strings (no user-controlled HTML injection). No new dependencies or backend.
- **Status:** No high-severity issues; nothing to fix.
