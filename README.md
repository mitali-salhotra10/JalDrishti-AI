# JalDrishti-AI: Geospatial Watershed Prioritisation & Decision Support System

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![GeoPandas](https://img.shields.io/badge/GIS-GeoPandas%20%7C%20Shapely-green.svg)](https://geopandas.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit%201.66-red.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Tests-52%20Passing-brightgreen.svg)](https://docs.pytest.org/)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**JalDrishti-AI** is an open-source, scientifically validated geospatial decision-support framework and interactive dashboard for watershed prioritization, Managed Aquifer Recharge (MAR), and Surface Water Harvesting (SWH) across all **518 HydroATLAS Level 8 catchments** in Maharashtra, India.

The platform bridges macro-scale hydrological basin intelligence with micro-scale village land-use and soil physics (44,468 village boundaries) using area-weighted geospatial aggregation, multi-scenario Multi-Criteria Decision Analysis (MCDA), empirical ground-truth validation with 6,026 government monitoring wells (CGWB & GSDA), and deterministic preliminary Detailed Project Report (DPR) screening dossier generation.

---

> [!IMPORTANT]
> **STATUTORY PLANNING & SCIENTIFIC SCREENING NOTICE**:
> 1. **Screening Tool Only**: JalDrishti-AI outputs, priority tiers, and Category A designations represent **macro-scale preliminary screening targets for field hydrogeological appraisal**, NOT approved Detailed Project Reports (DPRs), administrative financial sanctions, or civil engineering construction specifications.
> 2. **Groundwater Trend Sign Convention**: Groundwater levels are measured as **depth to water table below ground level (m bgl)**. A positive slope ($\beta > 0\text{ m/yr}$) designates increasing depth below ground level (**water table depletion**); a negative slope ($\beta < 0\text{ m/yr}$) designates decreasing depth (**water table recovery**).
> 3. **Non-Conflation of Interventions**: Managed Aquifer Recharge (MAR) and Surface Water Harvesting (SWH) are governed by distinct hydrogeological principles and evaluated independently. SWH relies on impermeable surface clay vertisols ($\ge 380\text{ g/kg}$) to prevent foundation seepage in unlined earthen structures. MAR requires uncommitted subsurface storage and permeable soils, or dedicated recharge shafts to bypass impermeable vertisol layers.
> 4. **Absent Inventory $\ne$ Zero Infrastructure**: The Maharashtra Remote Sensing Applications Centre (MRSAC) Jalyukt Shivar conservation structure inventory remains protected by state intranet authentication (`mrsac.maharashtra.gov.in/jalyukt/`). Unrecorded digital records are **never equated to zero physical structures on the ground**. Category B (maintenance only) is unassigned across all 518 catchments pending verified digital access.

---

## Table of Contents

1. [Problem Statement & Motivation](#problem-statement--motivation)
2. [Objectives & Research Questions](#objectives--research-questions)
3. [Study Area & Spatial Scale](#study-area--spatial-scale)
4. [Data Sources & Temporal Coverage](#data-sources--temporal-coverage)
5. [Data Processing & Quality Control Pipeline](#data-processing--quality-control-pipeline)
6. [Multi-Criteria Decision Analysis (MCDA) Framework](#multi-criteria-decision-analysis-mcda-framework)
7. [Consensus Prioritisation & Sensitivity Analysis](#consensus-prioritisation--sensitivity-analysis)
8. [Empirical Groundwater Evidence & Validation Analysis](#empirical-groundwater-evidence--validation-analysis)
9. [Action Categorisation: MAR vs. SWH](#action-categorisation-mar-vs-swh)
10. [Standardised DPR Screening Dossier Engine](#standardised-dpr-screening-dossier-engine)
11. [Interactive Geospatial Dashboard](#interactive-geospatial-dashboard)
12. [Scientific Safeguards & Invariants](#scientific-safeguards--invariants)
13. [Installation & Quick Start](#installation--quick-start)
14. [Reproducibility & Baseline Integrity](#reproducibility--baseline-integrity)
15. [Repository Structure](#repository-structure)
16. [Future Work & Limitations](#future-work--limitations)
17. [License & Attribution](#license--attribution)

---

## Problem Statement & Motivation

Maharashtra experiences an acute hydro-climatic dichotomy:
- The **Western Ghats (Konkan / Sahyadri)** receive extreme orographic monsoon rainfall (>3,000–4,000 mm/year), yet steep escarpments cause rapid torrential runoff directly into the Arabian Sea with minimal retention.
- The **Deccan Plateau rain-shadow** (Marathwada, Solapur, Ahmednagar, parts of Vidarbha) receives <600 mm/year, suffering frequent seasonal droughts, acute groundwater depletion, and high agricultural vulnerability.

Historically, water-conservation schemes (e.g., check dams, percolation tanks, nala bunds) have suffered from:
1. **Administrative Boundary Arbitrariness**: Schemes planned at block or district levels ignore natural hydrological drainage boundaries, leading to downstream starvation or structure overcrowding.
2. **Geological Conflation**: Surface runoff retention structures (SWH) and subsurface recharge structures (MAR) are frequently conflated, causing percolation tanks to be sited on impermeable heavy clay vertisols where water evaporates rather than recharging basaltic aquifers.
3. **Data Silos**: Macro-hydrological basin data (HydroATLAS), micro-village agricultural land-use, and decadal groundwater observations (CGWB/GSDA) have remained unintegrated in planning workflows.

---

## Objectives & Research Questions

### Objectives
1. **Multi-Scale Geospatial Harmonisation**: Integrate 44,468 village administrative boundaries with 518 natural hydrological catchments (WWF HydroATLAS Level 8) using vectorized polygon intersection.
2. **Multi-Scenario MCDA**: Formulate, test, and validate 7 multi-criteria decision models balancing climate drought stress, agricultural land use, surface terrain, and soil infiltration capacity.
3. **Empirical Ground-Truth Validation**: Triangulate MCDA model rankings against 6,026 government monitoring wells (CGWB & GSDA) spanning 1970–2025.
4. **Action Categorisation**: Formulate separate, defensible decision rules for Managed Aquifer Recharge (MAR) and Surface Water Harvesting (SWH).
5. **Operational Decision Support**: Deliver an interactive Streamlit dashboard and automated preliminary DPR screening dossier generator for engineers and hydrogeologists.

### Research Questions
- *RQ1*: How stably can multi-scale village socio-ecological data be aggregated into natural hydrological sub-basins without spatial artifacting?
- *RQ2*: Which catchments achieve robust consensus priority across widely divergent expert and policy weighting schemes?
- *RQ3*: To what degree do macro-scale physical MCDA suitability models correlate with decadal observational groundwater trends in fractured basalt Deccan Traps?

---

## Study Area & Spatial Scale

| Level | Spatial Units | Bounding Extent | Implementation Role |
|:---|:---:|:---:|:---|
| **State Level** | 1 State (36 Districts) | 307,713 km² | Primary operational study area (Maharashtra, India). |
| **Hydrological Catchments** | **518 Level 8 Basins** | WWF HydroATLAS v1.0 | Core hydrological unit for regional intervention planning (mean area: ~594 km²). |
| **Village Scale** | **44,468 Villages** | Maharashtra Revenue Census | Primary administrative unit for localized land-use, soil, and cropping metrics. |

---

## Data Sources & Temporal Coverage

| Asset / Dataset | Source Agency | Spatial Resolution | Temporal Coverage | Extracted Indicators / Role |
|:---|:---|:---:|:---:|:---|
| **HydroATLAS Level 8** | WWF / HydroSHEDS v1.0 | 518 Basins | Baseline | Sub-basin boundary polygons, upstream area, elevation, stream gradient. |
| **ISRIC SoilGrids 250m** | ISRIC World Soil Info | 250 m | v2.0 Static | Topsoil (0–5 cm) Clay, Sand, Silt (g/kg), Soil Organic Carbon (dg/kg). |
| **NASA SRTM GL1 DEM** | NASA / USGS | 30 m | Static | Terrain slope (degrees) and topographic elevation (m). |
| **CHIRPS Daily Rainfall** | Climate Hazards Center | 0.05° (~5.5 km) | 2001–2025 (25 yrs) | Long-term annual mean, standard deviation, anomaly %, drought frequency. |
| **ESA WorldCover** | European Space Agency | 10 m | 2021 | Cropland %, Tree cover %, Built-up %, Bare ground %. |
| **CGWB Ground Water** | Central Ground Water Board | 1,446 Stations | 1991–2025 (35 yrs) | Depth to water table (m bgl), decadal Theil-Sen trend ($\beta$), monsoon rise ($\Delta h$). |
| **GSDA Ground Water** | Ground Water Surveys & Dev. Agency | 4,580 Stations | 1970–2025 (55 yrs) | Decadal manual quarterly monitoring records (Maharashtra Ground Water Dept). |

---

## Data Processing & Quality Control Pipeline

```
Raw Multi-Agency Assets                 Vector Processing & Aggregation              Consolidated Decision Assets
┌───────────────────────────┐          ┌──────────────────────────────┐         ┌─────────────────────────────┐
│ 44,468 Village Boundaries │─────────▶│ Area-Weighted Intersection   │────────▶│ 518 Level 8 Catchment Layers│
│ CHIRPS 25-yr Rainfall     │─────────▶│ Polygon Fragment Overlay     │         │ (GPKG & Shapefile)          │
│ ISRIC SoilGrids 250m      │─────────▶│ Mass-Conservation Enforcement│────────▶│ Consolidated Basin CSV      │
│ NASA SRTM 30m DEM         │─────────▶│ EPSG:32643 / EPSG:4326       │         │ (v2 Indicators Table)       │
└───────────────────────────┘          └──────────────────────────────┘         └─────────────────────────────┘
                                                      │
┌───────────────────────────┐                         ▼                         ┌─────────────────────────────┐
│ CGWB (1,446 Wells)        │          ┌──────────────────────────────┐         │ Multi-Scenario MCDA Engine  │
│ GSDA (4,580 Wells)        │─────────▶│ Spatial Point-in-Polygon     │────────▶│ 7 Scenarios, AHP, Consensus │
│ 70,513 Quarterly Records  │          │ Theil-Sen Trend / Delta h    │         │ 87 DPR Screening Dossiers   │
└───────────────────────────┘          └──────────────────────────────┘         └─────────────────────────────┘
```

1. **Mass-Conservation Validation**: Infiltration proxy calculations and soil texture separates strictly satisfy $\text{Sand} + \text{Clay} + \text{Silt} = 1,000\text{ g/kg} \pm 1.0\text{ g/kg}$.
2. **Quality Control & Outlier Filtering**: Groundwater monitoring records were filtered for coordinate bounds ($15.6^\circ\text{N}–22.1^\circ\text{N}$, $72.6^\circ\text{E}–80.9^\circ\text{E}$), physical depth validity ($0 \le \text{mbgl} \le 150$), and minimum time series ($N \ge 5$ observation years for Theil-Sen decadal slope estimation).

---

## Multi-Criteria Decision Analysis (MCDA) Framework

Prioritization is structured into **Four Fundamental Pillars**:
1. **Climate Drought Stress**: Rainfall deficit, long-term coefficient of variation (CV), drought recurrence frequency.
2. **Land Use & Water Demand**: Cropland percentage, agricultural water draft pressure.
3. **Terrain & Runoff Potential**: Basin slope, elevation gradient, surface drainage velocity.
4. **Soil & Infiltration Capacity**: Topsoil sand/clay fractions, soil organic carbon (SOC), infiltration capacity proxy.

### Evaluated MCDA Scenarios
- **Scenario S1 (Equal Pillars)**: Unbiased baseline allocating 25% weight to each pillar.
- **Scenario S2 (AHP Expert)**: Analytic Hierarchy Process pairwise comparison matrix ($CR = 0.046 < 0.10$).
- **Scenario S3 (Drought Stress Focus)**: Prioritizes drought frequency and rainfall deficit (45% climate weight).
- **Scenario S4 (Managed Aquifer Recharge)**: Prioritizes sandy loam infiltration and uncommitted aquifer storage.
- **Scenario S5 (Surface Water Harvesting)**: Prioritizes runoff capture on impermeable clay vertisols.
- **Scenario S6 (Agrarian Vulnerability)**: Prioritizes smallholder rainfed cropland draft.
- **Scenario S7 (Winsorized AHP)**: Robust 5th/95th percentile trimmed score mitigating extreme geographic outliers.

---

## Consensus Prioritisation & Sensitivity Analysis

To ensure scientific defensibility against weight sensitivity, catchments are grouped into three consensus tiers based on cross-scenario stability:

| Consensus Priority Tier | Basin Count ($N$) | Definition & Criteria | Planning Implication |
|:---|:---:|:---|:---|
| **Consensus Tier 1** | **76 Basins** (14.7%) | Median Planning Rank $\le 100$ and rank standard deviation across scenarios $\sigma_{\text{rank}} \le 40$. | Robust high priority under all expert, climate, and agronomic weightings. Priority targets for field appraisal. |
| **Consensus Tier 2** | **109 Basins** (21.0%) | Specialized priority; top-ranked under specific scenarios (e.g., highly suitable for SWH but poor for MAR). | Specialized intervention targeting based on individual pillar suitability. |
| **Consensus Tier 3** | **333 Basins** (64.3%) | Moderate to low priority across all evaluated scenarios; high baseline precipitation or low agrarian vulnerability. | Watershed conservation, baseline monitoring, or maintenance. |

---

## Empirical Groundwater Evidence & Validation Analysis

MCDA macro-suitability scores were independently validated against decadal groundwater depth trends (2015–2024) across 6,026 government monitoring wells:

- **Matched Catchments with Valid Decadal Trends**: $N = 355$ basins.
- **Observed Correlation**: Spearman $\rho = -0.0748$, $p = 0.1598$ ($p > 0.05$, statistically non-significant).
- **Sensitivity Check by Monitoring Density**:
  - $\ge 1$ well/basin ($N = 355$): $\rho = -0.0748, p = 0.1598$
  - $\ge 2$ wells/basin ($N = 274$): $\rho = -0.0379, p = 0.5327$
  - $\ge 3$ wells/basin ($N = 206$): $\rho = -0.0530, p = 0.4491$
  - $\ge 5$ wells/basin ($N = 114$): $\rho = -0.1383, p = 0.1423$

### Why the Macro-Correlation is Weak (Deccan Trap Basalt Hydrogeology)
1. **Intensive Pumping in Vertisol Plains**: Cash crop flood irrigation (sugarcane, cotton) is concentrated in flat clay vertisol plains with slow surface infiltration, producing acute local drawdown where surface recharge is geologically constrained.
2. **Shallow vs. Deep Aquifer Decoupling**: Government observation dugwells tap shallow weathered basalt that recharges rapidly each monsoon ($\Delta h = +4.06\text{ m}$), whereas private agricultural extraction taps deep fractured basalt ($>80\text{ m}$).
3. **Suitability vs. Extraction**: Physical suitability identifies where recharge is geologically feasible, not where historical extraction has been most aggressive.

---

## Action Categorisation: MAR vs. SWH

Within Consensus Tier 1 ($N = 76$), interventions are partitioned using separate, hydrogeologically grounded decision rules:

```
                            Consensus Tier 1 Catchments (N = 76)
                                              │
                 ┌────────────────────────────┴───────────────────────────┐
                 ▼                                                        ▼
   Managed Aquifer Recharge (MAR)                           Surface Water Harvesting (SWH)
   Subsurface Infiltration & Storage                        Surface Runoff & Foundation Seepage
   ─────────────────────────────────                        ───────────────────────────────────
   • Category A (12 Basins):                                • Category A (75 Basins):
     Decadal Depletion (β > 0) +                              Impermeable Vertisols (Clay ≥ 380 g/kg) +
     Permeable Soil (Clay ≤ 400, Sand ≥ 250)                  Viable Runoff & Moderate Slope (≤ 15°)
   • Category C (56 Basins):                                • Category D (1 Basin):
     Heavy Clay Vertisol Surface Barrier                      Steep Escarpment Barrier (> 15°)
   • Category D (8 Basins):                                 • Category B (0 Basins):
     Recovering Water Table (β ≤ 0)                           Unassigned (MRSAC inventory pending)
   • Category B (0 Basins):
     Unassigned (MRSAC inventory pending)
```

---

## Standardised DPR Screening Dossier Engine

Batch generation via [`scripts/generate_dpr_screening_sheets.py`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/scripts/generate_dpr_screening_sheets.py) produces standardized feasibility sheets:
- **12 MAR Category A Screening Sheets**: In [`reports/dpr_screening_sheets/mar_category_a/`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/reports/dpr_screening_sheets/mar_category_a).
- **75 SWH Category A Screening Sheets**: In [`reports/dpr_screening_sheets/swh_category_a/`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/reports/dpr_screening_sheets/swh_category_a).
- **Master Index Table**: In [`reports/dpr_screening_sheets/dpr_screening_master_index.csv`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/reports/dpr_screening_sheets/dpr_screening_master_index.csv).
- **Reusable DPR Screening Template**: In [`reports/dpr_screening_sheets/DPR_SCREENING_TEMPLATE.md`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/reports/dpr_screening_sheets/DPR_SCREENING_TEMPLATE.md).

### Mandatory 5-Point Pre-Construction Engineering Checklist
Every screening sheet mandates field investigation prior to civil construction:
1. [ ] **Vertical Electrical Sounding (VES)**: Minimum 3 resistivity soundings to verify fractured basalt thickness.
2. [ ] **Double-Ring Infiltrometer Testing**: In situ infiltration rate measurement across percolation tank beds.
3. [ ] **Private Well Census**: Survey of commercial borewells within a 1.5 km radius to prevent public recharge capture.
4. [ ] **Physical Siltation Audit**: Micro-catchment inspection; where siltation exceeds 40%, prioritize desilting over new civil construction.
5. [ ] **Baseline Water Quality**: Electrical conductivity (EC) and nitrate testing to protect potable drinking aquifers.

---

## Interactive Geospatial Dashboard

The production dashboard ([`app.py`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/app.py)) provides five synchronized views:

1. **Executive Overview**: Statewide KPI metrics (518 catchments, 76 Tier 1, 459 monitored basins, 12 MAR Cat A, 75 SWH Cat A), MRSAC inventory warning banner, and category breakdown charts.
2. **Interactive Catchment Map (Dual Engine)**:
   - **Plotly Vector Choropleth**: High-performance WebGL vector layer with hover tooltips.
   - **Folium OpenStreetMap Leaflet Engine**: Real-world GIS tile viewer with dynamic pan/zoom, layer controls, and an interactive Catchment Quick-Inspection panel.
3. **Catchment Deep-Dive Profiler**: Four diagnostic cards for any selected basin (MCDA scenario scores, CGWB/GSDA observation statistics, soil/terrain physics, and transparent decision audit rules).
4. **Multi-Catchment Comparison**: Side-by-side trade-off matrix and scenario radar charts for 2 to 5 catchments simultaneously.
5. **DPR Dossiers & Data Export**: One-click filtered CSV download (`jaldrishti_filtered_catchments.csv`), single-catchment markdown dossier download, printable summary sheet view, and reusable DPR template download.

---

## Scientific Safeguards & Invariants

1. **Zero Fabrication**: No hallucinated IDs, no invented project budgets (no ₹/INR figures), and no fabricated structure coordinates exist in code, data, or dossiers.
2. **Cryptographic Baseline Protection**: Four Phase 3 and Phase 4 baseline datasets are cryptographically pinned and verified bit-for-bit before and after every execution.
3. **No Silent Zero Coercion**: Missing groundwater trends or soil attributes remain `NaN` or display as `"Inconclusive / N/A"`, preventing false reporting of zero depletion or zero slope.
4. **Explicit Planning Boundary**: Prominently displays statutory disclaimers stating these are preliminary macro-screening targets, not civil engineering sanctions.

---

## Installation & Quick Start

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13 (64-bit)
- PowerShell (Windows) or Bash (Linux/macOS)

### 1. Clone & Setup Environment
```powershell
# Navigate to workspace
cd "C:\Users\MITALI SALHOTRA\OneDrive\Desktop\JalDrishti"

# Install pinned dashboard dependencies
pip install -r requirements-dashboard.txt
```

### 2. Launch Interactive Dashboard
```powershell
streamlit run app.py
```
*The dashboard will automatically open in your browser at `http://localhost:8501`.*

### 3. Run Automated Tests
```powershell
python -m pytest tests/ -v
```
*Executes all 52 tests across 8 test modules (expected duration: ~25s).*

### 4. Regenerate DPR Screening Sheets
```powershell
python scripts/generate_dpr_screening_sheets.py
```
*Batch-generates all 87 Category A dossiers deterministically in ~2s.*

---

## Reproducibility & Baseline Integrity

The table below documents the cryptographic hashes of the four protected baseline datasets:

| Dataset / Asset File | Scope | Rows | Cols | Pinned SHA-256 Checksum |
|:---|:---|:---:|:---:|:---|
| `data/processed/jaldrishti_mcda_scenario_rankings.csv` | **Phase 3 Baseline** | 518 | 17 | `692b7dc9b7d56e5a964a452348c3086906f0e1d1630e26a6761306a2f875e982` |
| `data/processed/jaldrishti_consensus_priority_audit.csv` | **Phase 4 Baseline** | 518 | 42 | `85bece275a30aca3fd7aca0d81ef226179e6bb702f96a95b81e3f76669696ccb` |
| `data/processed/jaldrishti_watersheds_with_village_indicators_v2.csv` | **Phase 3/4 Baseline** | 518 | 57 | `93585556df7f91825e1efe4664d224e3fc2a4c437317e815efa8c6f9b01a4843` |
| `data/processed/jaldrishti_scored_watersheds.shp` | **Phase 2 Baseline** | 518 | — | `b600ca7cf8decf872b11cdcc2bb947c6ea9c7748bd2451d90c4b268f0339e372` |

---

## Repository Structure

```
JalDrishti/
├── app.py                                   # Production Streamlit decision support dashboard
├── requirements-dashboard.txt               # Pinned runtime dependencies
├── pyproject.toml                           # Project configuration & pytest settings
├── README.md                                # Master project documentation
│
├── data/
│   ├── raw/                                 # Raw CGWB and GSDA observation records
│   │   ├── ground_water_level_manual_quarterly_maharashtra_1970_2025.csv
│   │   ├── gwl_manual_quarterly_cgwb_mh_1991_2020.csv
│   │   └── gwl_manual_quarterly_cgwb_mh_2021_2025.csv
│   └── processed/                           # Verified processed CSV, GPKG, and Shapefile layers
│       ├── jaldrishti_phase7_evidence_assessment.csv        # Authoritative evidence ledger (518 rows)
│       ├── jaldrishti_infrastructure_by_catchment.csv       # Infrastructure policy ledger (518 rows)
│       ├── jaldrishti_groundwater_validation_results.csv    # Trend & recharge validation (518 rows)
│       ├── jaldrishti_mcda_scenario_rankings.csv            # Protected Phase 3 baseline
│       ├── jaldrishti_consensus_priority_audit.csv          # Protected Phase 4 baseline
│       ├── jaldrishti_watersheds_with_village_indicators_v2.csv # Protected Phase 3/4 baseline
│       └── jaldrishti_scored_watersheds.shp                 # Protected Phase 2 baseline shapefile
│
├── docs/                                    # Phase 1 through 11 technical & academic reports
│   ├── 17_DASHBOARD_USER_GUIDE.md           # Dashboard operator manual
│   ├── 18_PHASE9_FINAL_AUDIT_REPORT.md      # Comprehensive scientific audit report
│   ├── 19_PHASE10_RELEASE_READINESS_REPORT.md # Release readiness certification
│   ├── 20_FINAL_PROJECT_REPORT.md           # Formal academic submission report
│   ├── 21_PROJECT_DEMONSTRATION_SCRIPT.md   # 7–10 minute live presentation script
│   ├── 22_FINAL_PRESENTATION_OUTLINE.md     # 10–12 slide presentation deck outline
│   └── 23_SUBMISSION_READINESS_CHECKLIST.md # Academic submission verification checklist
│
├── reports/
│   └── dpr_screening_sheets/                # 87 Batch-generated screening dossiers
│       ├── dpr_screening_master_index.csv   # Master index of all 87 screening dossiers
│       ├── DPR_SCREENING_TEMPLATE.md        # Reusable field engineering template
│       ├── mar_category_a/                  # 12 MAR Category A catchment dossiers
│       │   └── DPR_MAR_HYBAS_*.md
│       └── swh_category_a/                  # 75 SWH Category A catchment dossiers
│           └── DPR_SWH_HYBAS_*.md
│
├── scripts/                                 # Processing, triangulation, and validation pipelines
│   ├── generate_dpr_screening_sheets.py     # Deterministic dossier batch generator
│   ├── triangulate_groundwater_and_infrastructure.py # Multi-evidence classification engine
│   ├── validate_independent_evidence.py     # CGWB/GSDA Theil-Sen trend & Spearman correlation
│   └── harmonize_cgwb_observations.py       # Ground water observation harmonization
│
└── tests/                                   # Automated test suite (52 tests, 8 modules)
    ├── test_dashboard_integration.py        # Dashboard workflows, UI, and hash immutability (10 tests)
    ├── test_consensus_ranking.py            # Consensus tiers & rank stability (5 tests)
    ├── test_independent_evidence_validation.py # Groundwater trend & QC rules (12 tests)
    ├── test_mcda_sensitivity.py             # MCDA scores, AHP CR & scenario bounds (6 tests)
    ├── test_phase7_triangulation.py         # Triangulation schemas & hash protection (5 tests)
    ├── test_phase8_scientific_audit.py      # Trend sign mathematics & zero-hallucination (6 tests)
    └── test_spatial_aggregation.py          # Spatial intersection & soil mass conservation (8 tests)
```

---

## Future Work & Limitations

1. **MRSAC Intranet Authentication Dependency**: Access to official Jalyukt Shivar conservation structure polygons (`mrsac.maharashtra.gov.in/jalyukt/`) requires Government of Maharashtra intranet credentials. Institutional access will unblock localized structure-density saturation modeling.
2. **High-Resolution Basalt Lineament Fracture Mapping**: HydroATLAS Level 8 catchments (~600 km²) identify prioritization sub-basins. Integrating ALOS PALSAR 12.5m DEMs to derive Topographic Wetness Index (TWI) and automated lineament extraction will support micro-siting within prioritized catchments.
3. **Automated PDF DPR Booklet Compilation**: Adding a headless `WeasyPrint` or LaTeX compilation pipeline to export print-ready multi-page PDF booklets with embedded vector choropleths.

---

## License & Attribution

- **Software Code**: Released under the MIT License.
- **Scientific Documentation & Reports**: Licensed under [Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/).
- **Data Attribution**:
  - HydroSHEDS / HydroATLAS: © World Wildlife Fund, Inc. (2019).
  - SoilGrids 250m: © ISRIC — World Soil Information (2020).
  - CHIRPS Precipitation: Climate Hazards Center, UC Santa Barbara.
  - NASA SRTM GL1: NASA / USGS Earth Resources Observation and Science Center.
  - Groundwater Data: Central Ground Water Board (CGWB) & Ground Water Surveys and Development Agency (GSDA), Govt. of Maharashtra.