# JalDrishti-AI: Watershed and Village Multi-Scale Spatial Aggregation Pipeline
# Author: JalDrishti-AI Team
# License: Apache-2.0 or project default

import argparse
import time
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely

def get_project_root() -> Path:
    """Detect project root directory dynamically."""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists() or (parent / "data").exists():
            return parent
    return Path.cwd()

def run_spatial_aggregation(
    project_root: Path = None,
    basins_shp: Path = None,
    validation_csv: Path = None,
    village_rainfall_csv: Path = None,
    village_landcover_csv: Path = None,
    out_csv: Path = None,
    out_gpkg: Path = None
):
    """
    Executes the vectorized area-weighted polygon overlay translating village-level
    rainfall and land-cover metrics onto the 518 HydroATLAS Level 8 catchments.
    """
    if project_root is None:
        project_root = get_project_root()

    data_dir = project_root / "data"
    raw_dir = data_dir / "raw"
    interim_dir = data_dir / "interim"
    processed_dir = data_dir / "processed"

    if basins_shp is None:
        basins_shp = processed_dir / "jaldrishti_scored_watersheds.shp"
    if validation_csv is None:
        validation_csv = interim_dir / "jaldrishti_watershed_validation_518_basins.csv"
    if village_rainfall_csv is None:
        village_rainfall_csv = raw_dir / "maharashtra_village_historical_rainfall_2001_2025_v2.csv"
    if village_landcover_csv is None:
        village_landcover_csv = raw_dir / "maharashtra_village_landcover_2021.csv"
    if out_csv is None:
        out_csv = processed_dir / "jaldrishti_watersheds_with_village_indicators.csv"
    if out_gpkg is None:
        out_gpkg = processed_dir / "jaldrishti_watersheds_with_village_indicators.gpkg"

    print("=" * 70)
    print("JALDRISHTI-AI: WATERSHED & VILLAGE SPATIAL AGGREGATION")
    print(f"Project Root: {project_root}")
    print("=" * 70)

    # 1. Load HydroATLAS Level 8 Basins
    print(f"Loading HydroATLAS shapefile: {basins_shp}...")
    t0 = time.time()
    gdf_basins = gpd.read_file(basins_shp)
    print(f"Loaded {len(gdf_basins)} basins in {time.time()-t0:.2f}s (CRS: {gdf_basins.crs})")

    # Load HydroATLAS validation table for QA flags
    print(f"Loading validation indicators: {validation_csv}...")
    df_val = pd.read_csv(validation_csv)
    val_cols = [
        "HYBAS_ID", "ele_mt_uav", "pre_mm_syr", "run_mm_syr",
        "slp_dg_sav_deg", "slp_dg_uav_deg",
        "quality_review_flag", "runoff_review_flag", "terrain_review_flag"
    ]
    gdf_basins = gdf_basins.merge(df_val[val_cols], on="HYBAS_ID", how="left")

    # Reproject basins to UTM Zone 43N (EPSG:32643) for metric area calculations
    print("Reprojecting basins to UTM Zone 43N (EPSG:32643)...")
    gdf_basins_utm = gdf_basins.to_crs(epsg=32643)
    gdf_basins_utm["basin_geom_area_km2"] = gdf_basins_utm.geometry.area / 1e6

    # 2. Load Village Datasets (Rainfall & Land Cover)
    print(f"Loading village historical rainfall dataset: {village_rainfall_csv}...")
    t0 = time.time()
    rf_cols = [
        "area_id", "district", "subdistric", "village", "vlcode",
        "baseline_mean_annual_mm_2001_2020", "baseline_sd_annual_mm_2001_2020",
        "rainfall_2024_mm", "rainfall_2025_mm", "rainfall_anomaly_2025_pct",
        ".geo"
    ]
    df_villages = pd.read_csv(village_rainfall_csv, usecols=rf_cols)
    print(f"Loaded {len(df_villages):,} village rows in {time.time()-t0:.2f}s")

    print("Parsing GeoJSON village boundaries...")
    t0 = time.time()
    geoms = shapely.from_geojson(df_villages[".geo"].values)
    gdf_villages = gpd.GeoDataFrame(df_villages.drop(columns=[".geo"]), geometry=geoms, crs="EPSG:4326")
    print(f"Parsed {len(gdf_villages):,} geometries in {time.time()-t0:.2f}s")

    # Load 2021 ESA WorldCover LULC
    print(f"Loading village 2021 land cover dataset: {village_landcover_csv}...")
    df_lulc = pd.read_csv(village_landcover_csv)
    lulc_cols = [
        "area_id", "tree_cover", "shrubland", "grassland", "cropland",
        "built_up", "bare_sparse", "water", "herbaceous_wetland", "mangroves"
    ]
    gdf_villages = gdf_villages.merge(df_lulc[lulc_cols], on="area_id", how="left")

    print("Reprojecting villages to UTM Zone 43N (EPSG:32643)...")
    t0 = time.time()
    gdf_villages_utm = gdf_villages.to_crs(epsg=32643)
    print(f"Villages reprojected in {time.time()-t0:.2f}s")

    # 3. Vectorized Polygon Intersection
    print("\nFinding candidate intersecting village-basin pairs...")
    t0 = time.time()
    pairs = gpd.sjoin(
        gdf_villages_utm[["area_id", "geometry"]],
        gdf_basins_utm[["HYBAS_ID", "geometry"]],
        how="inner",
        predicate="intersects"
    )
    print(f"Found {len(pairs):,} candidate pairs in {time.time()-t0:.2f}s")

    print("Computing exact intersection polygons and areas...")
    t0 = time.time()
    v_geoms = gdf_villages_utm.set_index("area_id")["geometry"].loc[pairs["area_id"]].values
    b_geoms = gdf_basins_utm.set_index("HYBAS_ID")["geometry"].loc[pairs["HYBAS_ID"]].values

    inter_geoms = shapely.intersection(v_geoms, b_geoms)
    inter_areas_km2 = shapely.area(inter_geoms) / 1e6

    # Filter out sliver intersections (< 100 m² = 1e-4 km²)
    valid_mask = inter_areas_km2 > 1e-4
    pairs_clean = pairs[valid_mask].copy()
    pairs_clean["inter_area_km2"] = inter_areas_km2[valid_mask]
    print(f"Retained {len(pairs_clean):,} valid intersection fragments in {time.time()-t0:.2f}s")

    # Attach village attributes to intersection fragments
    print("Attaching village indicators to fragments...")
    ind_cols = [
        "baseline_mean_annual_mm_2001_2020", "baseline_sd_annual_mm_2001_2020",
        "rainfall_2024_mm", "rainfall_2025_mm", "rainfall_anomaly_2025_pct",
        "tree_cover", "shrubland", "grassland", "cropland", "built_up",
        "bare_sparse", "water", "herbaceous_wetland", "mangroves"
    ]
    df_v_attrs = gdf_villages.set_index("area_id")[ind_cols]
    pairs_with_attrs = pairs_clean.join(df_v_attrs, on="area_id")

    # 4. Perform Area-Weighted Zonal Aggregation for Each Basin
    print("Calculating area-weighted averages per basin...")
    t0 = time.time()

    def aggregate_basin(group):
        w = group["inter_area_km2"].values
        total_w = w.sum()
        n_villages = group["area_id"].nunique()

        res = {
            "village_count_intersecting": n_villages,
            "village_covered_area_km2": total_w,
        }

        for col in ind_cols:
            vals = group[col].values
            valid = ~np.isnan(vals)
            if np.any(valid) and np.sum(w[valid]) > 0:
                res[f"v_{col}"] = np.sum(vals[valid] * w[valid]) / np.sum(w[valid])
            else:
                res[f"v_{col}"] = np.nan

        return pd.Series(res)

    # Pandas 2.2+ forward compatible with include_groups=False
    try:
        basin_agg = pairs_with_attrs.groupby("HYBAS_ID").apply(aggregate_basin, include_groups=False)
    except TypeError:
        basin_agg = pairs_with_attrs.groupby("HYBAS_ID").apply(aggregate_basin)

    print(f"Basin aggregation completed in {time.time()-t0:.2f}s for {len(basin_agg)} basins")

    # 5. Merge with All 518 Basins
    print("Merging aggregated metrics with full basin layer...")
    final_df = gdf_basins_utm.drop(columns=["geometry"]).merge(basin_agg, on="HYBAS_ID", how="left")

    final_df["village_coverage_pct"] = (final_df["village_covered_area_km2"] / final_df["basin_geom_area_km2"]) * 100
    final_df["village_coverage_pct"] = final_df["village_coverage_pct"].clip(upper=100.0)

    def classify_coverage(pct):
        if pd.isna(pct) or pct == 0:
            return "transboundary_uncovered"
        elif pct >= 90:
            return "full_coverage"
        elif pct >= 50:
            return "substantial_coverage"
        else:
            return "partial_border"

    final_df["village_coverage_flag"] = final_df["village_coverage_pct"].apply(classify_coverage)

    # Compute derived village rainfall CV (%)
    final_df["v_rainfall_baseline_cv_pct"] = (
        final_df["v_baseline_sd_annual_mm_2001_2020"] / final_df["v_baseline_mean_annual_mm_2001_2020"]
    ) * 100

    # Reorder and rename columns cleanly
    rename_dict = {
        "SUB_AREA": "sub_area_km2",
        "UP_AREA": "up_area_km2",
        "preliminar": "preliminary_screening_score",
        "v_baseline_mean_annual_mm_2001_2020": "village_rainfall_baseline_mean_mm",
        "v_baseline_sd_annual_mm_2001_2020": "village_rainfall_baseline_sd_mm",
        "v_rainfall_2024_mm": "village_rainfall_2024_mm",
        "v_rainfall_2025_mm": "village_rainfall_2025_mm",
        "v_rainfall_anomaly_2025_pct": "village_rainfall_anomaly_2025_pct",
        "v_rainfall_baseline_cv_pct": "village_rainfall_baseline_cv_pct",
        "v_cropland": "village_cropland_pct",
        "v_tree_cover": "village_tree_cover_pct",
        "v_shrubland": "village_shrubland_pct",
        "v_grassland": "village_grassland_pct",
        "v_built_up": "village_built_up_pct",
        "v_bare_sparse": "village_bare_sparse_pct",
        "v_water": "village_water_pct",
        "v_herbaceous_wetland": "village_herbaceous_wetland_pct",
        "v_mangroves": "village_mangroves_pct",
    }
    final_df = final_df.rename(columns=rename_dict)

    final_df.to_csv(out_csv, index=False)
    print(f"\nSaved aggregated watershed table to: {out_csv}")
    print(f"Final shape: {final_df.shape[0]} rows x {final_df.shape[1]} columns")

    gdf_final = gpd.GeoDataFrame(final_df, geometry=gdf_basins["geometry"], crs="EPSG:4326")
    gdf_final.to_file(out_gpkg, driver="GPKG")
    print(f"Saved GIS GeoPackage to: {out_gpkg}")

    print("\n[SUCCESS] Area-weighted spatial aggregation completed successfully!")
    return final_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JalDrishti-AI Area-Weighted Spatial Aggregation")
    parser.add_argument("--root", type=str, default=None, help="Project root directory")
    args = parser.parse_args()
    root_path = Path(args.root) if args.root else None
    run_spatial_aggregation(project_root=root_path)
