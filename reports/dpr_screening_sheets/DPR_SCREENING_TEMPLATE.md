# JalDrishti-AI: Reusable Preliminary DPR Screening Template
## Watershed Conservation Infrastructure Feasibility Dossier

> **STATUTORY PLANNING & LEGAL DISCLAIMER**:  
> *This template is designed for macro-screening feasibility assessment in the JalDrishti-AI decision support system. It serves to structure preliminary desk evaluations and target sub-basins for field hydrogeological investigation. It does NOT constitute an approved Detailed Project Report (DPR), administrative expenditure sanction, or civil engineering specification. Site-specific Vertical Electrical Sounding (VES), infiltration rate testing, hydraulic spillway modeling, and structural condition audits are legally mandatory prior to fund sanction or civil construction.*

---

### 1. Catchment Identity & Administrative Context
- **HydroATLAS Level 8 Basin ID**: `{{HYBAS_ID}}`
- **Sub-Catchment Drainage Area**: `{{SUB_AREA_KM2}} km²`
- **Intersecting Villages**: `{{VILLAGE_COUNT}} villages` (`{{VILLAGE_COVERAGE_PCT}}%` boundary area coverage, Flag: `{{VILLAGE_COVERAGE_FLAG}}`)
- **Consensus Prioritization Tier**: `{{CONSENSUS_PRIORITY_TIER}}`
- **Preliminary 2-Variable Screening Score**: `{{PRELIMINARY_SCREENING_SCORE}}`
- **Robust Consensus Rank**: `{{MEDIAN_PLANNING_RANK}} / 518` (Median Planning Rank across all scenarios)
- **Target Scenario Priority Score**: `{{SCENARIO_SCORE}}` (Rank: `#{{SCENARIO_RANK}}`)

---

### 2. Multi-Evidence Ground-Truth Observational Status
- **Active Monitoring Stations**: `{{TOTAL_WELL_COUNT}} wells` (CGWB: `{{CGWB_WELL_COUNT}}`, GSDA: `{{GSDA_WELL_COUNT}}`)
- **Decadal Groundwater Depth Trend (2015–2024)**: **`{{GW_DEPTH_TREND_M_YR}}`**
  - *Mathematical Sign Interpretation*: Depth below ground level (m bgl). Positive slope ($\beta > 0$) = increasing depth = secular water-table depletion. Negative slope ($\beta < 0$) = decreasing depth = water-table recovery.
- **Median Seasonal Water Table Fluctuation ($\Delta h$)**: `{{SEASONAL_RECHARGE_DELTA_H_M}}`
- **Evidence Confidence Level**: `{{EVIDENCE_CONFIDENCE_LEVEL}}`
- **Hydrogeological Interpretation**: `{{HYDROGEOLOGICAL_INTERPRETATION}}`

---

### 3. Soil, Topography & Physical Parameters
- **Topsoil Texture (0–5cm)**:
  - Clay Content: `{{CLAY_G_KG}} g/kg` (`{{CLAY_PCT}}%`)
  - Sand Content: `{{SAND_G_KG}} g/kg` (`{{SAND_PCT}}%`)
  - Silt Content: `{{SILT_G_KG}} g/kg`
  - Soil Organic Carbon: `{{SOC_DG_KG}} dg/kg`
- **Infiltration Capacity Proxy**: `{{INFILTRATION_CAPACITY_CM_HR}} cm/hr`
- **Terrain Topography**: Mean Slope: `{{MEAN_SLOPE_DEG}}°`, Mean Elevation: `{{MEAN_ELEVATION_M}} m amsl`
- **Climate & Rainfall Baseline**: Annual Precipitation: `{{MEAN_PRECIP_MM_YR}} mm/year`, Historical Drought Frequency: `{{DROUGHT_FREQUENCY_PCT}}%` (`{{DROUGHT_YEARS_COUNT}} severe drought years in 2001–2025`)
- **Agricultural Land Use**: Cropland Fraction: `{{CROPLAND_PCT}}%` of catchment area

---

### 4. Provisional Engineering Screening Assessment
- **Intervention Type**: `{{INTERVENTION_TYPE}}` (Managed Aquifer Recharge / Surface Water Harvesting)
- **Screening Classification**: **`{{PROVISIONAL_ACTION_CATEGORY}}`**
- **Decision Engine Rationale**: `{{DECISION_RATIONALE}}`
- **Recommended Primary Technology**:
  - *For MAR in Sandy/Loam Soils*: Surface Percolation Tanks, Check Dams with Recharge Pits, Loose Boulder Gully Plugs.
  - *For MAR in Heavy Clay Vertisols*: Subsurface Recharge Shafts or Dedicated Recharge Borewells penetrating through dense clay cap into underlying fractured basalt.
  - *For SWH in Heavy Clay Vertisols*: Earthen Nala Bunds, Cement Nala Bunds (CNBs), Unlined Farm Ponds (low seepage risk).
  - *For SWH in Coarse/Permeable Soils*: Check dams with masonry core walls, lined farm ponds with polythene or clay puddling.

---

### 5. Existing Conservation Infrastructure Status (MRSAC Audit)
- **Centralized Digital Inventory**: **`{{INVENTORY_STATUS}}`**
- **Inventory Confidence**: `{{INVENTORY_CONFIDENCE}}`
- **Statutory Policy Invariant**: `{{INVENTORY_DATA_POLICY}}`
- *Mandatory Planning Rule*: Centralized MRSAC GIS structure records are currently restricted behind state departmental credentials. **An unrecorded digital inventory must NEVER be interpreted as the physical absence of water conservation infrastructure on the ground.** A local physical survey must catalog all existing check dams, percolation tanks, and nala bunds in the micro-catchment before finalizing new structure locations.

---

### 6. Mandatory Pre-Construction Field Checklist
Prior to finalizing any DPR for Catchment `{{HYBAS_ID}}`, the investigating engineer and hydrogeologist must complete and sign:
1. [ ] **Geophysical Resistivity Profiling**: Minimum 3 Vertical Electrical Soundings (VES) along suspected joint/fracture lineaments to confirm fractured basalt thickness and aquifer geometry.
2. [ ] **Double-Ring Infiltrometer Tests**: In situ infiltration rate measurement across proposed percolation tank beds.
3. [ ] **Local Well Census**: Spatial inventory of existing agricultural dugwells and borewells within a 1.5 km radius to prevent capture by private commercial irrigators.
4. [ ] **Catchment Hydrological Yield & Spillway Modeling**: Strange's table / SCS-CN runoff estimation for a 75% dependable rainfall year, and waste weir sizing using Dicken's formula with adequate freeboard.
5. [ ] **Physical Structure Siltation & Damage Audit**: Field inspection of existing structures within the stream reach. Where siltation exceeds 40%, prioritize desilting and repair over new civil construction.
6. [ ] **Baseline Water Quality Testing**: Pre-monsoon electrical conductivity (EC), fluoride, and nitrate testing to ensure recharge water does not contaminate drinking water aquifers.
7. [ ] **Downstream Riparian Rights & Ecological Baseflow**: Verification that upstream storage will not starve downstream irrigation schemes or ecological reserve flows.
