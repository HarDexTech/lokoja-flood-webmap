import os
import json
import geopandas as gpd
import pandas as pd

SRC = r"C:\Users\admin\Documents\ArcGIS\Projects\Flood_Change_Lokoja\Processed"
OUT = r"C:\Users\admin\Documents\lokoja-flood-webmap\data"
os.makedirs(OUT, exist_ok=True)

def write_gj(gdf, name, simplify=None):
    g = gdf.copy()
    if g.crs is not None and g.crs.to_epsg() != 4326:
        g = g.to_crs(4326)
    if simplify is not None:
        g["geometry"] = g.geometry.simplify(simplify, preserve_topology=True)
    g["geometry"] = g.geometry.buffer(0)
    g.to_file(os.path.join(OUT, name), driver="GeoJSON")
    print(f"{name}: {len(g)} feat, {round(os.path.getsize(os.path.join(OUT,name))/1024)} KB")

boundary = gpd.read_file(os.path.join(SRC, "lokoja_boundary.shp"))
write_gj(boundary, "boundary.geojson", 0.0002)

fe = gpd.read_file(os.path.join(SRC, "Flood_Extent_Polygon.shp"))
fe = fe[fe["gridcode"] == 1]
fe_d = fe.dissolve()
flood_km2 = fe_d.to_crs(32632).area.sum() / 1e6
write_gj(fe_d, "flood_extent.geojson", 0.0002)

rz = gpd.read_file(os.path.join(SRC, "Risk_Zones.shp"))
rz_d = rz.dissolve(by="gridcode")
rz_areas = (rz_d.to_crs(32632).area / 1e6).round(2).to_dict()
write_gj(rz_d, "risk_zones.geojson", 0.0002)

fp = gpd.read_file(os.path.join(SRC, "Flood Extent Accuracy Assessment Point.shp"))
flood_oa = float((fp["Classified"] == fp["GrndTruth"]).mean())
write_gj(fp, "accuracy_flood.geojson")

rp = gpd.read_file(os.path.join(SRC, "Risk_Class_Mas_CreateAccurac.shp"))
cm = pd.crosstab(rp["GrndTruth"], rp["Classified"])
oa = float((rp["Classified"] == rp["GrndTruth"]).mean())
n = len(rp)
pe = float((cm.sum(axis=0) * cm.sum(axis=1)).sum() / (n * n))
kappa = (oa - pe) / (1 - pe)
write_gj(rp, "accuracy_risk.geojson")

stats = {
    "flood_extent_km2": round(float(flood_km2), 2),
    "risk_area_km2": {str(k): v for k, v in rz_areas.items()},
    "flood_accuracy": {"n": int(len(fp)), "overall_accuracy": round(flood_oa, 3)},
    "risk_accuracy": {"n": int(n), "overall_accuracy": round(oa, 3), "kappa": round(kappa, 3)},
    "confusion_risk": cm.to_dict(),
}
with open(os.path.join(OUT, "stats.json"), "w") as f:
    json.dump(stats, f, indent=2)

print(json.dumps(stats, indent=2))
