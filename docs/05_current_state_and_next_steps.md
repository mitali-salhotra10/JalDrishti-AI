# 5. Current State and Next Steps

## Recorded as completed

-   Prepared district rainfall indicators for 36 districts, intended
    period 2018--2025.
-   Prepared Dynamic World 2023 land-cover summaries for 36 districts.
-   Saved a combined district rainfall/LULC table.
-   Prepared HydroATLAS Level 8 attributes for 518 basin records.
-   Saved a watershed MCDA input table.
-   Saved a preliminary score table for 518 records.
-   Completed a Google Earth Engine export task for the preliminary
    score layer.

These are records of outputs, not independent confirmation that every
calculation is scientifically correct.

## Not confirmed complete

-   Download and extraction of the shapefile into the local project.
-   Local validation of geometry, CRS, row count, and attributes.
-   Creation and verification of the requested SVG map.
-   Final MCDA design and justified weights.
-   Spatial overlay to integrate district inputs into basin-level units.
-   Sensitivity analysis, independent validation, and field review.
-   Intervention-specific site suitability.

## Immediate next steps

### Step 1 --- Check the local folder

``` python
from pathlib import Path

DATA_DIR = Path(r"C:\Users\MITALI SALHOTRA\JalDrishti-AI")
shp_folder = DATA_DIR / "scored_watersheds"
shp_folder.mkdir(parents=True, exist_ok=True)

print("Folder:", shp_folder)
print("SHP files:", [p.name for p in shp_folder.glob("*.shp")])
print("All files:", [p.name for p in shp_folder.iterdir()])
```

If no `.shp` exists, download the export from the recorded Drive folder:
https://drive.google.com/drive/folders/1kL9lMyylc9C8sFbOBTk6snGk0lhYtxUv

Extract the downloaded archive into `scored_watersheds`. Do not assume
the download is local just because the Earth Engine task completed.

### Step 2 --- Load and validate

``` python
import geopandas as gpd
from pathlib import Path

DATA_DIR = Path(r"C:\Users\MITALI SALHOTRA\JalDrishti-AI")
shp_folder = DATA_DIR / "scored_watersheds"
shp_files = list(shp_folder.glob("*.shp"))
if not shp_files:
    raise FileNotFoundError(f"No shapefile found in {shp_folder}")

gdf = gpd.read_file(shp_files[0])
print("File:", shp_files[0].name)
print("Rows:", len(gdf))
print("CRS:", gdf.crs)
print("Columns:", gdf.columns.tolist())
print("Geometry types:", gdf.geom_type.value_counts(dropna=False).to_dict())
print("Null geometries:", int(gdf.geometry.isna().sum()))
print("Invalid geometries:", int((~gdf.geometry.is_valid).sum()))
display(gdf.head())
```

### Step 3 --- Audit the score table

``` python
import pandas as pd
DATA_DIR = Path(r"C:\Users\MITALI SALHOTRA\JalDrishti-AI")
scores = pd.read_csv(DATA_DIR / "jaldrishti_watershed_preliminary_screening.csv")
print(scores.shape, scores.columns.tolist())
print("Duplicate HYBAS_ID:", scores["HYBAS_ID"].duplicated().sum())
print(scores[["HYBAS_ID", "preliminary_screening_score"]].head())
```

Inspect actual shapefile field names before joining; shapefile
field-name limits may truncate names. Compare by `HYBAS_ID` and quantify
missing or mismatched scores.

### Step 4 --- Create SVG only after validating the layer

Use the verified geometry and score field. Include title, legend,
source/method note, and a visible statement: **"Preliminary screening
only; not an engineering approval or site-suitability assessment."** Use
an appropriate CRS. Verify the output path exists before sharing it.

### Step 5 --- Audit the formula and flags

Recompute the preliminary score independently, compare with the saved
score, handle zero ranges and missing values, and inspect quality flags.

### Step 6 --- Design the full MCDA model

Agree on the decision question, spatial unit, criteria, indicator
directions, normalisation, weights, missing-data rules, and validation
plan before adding more variables.

### Step 7 --- Integrate district data correctly

If district indicators must contribute to basin scores, use documented
zonal statistics or spatial overlay. Never join by row order.

### Step 8 --- Validate before operational use

Run sensitivity analysis, independent comparisons, expert review, and
field checks. Keep all results labelled preliminary until validation is
documented.

## Immediate task definition of done

-   Local shapefile and companion files exist.
-   Layer opens in GeoPandas/QGIS.
-   CRS, geometry validity, feature count, and fields are checked.
-   Score values match the CSV for the same `HYBAS_ID`.
-   SVG generated from the verified layer.
-   SVG contains a clear caveat and source/method note.
-   Exact output path verified.
