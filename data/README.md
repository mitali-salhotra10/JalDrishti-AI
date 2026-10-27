# JalDrishti-AI Data Catalog

This directory contains the geospatial datasets, tabular indicators, and administrative layers supporting watershed prioritisation in Maharashtra.

## Subdirectory Structure

- `raw/`: Unmodified primary source datasets and remote sensing zonal extracts.
- `interim/`: Intermediate validation tables, cleaned extracts, and QA review flags.
- `processed/`: Derived spatial products, HydroATLAS Level 8 basin layers, and area-weighted catchment aggregations.

## Data Sources & Provenance

| Dataset | Source Provider | Resolution | Temporal Scope | Description |
| :--- | :--- | :---: | :---: | :--- |
| **HydroATLAS Level 8** | WWF / HydroSHEDS v1.0 | 518 Basins | Static Baseline | Hydrological sub-basin boundaries, elevation, slope, and annual runoff. |
| **CHIRPS Rainfall** | Climate Hazards Center (UCSB) | 0.05° (~5.5 km) | 2001–2025 (25 yrs) | Village-level annual precipitation, standard deviation, anomaly, and drought metrics. |
| **ESA WorldCover** | European Space Agency (ESA) | 10 m | 2021 | Village-level land use/land cover (cropland, built-up, tree cover, water, wetland). |
| **Dynamic World** | WRI / Google Earth Engine | 10 m | 2023 | District and state-level LULC area aggregations. |
| **SRTM DEM** | NASA / USGS (SRTMGL1_003) | 30 m | 2000 Baseline | Mean elevation (m) and slope (degrees) zonal reductions. |
| **ISRIC SoilGrids** | ISRIC - World Soil Information | 250 m | Static v2.0 | Soil texture (sand, clay, silt in g/kg) and Soil Organic Carbon (SOC in dg/kg) at 0–5cm and 5–15cm. |
| **Village Boundaries** | JalDrishti Asset (`maharashtra_villages`) | 44,468 Polygons | Census / Administrative | Boundary geometries (`EPSG:4326`) and census codes (`vlcode`). |

## Coordinate Reference Systems

- **Geographic Storage**: `EPSG:4326` (WGS 84, degrees latitude/longitude).
- **Planar Calculation**: `EPSG:32643` (UTM Zone 43N, meters). Used for accurate metric area intersection ($m^2$ and $km^2$).

## Git Large File Storage (Git LFS)

The 25-year historical rainfall dataset (`data/raw/maharashtra_village_historical_rainfall_2001_2025_v2.csv`, ~149 MB) exceeds GitHub's standard 100 MB limit. It is tracked using Git LFS:

```bash
# Ensure Git LFS is installed and pulled
git lfs install
git lfs pull
```
