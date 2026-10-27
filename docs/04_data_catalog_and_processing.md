# 4. Data Catalog and Processing History

## Project location and environment

Known Windows project directory:
`C:\Users\MITALI SALHOTRA\JalDrishti-AI`

Google Earth Engine project: `jaldrishti-508107`

A kernel reset occurred during prior work. Treat saved CSVs as durable
state; do not assume notebook variables still exist.

## Known files

### Rainfall and district indicators

-   `maharashtra_rainfall_2018_2025.csv`
-   `jaldrishti_rainfall_indicators_2018_2025.csv`
-   `jaldrishti_rainfall_indicators_2018_2025_clean.csv` --- known 36 ×
    16
-   `jaldrishti_district_rainfall_swings_2018_2025.csv`
-   `jaldrishti_district_wettest_driest_years.csv`
-   `jaldrishti_largest_rainfall_deficit_pct.csv`
-   `jaldrishti_rainfall_deficit_magnitude.csv`
-   `jaldrishti_rainfall_mean_vs_variability.csv`
-   `jaldrishti_rainfall_variability_rankings.csv`

### Land cover and combined district table

-   `maharashtra_lulc_area_2023.csv`
-   `maharashtra_lulc_area_2023_download.csv`
-   `maharashtra_lulc_area_2023_with_area_totals.csv`
-   `jaldrishti_lulc_2023_all_36_districts.csv` --- known 36 × 25
-   `jaldrishti_district_rainfall_lulc_analysis.csv` --- known 36 × 21

### Basin/watershed files

-   `jaldrishti_hydroatlas_indicators_prepared.csv` --- known 518 × 13
-   `jaldrishti_district_mcda_inputs.csv`
-   `jaldrishti_watershed_mcda_inputs.csv`
-   `jaldrishti_watershed_preliminary_screening.csv` --- known 518 rows

File names and dimensions are from the previous project context. Verify
that each file still exists locally before relying on it.

## Rainfall schema

`jaldrishti_rainfall_indicators_2018_2025_clean.csv` fields:
`district_match, years_observed, mean_annual_mm, annual_sd_mm, min_annual_mm, max_annual_mm, mean_monsoon_mm, monsoon_sd_mm, annual_cv_pct, monsoon_cv_pct, range_mm, range_pct_of_mean, wettest_year, wettest_rainfall_mm, driest_year, driest_rainfall_mm`.

Verify actual years observed per district, rainfall units, monsoon-month
definition, missing-data handling, and whether SD uses sample or
population convention.

## Land-cover schema

`jaldrishti_lulc_2023_all_36_districts.csv` fields:
`district, year, analysis_scale_m, boundary_area_km2, water_km2, trees_km2, grass_km2, flooded_vegetation_km2, crops_km2, shrub_and_scrub_km2, built_up_km2, bare_ground_km2, snow_and_ice_km2, classified_area_km2, unclassified_or_uncovered_area_km2, coverage_pct, water_pct_of_boundary, trees_pct_of_boundary, grass_pct_of_boundary, flooded_vegetation_pct_of_boundary, crops_pct_of_boundary, shrub_and_scrub_pct_of_boundary, built_up_pct_of_boundary, bare_ground_pct_of_boundary, snow_and_ice_pct_of_boundary`.

Check whether percentages use the full boundary or only classified
pixels. Do not interpret class shares without checking `coverage_pct`
and unclassified area.

## Combined district table

`jaldrishti_district_rainfall_lulc_analysis.csv` contains rainfall
indicators, land-cover percentages, `total_lulc_km2`, and `_merge`. Some
sample rows previously showed `_merge = both`. Audit all merge
categories, duplicate district keys, and unmatched names before
analysis.

## HydroATLAS schema

Original basin table was recorded as 518 rows × 15 columns:
`system:index, HYBAS_ID, SUB_AREA, UP_AREA, ele_mt_uav, pre_mm_syr, quality_review_flag, run_mm_syr, runoff_review_flag, slp_dg_sav, slp_dg_sav_deg, slp_dg_uav, slp_dg_uav_deg, terrain_review_flag, .geo`.

Prepared CSV was recorded as 518 × 13, excluding `system:index` and
`.geo`.

Example basin record: - `HYBAS_ID=4081029590` - `SUB_AREA=646.7` -
`UP_AREA=11454` - `ele_mt_uav=385` - `pre_mm_syr=931` -
`run_mm_syr=252` - `slp_dg_sav=45`, `slp_dg_sav_deg=4.5` -
`slp_dg_uav=18`, `slp_dg_uav_deg=1.8`

The slope fields appear to be differently scaled representations; verify
metadata before choosing one. Do not automatically drop records with
`quality_review_flag`, `runoff_review_flag`, or `terrain_review_flag`
without understanding their meaning.

## Keep the counts distinct

-   36 district rainfall records;
-   36 district land-cover records;
-   518 basin records in prepared HydroATLAS/screening tables;
-   a separate terrain extraction previously had 522 basin records.

The 518 and 522 counts refer to different stages/outputs. Investigate
why before combining them.

## Preliminary score processing

Known formula:
`score = (0.5 * minmax(slp_dg_sav_deg) + 0.5 * (1 - minmax(pre_mm_syr))) * 100`.

The score output is a prototype. Recompute it from raw inputs and
compare with the saved output before reuse. Check nulls, infinite
values, zero-range inputs, ranking direction, and tie handling.

## Google Earth Engine export

A task completed with: - description
`JalDrishti_Preliminary_Watershed_Scores`; - folder `JalDrishti_AI`; -
prefix `jaldrishti_scored_watersheds`; - format `SHP`; - fields
`HYBAS_ID`, `preliminary_screening_score`, `SUB_AREA`, `UP_AREA`; - task
ID `7JWRR22BGJZX6TUT7MGEBYDN`.

Drive folder:
https://drive.google.com/drive/folders/1kL9lMyylc9C8sFbOBTk6snGk0lhYtxUv

The task completion was confirmed, but download/extraction to the local
folder was not confirmed. Expected local destination:
`C:\Users\MITALI SALHOTRA\JalDrishti-AI\scored_watersheds`. Keep `.shp`,
`.shx`, `.dbf`, `.prj`, and any `.cpg` together.

## Recommended audit cell

``` python
from pathlib import Path
import pandas as pd

DATA_DIR = Path(r"C:\Users\MITALI SALHOTRA\JalDrishti-AI")
files = [
    "jaldrishti_rainfall_indicators_2018_2025_clean.csv",
    "jaldrishti_lulc_2023_all_36_districts.csv",
    "jaldrishti_district_rainfall_lulc_analysis.csv",
    "jaldrishti_hydroatlas_indicators_prepared.csv",
    "jaldrishti_watershed_mcda_inputs.csv",
    "jaldrishti_watershed_preliminary_screening.csv",
]
for name in files:
    path = DATA_DIR / name
    print(f"\n{name}: exists={path.exists()}")
    if path.exists():
        df = pd.read_csv(path)
        print("shape:", df.shape)
        print("columns:", df.columns.tolist())
        print("duplicate rows:", df.duplicated().sum())
```
