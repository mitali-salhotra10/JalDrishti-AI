# 08. Project Audit Action Plan — JalDrishti-AI

**Status:** Ready for Execution Following Approval  
**Target Workspace:** `C:\Users\MITALI SALHOTRA\OneDrive\Desktop\JalDrishti`  
**Execution Sequence:** Strict Chronological Order  

---

## Phase 1: Code Modernisation & Path Portability (Immediate)

### Action 1.1 — Remove Hardcoded Paths in Pipeline Scripts
- **File**: `jaldrishti_spatial_aggregation.py`
- **Change**: Replace hardcoded `WORKSPACE = Path(r"c:\Users\MITALI SALHOTRA\OneDrive\Desktop\JalDrishti")` with dynamic path resolution:
  ```python
  WORKSPACE = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
  ```
- **Change**: Update `groupby.apply()` to include `include_groups=False` for Pandas 2.2+ forward compatibility.
- **Verification**: Run `python jaldrishti_spatial_aggregation.py` and confirm clean execution with zero deprecation warnings.

---

## Phase 2: Missing Data Resolution — Soil & Terrain (UNBLOCKED & VERIFIED)

**Current Status**: **UNBLOCKED & VALIDATED** (Documented in `09_SOIL_TERRAIN_UNBLOCKING_REPORT.md`)  
**Validation Evidence**: Tested on 24 representative villages across 8 districts (0.82s execution, 0.00% null rate, 100.0% soil texture mass conservation).

### Action 2.1 — Correct & Execute GEE Village Terrain Reducer
- **Source Script**: `Sentinel-2_Maharstra.ipynb` (Cell 60)
- **Defect Identified**: Mapping function referenced non-existent properties `feature.get("mean")` and `feature.get("mean_1")` instead of band names `elevation_m` and `slope_deg`.
- **Fix Implemented**: Directly mapped band names and stripped heavy polygon geometries via `ee.Feature(None, properties)`.
- **Status**: **RESOLVED & TESTED**. Implemented in `export_village_terrain_soil_gee.py` and `JalDrishti_Watershed_Analysis_Continued.ipynb` (Cells 10–12).

### Action 2.2 — Correct & Execute GEE Village SoilGrids Reducer
- **Source Script**: `Sentinel-2_Maharstra.ipynb` (Cells 82–84)
- **Defect Identified**: ISRIC SoilGrids 250m multi-band reduction exported unstripped geometries, causing GEE computation to drop/prune attributes.
- **Fix Implemented**: Explicit depth band selection (0–5cm, 5–15cm), geometry stripping (`ee.Feature(None, ...)`), and `tileScale=8`.
- **Status**: **RESOLVED & TESTED**. Implemented in `export_village_terrain_soil_gee.py` and `JalDrishti_Watershed_Analysis_Continued.ipynb`.

### Action 2.3 — Batch Export Execution (Pending User Approval)
- **Operational Tool**: `export_village_terrain_soil_gee.py`
- **Execution Command**: `python export_village_terrain_soil_gee.py --start-tasks`
- **Target Files**: `maharashtra_village_terrain_v2.csv` and `maharashtra_village_soilgrids_v2.csv` exported to Google Drive folder `JalDrishti_AI`.
- **Downstream Action**: Download CSVs and run spatial aggregation in `jaldrishti_spatial_aggregation.py` to calculate catchment-level indicators.

---

## Phase 3: Multi-Criteria Decision Framework (MCDA) Design

### Action 3.1 — Formulate Four-Pillar Indicator Architecture
Once terrain and soil metrics are re-extracted, structure the prioritisation framework around four physical pillars:

1. **Pillar 1: Climate Drought Stress** (from 25-yr village CHIRPS):
   - Baseline Mean Annual Precipitation ($mm$) [Direction: Inverted]
   - Long-Term Coefficient of Variation (CV %) [Direction: Direct]
   - 2025 Rainfall Anomaly (%) [Direction: Inverted]
2. **Pillar 2: Land Use & Human Demand** (from ESA WorldCover 2021):
   - Cultivated Cropland Fraction (%) [Direction: Direct — agricultural water demand]
   - Built-Up Settlement Fraction (%) [Direction: Direct — domestic water demand]
   - Tree Cover Fraction (%) [Direction: Inverted — natural retention indicator]
3. **Pillar 3: Surface Drainage & Slope** (from HydroATLAS & DEM):
   - Sub-Basin Average Slope (degrees) [Direction: Direct for runoff generation]
   - HydroATLAS Runoff Ratio ($Q/P$) [Direction: Direct for harvesting potential]
4. **Pillar 4: Soil Infiltration Capacity** (from SoilGrids):
   - Clay Content (%) [Direction: Inverted for recharge, Direct for surface storage]
   - Sand Content (%) [Direction: Direct for recharge structures]

### Action 3.2 — Normalisation & Weight Sensitivity Analysis
- Implement robust percentile scaling (1st–99th percentile) to avoid Western Ghats rainfall outlier distortions.
- Test rank stability across:
  - Equal Weights (illustrative baseline).
  - Analytical Hierarchy Process (AHP) weights based on hydrological literature.
  - Entropy-based objective weighting.

---

## Phase 4: Verification & Reporting

### Action 4.1 — Ground-Water Cross-Validation
- Overlay candidate priority catchments with Central Ground Water Board (CGWB) and Groundwater Surveys and Development Agency (GSDA) observation well hydrographs.
- Evaluate whether high-priority screening catchments correlate with documented groundwater decline.

### Action 4.2 — Publish Consolidated Handoff Pack
- Update project documentation (`README.md`, `05_CURRENT_STATE_AND_NEXT_STEPS.md`) to reflect the multi-pillar MCDA results.
- Export finalized GIS layers in ESRI Shapefile and OGC GeoPackage formats.
