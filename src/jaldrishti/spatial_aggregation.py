# JalDrishti-AI: Watershed and Village Multi-Scale Spatial Aggregation Pipeline
# Author: JalDrishti-AI Team
# License: Apache-2.0

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
    village_integrated_csv: Path = None,
    out_csv: Path = None,
    out_gpkg: Path = None,
    version: str = "v2"
):
    """
    Executes vectorized area-weighted polygon overlay translating village-level
    rainfall, land-cover, terrain, and soil indicators onto the 518 HydroATLAS Level 8 catchments.
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
    if village_integrated_csv is None:
        village_integrated_csv = processed_dir / "maharashtra_village_integrated_indicators_v1.csv"
    
    if out_csv is None:
        out_csv = processed_dir / f"jaldrishti_watersheds_with_village_indicators_{version}.csv"
    if out_gpkg is None:
        out_gpkg = processed_dir / f"jaldrishti_watersheds_with_village_indicators_{version}.gpkg"

    print("=" * 70)
    print(f"JALDRISHTI-AI: WATERSHED & VILLAGE SPATIAL AGGREGATION ({version.upper()})")
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

    # 2. Load Village Boundaries (.geo) and Integrated Indicators
    print(f"Loading village boundary geometries from: {village_rainfall_csv.name}...")
    t0 = time.time()
    df_geo = pd.read_csv(village_rainfall_csv, usecols=["area_id", ".geo"])
    print(f"Loaded {len(df_geo):,} GeoJSON strings in {time.time()-t0:.2f}s")

    print("Parsing GeoJSON village geometries into Shapely objects...")
    t0 = time.time()
    geoms = shapely.from_geojson(df_geo[".geo"].values)
    gdf_villages = gpd.GeoDataFrame(df_geo[["area_id"]], geometry=geoms, crs="EPSG:4326")
    print(f"Parsed {len(gdf_villages):,} geometries in {time.time()-t0:.2f}s")

    # Load Village Indicators Table
    print(f"Loading integrated village indicators: {village_integrated_csv.name}...")
    t0 = time.time()
    df_indicators = pd.read_csv(village_integrated_csv)
    print(f"Loaded {len(df_indicators):,} rows x {df_indicators.shape[1]} columns in {time.time()-t0:.2f}s")

    # Define Indicator Columns to Aggregate
    ind_cols = [
        # Climate / Drought
        "baseline_mean_annual_mm_2001_2020", "baseline_sd_annual_mm_2001_2020",
        "rainfall_cv_pct", "drought_years_count_2001_2025", "drought_frequency_pct",
        "rainfall_2024_mm", "rainfall_2025_mm", "rainfall_anomaly_2025_pct",
        # Land Cover
        "cropland", "tree_cover", "shrubland", "grassland",
        "built_up", "bare_sparse", "water", "herbaceous_wetland", "mangroves",
        "natural_veg_cover_pct",
        # Terrain v2
        "elevation_mean_m", "slope_mean_deg",
        # SoilGrids v2
        "sand_0_5cm", "clay_0_5cm", "silt_0_5cm", "soc_0_5cm",
        "sand_5_15cm", "clay_5_15cm", "silt_5_15cm", "soc_5_15cm",
        "infiltration_proxy"
    ]
    # Filter to only columns present in df_indicators
    ind_cols = [c for c in ind_cols if c in df_indicators.columns]

    print("Reprojecting villages to UTM Zone 43N (EPSG:32643)...")
    t0 = time.time()
    gdf_villages_utm = gdf_villages.to_crs(epsg=32643)
    print(f"Villages reprojected in {time.time()-t0:.2f}s")

    # 3. Vectorized Polygon Intersection
    print("\nFinding candidate intersecting village-basin pairs (sjoin)...")
    t0 = time.time()
    pairs = gpd.sjoin(
        gdf_villages_utm[["area_id", "geometry"]],
        gdf_basins_utm[["HYBAS_ID", "geometry"]],
        how="inner",
        predicate="intersects"
    )
    print(f"Found {len(pairs):,} candidate pairs in {time.time()-t0:.2f}s")

    print("Computing exact intersection polygons and areas (shapely)...")
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
    df_v_attrs = df_indicators.set_index("area_id")[ind_cols]
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

    # Standardize and humanize column names
    rename_dict = {
        "SUB_AREA": "sub_area_km2",
        "UP_AREA": "up_area_km2",
        "preliminar": "preliminary_screening_score",
        "v_baseline_mean_annual_mm_2001_2020": "village_rainfall_baseline_mean_mm",
        "v_baseline_sd_annual_mm_2001_2020": "village_rainfall_baseline_sd_mm",
        "v_rainfall_cv_pct": "village_rainfall_cv_pct",
        "v_drought_years_count_2001_2025": "village_drought_years_count",
        "v_drought_frequency_pct": "village_drought_frequency_pct",
        "v_rainfall_2024_mm": "village_rainfall_2024_mm",
        "v_rainfall_2025_mm": "village_rainfall_2025_mm",
        "v_rainfall_anomaly_2025_pct": "village_rainfall_anomaly_2025_pct",
        "v_cropland": "village_cropland_pct",
        "v_tree_cover": "village_tree_cover_pct",
        "v_shrubland": "village_shrubland_pct",
        "v_grassland": "village_grassland_pct",
        "v_built_up": "village_built_up_pct",
        "v_bare_sparse": "village_bare_sparse_pct",
        "v_water": "village_water_pct",
        "v_herbaceous_wetland": "village_herbaceous_wetland_pct",
        "v_mangroves": "village_mangroves_pct",
        "v_natural_veg_cover_pct": "village_natural_veg_pct",
        "v_elevation_mean_m": "village_elevation_mean_m",
        "v_slope_mean_deg": "village_slope_mean_deg",
        "v_sand_0_5cm": "village_sand_0_5cm_g_kg",
        "v_clay_0_5cm": "village_clay_0_5cm_g_kg",
        "v_silt_0_5cm": "village_silt_0_5cm_g_kg",
        "v_soc_0_5cm": "village_soc_0_5cm_dg_kg",
        "v_sand_5_15cm": "village_sand_5_15cm_g_kg",
        "v_clay_5_15cm": "village_clay_5_15cm_g_kg",
        "v_silt_5_15cm": "village_silt_5_15cm_g_kg",
        "v_soc_5_15cm": "village_soc_5_15cm_dg_kg",
        "v_infiltration_proxy": "village_infiltration_proxy"
    }
    final_df = final_df.rename(columns=rename_dict)

    # Export CSV
    final_df.to_csv(out_csv, index=False)
    print(f"\nSaved aggregated watershed table to: {out_csv}")
    print(f"Final shape: {final_df.shape[0]} rows x {final_df.shape[1]} columns")

    # Export GeoPackage
    gdf_final = gpd.GeoDataFrame(final_df, geometry=gdf_basins["geometry"], crs="EPSG:4326")
    gdf_final.to_file(out_gpkg, driver="GPKG")
    print(f"Saved GIS GeoPackage to: {out_gpkg}")

    print(f"\n[SUCCESS] Area-weighted spatial aggregation ({version}) completed successfully!")
    return final_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JalDrishti-AI Area-Weighted Spatial Aggregation")
    parser.add_argument("--root", type=str, default=None, help="Project root directory")
    parser.add_argument("--version", type=str, default="v2", help="Aggregation version tag (e.g. v1, v2)")
    args = parser.parse_args()
    root_path = Path(args.root) if args.root else None
    run_spatial_aggregation(project_root=root_path, version=args.version)
