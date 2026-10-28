# JalDrishti-AI — Phase 7: Data Provenance, Reconciliation, and Monitoring Coverage

**Document ID**: `JD-DOC-15-PROVENANCE`  
**Phase**: Phase 7 — Multi-Evidence Triangulation and Infrastructure Saturation  
**Status**: Complete & Verified  
**Date**: October 2026  
**Scope**: 518 HydroATLAS Level 8 Catchments, Maharashtra, India  

---

## 1. Executive Summary

This document establishes the official data provenance, spatial reconciliation, and catchment-scale monitoring network coverage for the official groundwater datasets and conservation-structure layers integrated in Phase 7 of JalDrishti-AI. 

Phase 7 expands observational grounding from the Central Ground Water Board (CGWB) quarterly observation network (ingested in Phase 6) to include the Ground Water Surveys and Development Agency (GSDA), Government of Maharashtra, manual monitoring network (1970–2025). Combining both independent state and national monitoring networks expands Level 8 catchment coverage from **72.39% (375 catchments)** to **88.61% (459 catchments)** across Maharashtra.

Furthermore, this document records the formal access status of the Maharashtra Remote Sensing Applications Centre (MRSAC) Jalyukt Shivar Abhiyan conservation structure spatial layer, detailing the exact departmental access barriers encountered and enforcing the project's zero-fabrication integrity policy.

---

## 2. Official Dataset Provenance

### 2.1 GSDA Maharashtra Ground Water Level Dataset

| Attribute | Specification |
| :--- | :--- |
| **Dataset Title** | Ground Water Level Manual Quarterly Maharashtra (1970–2025) |
| **Originating Agency** | Ground Water Surveys and Development Agency (GSDA), Water Supply and Sanitation Department, Government of Maharashtra |
| **Data Portal / Publishing Host** | National Water Data Portal (NWDP) / India WRIS / Open Government Data (OGD) Platform India (`data.gov.in`) |
| **Source URL** | Official Government of Maharashtra Water Resources Repository / WRIS GWL Resource ID `GSDA-GWL-MH-1970-2025` |
| **Local Storage Path** | `data/raw/ground_water_level_manual_quarterly_maharashtra_1970_2025.csv` |
| **Byte Size** | `91,492,435 bytes` (~87.25 MB) |
| **Cryptographic Hash (SHA-256)** | `5003c9030b34df310f0bdd0527df022b9b0e73aa780b5bbacc88cc49d1be0eb6` |
| **File Format & Encoding** | CSV, ISO-8859-1 (`latin-1` / `cp1252`), comma-delimited |
| **Record Count (Raw)** | 636,605 observation records |
| **Temporal Coverage** | 1970–2025 (Phase 7 evaluation focus: 2015–2024 decadal window: 153,047 records across 4,158 stations) |
| **Geographic Coverage** | All 36 districts of Maharashtra |
| **Measurement Unit** | Meters Below Ground Level (m bgl) |
| **Data Licensing / Terms** | Government Open Data License - India (GODL) / Official Use for Water Resource Planning |

#### Raw Data Schema (GSDA)
The raw dataset comprises 20 official attributes:
1. `state` (Text): State name ("MAHARASHTRA")
2. `district` (Text): Revenue district name
3. `tahsil` / `taluka` (Text): Administrative sub-district
4. `block` (Text): Community development block
5. `village` (Text): Village name (contains localized phonetic transcriptions and Marathi text)
6. `latitude` (Float): Decimal degrees (WGS 84, EPSG:4326)
7. `longitude` (Float): Decimal degrees (WGS 84, EPSG:4326)
8. `site_type` (Text): Well construction type (`Dug Well`, `Bore Well`, `Piezometer`, `Tube Well`)
9. `agency_name` (Text): Monitoring agency identifier (`GSDA`)
10. `site_id` (Text): GSDA unique station code
11. `site_name` (Text): Station name description
12. `basin` (Text): River basin (Godavari, Krishna, Tapi, Narmada, West Flowing Rivers)
13. `sub_basin` (Text): Hydrological sub-basin
14. `water_year` (Text/Int): Hydrological year
15. `pre_monsoon` (Float): May water level (m bgl)
16. `monsoon` (Float): August water level (m bgl)
17. `post_monsoon_kharif` (Float): September/October post-monsoon water level (m bgl)
18. `post_monsoon_rabi` (Float): January winter water level (m bgl)
19. `trend_10yrs_pre` (Float): 10-year pre-monsoon decadal trend slope
20. `trend_10yrs_post` (Float): 10-year post-monsoon decadal trend slope

---

### 2.2 CGWB Maharashtra Ground Water Level Datasets (Preserved from Phase 6)

| Attribute | Part 1 (1991–2020) | Part 2 (2021–2025) |
| :--- | :--- | :--- |
| **Local Raw Path** | `data/raw/gwl_manual_quarterly_cgwb_mh_1991_2020.csv` | `data/raw/gwl_manual_quarterly_cgwb_mh_2021_2025.csv` |
| **Byte Size** | 13,975,547 bytes | 1,754,883 bytes |
| **SHA-256 Hash** | `ec97b2fa941cfca0fc5dae7b99c7ea0770cb5038c9fe7ba64c1b979a0cf5086b` | `3aaee546d1838ae6292b1a134a41315904d9b43aa9430ea4ca7e30d70eb0e6a3` |
| **Harmonized Output** | `data/raw/cgwb_maharashtra_observation_wells.csv` (43,752 records, 1,936 stations) |
| **Originating Agency** | Central Ground Water Board (CGWB), Department of Water Resources, RD & GR, Ministry of Jal Shakti |

---

### 2.3 MRSAC Jalyukt Shivar Spatial Inventory Status

| Attribute | Audit Finding |
| :--- | :--- |
| **Layer Name** | `mrsac_jalyukt_shivar_structures.shp` (or equivalent GeoPackage) |
| **Originating Agency** | Maharashtra Remote Sensing Applications Centre (MRSAC), Planning Department, GoM |
| **Web Portal** | `https://mrsac.maharashtra.gov.in/jalyukt/` |
| **Access Restriction** | **Restricted / Departmental Intranet Authentication Required** |
| **Public Download API** | None. Web interface requires internal government credentials; public access is limited to static tiled map visualizers without bulk attribute/geometry download endpoints. |
| **Physical File Check** | No shapefile, GeoPackage, or raw structure inventory exists in `data/raw/`. |
| **Anti-Fabrication Policy** | **Strictly enforced**. In accordance with scientific integrity standards, no structure locations, capacities, siltation levels, or condition states have been fabricated or synthesized. |
| **Catchment Accounting** | All 518 catchments are explicitly flagged with `inventory_status = "INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS"` and `designed_storage_capacity_m3 = 0.0`. |
| **Scientific Policy Mandate** | *An unrecorded or missing structure inventory must never be interpreted as the physical absence of water conservation infrastructure on the ground.* |

---

## 3. Station Reconciliation: CGWB vs. GSDA

To ensure that combining GSDA and CGWB data produces a coherent, scientifically rigorous monitoring evidence base, a reconciliation audit was performed:

### 3.1 Identifier Disjunction
- **CGWB Station IDs**: Format `W[Lat][Long][Sequence]` (e.g., `W203412078330001`), derived from Survey of India coordinate blocks.
- **GSDA Station IDs**: Format `MH[DistrictCode][WellSeq]` or local departmental codes.
- **Result**: Zero (0) exact string identifier matches exist between the two datasets. Inter-agency merging cannot rely on station keys.

### 3.2 Spatial Proximity and Colocation Audit
Pairwise Euclidean distance analysis between 1,936 CGWB stations and 4,090 GSDA stations with valid coordinates revealed:

| Distance Threshold | Number of Matched Pairs | Percentage of CGWB Wells | Interpretation |
| :--- | :--- | :--- | :--- |
| **$\le 100\text{ m}$** | 48 station pairs | 2.5% | Collocated observation wells (often twin monitoring piezometers or shared village well site) |
| **$101\text{ m} - 500\text{ m}$** | 252 station pairs | 13.0% | Same village / local settlement cluster |
| **$501\text{ m} - 1,000\text{ m}$** | 227 station pairs | 11.7% | Same micro-watershed / valley fill |
| **$> 1,000\text{ m}$** | 1,409 stations | 72.8% | **Completely independent observation locations**, providing genuine spatial coverage expansion |

### 3.3 Measurement Cross-Validation
For the 48 collocated station pairs ($\le 100\text{ m}$ separation) evaluated across simultaneous monthly observation windows ($N = 705$ observation pairs):

- **Pearson Correlation ($r$)**: `0.8123` ($p = 9.39 \times 10^{-167}$)
- **Spearman Rank Correlation ($\rho$)**: `0.8469` ($p = 5.23 \times 10^{-195}$)
- **Median Measurement Difference**: `0.00 m`
- **Mean Absolute Discrepancy**: `1.17 m`

```
  Observation Discrepancy Distribution (m bgl):
  Min: -4.80 m | Q1: -0.32 m | Median: 0.00 m | Q3: +0.45 m | Max: +5.10 m
```

**Conclusion**: The strong statistical concordance ($r > 0.81$, median difference $0.00\text{ m}$) verifies that both agencies measure identical hydrological dynamics with high fidelity. Slight differences ($1.17\text{ m}$ mean) are attributable to differing collar elevations (measuring point above ground level) and timing within the observation month.

---

## 4. Catchment-Scale Network Coverage

A critical objective of Phase 7 is closing the spatial observation gap across Maharashtra's 518 Level 8 catchments (`HYBAS_ID`).

### 4.1 Coverage Expansion Breakdown

| Metric | CGWB Alone | GSDA Alone | Combined (CGWB $\cup$ GSDA) | Change vs. CGWB |
| :--- | :--- | :--- | :--- | :--- |
| **Total Monitored Catchments** | 375 | 450 | **459** | **+84 catchments (+22.4%)** |
| **Catchment Coverage Percentage** | 72.39% | 86.87% | **88.61%** | **+16.22 percentage points** |
| **Unmonitored Catchments** | 143 (27.61%) | 68 (13.13%) | **59 (11.39%)** | **-84 catchments (-58.7%)** |
| **Total Station Points Mapped** | 1,936 | 4,090 | **6,026** | **+4,090 stations (+211.3%)** |
| **Mean Stations per Catchment** | 3.74 | 7.90 | **11.63** | **+7.89 stations/catchment** |

### 4.2 Network Density Categorization
Across all 518 catchments, monitoring density is categorized as follows:

| Coverage Category | Criteria | Catchment Count ($N$) | Percentage (%) |
| :--- | :--- | :--- | :--- |
| **Dense Network ($\ge 5$ wells)** | Both agencies active; robust spatial sampling | 324 | 62.55% |
| **Moderate Network ($2 - 4$ wells)** | Basic monitoring presence; localized sampling | 103 | 19.88% |
| **Sparse Network ($1$ well)** | Single point observation; high vulnerability to local anomalies | 32 | 6.18% |
| **Unmonitored ($0$ wells)** | No active CGWB or GSDA monitoring well recorded | 59 | 11.39% |
| **Total** | | **518** | **100.00%** |

### 4.3 Spatial Characteristics of Unmonitored Catchments
The remaining 59 unmonitored catchments were analyzed for geographic distribution:
- **Western Ghats Scarp & Forest Reserves**: 38 catchments lie along steep basaltic escarpments and protected tiger reserves (Koyna, Radhanagari, Chandoli) where agricultural groundwater extraction is negligible and habitations are sparse.
- **Inter-State Boundary Margins**: 14 catchments along the Madhya Pradesh, Telangana, and Gujarat borders have $< 20\%$ of their area inside Maharashtra, where state agencies do not maintain permanent observation wells.
- **Coastal Estuarine Fringe**: 7 small coastal micro-creeks in Thane, Raigad, and Ratnagiri where saline intrusion dominates and shallow alluvial extraction is monitored through unrecorded community dug wells.

---

## 5. Output Datasets and Quality Verification

The Phase 7 pipeline produced two standardized, auditable processed datasets:

1. **`data/processed/jaldrishti_infrastructure_by_catchment.csv`**
   - **Dimensions**: 518 rows $\times$ 21 columns
   - **Key Attributes**: `HYBAS_ID`, `sub_area_km2`, `structure_count_total` (0, explicit flag), `inventory_status`, `inventory_data_policy`, `cgwb_monitoring_well_count`, `gsda_monitoring_well_count`, `total_monitoring_well_count`, `monitoring_network_coverage_flag`, `gw_depth_trend_median_m_yr`, `gw_seasonal_recharge_median_m`.
   - **Policy Assertion**: All structure metrics explicitly acknowledge pending official GIS inventory.

2. **`data/processed/jaldrishti_phase7_evidence_assessment.csv`**
   - **Dimensions**: 518 rows $\times$ 26 columns
   - **Key Attributes**: Multi-scenario scores and ranks (preserved unaltered from Phase 3/4), `consensus_priority_tier_revised`, `shortlist_surface_water_harvesting`, `shortlist_managed_aquifer_recharge`, `provisional_action_category_MAR`, `provisional_screening_rationale_MAR`, `provisional_action_category_SWH`, `provisional_screening_rationale_SWH`, `evidence_confidence_level`, `screening_disclaimer`.

---

## 6. Verification and Checksums

The integrity of all Phase 7 inputs, outputs, and preserved baseline assets is verified by SHA-256 cryptographic hashes:

```
Baseline Assets (Unaltered Phase 3 & 4 Baselines):
  692b7dc9b7d56e5a964a452348c3086906f0e1d1630e26a6761306a2f875e982  jaldrishti_mcda_scenario_rankings.csv
  85bece275a30aca3fd7aca0d81ef226179e6bb702f96a95b81e3f76669696ccb  jaldrishti_consensus_priority_audit.csv
  93585556df7f91825e1efe4664d224e3fc2a4c437317e815efa8c6f9b01a4843  jaldrishti_watersheds_with_village_indicators_v2.csv
  b600ca7cf8decf872b11cdcc2bb947c6ea9c7748bd2451d90c4b268f0339e372  jaldrishti_scored_watersheds.shp

Phase 7 Raw Datasets:
  5003c9030b34df310f0bdd0527df022b9b0e73aa780b5bbacc88cc49d1be0eb6  ground_water_level_manual_quarterly_maharashtra_1970_2025.csv
  ec97b2fa941cfca0fc5dae7b99c7ea0770cb5038c9fe7ba64c1b979a0cf5086b  gwl_manual_quarterly_cgwb_mh_1991_2020.csv
  3aaee546d1838ae6292b1a134a41315904d9b43aa9430ea4ca7e30d70eb0e6a3  gwl_manual_quarterly_cgwb_mh_2021_2025.csv
```
