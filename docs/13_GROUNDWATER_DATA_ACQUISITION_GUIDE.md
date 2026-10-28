# JalDrishti-AI: Groundwater Data Acquisition Guide

**Document ID**: `13_GROUNDWATER_DATA_ACQUISITION_GUIDE.md`  
**Date**: October 27, 2026  
**Audience**: GIS Engineers, Data Scientists, Field Hydrologists  
**Target Coverage**: Maharashtra State (36 Districts, 518 Level 8 Catchments)  

---

## Objective

This guide provides precise, step-by-step instructions for acquiring authoritative, official groundwater observation records from Government of India and Government of Maharashtra portals to execute independent empirical validation of the JalDrishti-AI watershed rankings.

---

## 1. Primary Institutional Sources

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     GROUNDWATER DATA ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Source 1: Central Ground Water Board]    [Source 2: GSDA Maharashtra]     │
│  National Hydrograph Network (NHN)         State Observation Well Network   │
│  ~1,820 Stations in Maharashtra            ~3,500 Dugwells & Piezometers    │
│  Portal: India-WRIS / NWIC                 Portal: GSDA Maharashtra        │
│                    │                                     │                  │
│                    └──────────────────┬──────────────────┘                  │
│                                       ▼                                     │
│                     ┌───────────────────────────────────┐                   │
│                     │ Harmonization & Quality Filtering │                   │
│                     │ - Bounding Box: MH Bounds         │                   │
│                     │ - mbgl Depth Verification         │                   │
│                     │ - QC: Valid, Dry, Pumping         │                   │
│                     └─────────────────┬─────────────────┘                   │
│                                       ▼                                     │
│                     ┌───────────────────────────────────┐                   │
│                     │ Target Local Ingestion File:      │                   │
│                     │ data/raw/                         │                   │
│                     │ cgwb_maharashtra_observation_     │                   │
│                     │ wells.csv                         │                   │
│                     └─────────────────┬─────────────────┘                   │
│                                       ▼                                     │
│                     ┌───────────────────────────────────┐                   │
│                     │ scripts/validate_independent_     │                   │
│                     │ evidence.py                       │                   │
│                     └───────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Step-by-Step Acquisition via India-WRIS / NWIC

The National Water Informatics Centre (NWIC), under the Ministry of Jal Shakti, hosts the official CGWB National Hydrograph Network database.

### Step 2.1: Access the Portal
1. Navigate to: **`https://indiawris.gov.in/wris/`**
2. In the top navigation bar, select **Data Download** $
ightarrow$ **Groundwater Level**.
3. Direct URL: `https://indiawris.gov.in/wris/#/groundWater`

### Step 2.2: Apply Query Filters
In the interactive query builder, select the following parameters:
- **Agency**: `Central Ground Water Board (CGWB)`
- **State**: `Maharashtra`
- **District**: Select `All Districts` (or query district by district if download size exceeds limits)
- **Station Type**: `All` (or select `Dug Well` and `Piezometer`)
- **Temporal Range**: 
  - Start Date: `01-01-2015`
  - End Date: `31-12-2024` (10-year decadal validation window)
- **Measurement Seasons**: Ensure **Pre-monsoon (May/June)** and **Post-monsoon (October/November)** are captured.

### Step 2.3: Export Data
1. Click **View / Fetch Data**.
2. Once the table populates, click **Download as CSV** / **Export to Excel**.
3. Save the exported raw file as `data/raw/cgwb_raw_export_maharashtra_2015_2024.csv`.

---

## 3. Alternative: CGWB Ground Water Year Book Reports

If portal downloads are unavailable due to server maintenance:
1. Navigate to: **`https://cgwb.gov.in/en/ground-water-year-book`**
2. Download the annual publication: **Ground Water Year Book - Maharashtra & Goa State** (latest available editions: 2020-21, 2021-22, 2022-23, 2023-24).
3. The report annexures contain complete station tables with Station Name, Latitude, Longitude, May Depth ($mbgl$), and November Depth ($mbgl$).
4. Extract the annexure tables using Python:
   ```bash
   pip install pdfplumber
   ```
   and extract the tabular pages to CSV.

---

## 4. Alternative: GSDA Maharashtra Watershed Records

The Groundwater Surveys and Development Agency (GSDA), Pune maintains the densest monitoring network across Maharashtra's 1,531 watersheds:
1. Portal: **`https://gsda.maharashtra.gov.in/`**
2. Navigate to **Watershed Reports** $
ightarrow$ **Groundwater Assessment**.
3. GSDA publishes annual pre-monsoon (May) and post-monsoon (October) water level tables for each administrative taluka.

---

## 5. Schema Harmonization Workflow

To ensure seamless ingestion into JalDrishti-AI, format the acquired records into the standardized schema defined in [`data/raw/templates/cgwb_maharashtra_observation_wells_template.csv`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/data/raw/templates/cgwb_maharashtra_observation_wells_template.csv).

### Required Fields & Format Rules:

| Field Name | Expected Type | Format & Validation Rule | Example |
| :--- | :--- | :--- | :--- |
| `station_id` | String | Unique station identifier | `CGWB_MH_PUN_012` |
| `station_name` | String | Village / location name | `Baramati` |
| `district` | String | Standard Maharashtra district | `Pune` |
| `taluka` | String | Sub-district name | `Baramati` |
| `latitude` | Float | Decimal degrees WGS84: $15.6 \le \text{lat} \le 22.1$ | `18.1517` |
| `longitude` | Float | Decimal degrees WGS84: $72.6 \le \text{lon} \le 80.9$ | `74.5772` |
| `well_type` | Categorical | `Dugwell`, `Borewell`, `Piezometer` | `Dugwell` |
| `aquifer_type` | Categorical | `Basalt_Vesicular`, `Basalt_Fractured`, `Alluvium` | `Basalt_Fractured` |
| `observation_year` | Integer | $2015 \le YYYY \le 2024$ | `2021` |
| `observation_date` | Date/String | `YYYY-MM-DD` | `2021-05-15` |
| `water_level_mbgl` | Float | Meters below ground level ($\ge 0$) | `12.45` |
| `pre_monsoon_wl_mbgl` | Float | May/June water level ($mbgl$) | `12.45` |
| `post_monsoon_wl_mbgl` | Float | October/November water level ($mbgl$) | `4.20` |
| `measurement_qc_flag` | Categorical | `Valid`, `Dry_Well`, `Pumping_Affected`, `Destroyed` | `Valid` |

### Harmonization Rules:
1. **Coordinate Format**: If coordinates are reported in Degrees-Minutes-Seconds (e.g., $18^\circ 09' 06''\text{ N}$), convert to Decimal Degrees:
   $$\text{Decimal Degrees} = \text{Degrees} + rac{\text{Minutes}}{60} + rac{\text{Seconds}}{3600}$$
2. **Measurement Depth Convention**: Depth MUST be recorded in **meters below ground level ($mbgl$)**. If source data is in meters above Mean Sea Level (m MSL), convert using the station ground elevation:
   $$\text{Depth } (mbgl) = \text{Elevation (m MSL)} - \text{Water Level (m MSL)}$$
3. **Quality Flags**:
   - Wells that were dry at the time of measurement must be flagged as `Dry_Well`.
   - Wells actively pumping or within an active cone of depression must be flagged as `Pumping_Affected`.
   - Normal, representative static water levels must be flagged as `Valid`.

---

## 6. Executing Validation in JalDrishti-AI

Once the data file is placed at `data/raw/cgwb_maharashtra_observation_wells.csv`:

```bash
# Run the validation pipeline with default paths
python scripts/validate_independent_evidence.py

# Or specify custom file paths and minimum observation years
python scripts/validate_independent_evidence.py     --wells data/raw/cgwb_maharashtra_observation_wells.csv     --min-years 5
```

### Expected Output:
1. Verification of schema and coordinates within Maharashtra.
2. Removal of flagged QC and duplicate observations.
3. Reprojection to UTM Zone 43N (`EPSG:32643`) and spatial join to 518 Level 8 catchments.
4. Annual seasonal recharge ($\Delta h$) and non-parametric Theil-Sen trend ($eta_{\text{trend}}$ in m/yr).
5. Spearman rank correlation $
ho$ between `score_S4_Managed_Aquifer_Recharge` and $eta_{\text{basin}}$, reporting sample size and $p$-value.
6. Export of catchment-aggregated metrics to `data/processed/jaldrishti_groundwater_validation_results.csv`.
