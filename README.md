# JalDrishti-AI: Geospatial Watershed Prioritisation & Decision-Support Framework

[![CI](https://github.com/mitali-salhotra10/JalDrishti-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/mitali-salhotra10/JalDrishti-AI/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Pending-orange.svg)](#data-licensing-and-attribution)
[![GeoPandas](https://img.shields.io/badge/GIS-GeoPandas%20%7C%20Shapely-green.svg)](https://geopandas.org/)
[![Google Earth Engine](https://img.shields.io/badge/Remote%20Sensing-Google%20Earth%20Engine-brightgreen.svg)](https://earthengine.google.com/)

**JalDrishti-AI** is a GIS-based hydrological decision-support system designed to screen, evaluate, and prioritise sub-watersheds for targeted water-conservation interventions, rainwater harvesting, and drought-mitigation planning across Maharashtra, India, with an extensible architecture designed for national pan-India scale.

The platform bridges macro-scale hydrological basin intelligence (WWF HydroATLAS Level 8) with micro-scale rural administrative units (44,468 village boundaries) using vectorized, area-weighted geospatial aggregation across 25 years of daily satellite precipitation (CHIRPS), high-resolution land use/land cover (ESA WorldCover), digital elevation models (SRTM), and soil texture models (ISRIC SoilGrids).

---

> [!IMPORTANT]
> **Scientific Notice & Score Status**: The preliminary watershed score presented in this repository is an **illustrative screening proxy** combining sub-basin slope and long-term annual precipitation with equal weights (50/50). It is **not a validated Multi-Criteria Decision Analysis (MCDA) model**, **not an AI prediction of intervention success**, and **not an engineering site-suitability assessment**. Validated implementation requires documented field review and ground-truth hydrogeological verification (CGWB/GSDA).

---

## Table of Contents

1. [Problem Statement & Objectives](#problem-statement--objectives)
2. [Geographic Scope: Maharashtra to Pan-India](#geographic-scope-maharashtra-to-pan-india)
3. [Current Project State & Architecture](#current-project-state--architecture)
4. [Data Sources & Temporal Coverage](#data-sources--temporal-coverage)
5. [Methodology & Spatial Aggregation](#methodology--spatial-aggregation)
6. [Repository Structure](#repository-structure)
7. [Installation & Environment Setup](#installation--environment-setup)
8. [Reproducing the Analysis](#reproducing-the-analysis)
   - [Running the Spatial Aggregation Pipeline](#running-the-spatial-aggregation-pipeline)
   - [Running the Earth Engine Export Tool](#running-the-earth-engine-export-tool)
   - [Executing Notebooks](#executing-notebooks)
   - [Running Automated Tests](#running-automated-tests)
9. [Documentation Index](#documentation-index)
10. [Known Limitations & Missing Data Accounting](#known-limitations--missing-data-accounting)
11. [Contributing & Git Workflow](#contributing--git-workflow)
12. [Data Licensing & Attribution](#data-licensing--attribution)

---

## Problem Statement & Objectives

Maharashtra's agriculture and rural livelihoods are subject to intense hydro-climatic volatility. The state faces an acute hydrological dichotomy:
- The **Western Ghats (Konkan / Sahyadri)** experience intense orographic monsoon rainfall (>3,000–4,000 mm/year), yet steep escarpments cause rapid torrential runoff directly into the Arabian Sea with minimal retention.
- The **Deccan Plateau rain-shadow** (Marathwada, Solapur, Ahmednagar, parts of Vidarbha) receives <600 mm/year, suffering frequent seasonal droughts, acute groundwater depletion, and high agricultural vulnerability.

### Project Objectives
1. **Multi-Scale Geospatial Harmonisation**: Translate 44,468 village-level socio-ecological indicators into 518 natural hydrological catchments (WWF HydroATLAS Level 8) via polygon fragment overlay.
2. **Objective Hydrological Screening**: Formulate transparent multi-criteria screening mechanisms to identify catchments with high runoff generation and severe rainfall deficits.
3. **Four-Pillar Decision Support**: Structure a comprehensive MCDA framework balancing (1) Climate Drought Stress, (2) Land Use Demand, (3) Surface Drainage & Slope, and (4) Soil Infiltration Capacity.
4. **Reproducible Open Data Engineering**: Provide clean, modular, tested, and portable CLI and Python workflows for GIS engineers, data scientists, and hydrological planning authorities.

---

## Geographic Scope: Maharashtra to Pan-India

| Level | Spatial Units | Bounding Extent | Implementation Role |
| :--- | :---: | :---: | :--- |
| **State Level** | 1 State (36 Districts) | 307,713 km² | Primary operational study area. |
| **Hydrological Catchments** | **518 Level 8 Basins** | WWF HydroATLAS v1.0 | Core hydrological unit for regional intervention planning. |
| **Village Scale** | **44,468 Villages** | Maharashtra Revenue Census | Primary administrative unit for localized implementation. |
| **National Extensibility** | HydroSHEDS Asia Level 8 | Pan-India Basin Network | Pipeline designed for seamless national scaling. |

---

## Current Project State & Architecture

```
Raw Remote Sensing Assets              Vector Processing Pipeline                 GIS Deliverables
┌──────────────────────────┐          ┌──────────────────────────┐         ┌──────────────────────────┐
│ CHIRPS 25-yr Rainfall    │─────────▶│                          │────────▶│ 518 Catchment GPKG       │
│ ESA WorldCover 2021 LULC │─────────▶│ Vectorized Area-Weighted │         │ (32 Aggregated Metrics)  │
│ WWF HydroATLAS Level 8   │─────────▶│ Intersection & Zonal     │────────▶│ Consolidated Basin CSV   │
│ 44,468 Village Polygons  │─────────▶│ Aggregator (EPSG:32643)  │         │ (jaldrishti_watersheds   │
└──────────────────────────┘          └──────────────────────────┘         │  _with_village_ind.csv)  │
                                                                           └──────────────────────────┘
┌──────────────────────────┐          ┌──────────────────────────┐         ┌──────────────────────────┐
│ SRTM 30m DEM             │─────────▶│ GEE Reducer Pipeline     │────────▶│ 8-District Sample Tested │
│ ISRIC SoilGrids 250m     │─────────▶│ (tileScale=8, stripped)  │         │ (Full Batch Primed)      │
└──────────────────────────┘          └──────────────────────────┘         └──────────────────────────┘
```

- **Phase Completed**: Advanced data integration, spatial intersection, catchment aggregation, and blocker unblocking.
- **Active GIS Layers**: 
  - `data/processed/jaldrishti_scored_watersheds.shp`: 518 basins, topological validity 100%, preliminary screening score reproduced to $1.42 \times 10^{-14}$.
  - `data/processed/jaldrishti_watersheds_with_village_indicators.gpkg`: 518 basins with 32 area-weighted indicators.
- **Soil & Terrain Status**: Unblocked and verified across 24 villages in 8 districts (0.82s execution, 100% soil texture mass conservation). Full GEE batch tasks primed for execution.

---

## Data Sources & Temporal Coverage

| Dataset | Source Agency | Resolution | Temporal Range | Key Indicators Extracted |
| :--- | :--- | :---: | :---: | :--- |
| **HydroATLAS Level 8** | WWF / HydroSHEDS v1.0 | 518 Basins | Baseline | `SUB_AREA`, `UP_AREA`, `ele_mt_uav`, `slp_dg_sav_deg`, `pre_mm_syr`, `run_mm_syr` |
| **CHIRPS Satellite Rain** | Climate Hazards Center | 0.05° (~5.5 km) | 2001–2025 (25 yrs) | Baseline Mean (2001–2020), SD, 2024 Rain, 2025 Rain, Anomaly %, Long-Term CV % |
| **ESA WorldCover** | European Space Agency | 10 m | 2021 | Cropland %, Tree Cover %, Built-Up %, Water %, Wetland %, Bare Ground % |
| **Dynamic World** | WRI / GEE | 10 m | 2023 | District and state-wide multi-temporal LULC summaries |
| **SRTM GL1 DEM** | NASA / USGS | 30 m | Static | Elevation (m) and terrain slope (degrees) |
| **ISRIC SoilGrids** | ISRIC World Soil Info | 250 m | v2.0 Static | Sand, Clay, Silt (g/kg), SOC (dg/kg) at 0–5cm and 5–15cm |
| **Village Boundaries** | JalDrishti GeoJSON Asset | 44,468 Polygons | Census Baseline | Polygon boundaries (`EPSG:4326`), `area_id`, `district`, `vlcode` |

---

## Methodology & Spatial Aggregation

### 1. Vectorized Area-Weighted Zonal Overlay
To bridge rural village boundaries with natural watersheds, both layers are reprojected to UTM Zone 43N (`EPSG:32643`). Exact polygon intersections are sliced using vectorized Shapely routines:

$$\bar{X}_j = \frac{\sum_{i} w_{ij} X_i}{\sum_{i} w_{ij}}, \quad w_{ij} = \text{Area}(V_i \cap B_j)$$

Where:
- $B_j$ is the $j$-th HydroATLAS Level 8 sub-basin.
- $V_i$ is the $i$-th revenue village polygon.
- $w_{ij}$ is the metric intersection area in $\text{km}^2$ (sliver fragments $< 100\text{ m}^2$ are excluded).
- $X_i$ is the village attribute (e.g. 25-year rainfall mean, cropland fraction).

### 2. Preliminary Screening Proxy Formula
$$\text{slope\_norm} = \frac{\text{slp\_dg\_sav\_deg} - 0.0}{14.7 - 0.0}$$
$$\text{rain\_inv\_norm} = 1.0 - \frac{\text{pre\_mm\_syr} - 465.0}{4136.0 - 465.0}$$
$$\text{Score}_{\text{preliminary}} = \left(0.5 \times \text{slope\_norm} + 0.5 \times \text{rain\_inv\_norm}\right) \times 100.0$$

---

## Repository Structure

```
JalDrishti-AI/
├── README.md                                  # Main project documentation and quickstart
├── CONTRIBUTING.md                            # Development, Git branching, and PR guidelines
├── pyproject.toml                             # Modern packaging and dependency specifications
├── requirements.txt                           # Pinned Python package dependencies
├── .gitignore                                 # Git exclusions for Python, GIS locks, and backups
├── .gitattributes                             # Git LFS configuration for large datasets
│
├── docs/                                      # Sequential project handoff packs and audit reports
│   ├── README.md                              # Documentation catalog and reading order
│   ├── 01_project_overview.md                 # Project purpose and scope
│   ├── 02_problem_solution_requirements.md    # Problem statement, solution goals, and constraints
│   ├── 03_methodology_mcda.md                 # Methodology, MCDA logic, and validation notes
│   ├── 04_data_catalog_and_processing.md      # Data schemas, processing history, quality checks
│   ├── 05_current_state_and_next_steps.md     # Current state and recommended engineering steps
│   ├── 06_stakeholders_and_ai_handoff.md      # Stakeholder analysis and developer handoff
│   ├── 07_continued_analysis_and_village_integration.md # Village-to-catchment spatial aggregation
│   ├── 08_project_audit_report.md             # Complete senior GIS/ML project audit report
│   ├── 08_audit_action_plan.md                # 4-phase technical action plan
│   ├── 09_soil_terrain_unblocking_report.md   # GEE bug diagnosis, resolution, and validation
│   └── GITHUB_PUBLICATION_REPORT.md           # Publication audit and repository verification
│
├── notebooks/                                 # Executable Jupyter notebooks
│   ├── README.md                              # Notebook descriptions and execution sequence
│   ├── JalDrishti_Watershed_Analysis_Continued.ipynb # Primary executed analytical notebook
│   ├── JalDrishti_Data_Validation_Step1_Cleaned.ipynb # Historical district & basin validation
│   └── Sentinel-2_Maharstra.ipynb             # Archival GEE reducer notebook (audit evidence)
│
├── src/                                       # Core reusable Python package
│   └── jaldrishti/
│       ├── __init__.py                        # Package initialization
│       └── spatial_aggregation.py             # Vectorized area-weighted overlay engine
│
├── scripts/                                   # Standalone CLI tools and pipelines
│   ├── run_spatial_pipeline.py                # Wrapper to run catchment aggregation
│   └── export_village_terrain_soil_gee.py     # Production GEE terrain & SoilGrids export CLI
│
├── data/                                      # Geospatial layers and indicator tables
│   ├── README.md                              # Data catalog, CRS notes, and LFS instructions
│   ├── raw/                                   # Primary remote sensing and census datasets
│   │   ├── README.md                          # Raw data schemas and descriptions
│   │   ├── maharashtra_village_historical_rainfall_2001_2025_v2.csv (149 MB, Git LFS)
│   │   ├── maharashtra_village_landcover_2021.csv (7.86 MB)
│   │   ├── maharashtra_village_soilgrids.csv  # Raw export table (keys intact)
│   │   ├── maharashtra_village_terrain.csv    # Raw export table (keys intact)
│   │   ├── maharashtra_lulc_area_2023_with_area_totals.csv
│   │   ├── maharashtra_palghar_lulc_area_2023.csv
│   │   └── palghar_lulc_2023_consistent_boundary.csv
│   ├── interim/                               # Intermediate validation extracts
│   │   ├── README.md
│   │   └── jaldrishti_watershed_validation_518_basins.csv
│   └── processed/                             # Authoritative GIS layers & aggregations
│       ├── README.md
│       ├── jaldrishti_scored_watersheds.shp   # 518 HydroATLAS basins (and sidecars)
│       ├── jaldrishti_watersheds_with_village_indicators.csv (518 basins x 32 columns)
│       └── jaldrishti_watersheds_with_village_indicators.gpkg (OGC GeoPackage)
│
├── outputs/                                   # Rendered figures, maps, and tables
│   ├── README.md
│   ├── figures/
│   │   └── watershed_village_indicators_panel.png # 3-panel comparative cartography
│   ├── maps/
│   │   └── jaldrishti_preliminary_watershed_screening.svg # Vector screening map
│   └── tables/
│       └── README.md
│
├── tests/                                     # Automated unit test suite
│   ├── __init__.py
│   └── test_spatial_aggregation.py            # Unit tests for GIS loading, math, and flags
│
└── .github/                                   # CI/CD workflows
    └── workflows/
        └── ci.yml                             # Automated testing on Python 3.11
```

---

## Installation & Environment Setup

### Prerequisites
- **Python**: Version 3.10, 3.11, 3.12, or 3.13.
- **Git & Git LFS**: Ensure Git LFS is installed prior to cloning.

### 1. Clone the Repository
```bash
# Clone with Git LFS
git clone https://github.com/mitali-salhotra10/JalDrishti-AI.git
cd JalDrishti-AI

# Verify LFS files are pulled
git lfs install
git lfs pull
```

### 2. Set Up Virtual Environment
```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt

# Or install editable package
pip install -e .
```

---

## Reproducing the Analysis

### Running the Spatial Aggregation Pipeline
To reproduce the full area-weighted overlay translating 44,468 village polygons onto the 518 Level 8 catchments:

```bash
# Using the CLI runner script
python scripts/run_spatial_pipeline.py

# Or via the installed Python module
python -m jaldrishti.spatial_aggregation
```
*Expected Runtime: ~10–15 seconds on modern multi-core CPUs. Outputs updated in `data/processed/`.*

### Running the Earth Engine Export Tool
The production script [`scripts/export_village_terrain_soil_gee.py`](./scripts/export_village_terrain_soil_gee.py) interfaces with Google Earth Engine for digital elevation (SRTM) and soil texture (SoilGrids) zonal extractions.

#### Earth Engine Authentication
Ensure you have authenticated to Google Earth Engine:
```bash
earthengine authenticate
```
*Note: No credentials or tokens are stored in this repository. Local Google Cloud Application Default Credentials (ADC) are used.*

#### Operational Commands
```bash
# 1. Run live sample extraction (24 representative villages across 8 districts)
python scripts/export_village_terrain_soil_gee.py --sample

# 2. Check recent Earth Engine task states and progress
python scripts/export_village_terrain_soil_gee.py --check-status

# 3. Launch full batch exports for all 44,468 villages to Google Drive
python scripts/export_village_terrain_soil_gee.py --start-tasks --folder JalDrishti_AI
```

### Executing Notebooks
The analytical workflow is documented and fully executed in Jupyter:
```bash
jupyter lab
```
Open [`notebooks/JalDrishti_Watershed_Analysis_Continued.ipynb`](./notebooks/JalDrishti_Watershed_Analysis_Continued.ipynb) to inspect:
1. Shapefile topology and CRS verification.
2. HydroATLAS Level 8 attribute inspection.
3. Machine-precision score recalculation.
4. Soil and terrain blocker resolution and live sample outputs.
5. Area-weighted spatial aggregation diagnostics.
6. 3-panel comparative cartography.

### Running Automated Tests
The repository includes a comprehensive unit test suite:
```bash
pytest tests/ -v
```
Tests verify:
- Complete directory structure and configuration files.
- HydroATLAS shapefile feature count (518) and validity.
- Bit-for-bit mathematical reproduction of the preliminary screening score.
- Aggregated catchment indicators, columns, and coverage classification flags.
- Soil texture mass conservation rules.

---

## Documentation Index

The full engineering history and scientific audit trail are preserved in the `docs/` directory:

- [`docs/01_project_overview.md`](./docs/01_project_overview.md) — Mission and geographic scope.
- [`docs/02_problem_solution_requirements.md`](./docs/02_problem_solution_requirements.md) — Problem statement and engineering constraints.
- [`docs/03_methodology_mcda.md`](./docs/03_methodology_mcda.md) — Hydrological indicators and scoring principles.
- [`docs/04_data_catalog_and_processing.md`](./docs/04_data_catalog_and_processing.md) — Catalog of primary datasets and schemas.
- [`docs/05_current_state_and_next_steps.md`](./docs/05_current_state_and_next_steps.md) — Original state and recommendations.
- [`docs/06_stakeholders_and_ai_handoff.md`](./docs/06_stakeholders_and_ai_handoff.md) — Institutional stakeholders and developer guide.
- [`docs/07_continued_analysis_and_village_integration.md`](./docs/07_continued_analysis_and_village_integration.md) — Spatial aggregation methodology.
- [`docs/08_project_audit_report.md`](./docs/08_project_audit_report.md) — Comprehensive senior audit report.
- [`docs/08_audit_action_plan.md`](./docs/08_audit_action_plan.md) — Prioritised engineering action plan.
- [`docs/09_soil_terrain_unblocking_report.md`](./docs/09_soil_terrain_unblocking_report.md) — Full blocker diagnosis and verification.
- [`docs/GITHUB_PUBLICATION_REPORT.md`](./docs/GITHUB_PUBLICATION_REPORT.md) — Repository audit and publication report.

---

## Known Limitations & Missing Data Accounting

1. **Preliminary Score Status**: The initial score is strictly an illustrative proxy combining slope and rainfall. It does not account for aquifer hydrogeology, groundwater storage, or structural feasibility.
2. **Soil & Terrain Batch Status**: The bug has been resolved and verified on 24 representative villages across 8 districts (0.00% missing values, 100.0% texture sum). Full batch export for all 44,468 villages is ready to run via `python scripts/export_village_terrain_soil_gee.py --start-tasks`.
3. **Boundary / Transboundary Basins**:
   - 402 basins have $\ge 90\%$ village coverage (`full_coverage`).
   - 53 basins have $50\%–90\%$ coverage (`substantial_coverage`).
   - 62 basins straddle state borders with $<50\%$ coverage (`partial_border`).
   - 1 basin (`HYBAS_ID: 4081063690`) lies across the Pranhita River in Telangana with $0\%$ Maharashtra village coverage (`transboundary_uncovered`).
4. **Data Integrity Standard**: Missing values are never filled with fabricated or synthetic numbers.

---

## Contributing & Git Workflow

- Pull requests must follow the guidelines in [`CONTRIBUTING.md`](./CONTRIBUTING.md).
- Keep source code modular within `src/jaldrishti/`.
- Ensure all tests pass (`pytest tests/`) before submitting PRs.
- Never commit files $>100\text{ MB}$ without Git LFS.

---

## Data Licensing & Attribution

- **WWF HydroATLAS / HydroSHEDS**: Derived from WWF-US and Lehner & Grill (2013). Free for academic, educational, and non-commercial scientific use.
- **CHIRPS Precipitation**: Developed by Climate Hazards Center (UCSB) / USGS. Public domain data.
- **ESA WorldCover 2021**: European Space Agency. Published under Creative Commons Attribution 4.0 International (CC BY 4.0).
- **ISRIC SoilGrids 250m**: Produced by ISRIC - World Soil Information. Open database license (ODbL).
- **USGS SRTM**: NASA / USGS Shuttle Radar Topography Mission. Public domain elevation data.
- **Repository Code**: Formal open-source license decision pending by project maintainers.
