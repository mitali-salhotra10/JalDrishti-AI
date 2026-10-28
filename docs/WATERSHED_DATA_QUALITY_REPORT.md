# JalDrishti-AI: Watershed Indicators (v2) Quality & Consistency Audit

**Target Layer**: `jaldrishti_watersheds_with_village_indicators_v2.csv` & `.gpkg`  
**Total Catchments**: 518 HydroATLAS Level 8 Basin Polygons  
**CRS**: EPSG:4326 (WGS84 Geographic) | Metric Projected CRS: EPSG:32643 (UTM 43N)  
**Total Features**: 46 Columns  

## 1. Geometric & Topological Verification

- **Feature Count**: Exactly 518 polygons.
- **Identifier Integrity**: 100% unique `HYBAS_ID` across all 518 catchments (zero duplicate keys).
- **Topological Validity**: 100% valid polygon geometries (verified via `shapely.is_valid`). Zero self-intersections or bowtie vertices.
- **Area Consistency**: Pearson $r = 0.999993$ between HydroATLAS `sub_area_km2` attribute and exact UTM 43N polygon geometry area (`basin_geom_area_km2`), demonstrating strict geometric preservation.

## 2. Spatial Coverage & Boundary Boundary Accounting

Maharashtra state borders intersect HydroATLAS Level 8 catchments that naturally extend beyond administrative frontiers. Each catchment is explicitly flagged:

| Coverage Category | Threshold | Catchment Count | Percentage (%) | Description |
| :--- | :--- | :--- | :--- | :--- |
| `full_coverage` | 77.6% | 402 | 77.61% | Entirely or almost entirely within Maharashtra; highly reliable aggregated metrics. |
| `partial_border` | 12.0% | 62 | 11.97% | Cross-border catchments along state perimeter; metrics represent the Maharashtra portion. |
| `substantial_coverage` | 10.2% | 53 | 10.23% | Majority within Maharashtra; robust area-weighted representation. |
| `transboundary_uncovered` | 0.2% | 1 | 0.19% | Single catchment with virtually zero village overlap (<0.01%); reserved for transboundary analysis. |

## 3. Multi-Scale Empirical Cross-Validation

To verify that area-weighted polygon overlay from 44,468 village polygons accurately scales to HydroATLAS Level 8 catchments, we computed cross-scale correlation statistics against independent HydroATLAS baseline variables for all 402 full-coverage catchments:

| Physical Variable | Basin Baseline Source | Village Aggregated Metric | Pearson $r$ | Spearman $\rho$ | Scientific Finding |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Elevation** | HydroATLAS `ele_mt_uav` | SRTM v2 `village_elevation_mean_m` | **0.9213** | **0.9170** | Near-perfect agreement confirms spatial alignment. |
| **Slope** | HydroATLAS `slp_dg_sav_deg` | SRTM v2 `village_slope_mean_deg` | **0.9909** | **0.9516** | High concordance confirms regional topographic fidelity. |
| **Precipitation** | HydroATLAS `pre_mm_syr` | CHIRPS `village_rainfall_baseline_mean_mm` | **0.9524** | **0.9398** | Strong regional correlation capturing Western Ghats-to-Plateau gradient. |

## 4. Soil Texture & Physical Consistency

- **Conservation of Mass**: Watershed-level mean texture sum (`sand` + `clay` + `silt`) is **1000.00 g/kg** (100.00%).
- **Catchment Soil Coverage**: 517 out of 518 catchments (99.81%) have complete, populated soil metrics. Only the single transboundary uncovered catchment has NaN, consistent with its zero village coverage.

## 5. Statistical Distribution of Key Aggregated Indicators

| Indicator | Mean | Std | Min | 25% | Median | 75% | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `village_rainfall_baseline_mean_mm` | 1121.28 | 509.06 | 518.58 | 779.69 | 983.34 | 1354.34 | 3082.47 |
| `village_rainfall_cv_pct` | 20.20 | 4.02 | 11.91 | 17.05 | 20.45 | 23.66 | 27.87 |
| `village_drought_years_count` | 2.17 | 1.30 | 0.00 | 1.00 | 2.00 | 3.29 | 5.25 |
| `village_cropland_pct` | 56.44 | 25.51 | 1.79 | 37.20 | 61.79 | 77.66 | 93.98 |
| `village_tree_cover_pct` | 19.64 | 22.56 | 0.31 | 3.31 | 8.80 | 28.70 | 91.06 |
| `village_elevation_mean_m` | 420.32 | 187.55 | 0.81 | 273.49 | 410.38 | 574.01 | 847.08 |
| `village_slope_mean_deg` | 4.22 | 2.78 | 0.78 | 2.45 | 3.14 | 4.77 | 18.93 |
| `village_clay_0_5cm_g_kg` | 403.95 | 44.90 | 261.90 | 370.43 | 404.24 | 439.41 | 510.38 |
| `village_sand_0_5cm_g_kg` | 287.94 | 55.79 | 119.52 | 255.45 | 288.52 | 324.30 | 471.33 |
| `village_soc_0_5cm_dg_kg` | 169.35 | 62.60 | 88.93 | 126.24 | 145.99 | 191.65 | 364.22 |
| `village_infiltration_proxy` | 1.12 | 0.25 | 0.69 | 0.92 | 1.10 | 1.29 | 2.30 |

