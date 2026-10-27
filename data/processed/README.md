# Processed Data Directory (`data/processed/`)

This directory houses the authoritative GIS layers and catchment-level aggregation products ready for multi-criteria decision modeling.

## Inventory of Files

### 1. WWF HydroATLAS Level 8 Basins (ESRI Shapefile)
- Files: `jaldrishti_scored_watersheds.shp`, `.shx`, `.dbf`, `.prj`, `.fix`
- **Features**: 518 polygonal basin features covering Maharashtra.
- **CRS**: `EPSG:4326` (WGS 84).
- **Attributes**: `HYBAS_ID`, `SUB_AREA` (km²), `UP_AREA` (km²), `preliminar` (illustrative screening score, 0–100).
- **Topological Integrity**: 100% valid geometries, 0 empty, 0 nulls.

### 2. Consolidated Catchment Indicators (CSV & GeoPackage)
- Files: `jaldrishti_watersheds_with_village_indicators.csv` (207 KB), `jaldrishti_watersheds_with_village_indicators.gpkg` (1.99 MB)
- **Features**: 518 catchments.
- **Attributes (32 columns)**:
  - Basin identifiers and HydroATLAS metrics: `HYBAS_ID`, `sub_area_km2`, `up_area_km2`, `ele_mt_uav`, `pre_mm_syr`, `run_mm_syr`, `slp_dg_sav_deg`, `slp_dg_uav_deg`.
  - Preliminary score: `preliminary_screening_score` (0–100).
  - Spatial coverage metrics: `village_count_intersecting`, `village_covered_area_km2`, `village_coverage_pct`, `village_coverage_flag`.
  - Area-weighted 25-year rainfall metrics: `village_rainfall_baseline_mean_mm`, `village_rainfall_baseline_sd_mm`, `village_rainfall_baseline_cv_pct`, `village_rainfall_2024_mm`, `village_rainfall_2025_mm`, `village_rainfall_anomaly_2025_pct`.
  - Area-weighted land-cover fractions: `village_cropland_pct`, `village_tree_cover_pct`, `village_shrubland_pct`, `village_grassland_pct`, `village_built_up_pct`, `village_bare_sparse_pct`, `village_water_pct`, `village_herbaceous_wetland_pct`, `village_mangroves_pct`.
  - Hydrological QA flags: `quality_review_flag`, `runoff_review_flag`, `terrain_review_flag`.
