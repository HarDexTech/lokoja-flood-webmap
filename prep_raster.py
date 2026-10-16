import os, json, math
import numpy as np
import rasterio
from affine import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling
from PIL import Image

MAXPX = 2000
import geopandas as gpd
import pandas as pd

SRC = r"C:\Users\admin\Documents\ArcGIS\Projects\Flood_Change_Lokoja\Processed"
OUT = r"C:\Users\admin\Documents\lokoja-flood-webmap\data"
os.makedirs(OUT, exist_ok=True)

def to_overlay(tif, mapping, out_png):
    with rasterio.open(tif) as src:
        dst_crs = "EPSG:4326"
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        step = max(1, math.ceil(max(width, height) / MAXPX))
        width = math.ceil(width / step)
        height = math.ceil(height / step)
        transform = transform * Affine.scale(step, step)
        data = np.zeros((height, width), dtype="float32")
        reproject(
            source=rasterio.band(src, 1), destination=data,
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=transform, dst_crs=dst_crs,
            resampling=Resampling.nearest)
        rgba = np.zeros((height, width, 4), dtype=np.uint8)
        for val, (r, g, b, a) in mapping.items():
            rgba[data == val] = (r, g, b, a)
        Image.fromarray(rgba, "RGBA").save(os.path.join(OUT, out_png))
        west = transform.c
        north = transform.f
        east = transform.c + transform.a * width
        south = transform.f + transform.e * height
        kb = os.path.getsize(os.path.join(OUT, out_png)) / 1024
        print(f"{out_png}: {width}x{height}, {kb:.0f} KB, bounds {west},{south},{east},{north}")
        return [west, south, east, north]

risk_map = {1: (26, 152, 80, 190), 2: (254, 204, 92, 190), 3: (215, 48, 39, 190)}
flood_map = {1: (43, 140, 255, 170)}
risk_bounds = to_overlay(os.path.join(SRC, "Risk_Class.tif"), risk_map, "risk_classes.png")
flood_bounds = to_overlay(os.path.join(SRC, "Flood_Extent_Clean.tif"), flood_map, "flood_extent.png")

def points_geojson(tif_pts, out_name):
    g = gpd.read_file(tif_pts)
    if g.crs.to_epsg() != 4326:
        g = g.to_crs(4326)
    g.to_file(os.path.join(OUT, out_name), driver="GeoJSON")
    print(f"{out_name}: {len(g)} pts")

points_geojson(os.path.join(SRC, "Flood Extent Accuracy Assessment Point.shp"), "accuracy_flood.geojson")
points_geojson(os.path.join(SRC, "Risk_Class_Mas_CreateAccurac.shp"), "accuracy_risk.geojson")

fp = gpd.read_file(os.path.join(SRC, "Flood Extent Accuracy Assessment Point.shp"))
f_acc = float((fp["Classified"] == fp["GrndTruth"]).mean())

rp = gpd.read_file(os.path.join(SRC, "Risk_Class_Mas_CreateAccurac.shp"))
cm = pd.crosstab(rp["GrndTruth"], rp["Classified"])
oa = float((rp["Classified"] == rp["GrndTruth"]).mean())
n = len(rp)
pe = float((cm.sum(axis=0) * cm.sum(axis=1)).sum() / (n * n))
kappa = (oa - pe) / (1 - pe)

with rasterio.open(os.path.join(SRC, "Flood_Extent_Clean.tif")) as src:
    px = abs(src.transform.a * src.transform.e)
    flood_px = int((src.read(1) == 1).sum())
flood_km2 = round(flood_px * px / 1e6, 2)

with rasterio.open(os.path.join(SRC, "Risk_Class.tif")) as src:
    px = abs(src.transform.a * src.transform.e)
    band = src.read(1)
    risk_km2 = {str(v): round(int((band == v).sum()) * px / 1e6, 2) for v in (1, 2, 3)}

stats = {
    "flood_extent_km2": flood_km2,
    "risk_area_km2": risk_km2,
    "flood_accuracy": {"n": int(len(fp)), "overall_accuracy": round(f_acc, 3)},
    "risk_accuracy": {"n": int(n), "overall_accuracy": round(oa, 3), "kappa": round(kappa, 3)},
    "risk_bounds": risk_bounds,
    "flood_bounds": flood_bounds,
    "confusion_risk": cm.to_dict(),
}
with open(os.path.join(OUT, "stats.json"), "w") as f:
    json.dump(stats, f, indent=2)
print(json.dumps(stats, indent=2))
