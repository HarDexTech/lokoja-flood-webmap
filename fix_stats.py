import os, json
import rasterio
import geopandas as gpd
import pandas as pd

SRC = r"C:\Users\admin\Documents\ArcGIS\Projects\Flood_Change_Lokoja\Processed"
OUT = r"C:\Users\admin\Documents\lokoja-flood-webmap\data"

ref = gpd.read_file(os.path.join(SRC, "Accuracy_Points_Ref.shp"))
oa = float((ref["Classified"] == ref["GrndTruth"]).mean())
ref = ref.to_crs(4326) if ref.crs.to_epsg() != 4326 else ref
ref["correct"] = (ref["Classified"] == ref["GrndTruth"]).astype(int)
ref.to_file(os.path.join(OUT, "accuracy_points.geojson"), driver="GeoJSON")

with rasterio.open(os.path.join(SRC, "Flood_Extent_Clean.tif")) as src:
    px = abs(src.transform.a * src.transform.e)
    flood_km2 = round(int((src.read(1) == 1).sum()) * px / 1e6, 2)
with rasterio.open(os.path.join(SRC, "Risk_Class_Masked.tif")) as src:
    px = abs(src.transform.a * src.transform.e)
    band = src.read(1)
    risk_km2 = {str(v): round(int((band == v).sum()) * px / 1e6, 2) for v in (1, 2, 3)}

stats = {
    "flood_extent_km2": flood_km2,
    "risk_area_km2": risk_km2,
    "flood_accuracy": {"n": int(len(ref)), "overall_accuracy": round(oa, 3)},
}
with open(os.path.join(OUT, "stats.json"), "w") as f:
    json.dump(stats, f, indent=2)
print(json.dumps(stats, indent=2))
