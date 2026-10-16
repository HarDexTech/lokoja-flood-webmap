# Change Report — lokoja-flood-webmap

## 2026-10-16 14:36
- **What changed:** Replaced single-PNG image overlays with XYZ raster tiles.
  - New: `data/tiles/flood/{z}/{x}/{y}.png` (z10–14, 541 tiles), `data/tiles/risk/{z}/{x}/{y}.png` (z10–13, 824 tiles).
  - `index.html`: `L.imageOverlay` → `L.tileLayer`; map `minZoom:9, maxZoom:16`; risk `maxNativeZoom:13`, flood `maxNativeZoom:14`.
  - Removed `data/risk_classes.png`, `data/flood_extent.png` (obsolete).
  - Added `.gitignore` (ignores `build/` intermediates: RGBA GeoTIFFs, colour tables).
  - `README.md`: data table updated to tile paths.
  - Why: single PNG was blurry when zoomed; tiles are sharp at every zoom and only visible tiles load.
- **Verification:** Local `python -m http.server 8123` — index, a flood tile, a risk tile, boundary and stats all HTTP 200. Tile counts/size: 1365 tiles, 4.14 MB.
- **Notable:** Committed as `bdce90a`. Not yet pushed. Tiles generated with QGIS `gdal2tiles` (`--xyz`, mercator profile) from `gdaldem color-relief -alpha` RGBA rasters of the ArcGIS source layers.
