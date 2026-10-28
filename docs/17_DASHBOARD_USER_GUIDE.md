# JalDrishti-AI — Phase 9: Interactive Decision Support Dashboard User Guide

**Document ID**: `JD-DOC-17-DASHBOARD-GUIDE`  
**Phase**: Phase 9 — Interactive Decision Support Dashboard & Stakeholder Reporting  
**Status**: Complete, Verified & Tested  
**Date**: October 2026  
**Target Audience**: State Watershed Development Authorities, GSDA Hydrogeologists, District Agricultural Officers, and Water Planners  
**Scope**: 518 HydroATLAS Level 8 Catchments, Maharashtra, India  

---

## 1. Introduction & Operational Objective

The **JalDrishti-AI Geospatial Decision Support Dashboard** is a local, interactive web application that operationalizes the multi-scale scientific data pipeline, multi-scenario MCDA models, and empirical ground-truth observational records developed across Phases 1 through 8.

The dashboard provides state watershed officers and planning engineers with:
1. **Interactive Geospatial Visualization**: Color-coded choropleth maps across all 518 Level 8 catchments in Maharashtra.
2. **Transparent Decision Traceability**: Detailed inspection of the physical metrics (soil texture, slope, infiltration, rainfall, and drought history) and exact decision rules that govern priority tiers and action categories.
3. **Observational Ground-Truth Integration**: Decadal groundwater trends (2015–2024) and seasonal fluctuation ($\Delta h$) from 6,026 monitoring stations across the Central Ground Water Board (CGWB) and Ground Water Surveys and Development Agency (GSDA).
4. **Standardized DPR Screening Dossiers**: Rapid generation and download of preliminary Detailed Project Report (DPR) screening sheets for confirmed high-priority catchments.

---

## 2. Quick Start & Local Execution

### 2.1 System Requirements
- **Operating System**: Windows, Linux, or macOS
- **Python**: Version 3.10, 3.11, 3.12, or 3.13
- **Primary Dependencies**: `streamlit>=1.35.0`, `geopandas>=1.0.0`, `plotly>=5.20.0`, `folium>=0.16.0`, `streamlit-folium>=0.20.0`

### 2.2 Installation
From the project root directory (`C:\Users\MITALI SALHOTRA\OneDrive\Desktop\JalDrishti`), install dependencies:

```powershell
# Install dashboard dependencies
pip install -r requirements-dashboard.txt
```

### 2.3 Launching the Application
Execute the following command in PowerShell or terminal:

```powershell
# Launch the Streamlit dashboard
streamlit run app.py
```

The application will launch automatically in your default browser at:
```
http://localhost:8501
```

*(To run headlessly on a custom port or remote server, use `streamlit run app.py --server.port 8501 --server.headless true`)*.

---

## 3. Dashboard Architecture & Navigation

The dashboard features a persistent sidebar with global filtering capabilities and five primary views:

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │              JALDRISHTI-AI DECISION SUPPORT DASHBOARD ARCHITECTURE          │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │ 1. 📊 Executive Overview    │ Statewide KPI scorecards, infrastructure      │
  │                             │ warnings, and multi-agency validation summary │
  ├─────────────────────────────┼───────────────────────────────────────────────┤
  │ 2. 🗺️ Interactive Map       │ Full-state vector choropleth map styled by    │
  │                             │ tiers, screening categories, and soil metrics │
  ├─────────────────────────────┼───────────────────────────────────────────────┤
  │ 3. 🔍 Catchment Profiler    │ Single-catchment deep dive, scenario radar    │
  │                             │ chart, ground-truth wells, and decision trace │
  ├─────────────────────────────┼───────────────────────────────────────────────┤
  │ 4. ⚖️ Multi-Catchment Comp. │ Side-by-side comparison of 2–5 catchments     │
  │                             │ with trade-off and parameter tables           │
  ├─────────────────────────────┼───────────────────────────────────────────────┤
  │ 5. 📑 DPR Dossiers & Export │ Downloadable CSV tables and standardized DPR  │
  │                             │ preliminary screening sheets (87 catchments)  │
  └─────────────────────────────┴───────────────────────────────────────────────┘
```

---

## 4. Feature Walkthrough

### 4.1 📊 Executive Overview
- **Statewide Metric Scorecards**:
  - **Total Catchments**: 518 Level 8 HydroATLAS basins.
  - **Consensus Tier 1**: 76 high-priority multi-scenario catchments (14.7%).
  - **Monitoring Coverage**: 459 catchments (88.61% of Maharashtra) actively monitored by 6,026 government wells.
  - **MAR Category A**: 12 catchments with confirmed decadal groundwater depletion.
  - **SWH Category A**: 75 catchments with surface runoff deficits and impermeable clay soils.
- **Infrastructure Inventory Warning Banner**:
  - Highlights that the Maharashtra Remote Sensing Applications Centre (MRSAC) Jalyukt Shivar shapefile is protected by departmental intranet authentication (`mrsac.maharashtra.gov.in/jalyukt/`).
  - Mandates the project invariant: **Absent digital records must never be interpreted as the physical absence of water conservation infrastructure on the ground**.
- **Interactive Visualizations**:
  - Consensus tier donut chart.
  - Comparative bar chart showing MAR vs. SWH action category breakdowns.
  - Decadal groundwater depth trend histogram.

---

### 4.2 🗺️ Interactive Catchment Map (Dual Engine)
The geospatial module provides two synchronized map rendering engines selectable via the **Map Visualization Engine** toggle:

1. **Plotly Vector Choropleth Engine**:
   - High-performance WebGL/SVG choropleth with full panning, zooming, and dynamic hover tooltips displaying catchment area, median rank, decadal trend, and monitoring well density.
   - Ideal for statewide pattern recognition, trend distribution inspection, and rapid thematic switching.

2. **Folium OpenStreetMap Leaflet Engine**:
   - Interactive GIS Leaflet map overlaid on live OpenStreetMap base tiles.
   - Displays all 518 Level 8 catchment polygons colored by priority tier, screening category, or groundwater trend.
   - Includes full Leaflet layer controls, zoom-to-extent, and a **Catchment Quick-Inspection Panel** that allows engineers to select any catchment directly and view its complete hydrological metrics and screening category breakdown.

#### Layer Attributes:
- **Consensus Priority Tier**: Red (Tier 1: Robust Multi-Scenario Priority), Orange (Tier 2: Moderate Priority), Green (Tier 3: Low Priority).
- **MAR Provisional Action Category**: Royal Blue (Category A: Potential New MAR Infrastructure), Amber (Category C: Mixed / Low Infiltration), Light Blue (Category D: Stable / Insufficient Data).
- **SWH Provisional Action Category**: Ochre (Category A: Potential New SWH Infrastructure), Grey (Category C/D: Non-Tier-1 or Severe Slope).
- **Decadal Groundwater Depth Trend**: Diverging red-blue scale (Red = Depletion $\beta > 0$, Blue = Recovery $\beta < 0$).
- **Physical Soil & Terrain Layers**: Topsoil Clay Content ($g/kg$), Infiltration Proxy ($cm/hr$), Annual Precipitation ($mm/yr$).

---

### 4.3 🔍 Catchment Deep-Dive Profiler
Select any catchment by `HYBAS_ID` from the searchable dropdown to access a comprehensive four-card diagnostic dossier:
1. **Multi-Scenario Scoring Card**: Bar chart showing normalized scores across $S_1$ (Equal Pillars), $S_2$ (AHP Expert), $S_4$ (MAR), $S_5$ (SWH), and $S_7$ (Winsorized AHP), with median planning rank.
2. **Ground-Truth Observational Card**: CGWB well count, GSDA well count, decadal depth trend ($\beta_{\text{trend}}$ in m/yr), seasonal recharge rise ($\Delta h$), and evidence confidence rating.
3. **Physical & Terrain Card**: Topsoil clay, sand, silt, soil organic carbon (SOC), infiltration capacity proxy, mean slope, elevation, annual precipitation, and cropland percentage.
4. **Decision Engine Audit Trace**: Displays the exact physical and observational rules that assigned the catchment's MAR and SWH screening categories.

---

### 4.4 ⚖️ Multi-Catchment Comparison
Enables side-by-side comparative trade-off analysis for 2 to 5 catchments simultaneously:
- **Comparative Bar Chart**: Visualizes scenario scores across selected catchments.
- **Parameters Matrix**: Displays a side-by-side table of drainage area, consensus tier, depth trend, well count, clay %, sand %, and infiltration proxy.
- **Scientific Safeguard**: Emphasizes that MAR ($S_4$) and SWH ($S_5$) scores represent separate hydrogeological mechanisms and must not be treated as interchangeable.

---

### 4.5 📑 DPR Screening Dossiers, Printable Summary & Data Export
- **CSV Data Export**: One-click download of the currently filtered catchment dataset (`jaldrishti_filtered_catchments.csv`), containing all 43 physical and decision attributes.
- **DPR Dossier Viewer & Download**: Inspect and download complete preliminary DPR screening sheets for:
  - **12 Confirmed MAR Category A Catchments** (e.g., `4081076330`, `4081069540`, `4081044860`).
  - **75 Confirmed SWH Category A Catchments**.
- **Printable Summary Sheet**: Clean, formatted markdown screening summary view for any selected catchment, formatted for one-click printing or PDF export.
- **Reusable DPR Screening Template**: Direct download of `DPR_SCREENING_TEMPLATE.md` containing standardized field verification protocols, statutory disclaimers, and pre-construction engineering checklists.

---

## 5. Scientific Principles & Decision Governance

The dashboard strictly enforces core scientific safeguards established in Phase 8:

### 5.1 Groundwater Depth Trend Sign Convention
- Depth is measured in **meters below ground level (m bgl)**.
- **Positive Trend ($\beta > 0\text{ m/year}$)**: Depth is increasing $\implies$ **Groundwater Depletion**.
- **Negative Trend ($\beta < 0\text{ m/year}$)**: Depth is decreasing $\implies$ **Groundwater Recovery**.

### 5.2 Hydrogeological Separation of MAR and SWH
- **Managed Aquifer Recharge (MAR)**: Requires uncommitted aquifer storage and observed water table depletion. In sandy loam terrains, surface percolation tanks are screened; in heavy clay vertisols ($\text{clay} \ge 400\text{ g/kg}$), subsurface recharge shafts or recharge borewells are required to bypass the impermeable surface layer.
- **Surface Water Harvesting (SWH)**: Operates on surface runoff capture and relies on impermeable clay vertisols to prevent foundation seepage in unlined earthen structures (check dams, nala bunds, farm ponds). Evaluated independently of groundwater depth trends.

### 5.3 Explanation of Non-Significant Correlation ($\rho = -0.075, p = 0.16$)
The weak correlation between physical MAR suitability and decadal groundwater trends is an expected characteristic of the Deccan Volcanic Province:
1. Intensive agricultural pumping (cash crops, flood irrigation) is concentrated in flat vertisol plains with low surface permeability, causing acute local depletion.
2. Shallow government dugwells recharge rapidly each monsoon ($\Delta h = +4.06\text{ m}$), whereas private agricultural extraction taps deep fractured basalt ($>80\text{ m}$).
3. Physical suitability screening identifies where recharge is geologically viable, not where historical pumping has been most aggressive.

---

## 6. Statutory Planning Disclaimer & Mandatory Field Checklist

> **STATUTORY DISCLAIMER**:  
> The JalDrishti-AI dashboard is a **macro-screening decision support tool designed to target sub-basins for detailed field investigation**. It is **NOT** an approved Detailed Project Report (DPR), administrative expenditure sanction, or civil engineering specification.

### Mandatory Pre-Construction Engineering Checklist
Prior to sanctioning any civil water conservation structure identified as Category A:
1. [ ] **Vertical Electrical Sounding (VES)**: Conduct minimum 3 resistivity soundings along suspected lineaments to verify fractured basalt thickness.
2. [ ] **Infiltration Testing**: Perform double-ring infiltrometer tests across prospective percolation tank beds.
3. [ ] **Local Well Census**: Map private borewells within a 1.5 km radius to prevent capture by private commercial irrigators.
4. [ ] **Physical Siltation Audit**: Physically inspect existing structures in the micro-catchment; where siltation exceeds 40%, prioritize desilting over new civil construction.
5. [ ] **Water Quality Baseline**: Measure baseline electrical conductivity (EC) and nitrate levels to safeguard potable aquifers.
