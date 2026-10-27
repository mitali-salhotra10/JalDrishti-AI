# Raw Data Directory (`data/raw/`)

This directory houses primary remote-sensing extraction exports and village-level baseline datasets.

## Inventory of Files

### 1. Village 25-Year Historical Rainfall (2001–2025)
- **Filename**: `maharashtra_village_historical_rainfall_2001_2025_v2.csv`
- **File Size**: 149,020,409 bytes (~142.1 MB)
- **Feature Count**: 44,468 village polygons
- **SHA-256 Checksum**: `0F00832AF65A31A1B82D81756A2649F349110583F28CF6E7F6136E38C51F49AF`
- **Git Tracking Status**: Preserved locally on disk. Excluded from repository tracking via `.gitignore` to prevent exceeding GitHub's 100 MB commit limit and avoiding residential upload timeouts / LFS bandwidth exhaustion.
- **Source & Provenance**: Generated via Google Earth Engine Task `4MYWOOQ3YFDZJAV24E4RQ3GG` (CHIRPS Daily 2001–2025 zonal reduction over asset `projects/jaldrishti-508107/assets/maharashtra_villages`).
- **Retrieval Instructions**:
  - The dataset is stored in the project Google Drive repository folder: `JalDrishti_AI`.
  - Download `maharashtra_village_historical_rainfall_2001_2025_v2.csv` directly into `data/raw/`.
  - Verify integrity using PowerShell:
    ```powershell
    Get-FileHash -Path "data\raw\maharashtra_village_historical_rainfall_2001_2025_v2.csv" -Algorithm SHA256
    ```
  - Note: All downstream aggregated catchment indicators derived from this file are already pre-computed and included directly in `data/processed/jaldrishti_watersheds_with_village_indicators.csv` and `.gpkg`.

### 2. Village ESA WorldCover Land Cover (2021)
- **Filename**: `maharashtra_village_landcover_2021.csv` (7.86 MB)
- **Status**: Tracked in Git repository.
- **Rows**: 44,468 villages.
- **Key Fields**: `area_id`, `tree_cover`, `shrubland`, `grassland`, `cropland`, `built_up`, `bare_sparse`, `water`, `herbaceous_wetland`, `mangroves`.

### 3. Village ISRIC SoilGrids 250m (Raw Export)
- **Filename**: `maharashtra_village_soilgrids.csv` (2.22 MB)
- **Status**: Tracked in Git repository. Original GEE export with 100% intact administrative keys (`area_id`, `village`, `vlcode`), but empty physical attributes due to audited reducer bug. To be replaced by `_v2` once batch task completes.

### 4. Village SRTM Terrain (Raw Export)
- **Filename**: `maharashtra_village_terrain.csv` (1.95 MB)
- **Status**: Tracked in Git repository. Original GEE export with 100% intact administrative keys, empty physical attributes due to property naming bug (`mean` vs `elevation_m`). To be replaced by `_v2` once batch task completes.

### 5. District-Level Land Cover & Palghar Boundary Extracts
- `maharashtra_lulc_area_2023_with_area_totals.csv` (2.10 MB)
- `maharashtra_palghar_lulc_area_2023.csv` (451 B)
- `palghar_lulc_2023_consistent_boundary.csv` (436 B)
