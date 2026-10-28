# JalDrishti-AI: Independent Validation Data Acquisition & Protocol Plan

**Document ID**: `12_INDEPENDENT_VALIDATION_DATA_PLAN.md`  
**Date**: October 27, 2026  
**Target Coverage**: 518 HydroATLAS Level 8 Catchments, Maharashtra  
**Author**: JalDrishti-AI Data Science & Geospatial Engineering Team  

---

> [!IMPORTANT]
> **Independent Data Inventory Status: Datasets Currently Absent From Workspace**  
> An exhaustive audit of the workspace (`data/raw/`, `data/interim/`, `data/processed/`, and `outputs/`) confirms that **no verified external ground-truth observations** (CGWB monitoring wells, MRSAC structure GIS shapefiles, or official tanker deployment registries) are currently present.  
> In accordance with scientific ethics and user guidelines, **no synthetic or fabricated validation data have been created, and no unverified performance metrics are claimed**. This document establishes the complete, production-ready data schemas, acquisition channels, spatial join specifications, and statistical evaluation protocols required to execute independent empirical validation upon dataset acquisition.

---

## 1. Required External Datasets & Schema Specifications

```
                                  INDEPENDENT VALIDATION STREAMS
                                                │
         ┌──────────────────────────────────────┼──────────────────────────────────────┐
         │                                      │                                      │
         ▼                                      ▼                                      ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ Stream A: Hydrogeological       │ │ Stream B: Intervention          │ │ Stream C: Socio-Economic        │
│ Groundwater Dynamics            │ │ Infrastructure Inventory        │ │ Water Scarcity Records          │
│ (CGWB & GSDA Monitoring Wells)  │ │ (MRSAC Jalyukt Shivar GIS)      │ │ (State Tanker Deployment Logs)  │
└─────────────────────────────────┘ └─────────────────────────────────┘ └─────────────────────────────────┘
```

---

### Stream A: Groundwater Level Observations (Subsurface Outcome)

#### 1. Data Sources & Institutional Access
- **Primary Institutional Source**: Central Ground Water Board (CGWB), Ministry of Jal Shakti, Government of India.
- **State Collaborative Source**: Groundwater Surveys and Development Agency (GSDA), Water Supply and Sanitation Department, Maharashtra.
- **Public Data Portal**: India-WRIS / National Water Informatics Centre (NWIC) (`https://indiawris.gov.in/wris/`) and GSDA Maharashtra Portal.
- **Monitoring Network Density**: Approximately 1,820 CGWB National Hydrograph Network (NHN) monitoring stations and >3,500 GSDA observation dugwells/piezometers across Maharashtra.

#### 2. Required Fields & Schema Specification

| Field Name | Data Type | Units / Format | Description & Standards |
| :--- | :--- | :--- | :--- |
| `station_id` | String | Alphanumeric (e.g. `CGWB_MH_PUN_012`) | Unique national hydrograph station identifier. |
| `station_name` | String | Text | Location village / town name. |
| `district` | String | Text | Administrative district name (standardized to 36 districts). |
| `taluka` | String | Text | Administrative sub-district name. |
| `latitude` | Float | Decimal Degrees (WGS84, `EPSG:4326`) | Geodetic latitude (verified $\in [15.6, 22.1]$). |
| `longitude` | Float | Decimal Degrees (WGS84, `EPSG:4326`) | Geodetic longitude (verified $\in [72.6, 80.9]$). |
| `well_type` | Categorical | `Dugwell`, `Borewell`, `Piezometer` | Well construction type. Piezometers isolate specific aquifer zones; dugwells tap unconfined phreatic aquifers. |
| `aquifer_type` | Categorical | `Basalt_Vesicular`, `Basalt_Fractured`, `Alluvium`, `Sedimentary` | Hydrogeological formation. Essential for interpreting yield and storage coefficient ($S$). |
| `observation_year` | Integer | YYYY (e.g. 2015–2024) | Calendar year of record. Minimum 10-year continuous series required. |
| `pre_monsoon_wl_mbgl` | Float | Meters below ground level ($mbgl$) | Water level depth measured in **May/June** (annual lowest water table). |
| `post_monsoon_wl_mbgl` | Float | Meters below ground level ($mbgl$) | Water level depth measured in **November** (annual peak post-recharge table). |
| `measurement_qc_flag` | Categorical | `Valid`, `Dry_Well`, `Pumping_Affected`, `Destroyed` | Rigorous quality flag. Pumping-affected or dry well records must be handled separately. |

#### 3. Mathematical Derivation: Depth vs. Level Change
A common error is conflating static groundwater depth with dynamic recharge. The protocol mandates two derived variables:

1. **Annual Seasonal Fluctuation ($\Delta h$)**:
   $$\Delta h_t = \text{pre\_monsoon\_wl\_mbgl}_t - \text{post\_monsoon\_wl\_mbgl}_t$$
   *(Note: Because measurements are in meters below ground level, a decrease in $mbgl$ represents a rise in water table elevation; $\Delta h > 0$ indicates net seasonal recharge).*

2. **Decadal Groundwater Trend ($\beta_{\text{trend}}$)**:
   Computed via non-parametric **Theil-Sen slope estimator** across 10 years of May pre-monsoon water levels:
   $$\beta_{\text{trend}} = \text{median}\left( \frac{h_j - h_i}{j - i} \right) \quad \forall i < j$$
   $\beta_{\text{trend}} > 0$ signifies declining water tables ($mbgl$ increasing year-on-year); $\beta_{\text{trend}} < 0$ indicates recovering aquifers.

---

### Stream B: Existing Water-Conservation Structures (Intervention Inventory)

#### 1. Data Sources & Institutional Access
- **Primary Source**: Maharashtra Remote Sensing Application Centre (MRSAC), Nagpur (`https://mrsac.gov.in`).
- **Program Repositories**:
  - *Jalyukt Shivar Abhiyan (JSA)* GIS Geo-database (Department of Soil and Water Conservation, Govt. of Maharashtra).
  - *Gal Mukt Dharan, Gal Yukt Shivar* (Reservoir De-silting) monitoring database.
  - Minor Irrigation (Local Sector) GIS inventories from Zilla Parishad water conservation wings.

#### 2. Required Fields & Schema Specification

| Field Name | Data Type | Units / Format | Description & Verification Standard |
| :--- | :--- | :--- | :--- |
| `structure_id` | String | Unique Code (e.g. `JSA_2016_142095`) | Unique state intervention registry identifier. |
| `structure_type` | Categorical | Standardized classification | `Check_Dam_Masonry`, `Cement_Nala_Bund`, `Earthen_Gully_Plug`, `Percolation_Tank`, `Continuous_Contour_Trench`, `Farm_Pond`. |
| `latitude` | Float | Decimal Degrees (`EPSG:4326`) | Geotagged coordinates captured via state mobile survey app. |
| `longitude` | Float | Decimal Degrees (`EPSG:4326`) | Geotagged coordinates. |
| `village_code` | Integer | Census 2011 Village Code | Used for cross-verification with `vlcode` and `area_id`. |
| `construction_year` | Integer | YYYY (e.g. 2015–2023) | Year of project completion. Essential for temporal alignment with satellite LULC. |
| `gross_storage_capacity_m3` | Float | Cubic meters ($m^3$) | Designed impoundment capacity behind the structure. |
| `operational_status` | Categorical | `Functional`, `Silted`, `Breached`, `Dry` | Field physical condition. Silted or breached structures provide diminished active storage. |

#### 3. Catchment Storage Saturation Calculation
For each of the 518 Level 8 catchments, aggregate the total existing storage volume:
$$V_{\text{existing}} = \sum_{k \in B_j} \text{gross\_storage\_capacity\_m3}_k \quad (m^3)$$
$$\text{Storage Density} = \frac{V_{\text{existing}}}{\text{basin\_geom\_area\_km2}} \quad (m^3/\text{km}^2)$$
*Engineering Role*: If a catchment has $\text{Storage Density} > 50,000\text{ m}^3/\text{km}^2$, its hydrologic yield is saturated; additional check dam construction would starve downstream water rights.

---

### Stream C: Water-Scarcity Evidence (Socio-Economic Stress)

#### 1. Data Sources & Institutional Access
- **Primary Source**: Water Supply and Sanitation Department, Government of Maharashtra (Emergency Drinking Water Tanker Management System).
- **Secondary Source**: Department of Relief and Rehabilitation (Official Scarcity / Drought Declarations under the Manual for Drought Management, 2020).

#### 2. Required Fields & Schema Specification

| Field Name | Data Type | Units / Format | Description & Standards |
| :--- | :--- | :--- | :--- |
| `record_id` | String | Unique ID | Transaction log code. |
| `district` | String | Text | District name. |
| `taluka` | String | Text | Taluka name. |
| `village_name` | String | Text | Affected village name. |
| `reporting_week` | Date | YYYY-MM-DD | Weekly reporting cycle during summer peak (March 1 to June 30). |
| `active_tankers_count` | Integer | Count | Number of government-deployed water tankers servicing the village. |
| `tanker_trips_weekly` | Integer | Trips/week | Total tanker delivery trips completed. |
| `scarcity_category` | Categorical | `Severe`, `Moderate`, `Normal` | State-notified drought declaration level. |

#### 3. Geographic Resolution & Potential Reporting Biases
- **Spatial Granularity**: Tanker deployment is recorded at village revenue level and compiled at taluka level.
- **Reporting Biases Addressed**:
  - *Political Influence Bias*: Certain talukas with vocal political leadership may secure higher tanker allocations despite moderate physical deficits.
  - *Infrastructure Masking*: Villages connected to functional regional rural water supply schemes (e.g. Jal Jeevan Mission piped networks) will NOT receive tankers even during severe meteorological droughts.
  - *Mitigation*: Use tanker deployment as a binary high-stress indicator (e.g. top decile of tanker trips) rather than a continuous linear proxy for physical deficit.

---

## 2. Spatial Join Protocol & Temporal Alignment Rules

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SPATIAL JOIN ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Point Shapefile / CSV]                  [Polygon Basin Layer]             │
│  CGWB Wells or JSA Structures             518 HydroATLAS Level 8 Basins     │
│  CRS: EPSG:4326                           CRS: EPSG:4326                    │
│             │                                           │                   │
│             └─────────────────────┬─────────────────────┘                   │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │  gpd.sjoin(points, basins,  │                          │
│                    │       how='inner',          │                          │
│                    │       predicate='within')   │                          │
│                    └──────────────┬──────────────┘                          │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │ Attach HYBAS_ID to Points   │                          │
│                    └──────────────┬──────────────┘                          │
│                                   ▼                                         │
│                    ┌─────────────────────────────┐                          │
│                    │ Groupby HYBAS_ID:           │                          │
│                    │ - Median Decadal Trend      │                          │
│                    │ - Total Storage Capacity    │                          │
│                    │ - Summed Tanker Trips       │                          │
│                    └─────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Protocol Guidelines:
1. **Coordinate Reference System (CRS)**: All incoming point datasets must be validated in `EPSG:4326` (WGS84) before spatial join. Basins are projected to UTM Zone 43N (`EPSG:32643`) whenever spatial distances or buffer radiuses are calculated.
2. **Temporal Alignment**:
   - Satellite indicators represent the **2001–2025 baseline**.
   - Groundwater trends must span the corresponding decadal window (**2015–2024**).
   - Validation must avoid evaluating 2024 MCDA priority scores against historical 2005 well data.
3. **Handling Wells on Catchment Boundaries**:
   - Monitoring wells falling within a 200-meter buffer of Level 8 catchment boundaries are assigned to the basin sharing its surface topological drainage direction, preventing boundary misclassification.

---

## 3. Evaluation Framework & Statistical Validation Metrics

To avoid claiming that correlation alone proves predictive validity or relying on arbitrary p-values, the evaluation protocol establishes **three formal statistical tests**:

### Test 1: Groundwater Depletion Concordance (Continuous Validation)
- **Hypothesis**: Catchments assigned high priority in the Managed Aquifer Recharge (MAR) scenario should correlate with observed historical groundwater depletion rates.
- **Statistical Model**: Weighted Least Squares (WLS) regression of `score_S4_MAR` on 10-year median groundwater decline rate $\beta_{\text{trend}}$, weighted by the number of observation wells per basin ($n_w$):
  $$\beta_{\text{trend}, i} = \alpha + \gamma \cdot \text{score\_S4\_MAR}_i + \epsilon_i$$
- **Reporting Metrics**: Spearman rank correlation $\rho$, $R^2$, and $95\%$ bootstrap confidence intervals.

### Test 2: Emergency Tanker Scarcity Discrimination (Binary Classification)
- **Hypothesis**: Catchments in Consensus Tier 1 should discriminate between communities requiring emergency summer drinking water tankers versus water-secure communities.
- **Statistical Model**: Receiver Operating Characteristic (ROC) analysis treating basins in the top 20th percentile of tanker deployment as the ground-truth scarcity class ($Y_i = 1$).
- **Reporting Metrics**: Area Under the Curve (ROC-AUC) with DeLong's variance test, Precision-Recall AUC (PR-AUC), sensitivity at $80\%$ specificity. A model achieving $\text{AUC} > 0.75$ with tight confidence intervals provides empirical validation.

### Test 3: Existing Infrastructure Saturation Check (Residual Opportunity)
- **Analysis**: Cross-tabulation of MCDA priority tiers against existing structure density ($m^3/\text{km}^2$).
- **Goal**: Segregate Tier 1 catchments into:
  - *Tier 1A (Unmet Opportunity)*: High priority score AND low existing structure density (prime target for immediate capital allocation).
  - *Tier 1B (Saturated / Maintenance)*: High priority score BUT high existing structure density (target for de-silting and repair of existing assets, NOT new dam construction).

---

## 4. Ready-to-Run Validation Script Template

A structured template script [`scripts/validate_independent_evidence.py`](file:///c:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/scripts/validate_independent_evidence.py) is documented below, ready to execute as soon as official CGWB or MRSAC files are deposited into `data/raw/`:

```python
# JalDrishti-AI: Independent Evidence Validation Pipeline
# Ingests external CGWB well observations and MRSAC structures to validate MCDA rankings
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score

def validate_external_evidence(cgwb_csv_path, structures_shp_path, mcda_audit_csv_path):
    print("Loading MCDA consensus audit table...")
    df_mcda = pd.read_csv(mcda_audit_csv_path)
    
    # 1. Validate Groundwater Observations
    if cgwb_csv_path.exists():
        df_wells = pd.read_csv(cgwb_csv_path)
        gdf_wells = gpd.GeoDataFrame(df_wells, geometry=gpd.points_from_xy(df_wells.longitude, df_wells.latitude), crs="EPSG:4326")
        
        # Spatial join with 518 catchments
        gdf_basins = gpd.read_file("data/processed/jaldrishti_scored_watersheds.shp")
        joined_wells = gpd.sjoin(gdf_wells, gdf_basins[["HYBAS_ID", "geometry"]], how="inner", predicate="within")
        
        # Aggregate median decline per basin
        basin_gw = joined_wells.groupby("HYBAS_ID")["decadal_trend_m_yr"].median().reset_index()
        eval_df = df_mcda.merge(basin_gw, on="HYBAS_ID", how="inner")
        
        rho, pval = spearmanr(eval_df["score_S4_Managed_Aquifer_Recharge"], eval_df["decadal_trend_m_yr"])
        print(f"Groundwater Validation (N={len(eval_df)} basins): Spearman rho = {rho:.4f} (p-value = {pval:.4e})")
    else:
        print("[NOTICE] External CGWB well observations file not found. Skipping empirical groundwater test.")

if __name__ == "__main__":
    print("Independent Validation Pipeline Ready for Ingestion.")
```
