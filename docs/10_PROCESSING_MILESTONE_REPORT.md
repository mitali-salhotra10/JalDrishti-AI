# JalDrishti-AI — Processing Milestone Report (Milestone 10)

**Date**: October 27, 2026  
**Execution Environment**: Python 3.13.1 on Windows (x64)  
**Earth Engine Project**: `jaldrishti-508107`  
**Google Drive Destination**: `JalDrishti_AI`  
**Git Repository**: `mitali-salhotra10/JalDrishti-AI` (Commit `aba5048`+)

---

## 1. Executive Summary & Verification of Export Status (Step 1 & Step 2)

Before initiating data transformations, an audit of the Earth Engine export task queue was executed via `export_village_terrain_soil_gee.py --check-status`. The pre-flight 24-village sample tests and batch exports were inspected:

### Earth Engine Task Registry Audit

| Task ID | Task Description | Target Output | Status | EECU-Seconds | Verification & Findings |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `AWTFFQN4LV4YFEUUF3A3CD7Y` | `JalDrishti_Maharashtra_Village_Terrain_v2` | `maharashtra_village_terrain_v2.csv` | **COMPLETED** | 24,292 | Full extraction for all 44,468 villages; 100% non-null measurements. |
| `E72XGBO6ETBA4OISPTF6EXVV` | `JalDrishti_Maharashtra_Village_SoilGrids_v2` | `maharashtra_village_soilgrids_v2.csv` | **COMPLETED** | 604.9 | Reprojected with `crs="EPSG:4326"`; 44,417 valid terrestrial records (99.89%). |
| `FNTLTGZWSGKOKWJGOVEGD4OS` | `Test_Soil_Export_Small` | Drive Test CSV | **COMPLETED** | 12.1 | Pre-flight test verifying non-null output after `EPSG:4326` CRS fix. |
| `EZWHBY4N7N3PJYW6XC3KITQD` | `JalDrishti_Maharashtra_Village_SoilGrids_v2` | `maharashtra_village_soilgrids_v2.csv` | *FAILED (Nulls)* | 582.4 | Prior execution lacking `crs="EPSG:4326"`; caused World Mollweide spatial clip failure. Superseded by `E72XGBO6ETBA4OISPTF6EXVV`. |

Because both full exports were successfully executed and completed on GEE, no duplicate exports were launched. Both resulting files were programmatically retrieved from Google Drive via the Drive v3 API and saved to `data/raw/`.

---

## 2. Validation of Completed Files (Step 3)

Original raw CSVs (`maharashtra_village_terrain.csv` and `maharashtra_village_soilgrids.csv`) were preserved untouched in `data/raw/` and `backup_original/`. The versioned outputs were subjected to strict automated verification:

### File Statistics & Coverage

- **`maharashtra_village_terrain_v2.csv`**:
  - File Size: 3,492,651 bytes
  - Dimensions: 44,468 rows $\times$ 7 columns
  - Unique `area_id`: **44,468** (100.0% unique; zero duplicate keys)
  - Unique `vlcode`: 44,203 (forest blocks share placeholder codes)
  - Completeness: **100.00% (0 nulls)** across both physical columns:
    - `elevation_mean_m`: Mean = 399.21 m, Min = -0.56 m, Max = 1,328.08 m, SD = 209.77 m
    - `slope_mean_deg`: Mean = 4.27°, Min = 0.00°, Max = 40.11°, SD = 3.74°

- **`maharashtra_village_soilgrids_v2.csv`**:
  - File Size: 8,378,715 bytes
  - Dimensions: 44,468 rows $\times$ 13 columns
  - Unique `area_id`: **44,468** (100.0% unique; zero duplicate keys)
  - Completeness: **99.89% (44,417 valid, 51 nulls)**. The 51 nulls are coastal islands (Mumbai harbor, Raigad) and open reservoir bodies masked in ISRIC's global land mask. No missing values were fabricated.
  - Physical Mass Conservation Check:
    $$\text{Sum} = \text{Sand}_{0-5cm} + \text{Clay}_{0-5cm} + \text{Silt}_{0-5cm}$$
    - Mean Sum: **$1,000.00\text{ g/kg}$** ($\sigma = 0.10\text{ g/kg}$, Min = 999.00, Max = 1001.00)
    - Validates 100% physical consistency and correct band mapping.
  - Soil Organic Carbon (`soc_0_5cm`):
    - Units: decigrams per kilogram ($dg/kg$, where $10\text{ dg/kg} = 1\text{ g/kg} = 0.1\%$).
    - Mean = 173.27 dg/kg (1.73%), Min = 75.75 dg/kg (0.76%), Max = 792.33 dg/kg (7.92%). High values align with dense forest soils in the Western Ghats; lower values characterize intensively tilled vertisols.

---

## 3. Integrated Village Dataset Construction (Step 4)

- **Script**: `scripts/build_village_integrated_indicators.py`
- **Output File**: `data/processed/maharashtra_village_integrated_indicators_v1.csv` (46,442,715 bytes, 44,468 rows $\times$ 69 columns)
- **Quality Report**: `docs/VILLAGE_DATA_QUALITY_REPORT.md`

### Integration Architecture
1. **Join Key**: Joined strictly on `area_id`. Validated 1:1 cardinality (exactly 44,468 rows maintained without drops or cartesian inflation).
2. **Memory & I/O Optimization**: The 140 MB `.geo` GeoJSON column from the raw rainfall CSV was omitted from the tabular integrated CSV, reducing file size by 70% while accelerating load times to under 1 second.
3. **Derived Analytical Variables**:
   - `rainfall_cv_pct`: Inter-annual coefficient of variation ($SD / Mean \times 100$). Mean = 19.90%, Max = 29.04%.
   - `drought_years_count_2001_2025`: Number of years (out of 25) where annual rainfall was $< 75\%$ of the 2001–2020 baseline mean. Mean = 2.01 years, Max = 6.00 years.
   - `natural_veg_cover_pct`: Sum of tree cover, shrubland, and grassland from ESA WorldCover 2021.
   - `infiltration_proxy`: Hydraulic texture ratio $(Sand + 0.5 \cdot Silt) / (Clay + 1.0)$. Mean = 1.09, Range = 0.55 to 2.37.
   - `usda_texture_class`: Standard USDA soil classification:
     - Clay: 23,909 villages (53.77%)
     - Clay Loam: 18,419 villages (41.42%)
     - Silty Clay: 1,247 villages (2.80%)
     - Silty Clay Loam: 708 villages (1.59%)
     - Sandy Clay Loam: 94 villages (0.21%)
     - Loam / Sand: 40 villages (0.09%)
     - Unclassified Water/Coastal Mask: 51 villages (0.11%)

---

## 4. Multi-Scale Watershed Aggregation (v2) (Step 5)

- **Pipeline**: `src/jaldrishti/spatial_aggregation.py` (with root CLI entrypoint `jaldrishti_spatial_aggregation.py`)
- **Version Tag**: `v2`
- **Output Files**:
  - `data/processed/jaldrishti_watersheds_with_village_indicators_v2.csv` (219,836 bytes, 518 rows $\times$ 46 columns)
  - `data/processed/jaldrishti_watersheds_with_village_indicators_v2.gpkg` (3,747,840 bytes, 518 polygons, EPSG:4326)
- **Quality Report**: `docs/WATERSHED_DATA_QUALITY_REPORT.md`

### Spatial Aggregation Performance & Diagnostics
- Village geometries parsed: 44,468 polygons in 1.55s.
- Spatial indexing (`sjoin`): 56,645 candidate intersecting pairs in 2.36s.
- Exact fragment clipping (`shapely.intersection` in UTM Zone 43N `EPSG:32643`): 56,575 valid fragments in 5.97s.
- Total execution time: **12.4 seconds**.

### Boundary & Coverage Flag Breakdown
Each of the 518 HydroATLAS Level 8 catchments was classified according to the percentage of its area covered by Maharashtra village polygons:
- `full_coverage` ($\ge 90\%$ inside Maharashtra): **402 catchments (77.61%)**
- `substantial_coverage` ($50\% - 90\%$): **53 catchments (10.23%)**
- `partial_border` ($< 50\%$): **62 catchments (11.97%)**
- `transboundary_uncovered` ($< 0.01\%$): **1 catchment (0.19%)** (`HYBAS_ID = 4081063690`, located across the Pranhita river on the Telangana bank).

### Multi-Scale Empirical Cross-Validation
Aggregated village indicators were cross-correlated against independent HydroATLAS baseline variables for all 402 full-coverage catchments to verify scaling fidelity:

| Physical Variable | HydroATLAS Baseline Metric | Village Aggregated Metric | Pearson $r$ | Spearman $\rho$ | Validation Finding |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Elevation** | `ele_mt_uav` | `village_elevation_mean_m` | **0.9213** | **0.9170** | Near-perfect spatial concordance across plateau and ghats. |
| **Slope** | `slp_dg_sav_deg` | `village_slope_mean_deg` | **0.9909** | **0.9516** | Strict topographic preservation; slope energy correctly captured. |
| **Precipitation** | `pre_mm_syr` | `village_rainfall_baseline_mean_mm` | **0.9524** | **0.9398** | Validates capture of the Western Ghats-to-Plateau rainshadow gradient. |
| **Area Consistency** | `sub_area_km2` | `basin_geom_area_km2` | **0.999993** | **0.999989** | Median area delta = 0.33%; maximum delta < 1.5%. |

---

## 5. Four-Pillar MCDA Design (Step 6)

- **Deliverable**: `docs/10_MCDA_INDICATOR_DESIGN.md`
- **Status**: Candidate Design Architecture (**Explicitly Not a Validated Final Score**)

The document establishes the 13 candidate indicators structured across 4 distinct pillars:
1. **Climate Stress**: Baseline Mean Annual Rainfall (Cost), Rainfall CV (Benefit), Empirical Drought Frequency (Benefit), 2025 Rainfall Anomaly (Cost).
2. **Agricultural Demand**: Cropland Area Fraction (Benefit), Natural Vegetation Buffer (Cost), Built-up Land Fraction (Benefit).
3. **Topographic Runoff**: Catchment Mean Slope (Benefit), Surface Runoff Depth (Benefit), Mean Elevation (Benefit).
4. **Infiltration Potential & Storage**: Soil Clay Fraction (Benefit for surface impoundment), Soil Sand Fraction (Cost for seepage), Soil Organic Carbon (Benefit), Infiltration Proxy (Dual).

### Critical Physical Limitations Addressed
- **Slope Alone $\ne$ Runoff**: Runoff volume is non-linearly governed by USDA-SCS Curve Numbers ($CN$), rainfall intensity (Horton overland flow), and soil moisture condition ($AMC$). Excessively steep slopes (>15°) cause scour and structural failure rather than viable harvesting.
- **Soil Texture Alone $\ne$ Infiltration**: Deccan Trap hydrogeology is governed by fractured basalt secondary porosity (columnar joints, vesicular flow tops, weathered murrum), not merely topsoil texture. Vertisols exhibit shrink-swell behavior that shuts down percolation when wet.
- **Collinearities Identified**: Elevation vs. Rainfall ($r \approx 0.65$ due to orographic effects); Clay vs. Sand ($r = -0.72$ due to constant sum).

---

## 6. Sensitivity Analysis & Prioritization Insights

To evaluate the mathematical robustness of the proposed framework, `src/jaldrishti/mcda_framework.py` benchmarked three weighting paradigms across the 518 catchments:
- **Equal Weighting**: 25% per pillar, equally divided among indicators.
- **AHP Domain Model**: Calibrated to state watershed priorities (Climate 35%, Ag 30%, Runoff 20%, Infiltration 15%).
- **Shannon Entropy**: Objective data-driven weighting based on information dispersion.

### Findings & Deliverables
- **Rank Correlation**:
  - AHP vs. Equal Weights: Spearman $\rho = \mathbf{0.8859}$ (demonstrates high ranking preservation).
  - AHP vs. Shannon Entropy: Spearman $\rho = 0.4990$ (Entropy heavily weights runoff depth [26.3%] and built-up land [20.1%] due to high geographic contrast between Konkan and the plateau).
- **Consensus High-Priority Catchments (Tier 1)**: Exactly **104 catchments (20.1%)** emerge as Tier 1 priorities, concentrated in the drought-prone rainshadow belt (Ahmednagar, Solapur, Beed, Osmanabad, Jalgaon) where rainfall is $500–650\text{ mm}$, cropland $>75\%$, and clay vertisols $>440\text{ g/kg}$.
- **Output Files**:
  - `data/processed/jaldrishti_watersheds_mcda_scores.csv`
  - `data/processed/jaldrishti_watersheds_mcda_scores.gpkg`
  - `docs/MCDA_SENSITIVITY_REPORT.md`
  - `outputs/figures/mcda_weight_comparison.png`
  - `outputs/figures/mcda_ranking_stability_scatter.png`

---

## 7. Automated Test Suite Status

All unit tests in `tests/test_spatial_aggregation.py` were expanded from 5 to 8 tests, verifying file existence, schema validity, soil mass conservation, and MCDA scoring bounds:

```bash
$ pytest -v
tests/test_spatial_aggregation.py::test_project_structure PASSED         [ 12%]
tests/test_spatial_aggregation.py::test_hydroatlas_basins_shapefile PASSED [ 25%]
tests/test_spatial_aggregation.py::test_preliminary_score_formula_reproducibility PASSED [ 37%]
tests/test_spatial_aggregation.py::test_aggregated_watershed_indicators PASSED [ 50%]
tests/test_spatial_aggregation.py::test_soil_physical_sanity_rules PASSED [ 62%]
tests/test_spatial_aggregation.py::test_village_integrated_indicators_v1 PASSED [ 75%]
tests/test_spatial_aggregation.py::test_aggregated_watershed_indicators_v2 PASSED [ 87%]
tests/test_spatial_aggregation.py::test_mcda_scoring_and_ranking PASSED  [100%]

============================== 8 passed in 1.88s ==============================
```

---

## 8. Remaining Blockers & Next Recommended Steps

### Blockers Resolved in this Milestone:
1. **Soil & Terrain 100% NaN Issue**: Completely resolved via `EPSG:4326` CRS specification; verified across all 44,468 villages.
2. **Data Integration**: Successfully unified 25 years of rainfall, 10m LULC, 30m terrain, and 250m soil physics into a single versioned file.
3. **Catchment Aggregation (v2)**: Area-weighted overlay extended and validated against independent HydroATLAS baselines ($r > 0.92$).
4. **MCDA Transition**: Comprehensive indicator design delivered, removing dependence on the preliminary toy score.

### Remaining External Gaps & Next Steps:
1. **Groundwater Observation Well Trends**: Integrate Central Ground Water Board (CGWB) observation well water level trends (pre-monsoon vs. post-monsoon decline rates) to empirically validate the Priority Tier 1 classifications.
2. **Existing Water Structure Accounting**: Ingest state intervention inventories (Jalyukt Shivar Abhiyan, Gal Mukt Dharan) to discount catchments where storage capacity is already saturated.
3. **Stakeholder Alignment**: Present `10_MCDA_INDICATOR_DESIGN.md` to district and state irrigation authorities to finalize operational weighting before certifying final field investment scores.
