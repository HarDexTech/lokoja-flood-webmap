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

## 2026-10-16 16:01
- **What changed:** Fixed the red rectangular patch visible outside the Lokoja boundary, and lowered the minimum zoom to 9.
  - **Root cause:** risk tiles were generated from the **unmasked** `Risk_Class.tif`, whose class 3 (High = red) covers ~6.79M cells including the whole area *outside* the boundary. Switched to `Risk_Class_Masked.tif` (boundary-clipped, NoData=0 outside) so that area is now transparent.
  - Regenerated risk RGBA + tiles (z9–13, 547 tiles) and flood tiles (z9–14, 544 tiles) so both layers render at zoom 9.
  - `index.html`: `minZoom:9`.
  - `fix_stats.py`: now reads `Risk_Class_Masked.tif`; regenerated `data/stats.json` and `data/accuracy_points.geojson`.
  - **Corrected risk areas** (previously inflated by outside-boundary cells): Low 4414.55 km², Medium 2119.47 km², High 981.39 km² (High was ~6113 km²).
- **Verification:** local `python -m http.server` — index, a z9 flood tile, a z9 risk tile and `stats.json` all HTTP 200. Flood accuracy unchanged (96.2%, n=208).
- **Notable:** Committed as `9a7e840`. Not yet pushed. `prep_layers.py` had unrelated formatting changes in the working tree (not made here) — left uncommitted.
