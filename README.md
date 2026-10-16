# Flood Extent & Risk Web Map — Lokoja, Kogi State, Nigeria

Interactive web map of the 2022 flood extent and flood-risk zones for the Lokoja
study area, built from satellite imagery and terrain analysis in ArcGIS Pro.

**Live map:** _add your GitHub Pages link here after deploy_

## What it shows

- **2022 flood extent** — 151 km² mapped from Sentinel-1 SAR change detection.
- **Flood-risk zones** — terrain reclassified into three risk classes.
- **Validation points** — reference points with correct/incorrect classification.

## Method

1. Sentinel-1 SAR change detection (pre-flood vs post-flood scenes).
2. DEM hydrology — fill, flow direction, flow accumulation, stream network, watershed.
3. Slope, elevation and flow reclassified into flood-risk zones.
4. Population exposure estimated with a WorldPop overlay.
5. Accuracy assessed against reference points: **96.2% overall (n = 208)**.

## Data

| Layer | File | Type |
|---|---|---|
| Flood risk zones | `data/risk_classes.png` | image overlay |
| 2022 flood extent | `data/flood_extent.png` | image overlay |
| Study area boundary | `data/boundary.geojson` | vector |
| Validation points | `data/accuracy_points.geojson` | vector |
| Figures | `data/stats.json` | table |

## Stack

- **Analysis:** ArcGIS Pro (SAR, Spatial Analyst, WorldPop)
- **Web map:** Leaflet, HTML/CSS/JavaScript
- **Hosting:** GitHub Pages

## Run locally

```
python -m http.server 8123
```

Then open `http://localhost:8123`.
