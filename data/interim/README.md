# Interim Data Directory (`data/interim/`)

This directory contains intermediate analytical tables, quality assurance extracts, and validation cross-checks.

## Inventory of Files

1. `jaldrishti_watershed_validation_518_basins.csv` (3.22 MB)
   - **Rows**: 518 Level 8 basins.
   - **Purpose**: Ground-truth validation extract from WWF HydroATLAS v1.0.
   - **Key Fields**:
     - `HYBAS_ID`: Unique global basin identifier.
     - `ele_mt_uav`: Upstream average elevation (m).
     - `slp_dg_sav_deg`: Sub-basin average slope (degrees).
     - `slp_dg_uav_deg`: Upstream average slope (degrees).
     - `pre_mm_syr`: Sub-basin mean annual precipitation (mm/yr).
     - `run_mm_syr`: Sub-basin annual runoff (mm/yr).
     - `quality_review_flag`: Flagged hydrological anomalies (e.g. Runoff > Precipitation).
     - `runoff_review_flag`: Review flags for arid catchments with high runoff coefficients.
     - `terrain_review_flag`: Catchments with steep escarpment slopes.
