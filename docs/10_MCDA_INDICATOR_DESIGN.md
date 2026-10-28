# JalDrishti-AI: Four-Pillar Multi-Criteria Decision Analysis (MCDA) Indicator Design

> [!IMPORTANT]
> **Design Framework Status: Candidate Architecture — Not a Validated Engineering Score**  
> This document formalizes the candidate indicator design, physical rationale, normalisation methods, and multi-criteria weighting architecture for Maharashtra watershed prioritization. It explicitly outlines physical limitations, collinearities, and unobserved variables (e.g., fractured basalt hydrogeology, groundwater draft). In accordance with engineering rigor, **no final MCDA score is presented or labeled as validated**; field validation against Central Ground Water Board (CGWB) observation wells and ground-truth intervention inventories remains a prerequisite for operational deployment.

---

## 1. Executive Summary & Conceptual Architecture

The JalDrishti-AI framework transitions beyond the preliminary 2-indicator screening proxy (`0.5 * slope + 0.5 * low rainfall`) to a multi-dimensional **Four-Pillar Decision Support Framework** structured around the physical and socio-ecological drivers of watershed vulnerability and water harvesting feasibility:

```
                              ┌──────────────────────────────────────────────┐
                              │    JalDrishti-AI Four-Pillar MCDA Design     │
                              └──────────────────────┬───────────────────────┘
                                                     │
         ┌───────────────────┬───────────────────────┴───────────────────────┬───────────────────┐
         │                   │                                               │                   │
         ▼                   ▼                                               ▼                   ▼
┌─────────────────┐ ┌─────────────────┐                             ┌─────────────────┐ ┌─────────────────┐
│  Pillar 1:      │ │  Pillar 2:      │                             │  Pillar 3:      │ │  Pillar 4:      │
│  Climate Stress │ │  Agricultural   │                             │  Topographic    │ │  Infiltration   │
│  & Rainfall     │ │  Demand & Land  │                             │  Runoff &       │ │  Potential &    │
│  Deficit        │ │  Pressure       │                             │  Drainage       │ │  Soil Storage   │
└─────────────────┘ └─────────────────┘                             └─────────────────┘ └─────────────────┘
```

The four pillars aggregate multi-scale Earth Observation datasets (CHIRPS precipitation, ESA WorldCover, SRTM topography, ISRIC SoilGrids, and HydroATLAS catchments) across **44,468 villages** onto **518 HydroATLAS Level 8 catchments**.

---

## 2. Comprehensive Indicator Matrix

Every candidate indicator is documented below with its formal definition, primary data source, physical units, decision direction, missingness rate across Maharashtra catchments, normalisation formula, weighting rationale, and scientific limitations.

| Pillar | Candidate Indicator | Field Name | Source | Units | Direction | Missingness | Normalisation | Weighting Rationale | Scientific Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Climate Stress** | **Baseline Mean Annual Rainfall** | `village_rainfall_baseline_mean_mm` | CHIRPS / IMD (2001–2020) | mm/year | **Cost (-)** | 0.0% (1 transboundary) | Min-Max (Cost) | Chronic rainfall deficits create acute groundwater dependence and drought vulnerability. | Gridded satellite rainfall (0.05°) smooths localized convective cloudbursts. |
| | **Rainfall Inter-Annual CV** | `village_rainfall_cv_pct` | CHIRPS 25-yr time series | % | **Benefit (+)** | 0.0% (1 transboundary) | Min-Max (Benefit) | Higher inter-annual variability indicates erratic monsoon regimes prone to severe failure. | Does not capture intra-seasonal dry spells (breaks in monsoon) within a single agricultural season. |
| | **Empirical Drought Frequency** | `village_drought_years_count` | 25-yr annual records (<75% mean) | Count (0–25) | **Benefit (+)** | 0.0% (1 transboundary) | Min-Max (Benefit) | Direct historical frequency of meteorological drought episodes over a 25-year baseline. | Threshold (<75%) represents meteorological drought; agricultural/hydrological drought lags rainfall. |
| | **Recent Rainfall Anomaly (2025)** | `village_rainfall_anomaly_2025_pct` | CHIRPS 2025 vs baseline | % | **Cost (-)** | 0.0% (1 transboundary) | Min-Max (Cost) | Negative recent anomaly captures immediate, acute water stress entering the subsequent rabi season. | Single-year snapshot; sensitive to late-monsoon post-withdrawal storms. |
| **2. Agricultural Demand** | **Cropland Area Fraction** | `village_cropland_pct` | ESA WorldCover 2021 (10m) | % of area | **Benefit (+)** | 0.0% (1 transboundary) | Min-Max (Benefit) | Cropland density is the primary proxy for consumptive crop evapotranspiration and irrigation draft. | Does not distinguish between water-intensive sugarcane/banana versus rainfed millets/pulses. |
| | **Natural Vegetation Buffer** | `village_natural_veg_pct` | ESA WorldCover (Tree+Shrub+Grass) | % of area | **Cost (-)** | 0.0% (1 transboundary) | Min-Max (Cost) | Catchments lacking forest/grassland sponges have lower soil moisture retention and higher erosion risk. | Does not account for canopy density or forest degradation stage. |
| | **Settlement & Built-up Pressure** | `village_built_up_pct` | ESA WorldCover 2021 | % of area | **Benefit (+)** | 0.0% (1 transboundary) | Min-Max (Benefit) | Higher impervious fraction accelerates surface runoff and concentrates domestic water demand. | Rural village settlements occupy small areal percentages (<5% in most rural basins). |
| **3. Topographic Runoff** | **Catchment Mean Slope** | `village_slope_mean_deg` | SRTM 30m v2 (GEE) | Degrees | **Benefit (+)** | 0.0% (1 transboundary) | Min-Max (Benefit) | Steeper terrain generates hydraulic gradient and kinetic energy for surface runoff. | High slope increases runoff velocity but reduces infiltration time; extreme slopes (>20°) cause structure failure. |
| | **Natural Runoff Depth** | `run_mm_syr` | HydroATLAS / Composite Runoff | mm/year | **Benefit (+)** | 0.0% (0 transboundary) | Min-Max (Benefit) | Direct volumetric estimate of annual surface runoff available for harvesting. | Modeled global water balance; does not reflect local farm bunds, check dams, or micro-storage already built. |
| | **Catchment Mean Elevation** | `village_elevation_mean_m` | SRTM 30m v2 (GEE) | Meters | **Contextual** | 0.0% (1 transboundary) | Min-Max (Benefit) | Headwater ridge catchments act as regional recharge sources feeding valley aquifers. | Elevation alone does not determine water yield without precipitation coupling. |
| **4. Infiltration Potential** | **Topsoil Clay Content** | `village_clay_0_5cm_g_kg` | ISRIC SoilGrids 250m v2 | g/kg | **Benefit (+)** *(surface)* / **Cost (-)** *(recharge)* | 0.19% (1 transboundary) | Min-Max | High clay soils (Vertisols) are ideal for surface retention structures (ponds, check dams) due to low seepage. | Clay retards groundwater percolation; vertisols shrink-swell, creating deep summer cracks but swelling shut when wet. |
| | **Topsoil Sand Content** | `village_sand_0_5cm_g_kg` | ISRIC SoilGrids 250m v2 | g/kg | **Cost (-)** *(surface)* / **Benefit (+)** *(recharge)* | 0.19% (1 transboundary) | Min-Max | High sand causes seepage loss in unlined farm ponds, but enables rapid recharge in percolation tanks. | Pure sands are rare in Maharashtra's basalt plateau; primarily confined to Konkan coastal bars and river channels. |
| | **Soil Organic Carbon (SOC)** | `village_soc_0_5cm_dg_kg` | ISRIC SoilGrids 250m v2 | dg/kg (0.1%) | **Benefit (+)** | 0.19% (1 transboundary) | Min-Max (Benefit) | Organic matter enhances aggregate stability, macro-porosity, and soil available water capacity (AWC). | Reflects topsoil (0–5cm) conditions; subsurface vadose zone geology may govern deep recharge. |
| | **Infiltration Capacity Proxy** | `village_infiltration_proxy` | Derived: $(Sand + 0.5 \cdot Silt)/(Clay + 1)$ | Ratio | **Dual** | 0.19% (1 transboundary) | Min-Max | Captures hydraulic texture grading: higher values indicate permeable textures; lower values indicate heavy clays. | Empirical texture proxy; does not measure saturated hydraulic conductivity ($K_{sat}$) in situ. |

---

## 3. Physical Limitations & Hydrogeological Realities

### 3.1 Why Slope Alone Does Not Measure Runoff
In preliminary screening, slope was used as a direct surrogate for runoff. However, hydrology dictates that:
1. **SCS-CN Runoff Dynamics**: Surface runoff is governed by the USDA-SCS Curve Number ($CN$), which depends non-linearly on soil hydrologic group, land use, conservation treatment, and Antecedent Moisture Condition ($AMC$). A 10° slope under dense deciduous forest generates significantly less runoff than a 2° slope over crusted black soil with intense rainfall.
2. **Rainfall Intensity vs. Infiltration Capacity**: Runoff generation in semi-arid Maharashtra is predominantly **Horton overland flow** (rainfall intensity exceeding infiltration rate) during short convective storms, or **Dunne saturation overland flow** in valley bottoms. A gentle slope with high-intensity precipitation can yield extreme runoff.
3. **Storage Structures Engineering Constraints**: Extremely steep slopes (>15°–20°) are unsuitable for standard masonry check dams, earthen nala bunds, or farm ponds due to high scour risk, siltation rates, and excessive dam wall heights. Optimum slopes for rainwater harvesting structures generally lie in the **1° to 5° (gentle to rolling)** range.

### 3.2 Why Soil Texture Alone Does Not Determine Infiltration Capacity
1. **Deccan Trap Basalt Hydrogeology**: Over 85% of Maharashtra is underlain by the Deccan Volcanic Province (Deccan Traps)—layered basaltic lava flows. Infiltration from surface ponds into regional aquifers is governed by **secondary porosity** (vesicular flow tops, columnar joints, tectonic fractures, and weathering depth of murrum layers), not merely the top 5cm of soil texture.
2. **Vertisol (Black Cotton Soil) Behavior**: Maharashtra's dominant soils are deep to medium black vertisols (smectite/montmorillonite clays). During the dry season, they develop deep shrinkage cracks (promoting bypass/macropore flow upon the first rains). Once saturated, the clays expand, reducing hydraulic conductivity to near zero and promoting high surface runoff.
3. **Caliche and Hardpan Horizons**: Subsurface calcic or silica-cemented hardpans at 30–90cm depth can completely arrest percolation regardless of topsoil texture.

---

## 4. Missing Evidence & Unobserved Variables

To advance from an indicative screening model to a defensible civil engineering planning tool, the following missing datasets should be integrated in future phases:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CRITICAL UNOBSERVED VARIABLES                         │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Variable / Dataset             │ Impact on Priority Model                   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ CGWB Observation Well Trends   │ Direct measurement of groundwater decline  │
│ (Pre- vs Post-Monsoon water table) │ and over-exploited assessment units (OE).   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Crop-Specific Water Footprints │ Distinguishes sugarcane (2,000 mm draft)   │
│ (e.g. Remote Sensing crop maps)│ from rainfed soybean or sorghum (400 mm).  │
├────────────────────────────────┼────────────────────────────────────────────┤
│ Existing Intervention Inventory│ Accounting for thousands of existing check │
│ (Jalyukt Shivar, farm ponds)   │ dams, preventing over-allocation of budget.│
├────────────────────────────────┼────────────────────────────────────────────┤
│ Hydrogeological Aquifer Map    │ Aquifer yield, transmissivity, and depth to │
│ (CGWB / GSDA 1:50,000 mapping) │ massive un-weathered trap rock.           │
└────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 5. Potential Indicator Correlations & Redundancies

Multivariate collinearity must be evaluated before applying additive weighting models:
- **Elevation and Rainfall**: Strong orographic correlation ($r \approx 0.60–0.75$) along the Western Ghats (high elevation catchments receive >3,000 mm, while plateau catchments receive <600 mm). Combining both as independent benefits or costs can double-count regional topography.
- **Clay, Sand, and Infiltration Proxy**: Because SoilGrids texture fractions sum to 1000 g/kg ($\text{sand} + \text{clay} + \text{silt} = 1000$), clay and sand are inherently negatively correlated ($r = -0.72$ in Maharashtra). Including both requires careful directional alignment or using a single composite soil index.
- **Runoff Depth and Rainfall**: Runoff depth (`run_mm_syr`) is derived from rainfall and evapotranspiration models ($r > 0.85$ with `pre_mm_syr`). In drought-focused weighting, runoff depth and rainfall deficit represent competing objectives (water harvesting potential vs water scarcity need).

---

## 6. Proposed Multi-Criteria Weighting Paradigms

Rather than imposing a single arbitrary set of weights, the design establishes three benchmarking schemes:

### Scheme A: Equal Weighting (Reference Baseline)
- Pillar weights: 25% each across the four pillars.
- Indicator weights: Equal division within each pillar ($w_{ij} = 0.25 / k_p$).
- Serves as an un-biased neutral benchmark.

### Scheme B: Analytical Hierarchy Process (AHP - Domain Expert Model)
- Pairwise comparison matrix calibrated to state watershed guidelines:
  - Climate Stress: **35%** (primary trigger of crisis)
  - Agricultural Demand: **30%** (primary driver of depletion)
  - Topographic Runoff: **20%** (physical structure feasibility)
  - Infiltration Potential: **15%** (vadose retention capacity)
- Requires verification of Consistency Ratio ($CR < 0.10$).

### Scheme C: Shannon Entropy Weighting (Objective Data Dispersion)
- Measures the intrinsic contrast intensity (information entropy) of each indicator across the 518 basins:
  $$E_j = -\frac{1}{\ln(m)} \sum_{i=1}^m p_{ij} \ln(p_{ij})$$
- Indicators with high spatial contrast receive higher objective weights.

---

## 7. Directional Normalization Methodology

Every indicator $x_{ij}$ (catchment $i$, criterion $j$) is mapped to a dimensionless standard scale $r_{ij} \in [0, 1]$:

$$\text{Benefit Criteria (Higher is Priority):} \quad r_{ij} = \frac{x_{ij} - x_j^{\min}}{x_j^{\max} - x_j^{\min}}$$

$$\text{Cost Criteria (Lower is Priority):} \quad r_{ij} = \frac{x_j^{\max} - x_{ij}}{x_j^{\max} - x_j^{\min}}$$

Where extreme outliers exist (e.g. coastal rainfall $>3,500\text{ mm}$ or steep scarps $>35^\circ$), 1st and 99th percentile winsorisation is recommended prior to min-max scaling to prevent distortion of plateau catchments.

---

## 8. Summary & Next Steps for Stakeholder Review

1. **Stakeholder Alignment**: Present this indicator design to hydrologists and state decision-makers (GSDA / DoLR) to align on priority directions (e.g., surface storage vs. managed aquifer recharge).
2. **Sensitivity Testing**: Run comparative sensitivity analysis (Equal vs. AHP vs. Entropy) to assess rank stability.
3. **Groundwater Verification**: Integrate CGWB pre- and post-monsoon water table decline rates before certifying any composite score for field deployment.
