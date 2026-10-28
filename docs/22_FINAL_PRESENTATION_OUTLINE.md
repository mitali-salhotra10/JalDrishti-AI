# JalDrishti-AI: Final Academic Presentation Outline (10–12 Slides)

**Document ID**: `JD-DOC-22-PRESENTATION-OUTLINE`  
**Format**: 11-Slide Master Outline for Technical Defense, Evaluation Committee & Capstone Presentation  
**Project**: JalDrishti-AI — Multi-Scale Geospatial Decision Support for Watershed Prioritisation  
**Target Duration**: 10 Minutes (~1 Minute Per Slide)  
**Authors**: JalDrishti-AI Engineering Team  

---

## Slide Index & Overview

| Slide # | Slide Title | Core Theme | Suggested Visual Asset |
|:---:|:---|:---|:---|
| **Slide 1** | **Title Slide: JalDrishti-AI** | Project Identity & Scope | Project title banner, logos, author credentials |
| **Slide 2** | **The Hydrological Dilemma of Maharashtra** | Problem Statement & Context | Western Ghats vs. Deccan Plateau precipitation map |
| **Slide 3** | **Objectives & Multi-Scale Architecture** | Scientific Scope & Spatial Scales | System architecture diagram (44k villages to 518 basins) |
| **Slide 4** | **Multi-Source Data Ingestion & QC** | Environmental Datasets & Mass Conservation | Data source matrix & SoilGrids mass-conservation equation |
| **Slide 5** | **Four-Pillar MCDA & 7 Policy Scenarios** | Decision Modeling & AHP | MCDA hierarchy flowchart & radar weight comparison |
| **Slide 6** | **Consensus Prioritisation & Tiering** | Sensitivity & Robust Tiers | Consensus tier distribution donut chart (76 Tier 1 basins) |
| **Slide 7** | **Empirical Ground-Truth Triangulation** | 6,026 Wells & Theil-Sen Trends | Theil-Sen trend sign diagram & Deccan Trap basalt schematic |
| **Slide 8** | **Action Categorisation: MAR vs. SWH** | Hydrogeological Separation | Divergent MAR vs. SWH decision tree & category counts |
| **Slide 9** | **Interactive Decision Support Dashboard** | Operational Streamlit Software | Screenshots: Dual Map Engine & Catchment Profiler |
| **Slide 10** | **Automated DPR Screening Dossiers** | Operational Implementation Briefs | Sample MAR Category A dossier & 5-point checklist |
| **Slide 11** | **Scientific Invariants, Limitations & Future Work** | Governance, Boundaries & Next Steps | Invariants table, MRSAC notice, final conclusion |

---

## Slide-by-Slide Content & Speaker Notes

### Slide 1: Title Slide: JalDrishti-AI
- **Header**: JalDrishti-AI: A Multi-Scale Geospatial Decision Framework for Watershed Prioritisation
- **Subtitle**: Multi-Criteria Decision Analysis, Ground-Truth Observational Triangulation & Interactive Screening across 518 Catchments in Maharashtra, India
- **Metadata**: 
  - Author: Scientific Software & GIS Engineering Team
  - Institution: University Department of Geospatial Engineering & Hydrology
  - Scope: 518 HydroATLAS Level 8 Sub-basins (307,713 km²) | 44,468 Villages
- **Suggested Visual**:
  - `[Existing Figure]`: `outputs/figures/mcda_ranking_stability_scatter.png` or dashboard hero graphic.
- **Speaker Notes**:
  > *"Good morning committee members. I am pleased to present JalDrishti-AI, an end-to-end geospatial decision support framework designed to scientifically prioritize sub-watersheds for water conservation interventions across Maharashtra."*

---

### Slide 2: The Hydrological Dilemma of Maharashtra
- **Bullet Points**:
  - **Acute Spatial Dichotomy**:
    - *Western Ghats (Konkan/Sahyadri)*: High orographic rainfall (>3,000–4,000 mm/yr) lost to high-velocity runoff into the Arabian Sea.
    - *Deccan Plateau Rain-Shadow*: Low rainfall (<600 mm/yr), chronic moisture deficits, high agrarian drought recurrence.
  - **Hydrogeology of the Deccan Traps**:
    - Low primary porosity (<1%–3%) and low specific yield ($S_y \approx 0.01–0.03$).
    - Ground-water extraction for cash crops (sugarcane, cotton) severely depletes weathered basalt.
  - **Conventional Planning Pitfalls**:
    - Administrative boundary bias (districts/blocks rather than hydrological catchments).
    - Conflation of surface water harvesting (SWH) with managed aquifer recharge (MAR).
    - Lack of multi-scenario sensitivity testing or ground-truth validation.
- **Suggested Visual**:
  - `[Dashboard Capture Required]`: Annual precipitation choropleth layer from View 2 showing the extreme east-west rainfall contrast.
- **Speaker Notes**:
  > *"Maharashtra presents one of the most severe hydrological contrasts in the world. Earthen conservation structures are frequently misallocated due to administrative boundary bias and a fundamental confusion between surface runoff capture and subsurface recharge."*

---

### Slide 3: Objectives & Multi-Scale Architecture
- **Bullet Points**:
  - **Core Objectives**:
    1. Harmonize micro-administrative village data into natural hydrological drainage units.
    2. Model multi-scenario MCDA suitability across competing expert and policy perspectives.
    3. Triangulate model scores against long-term observational well trends (CGWB & GSDA).
    4. Separate MAR and SWH intervention planning with strict physical criteria.
    5. Operationalize results in an interactive GIS dashboard with automated screening dossiers.
  - **Multi-Scale Hierarchy**:
    - 44,468 Village Boundaries $\implies$ Vectorized Intersection $\implies$ 518 Level 8 Basins (WWF HydroATLAS).
- **Suggested Visual**:
  - `[Existing Figure]`: System architecture workflow diagram from Section 4 of `README.md`.
- **Speaker Notes**:
  > *"Our primary technical contribution is bridging micro-scale rural village data with macro-scale natural drainage basins. Water flows according to topography, not administrative borders."*

---

### Slide 4: Multi-Source Data Ingestion & Mass Conservation
- **Bullet Points**:
  - **Ingested Remote Sensing & GIS Assets**:
    - *HydroATLAS v1.0*: 518 Level 8 basins, baseline morphology, drainage networks.
    - *CHIRPS v2.0 (2001–2025)*: 25-year daily precipitation, anomaly %, drought frequency.
    - *NASA SRTM 30m GL1*: Topographic elevation and slope gradient.
    - *ESA WorldCover 10m (2021)*: Cropland %, tree cover %, built-up area.
    - *ISRIC SoilGrids 250m v2.0*: Sand, clay, silt, and soil organic carbon (SOC) at 0–5 cm.
  - **Physical Quality Control**:
    - Vectorized area-weighted fragment aggregation in `EPSG:32643`.
    - Soil texture mass conservation strictly enforced: $\text{Sand} + \text{Clay} + \text{Silt} = 1,000\text{ g/kg} \pm 1.0$.
    - Saxton-Rawls continuous infiltration capacity proxy ($cm/hr$).
- **Suggested Visual**:
  - `[Existing Figure]`: Soil texture sanity validation log or infiltration proxy formula.
- **Speaker Notes**:
  > *"Every single catchment underwent strict physical quality control. Infiltration capacity was modeled using continuous pedotransfer functions, guaranteeing that soil texture fractions conserve mass."*

---

### Slide 5: Four-Pillar MCDA & 7 Policy Scenarios
- **Bullet Points**:
  - **Four Fundamental Pillars**:
    1. *Climate Drought Stress*: Rainfall deficit, long-term CV %, drought recurrence frequency.
    2. *Agrarian Water Demand*: Cropland percentage, agricultural draft pressure.
    3. *Terrain Runoff Potential*: Mean terrain slope, elevation gradient.
    4. *Soil Infiltration Capacity*: Sand %, clay %, infiltration proxy.
  - **Seven Policy Scenarios Evaluated**:
    - $S_1$ (Equal Pillars: 25% each) | $S_2$ (AHP Expert: Consistency Ratio $CR = 0.046$)
    - $S_3$ (Drought Stress Focus: 45% Climate) | $S_4$ (MAR Focus: 40% Soil/Infiltration)
    - $S_5$ (SWH Focus: 35% Terrain/Slope) | $S_6$ (Agrarian Vulnerability: 45% Land Use)
    - $S_7$ (Winsorized AHP: 5th/95th percentile outlier dampening)
- **Suggested Visual**:
  - `[Existing Figure]`: `outputs/figures/mcda_weight_comparison.png`.
- **Speaker Notes**:
  > *"Single-formula scoring is vulnerable to subjective bias. We formulated seven diverse scenarios, including an Analytic Hierarchy Process model with a consistency ratio of 0.046, well within Saaty's 0.10 threshold."*

---

### Slide 6: Consensus Prioritisation & Tiering
- **Bullet Points**:
  - **Eliminating Weight Subjectivity**:
    - Calculated **Median Planning Rank** and rank standard deviation ($\sigma_{\text{rank}}$) across all 7 scenarios.
  - **Statewide Classification**:
    - **Consensus Tier 1 (76 Basins / 14.7%)**: Robust high-priority ($\text{Rank}_{\text{median}} \le 100, \sigma_{\text{rank}} \le 40$).
    - **Consensus Tier 2 (109 Basins / 21.0%)**: Specialized priority (highly ranked under specific scenarios).
    - **Consensus Tier 3 (333 Basins / 64.3%)**: Moderate to low priority / baseline conservation.
  - **Cross-Scenario Stability**:
    - High inter-scenario correlation ($r_s = 0.82–0.98$) across broad policy scenarios.
    - Deliberate and scientifically expected divergence between MAR and SWH ($r_s = 0.61$).
- **Suggested Visual**:
  - `[Existing Figure]`: `outputs/figures/mcda_ranking_stability_scatter.png`.
- **Speaker Notes**:
  > *"By analyzing the median rank across all scenarios, we isolated 76 catchments that consistently emerge as top-priority targets regardless of whether decision-makers prioritize climate, agronomy, or slope."*

---

### Slide 7: Empirical Ground-Truth Triangulation
- **Bullet Points**:
  - **Government Well Network**:
    - Ingested 70,513 quarterly records across 6,026 stations (1,446 CGWB + 4,580 GSDA; 1970–2025).
    - 459 catchments (88.61% of Maharashtra) actively monitored; 355 possess valid decadal trends.
  - **Theil-Sen Trend Sign Mathematics**:
    - Depth below ground level (m bgl): $\beta > 0 \implies$ Depletion | $\beta < 0 \implies$ Recovery.
  - **Statistical Finding & The Deccan Trap Paradox**:
    - Correlation between physical MAR score and decadal depth trend: **Spearman $\rho = -0.0748, p = 0.1598$ (non-significant)**.
    - *Why?* Cash-crop extraction is concentrated in flat vertisol plains where surface infiltration is slowest; shallow dugwells recharge rapidly each monsoon ($\Delta h = +4.06\text{ m}$), while private tube-wells pump from deep fractured basalt ($>80\text{ m}$).
- **Suggested Visual**:
  - `[Dashboard Capture Required]`: Diverging decadal groundwater depth trend histogram and choropleth from View 1.
- **Speaker Notes**:
  > *"Triangulating our model against 6,026 government wells revealed a vital insight: macro-suitability does not correlate with historical depletion because heavy pumping occurs in flat clay vertisols where surface recharge is geologically hardest to achieve."*

---

### Slide 8: Action Categorisation: MAR vs. SWH
- **Bullet Points**:
  - **Strict Hydrogeological Separation**:
    - *Surface Water Harvesting (SWH)*: Requires impermeable clay vertisols ($\ge 380\text{ g/kg}$) to prevent foundation seepage in unlined earthen structures (check dams, nala bunds).
    - *Managed Aquifer Recharge (MAR)*: Requires uncommitted storage, active depletion, and permeable soils (or subsurface recharge shafts to bypass clay).
  - **Tier 1 ($N = 76$) Category Breakdown**:
    - **MAR Category A (12 Basins)**: Active depletion ($\beta > 0$) + permeable sandy loam.
    - **MAR Category C (56 Basins)**: High priority, but heavy clay vertisols $\implies$ **Requires subsurface recharge shafts / borewells**.
    - **MAR Category D (8 Basins)**: Recovering water table ($\beta \le 0$).
    - **SWH Category A (75 Basins)**: Favorable surface runoff & clay retention.
    - **Category B (0 Basins)**: Strictly unassigned (MRSAC inventory protected).
- **Suggested Visual**:
  - `[Existing Figure]`: MAR vs. SWH decision tree diagram from Section 8 of `README.md`.
- **Speaker Notes**:
  > *"We strictly separated MAR and SWH. Out of 76 Tier 1 basins, 75 qualify for surface runoff harvesting, but only 12 qualify for conventional surface percolation tanks. The other 56 basins have heavy clay vertisols and are flagged for subsurface recharge shafts."*

---

### Slide 9: Interactive Decision Support Dashboard
- **Bullet Points**:
  - **Production Architecture (`app.py`)**:
    - Built using Streamlit, Plotly WebGL, GeoPandas, and Folium Leaflet.
    - Five synchronized operational views with persistent multi-criteria filtering.
  - **Dual Map Rendering Engine**:
    - *Plotly Vector Choropleth*: High-performance thematic rendering by Tiers, MAR, SWH, or Trends.
    - *Folium OpenStreetMap Leaflet*: Real-world satellite & road base tiles with interactive Catchment Quick-Inspection panel.
  - **Catchment Profiler & Comparison**:
    - Deep-dive diagnostic cards, scenario radar charts, well stats, and side-by-side trade-off matrix.
- **Suggested Visual**:
  - `[Dashboard Capture Required]`: Dual Map Engine screenshot and Catchment Profiler for basin `4081076330`.
- **Speaker Notes**:
  > *"Our Streamlit dashboard provides water planning authorities with an intuitive operational interface, featuring high-speed vector choropleths and interactive Leaflet GIS maps with full inspection capabilities."*

---

### Slide 10: Automated DPR Screening Dossiers
- **Bullet Points**:
  - **Deterministic Generation Engine**:
    - Script `scripts/generate_dpr_screening_sheets.py` generates 87 standardized preliminary DPR dossiers.
    - 12 MAR Category A screening sheets + 75 SWH Category A screening sheets.
  - **Zero Fabrication Invariant**:
    - 0 hallucinated IDs, 0 invented budgets (no ₹/INR figures), 0 fabricated coordinates.
  - **Mandatory 5-Point Pre-Construction Checklist**:
    1. Vertical Electrical Sounding (VES) resistivity profiling.
    2. Double-ring infiltrometer testing.
    3. Private commercial borewell census within 1.5 km.
    4. Structure siltation audit (prioritize desilting if $>40\%$).
    5. Baseline water quality testing (EC & nitrate).
- **Suggested Visual**:
  - `[Existing Figure]`: Screenshot or excerpt of `reports/dpr_screening_sheets/DPR_SCREENING_TEMPLATE.md`.
- **Speaker Notes**:
  > *"Our automated engine produces reproducible, standardized screening sheets. Every sheet enforces our mandatory 5-point field checklist, ensuring engineers conduct resistivity soundings and well censuses before sanctioning funds."*

---

### Slide 11: Scientific Invariants, Limitations & Future Work
- **Bullet Points**:
  - **Enforced Scientific Invariants**:
    - Cryptographic baseline immutability (all 4 baseline SHA-256 hashes verified bit-for-bit).
    - Unrecorded digital inventory $\ne$ zero physical structures (Category B unassigned).
    - 52 automated tests passing with zero failures.
  - **Known Limitations**:
    - Macro-scale screening (~600 km² basins) requires micro-watershed site lineament mapping.
    - MRSAC Jalyukt Shivar GIS layers remain protected behind state intranet credentials.
  - **Future Research Directions**:
    - Institutional API ingestion for structure-density saturation modeling.
    - High-resolution ALOS PALSAR 12.5m DEM ingestion for Topographic Wetness Index (TWI).
    - Pan-India scaling across HydroSHEDS Asia network.
- **Suggested Visual**:
  - `[Existing Figure]`: Baseline hash verification table and pytest summary output.
- **Speaker Notes**:
  > *"JalDrishti-AI prioritizes scientific honesty over false precision. All baselines are cryptographically verified, and our explicit disclaimers prevent macro-screening from being mistaken for civil engineering designs. Thank you."*