# JalDrishti-AI: Groundwater Data Provenance & Ingestion Audit Log

**Document ID**: `14_GROUNDWATER_DATA_PROVENANCE_LOG.md`  
**Date**: October 28, 2026  
**Audience**: GIS Data Engineers, Hydrologists, Quality Assurance Auditors  
**Project**: JalDrishti-AI (Maharashtra Watershed Prioritisation)  

---

## Executive Summary

This provenance log documents the verifiable institutional origin, download URLs, cryptographic SHA-256 hashes, licensing conditions, schema transformations, and traceable exclusion ledger for the official groundwater observation datasets acquired in Phase 6.

All raw files downloaded from the **National Water Data Portal (NWDP / NWIC, Ministry of Jal Shakti)** are preserved byte-for-byte in `data/raw/` without modification.

---

## 1. Source Verification & Provenance Registry

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DATA PROVENANCE LINEAGE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Source: National Water Informatics Centre (NWIC)]                         │
│  Ministry of Jal Shakti, Department of Water Resources, RD & GR, GoI        │
│  Portal: National Water Data Portal (CKAN Repository: nwdp.nwic.gov.in)     │
│  Dataset Package: gwl-manual-quarterly-central-ground-water-board-department│
│  Package UUID: 956add67-cba9-41a5-9d5c-96d73db44aef                         │
│                    │                                                        │
│         ┌──────────┴────────────────────────┐                               │
│         ▼                                   ▼                               │
│  [Resource 1: 1991–2020]             [Resource 2: 2021–2025]                │
│  UUID: 0e7180fa-5282-4df6-           UUID: 073029e8-492d-416c-              │
│        bead-8ca7a7557e74                   9857-3ad3e27c69a6                │
│  Size: 13,975,547 bytes              Size: 1,754,883 bytes                  │
│  Rows: 106,507                       Rows: 13,430                           │
│  SHA-256: 8e2c13f5aa5af132...        SHA-256: 5fd40cbfc51ad349...           │
│         │                                   │                               │
│         └──────────┬────────────────────────┘                               │
│                    ▼                                                        │
│     [Harmonization Pipeline: scripts/harmonize_cgwb_observations.py]        │
│     - Decadal Window Filter (2015-01-01 to 2024-12-31)                      │
│     - Unambiguous Station Key (LGD + Coords)                                │
│     - Exclusion Ledger: 43,752 Valid Observations Retained                  │
│                    ▼                                                        │
│     [Harmonized File: data/raw/cgwb_maharashtra_observation_wells.csv]      │
│     14-Column Template Schema, 1,936 Distinct Monitoring Stations           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Table 1.1: Raw Dataset Manifest

| Attribute | Dataset A (1991–2020) | Dataset B (2021–2025) |
| :--- | :--- | :--- |
| **Filename in `data/raw/`** | `gwl_manual_quarterly_cgwb_mh_1991_2020.csv` | `gwl_manual_quarterly_cgwb_mh_2021_2025.csv` |
| **Originating Agency** | Central Ground Water Board (CGWB) | Central Ground Water Board (CGWB) |
| **Publishing Portal** | National Water Data Portal (NWDP / NWIC) | National Water Data Portal (NWDP / NWIC) |
| **Package Title** | Ground Water Level (Manual - Quarterly), CGWB | Ground Water Level (Manual - Quarterly), CGWB |
| **Package UUID** | `956add67-cba9-41a5-9d5c-96d73db44aef` | `956add67-cba9-41a5-9d5c-96d73db44aef` |
| **Resource UUID** | `0e7180fa-5282-4df6-bead-8ca7a7557e74` | `073029e8-492d-416c-9857-3ad3e27c69a6` |
| **Download URL** | [Download CSV](https://nwdp.nwic.gov.in/dataset/956add67-cba9-41a5-9d5c-96d73db44aef/resource/0e7180fa-5282-4df6-bead-8ca7a7557e74/download/gwl_manual_quarterly_cgwb_mh_1991_2020.csv) | [Download CSV](https://nwdp.nwic.gov.in/dataset/956add67-cba9-41a5-9d5c-96d73db44aef/resource/073029e8-492d-416c-9857-3ad3e27c69a6/download/gwl_manual_quarterly_cgwb_mh_2021_2025.csv) |
| **Retrieval Date** | October 28, 2026 | October 28, 2026 |
| **File Size (Bytes)** | **13,975,547 bytes** | **1,754,883 bytes** |
| **Line / Record Count**| 106,508 lines (106,507 data rows) | 13,431 lines (13,430 data rows) |
| **Cryptographic Hash (SHA-256)** | `8e2c13f5aa5af13245cd51056ba0062550967f869901a75a56733fd28e4de3c0` | `5fd40cbfc51ad349e25cd7678e3bafdac732d470986ec1c55c39a23b174b04d0` |
| **Licensing** | Government Open Data License - India (GODL-India) / NDSAP | Government Open Data License - India (GODL-India) / NDSAP |
| **Preservation Status** | Preserved byte-for-byte in `data/raw/` | Preserved byte-for-byte in `data/raw/` |

---

## 2. Institutional Dataset Comparison: CGWB vs. GSDA Maharashtra

The NWDP CKAN catalog provides two independent monitoring streams for Maharashtra:

1. **Central Ground Water Board (CGWB) Manual Quarterly**:
   - *Strengths*: National Hydrograph Network (NHN) standard; strict quarterly monitoring schedule (January, May, August, November); seamless column structure between historical (1991–2020) and modern (2021–2025) files; 100% parseable timestamps; verified high geodetic accuracy.
   - *Selection*: **Selected for Phase 6 Primary Empirical Evaluation**.

2. **Maharashtra Ground Water Department (GSDA) Dataset**:
   - *Resource*: `ground_water_level_manual_quarterly_maharashtra_1970_2025.csv` (UUID `bb185a88-c7c3-483f-b06e-784ce5322ff8`, 91.49 MB, ~700,000 rows).
   - *Characteristics*: Rich state dugwell inventory with explicit `Well ID` (`W1538...`) and well depths, but variable historical reporting frequency across talukas and different schema formatting.
   - *Role*: Retained as a secondary state benchmark for future micro-watershed deep dives.

---

## 3. Schema Harmonization Mapping Lineage

The raw CGWB table schema was mapped into the standardized 14-column template schema defined in `data/raw/templates/cgwb_maharashtra_observation_wells_template.csv` using [`scripts/harmonize_cgwb_observations.py`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/scripts/harmonize_cgwb_observations.py):

| Target Template Column | Source Column / Transformation Rule | Rationale & Standards |
| :--- | :--- | :--- |
| `station_id` | `CGWB_{District_LGD}_{District}_{Tehsil}_{Station}_{Lat:.4f}_{Lon:.4f}` | Unambiguous deterministic station identifier incorporating national Local Government Directory (LGD) code, administrative hierarchy, and 4-decimal geodetic coordinates to prevent collisions among common village names. |
| `station_name` | `Station.str.strip()` | Preserves original source station name verbatim. |
| `district` | `District.str.strip()` | Administrative district name. |
| `taluka` | `Tehsil.str.strip()` | Administrative sub-district name. |
| `latitude` | `pd.to_numeric(Latitude)` | Verified WGS84 decimal degrees ($15.6667^\circ - 21.8267^\circ\text{N}$). |
| `longitude` | `pd.to_numeric(Longitude)` | Verified WGS84 decimal degrees ($72.7333^\circ - 80.6000^\circ\text{E}$). |
| `well_type` | `"Observation_Well"` | Standardized hydrograph monitoring category. |
| `aquifer_type` | `"Unknown"` | In accordance with strict guidelines, `Unknown` is assigned rather than assuming `Deccan_Basalt`, because source quarterly CSV does not report lithological borehole logs. |
| `observation_year` | `parsed_datetime.dt.year` | Year of observation ($2015 \le YYYY \le 2024$). |
| `observation_date` | `parsed_datetime.dt.strftime("%Y-%m-%d")` | Standardized ISO-8601 observation date. |
| `water_level_mbgl` | `Groundwater Level Quarterly Manual (meter)` | Depth to water table in meters below ground level ($mbgl \ge 0$). |
| `pre_monsoon_wl_mbgl`| `NaN` (in timeseries record format) | Computed per station-year during aggregation from May observations. |
| `post_monsoon_wl_mbgl`| `NaN` (in timeseries record format) | Computed per station-year during aggregation from November observations. |
| `measurement_qc_flag`| `"Valid"` | Records passing numeric range and coordinate bounds checks. |

---

## 4. Traceable Exclusion Ledger

Every exclusion applied during ingestion is sequential and documented in [`data/processed/cgwb_ingestion_exclusion_summary.csv`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/data/processed/cgwb_ingestion_exclusion_summary.csv):

| Stage | Filter Criterion | Records Excluded | Records Remaining | % of Total Raw | Engineering & Methodological Rationale |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **0** | **Total Raw Input Records** | **0** | **119,937** | **100.00%** | Combined total from 1991–2020 (106,507) and 2021–2025 (13,430) files. |
| **1** | Unparseable Date / Malformed Timestamp | 0 | 119,937 | 0.00% | 100% of raw timestamps conformed to `%d-%m-%Y %H:%M` or `%d-%m-%Y`. |
| **2** | Outside Decadal Window (2015–2024) | 76,147 | 43,790 | 63.49% | Historical records prior to 2015-01-01 filtered to focus on 10-year baseline. |
| **3** | Missing (NaN) or Negative Depth Value | 17 | 43,773 | 0.01% | 17 records had null depth values. Exactly 0 negative values were observed. |
| **4** | Out-of-Envelope Coordinates | 0 | 43,773 | 0.00% | All stations fall strictly within Maharashtra's bounding box ($15.6^\circ-22.1^\circ\text{N}$, $72.6^\circ-80.9^\circ\text{E}$). |
| **5** | Duplicate Station-Date Observations | 21 | **43,752** | 0.02% | 21 duplicate timestamp entries for the exact same station on the same date dropped (retaining first valid record). |

**Net Harmonized Ingestion Dataset**:
- **Output File**: `data/raw/cgwb_maharashtra_observation_wells.csv`
- **Total Valid Observations**: **43,752 records**
- **Unique Monitoring Stations**: **1,936 stations**
- **Temporal Coverage**: January 1, 2015 to August 10, 2023

---

## 5. Unaltered Baseline Hash Verification

To guarantee that data acquisition and harmonization did NOT alter Phase 3 or Phase 4 analytical outputs, cryptographic hashes were computed before and after processing:

| Baseline File | SHA-256 Hash | Integrity Status |
| :--- | :--- | :--- |
| `data/processed/jaldrishti_mcda_scenario_rankings.csv` | `692b7dc9b7d56e5a964a452348c3086906f0e1d1630e26a6761306a2f875e982` | **100% UNALTERED (EXACT MATCH)** |
| `data/processed/jaldrishti_consensus_priority_audit.csv` | `85bece275a30aca3fd7aca0d81ef226179e6bb702f96a95b81e3f76669696ccb` | **100% UNALTERED (EXACT MATCH)** |
| `data/processed/jaldrishti_watersheds_with_village_indicators_v2.csv` | `93585556df7f91825e1efe4664d224e3fc2a4c437317e815efa8c6f9b01a4843` | **100% UNALTERED (EXACT MATCH)** |
| `data/processed/jaldrishti_scored_watersheds.shp` | `b600ca7cf8decf872b11cdcc2bb947c6ea9c7748bd2451d90c4b268f0339e372` | **100% UNALTERED (EXACT MATCH)** |
