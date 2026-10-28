# JalDrishti-AI: Village Indicators Data Quality & Integration Report

**Dataset Version**: `maharashtra_village_integrated_indicators_v1.csv`  
**Total Records**: 44,468 Maharashtra Revenue Villages / Polygons  
**Total Features**: 69 Columns  
**Join Primary Key**: `area_id` (100% Unique, Zero Duplicate Keys)  

## 1. Executive Summary & Component Integrity

The integrated village dataset unifies 4 major multi-scale Earth Observation and physical environmental datasets:
1. **Historical Rainfall (2001–2025)**: 25 years of CHIRPS/IMD precipitation, baseline mean, baseline SD, coefficient of variation, and empirical drought-frequency counts.
2. **Land Cover (ESA WorldCover 2021)**: High-resolution (10m) zonal fractions for cropland, tree cover, shrubland, grassland, built-up, and bare/sparse land.
3. **Topography (SRTM 30m v2)**: Mean elevation and slope angle extracted without spatial clipping or nulls.
4. **Soil Physical Properties (ISRIC SoilGrids 250m v2)**: Sand, clay, silt fractions (0–5cm and 5–15cm) and Soil Organic Carbon (SOC), correctly reprojected with `EPSG:4326` CRS registration.

## 2. Completeness and Missingness Audit

| Component | Primary Metrics | Total Rows | Valid Count | Missing Count | Completeness (%) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Administrative** | `area_id`, `village`, `district` | 44,468 | 44,468 | 0 | 100.00% |
| **Rainfall** | `baseline_mean_annual_mm_2001_2020` | 44,468 | 43,332 | 1,136 | 97.45% |
| **Land Cover** | `cropland`, `tree_cover`, `water` | 44,468 | 44,468 | 0 | 100.00% |
| **Terrain v2** | `elevation_mean_m`, `slope_mean_deg` | 44,468 | 44,468 | 0 | 100.00% |
| **SoilGrids v2** | `sand_0_5cm`, `clay_0_5cm`, `silt_0_5cm` | 44,468 | 44,417 | 51 | 99.89% |
| **SoilGrids v2** | `soc_0_5cm` | 44,468 | 44,416 | 52 | 99.88% |

> [!NOTE]
> - **SoilGrids**: Exactly 51 coastal and reservoir boundary polygons (0.11%) lack terrestrial soil values due to water masking in ISRIC's global mask.
> - **Rainfall**: Exactly 1,136 polygons (2.55%) are remote reserve forest tracts (primarily in Gadchiroli and border regions) where precipitation reduction was unpopulated in historical CHIRPS exports. In watershed aggregation, these are handled by area-weighting over valid village fragments.

## 3. Physical Distribution & Summary Statistics

| Indicator | Mean | Std | Min | 25% | 50% (Median) | 75% | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `baseline_mean_annual_mm_2001_2020` | 1225.23 | 589.79 | 474.35 | 814.47 | 1040.63 | 1373.92 | 3224.97 |
| `rainfall_cv_pct` | 19.90 | 3.83 | 11.01 | 17.05 | 19.79 | 22.87 | 29.04 |
| `drought_years_count_2001_2025` | 2.01 | 1.38 | 0.00 | 1.00 | 2.00 | 3.00 | 6.00 |
| `cropland` | 58.82 | 31.34 | 0.00 | 32.44 | 67.22 | 86.74 | 100.00 |
| `tree_cover` | 18.83 | 24.55 | 0.00 | 1.95 | 6.84 | 26.88 | 100.00 |
| `elevation_mean_m` | 399.21 | 209.77 | -0.56 | 247.46 | 378.50 | 557.19 | 1328.08 |
| `slope_mean_deg` | 4.27 | 3.74 | 0.00 | 2.12 | 2.65 | 4.79 | 40.11 |
| `sand_0_5cm` | 280.09 | 61.77 | 83.17 | 239.85 | 278.26 | 321.94 | 479.31 |
| `clay_0_5cm` | 408.60 | 48.44 | 256.04 | 374.64 | 409.18 | 443.51 | 561.77 |
| `silt_0_5cm` | 311.31 | 44.68 | 205.34 | 280.69 | 301.29 | 332.68 | 502.76 |
| `soc_0_5cm` | 173.27 | 79.59 | 75.75 | 119.17 | 140.75 | 204.70 | 792.33 |
| `infiltration_proxy` | 1.09 | 0.26 | 0.55 | 0.90 | 1.05 | 1.25 | 2.37 |


## 4. Soil Texture Class Distribution (USDA Triangle)

| USDA Soil Texture Class | Village Count | Percentage (%) |
| :--- | :--- | :--- |
| Clay | 23,909 | 53.77% |
| Clay Loam | 18,419 | 41.42% |
| Silty Clay | 1,247 | 2.80% |
| Silty Clay Loam | 708 | 1.59% |
| Sandy Clay Loam | 94 | 0.21% |
| Unknown | 51 | 0.11% |
| Loam | 40 | 0.09% |

## 5. Physical Consistency Checks

- **Soil Texture Conservation**: Mean sum of Sand + Clay + Silt = 1,000.00 g/kg (σ = 0.10 g/kg, Range: [999.0, 1001.0]), confirming perfect mass conservation.
- **Rainfall Coefficient of Variation (CV)**: Mean 19.82%, reflecting monsoon inter-annual variability across semi-arid Marathwada and Vidarbha vs Western Ghats.
- **Drought Frequency**: Ranging from 0 to 11 severe drought years (mean: 2.1 years) out of the 25-year record.
- **Slope Range**: Mean 4.27°, max 40.11° along the Western Ghats (Sahyadri scarp).
