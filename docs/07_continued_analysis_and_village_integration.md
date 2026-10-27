# 7. Continued Analysis & Village-Level Spatial Integration

## Overview of Completed Work
This document records the progress achieved in continuing the JalDrishti-AI GIS decision-support framework from the verified state of the HydroATLAS Level 8 basin layer and village-level physical/demographic datasets.

All operations were executed directly in the project environment using verified Python GIS pipelines without modifying or destroying any original raw source files. A full mirror backup of all 20 initial workspace files was archived under `backup_original/`.

---

## 1. Notebook Audit & Root-Cause Analysis

### 1.1 Audit of Historical Notebooks
An audit of `JalDrishti_Data_Validation_Step1_Cleaned.ipynb` and related notebooks identified:
- **Completed Stages**: District rainfall extraction (2018–2025 CHIRPS), Dynamic World 2023 land cover processing (35 districts + total), Palghar boundary vintage isolation, HydroATLAS Level 8 basin indicator extraction ($N=518$), preliminary screening score computation, and GEE Drive export.
- **Interrupted / Failed Stages**: 
  - Cell 46: Uninitialized Earth Engine authentication.
  - Cells 70 & 80: Memory/timeout limits during single-request composite reductions.
  - Cell 84: Windows PowerShell command syntax error inside Python cell.
  - Cell 258: KeyError on `'abs_difference_pct'`.
  - Cell 291: KeyError `'1080024190'` during dictionary lookup in Earth Engine.
  - Cell 298: Local FileNotFoundError searching for shapefile in `JalDrishti-AI\scored_watersheds\`.
  - Cells 299, 301, 302: NameError due to kernel reset losing variables `task` and `scored_basins`.
  - Notebook terminated at Cell 308; village-level datasets were never processed or integrated.

### 1.2 Root Cause of Missing Village Soil & Terrain Data
Investigation of `maharashtra_village_soilgrids.csv` and `maharashtra_village_terrain.csv` revealed 100% NaN values for physical measurements:
1. **Terrain Bug (`Sentinel-2_Maharstra.ipynb` Cell 60)**:
   The GEE reducer executed `ee.Reducer.mean()` on a multi-band image containing `elevation_m` and `slope_deg`. GEE assigns output property names corresponding to the band names. However, the subsequent export mapping function retrieved `feature.get("mean")` and `feature.get("mean_1")`. Because these keys did not exist, GEE exported `null` across all 44,468 rows.
2. **SoilGrids Bug (`Sentinel-2_Maharstra.ipynb` Cells 82–84)**:
   The ISRIC SoilGrids 250m composite reduction over 44,468 village polygons completed in only 1.69 seconds (Task `WT5KWPMM7P57LQI25CBAZMHA`), demonstrating that the computation was either bypassed, timed out, or omitted from feature attributes.
3. **Preservation Rule**: These columns were left as NaN rather than populated with fabricated or interpolated values. Re-extraction via corrected GEE scripts is documented in the roadmap.

---

## 2. Shapefile & Preliminary Score Validation

The shapefile `jaldrishti_scored_watersheds.shp` was validated with GeoPandas:
- **Topology & Geometry**: 506 Polygons, 12 MultiPolygons ($N=518$). 100% topologically valid (`is_valid == True`), 0 null geometries, 0 empty geometries.
- **CRS**: `EPSG:4326` (WGS 84).
- **Attribute Fields**: `SUB_AREA` ($km^2$), `preliminar` (preliminary screening score, truncated to 10 chars by dBASE format), `HYBAS_ID`, `UP_AREA` ($km^2$).
- **Score Re-computation**:
  $$\text{Score} = \left(0.5 \times \frac{\text{slp\_dg\_sav\_deg} - 0.0}{14.7 - 0.0} + 0.5 \times \left(1 - \frac{\text{pre\_mm\_syr} - 465}{4136 - 465}\right)\right) \times 100$$
  The recomputed score matches `preliminar` in the shapefile with maximum absolute difference of **$1.42 \times 10^{-14}$** (machine precision).
- **Quality Flags in Validation Table**:
  - `runoff_review_flag = 1`: Basins `4081073310` and `4081068170` (Runoff > Precipitation).
  - `terrain_review_flag = 1`: Basin `4080031100` (Flat sea-level coastal catchment).

---

## 3. Spatial Aggregation Methodology: Village to Catchment

### 3.1 Spatial Compatibility
- Administrative village boundaries and hydrological basin catchments do not nest hierarchically. Direct tabular joins by row order or name are invalid.
- However, `maharashtra_village_historical_rainfall_2001_2025_v2.csv` embeds valid GeoJSON Polygon geometries in `.geo`.

### 3.2 Area-Weighted Zonal Aggregation
Using shapely vectorization and UTM Zone 43N (`EPSG:32643`) metric projections:
1. Candidate village-basin intersections: 56,645 pairs identified via spatial index.
2. Exact polygon intersection fragments computed: 56,575 valid fragments (> $100\text{ m}^2$).
3. Area-weighted indicator formula:
   $$\bar{X}_j = \frac{\sum_{i} w_{ij} X_i}{\sum_{i} w_{ij}}, \quad w_{ij} = \text{Area}(V_i \cap B_j)$$
4. Coverage Classification:
   - `full_coverage` ($\ge 90\%$): 402 basins.
   - `substantial_coverage` ($50\% - 90\%$): 53 basins.
   - `partial_border` ($< 50\%$): 62 basins.
   - `transboundary_uncovered` ($0\%$): 1 basin (`4081063690`, located across the Pranhita river on the Telangana bank, ~160m from Maharashtra boundary).

---

## 4. Newly Generated & Verified Deliverables

1. **`backup_original/`**: Complete mirror directory preserving all 20 initial workspace files.
2. **`jaldrishti_spatial_aggregation.py`**: Standalone, reusable, fully vectorized Python script to repeat the spatial intersection and aggregation.
3. **`jaldrishti_watersheds_with_village_indicators.csv`**: Consolidated 518-basin table with 32 columns including HydroATLAS attributes, QA review flags, coverage flags, 25-year CHIRPS rainfall metrics, and 2021 ESA WorldCover land use percentages.
4. **`jaldrishti_watersheds_with_village_indicators.gpkg`**: Open-standard OGC GeoPackage preserving full geometry, spatial index, and long descriptive column names without dBASE truncation.
5. **`jaldrishti_preliminary_watershed_screening.svg`**: Publication-ready vector choropleth map with required metadata, projection, and mandatory non-engineering caveat.
6. **`JalDrishti_Watershed_Analysis_Continued.ipynb`**: Complete, self-contained Jupyter notebook containing all analytical steps, executed in place with all outputs and figures embedded.
7. **`watershed_village_indicators_panel.png`**: High-resolution comparative cartographic panel displaying Preliminary Screening Score, 25-year Village Rainfall Baseline, and Village Cropland Intensity.

---

## 5. Next Analytical Stages

1. **Correct & Re-execute GEE Village Reducers**:
   - Re-extract SoilGrids (sand, clay, silt, SOC) and SRTM DEM (elevation, slope) using corrected property keys (`elevation_m` and `slope_deg`).
2. **Design Four-Pillar Multi-Criteria Prioritisation Model (MCDA)**:
   - Pillar 1: Climate Stress & Drought Recurrence (from 25-yr village CHIRPS).
   - Pillar 2: Land Surface & Human Pressure (from village cropland, tree cover, built-up %).
   - Pillar 3: Surface Drainage & Slope (from HydroATLAS slope and DEM metrics).
   - Pillar 4: Infiltration & Soil Retentivity (from re-extracted SoilGrids texture).
3. **Sensitivity & Stakeholder Review**:
   - Perform rank sensitivity analysis across equal weighting, AHP, and entropy weighting.
   - Keep preliminary outputs clearly designated as screening proxies prior to ground validation.
