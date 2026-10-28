# JalDrishti-AI: MCDA Consensus Ranking Audit & Intervention Shortlisting

**Document ID**: `12_CONSENSUS_RANKING_AUDIT.md`  
**Date**: October 27, 2026  
**Target Coverage**: 518 HydroATLAS Level 8 Catchments, Maharashtra  
**Author**: JalDrishti-AI Geospatial Engineering & Data Science Team  

---

> [!IMPORTANT]
> **Exploratory Decision Support Disclaimer**  
> All candidate shortlists, scores, and consensus ranks presented in this document represent **exploratory multi-criteria screening shortlists**, NOT a final construction authorization. Watershed-level scores aggregate regional hydro-meteorological and edaphic conditions across multi-village catchments. **No construction of check dams, farm ponds, or recharge shafts should be commissioned at individual sites without on-ground hydrogeological resistivity surveys, geotechnical foundation testing, and village panchayat stakeholder verification.**

---

## 1. Investigation of the Phase 3 Consensus Shortlist Discrepancy

### 1.1 The Mathematical Problem: Naive Arithmetic Mean Rank
In the initial Phase 3 exploratory reporting, catchments were sorted by their unweighted arithmetic mean rank across all scenarios, including pure objective Shannon Entropy ($S_3$) and Managed Aquifer Recharge ($S_4$). A close audit reveals that simple arithmetic mean ranking suffers from severe mathematical and hydrological flaws:

1. **Hydrological Opposition of Interventions (MAR vs. SWH)**:
   - **Surface Water Harvesting (SWH)** requires heavy, impermeable clay vertisols ($>400\text{ g/kg}$) to prevent seepage losses in unlined earthen structures.
   - **Managed Aquifer Recharge (MAR)** requires coarse, permeable sandy/alluvial strata ($>280\text{ g/kg}$) and high infiltration capacity to conduct water into subsurface aquifers.
   - When a catchment is ideally suited for SWH (e.g. heavy black cotton soil in Ahmednagar or Solapur), it is naturally penalized in the MAR scenario. Averaging its rank across both interventions arbitrarily drags its composite rank down.
2. **Shannon Entropy Runoff Distortion**:
   - Pure objective Shannon Entropy assigns 26.3% of its weight to natural annual runoff depth (`run_mm_syr`) because runoff varies over a massive numerical range ($<50\text{ mm}$ in eastern Solapur to $>3,000\text{ mm}$ in coastal Konkan).
   - This severely penalizes acute drought-prone agricultural basins (e.g., Godavari south tributaries) where runoff is modest, skewing their mean rank.
3. **Outlier Sensitivity of Arithmetic Mean**:
   - The arithmetic mean is heavily distorted by single-scenario outliers. For example, Catchment `4081066790`:
     - Rank 1 in AHP Expert ($S_2$)
     - Rank 1 in Winsorized AHP ($S_7$)
     - Rank 1 in Core Basins ($S_6$)
     - Rank 11 in Surface Water Harvesting ($S_5$)
     - Rank 16 in Equal Pillars ($S_1$)
     - BUT Rank 162 in MAR ($S_4$) and Rank 127 in Shannon Entropy ($S_3$)!
     - Because of these two extreme outliers, its rank standard deviation blew up to **71.97**, and its arithmetic mean rank dropped to **53.00**, obscuring its status as Maharashtra's highest-priority agricultural drought basin.

---

## 2. Revised, Transparent Multi-Scenario Consensus Rules

To eliminate outlier distortion while preserving intervention-specific integrity, we establish a robust non-parametric consensus architecture evaluated across the **five core planning scenarios** (`S1_Equal`, `S2_AHP`, `S4_MAR`, `S5_SWH`, `S7_Winsorized_AHP`):

1. **Median Rank across Planning Scenarios (`rank_median_planning`)**:
   - The median is mathematically immune to single-scenario outlier skew, capturing the true central tendency of a catchment's priority.
2. **Frequency of Top-Tier Inclusion**:
   - `top10pct_count_planning`: Number of scenarios (out of 5) where the catchment ranks in the Top 10% ($\text{rank} \le 52$).
   - `top20pct_count_planning`: Number of scenarios where the catchment ranks in the Top 20% ($\text{rank} \le 104$).
   - `top25pct_count_planning`: Number of scenarios where the catchment ranks in the Top 25% ($\text{rank} \le 130$).
3. **Rank Dispersion Metrics**:
   - Interquartile Range (`rank_iqr_planning` = 75th percentile - 25th percentile). Catchments with low IQR exhibit stable, consistent priority across varying stakeholder weightings.
4. **Three Separate Intervention Shortlists**:
   - **Shortlist A: Surface Water Harvesting (SWH)** — Prioritizing heavy clay retention, runoff volume, and agricultural cropland water draft.
   - **Shortlist B: Managed Aquifer Recharge (MAR)** — Prioritizing vadose permeability, rolling slope, and multi-year drought recurrence.
   - **Shortlist C: Robust Multi-Scenario Consensus** — Catchments with the lowest median rank and persistent top-tier representation across all models.

---

## 3. Revised Consensus Priority Tier Distribution

The 518 catchments are classified according to strict, transparent rules:

| Consensus Priority Tier | Definition & Inclusion Rule | Catchment Count | Percentage (%) | Actionable Field Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Consensus Tier 1: Robust Priority (Multi-Scenario)** | Appears in Top 20% ($\text{rank} \le 104$) in $\ge 4$ of 5 core planning scenarios, AND `rank_median_planning` $\le 104$. | **76** | **14.67%** | Core priority for immediate state intervention. Stable against weighting shifts. |
| **Consensus Tier 2: Specialized / Moderate Priority** | Appears in Top 20% in 2 or 3 scenarios, OR `rank_median_planning` $\le 180$. | **109** | **21.04%** | Highly suitable for specialized single-intervention programs (e.g. exclusively MAR or exclusively SWH). |
| **Consensus Tier 3: Low Priority / Conservation** | Catchments failing Tier 1 and Tier 2 criteria. | **333** | **64.29%** | Catchments with adequate natural forest buffer, lower agricultural draft, or coastal high rainfall. |

---

## 4. Candidate Shortlists: Analysis & Physical Indicators

### Shortlist A: Top-10 Surface Water Harvesting (SWH)
*Target Interventions*: Earthen check dams, nala bunds, continuous contour trenches, de-silting of existing village percolation tanks, farm ponds with natural clay sealing.

| S5 Rank | HYBAS_ID | Basin Area ($km^2$) | S2 AHP Rank | S1 Equal Rank | Village Clay (g/kg) | Village Cropland (%) | Runoff Depth (mm) | Baseline Rain (mm) | Primary Physical Rationale & Engineering Nuance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `4081064550` | 290.5 | 174 | 29 | 415.1 | 26.9% | 1916 | 2154.5 | High runoff volume; clayey subsoil provides natural watertight pond basins. |
| **2** | `4081079470` | 952.2 | 63 | 2 | 377.8 | 39.7% | 1260 | 1713.8 | Solapur/Bhima basin; substantial runoff generation coupled with high seasonal irrigation draft. |
| **3** | `4081079540` | 329.3 | 108 | 1 | 377.8 | 30.0% | 1432 | 1851.3 | Sina River sub-basin; steep tributary headwaters yield high kinetic runoff for check dams. |
| **4** | `4081073360` | 378.3 | 157 | 6 | 402.2 | 20.4% | 1421 | 1860.6 | Upper Manjara headwaters; excellent clay retention prevents deep seepage in unlined ponds. |
| **5** | `4081073250` | 272.4 | 204 | 14 | 417.0 | 8.7% | 1517 | 1944.4 | High clay vertisols (41.7%); suitable for community storage tanks and gully plugs. |
| **6** | `4081068280` | 744.5 | 169 | 4 | 394.1 | 7.7% | 1555 | 1957.9 | Dudhana catchment; rolling terrain with reliable annual surface runoff depth. |
| **7** | `4081067310` | 720.7 | 176 | 8 | 397.6 | 17.6% | 1740 | 2043.6 | Jalna/Parbhani border; heavy soils minimize earthen bund seepage. |
| **8** | `4081073260` | 545.3 | 98 | 10 | 379.5 | 28.1% | 1246 | 1709.2 | Osmanabad rainshadow; high seasonal deficit makes surface impoundment vital for livestock and rabi crops. |
| **9** | `4081044250` | 1713.7 | 10 | 5 | 460.0 | 68.7% | 612 | 878.1 | High cropland intensity (68.7%) and heavy vertisols (46.0% clay); ideal for on-farm ponds. |
| **10** | `4080031450` | 2221.4 | 81 | 12 | 442.4 | 52.8% | 850 | 1146.4 | Tapi basin agricultural tributary; broad alluvial-clay plains suitable for cascading check dams. |

---

### Shortlist B: Top-10 Managed Aquifer Recharge (MAR)
*Target Interventions*: Recharge shafts, injection borewells in fractured basalt, percolation tanks in weathered murrum layers, sub-surface dykes.

| S4 Rank | HYBAS_ID | Basin Area ($km^2$) | S2 AHP Rank | S1 Equal Rank | Village Sand (g/kg) | Infiltration Proxy | Drought Yrs (0–25) | Baseline Rain (mm) | Primary Physical Rationale & Engineering Nuance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `4081093520` | 431.9 | 148 | 84 | 471.3 | 2.30 | 3.40 | 1205.8 | Coarse texture (47.1% sand); high permeability allows rapid transmission without surface evaporation. |
| **2** | `4081091960` | 492.1 | 179 | 93 | 465.3 | 2.23 | 2.69 | 1269.4 | Sandy loam topsoil; ideal for spreading basins and unlined percolation tanks. |
| **3** | `4081094030` | 398.2 | 83 | 48 | 425.0 | 1.81 | 4.00 | 1007.4 | Acute drought recurrence (4 major drought years); high vadose permeability supports aquifer replenishment. |
| **4** | `4081093850` | 162.5 | 72 | 41 | 403.5 | 1.69 | 4.58 | 986.3 | Frequent drought failure (4.6 drought years); coarse soil texture prevents pond stagnation. |
| **5** | `4081099040` | 1022.7 | 229 | 118 | 411.2 | 1.82 | 5.25 | 1324.9 | Severe historical drought frequency (>5 drought years); high infiltration proxy enables deep recharge. |
| **6** | `4081099000` | 1412.2 | 306 | 136 | 419.0 | 1.81 | 4.56 | 1353.9 | Substantial catchment area with permeable topsoil; suitable for regional recharge shaft networks. |
| **7** | `4081089450` | 1322.4 | 82 | 53 | 391.9 | 1.50 | 4.41 | 936.4 | Semi-arid drought belt; high infiltration index minimizes evaporation losses compared to open farm ponds. |
| **8** | `4081104550` | 776.0 | 366 | 172 | 420.6 | 1.97 | 5.19 | 1438.7 | High drought frequency (>5 years); coarse weathered material overlying fractured basalt aquifer. |
| **9** | `4081092420` | 580.0 | 66 | 37 | 396.5 | 1.51 | 3.96 | 936.5 | Low rainfall (936mm) and permeable texture; excellent target for artificial aquifer recharge. |
| **10** | `4081098970` | 1235.8 | 255 | 127 | 400.5 | 1.72 | 4.21 | 1284.1 | Large catchment with consistent soil permeability and historical drought vulnerability. |

> [!NOTE]
> **Zero Overlap Insight**: There is **only 1 catchment (`4081079470`)** shared between the Top 20 SWH and Top 20 MAR shortlists. SWH prioritizes impermeable clay plains in the rainshadow agricultural heartland, whereas MAR prioritizes coarser weathered basalt corridors with high infiltration rates.

---

### Shortlist C: Top-10 Robust Multi-Scenario Consensus Catchments
*Criteria*: Minimum median rank across all planning scenarios, low interquartile range (IQR), and inclusion in the Top 20% in at least 4 of 5 core planning models.

| Consensus Rank | HYBAS_ID | Basin Area ($km^2$) | Median Rank | Rank IQR | Top 20% Count (out of 5) | S1 Equal Rank | S2 AHP Rank | S5 SWH Rank | Baseline Rain (mm) | Cropland (%) | District Location |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `4081044250` | 1713.7 | **9.0** | **5.0** | **4** | 5 | 10 | 9 | 878.1 | 68.7% | Aurangabad / Jalna |
| **2** | `4081066790` | 351.2 | **11.0** | **15.0** | **4** | 16 | 1 | 11 | 537.9 | 82.5% | Ahmednagar / Beed |
| **3** | `4081044290` | 461.3 | **13.0** | **14.0** | **4** | 13 | 4 | 18 | 755.4 | 73.0% | Beed (Godavari South) |
| **4** | `4081079470` | 952.2 | **15.0** | **41.0** | **5** | 2 | 63 | 2 | 1713.8 | 39.7% | Solapur (Bhima Basin) |
| **5** | `4081070610` | 15.8 | **15.0** | **8.0** | **4** | 19 | 6 | 15 | 606.2 | 77.4% | Solapur / Osmanabad |
| **6** | `4081070330` | 199.4 | **20.0** | **33.0** | **4** | 38 | 3 | 20 | 587.8 | 84.9% | Osmanabad / Latur |
| **7** | `4081072720` | 380.7 | **22.0** | **22.0** | **4** | 43 | 16 | 21 | 618.3 | 82.2% | Latur (Manjara River) |
| **8** | `4081069430` | 420.7 | **22.0** | **35.0** | **4** | 37 | 2 | 22 | 555.8 | 85.7% | Beed / Osmanabad |
| **9** | `4081073260` | 545.3 | **23.0** | **50.0** | **5** | 10 | 98 | 8 | 1709.2 | 28.1% | Osmanabad Tributary |
| **10** | `4081048850` | 757.9 | **23.0** | **3.0** | **4** | 22 | 23 | 25 | 650.3 | 80.2% | Jalna / Parbhani |

---

## 5. Site-Specific Engineering Limitations of Catchment-Level Scores

While these shortlists identify macro-level watershed priority with statistical defensibility, civil engineers must NOT select specific structure locations based solely on catchment-level indicators:

1. **Hydraulic Micro-Siting Constraints**:
   - A catchment with high clay content may still feature fractured basalt outcrops in nala beds where check dam foundations require dental concrete or pressure grouting.
   - Contour bunding and trenching require field slope measurements; SRTM 30m smoothed slope underestimates localized gully incisions.
2. **Existing Water Conservation Density**:
   - Maharashtra has implemented extensive watershed programs over three decades (Jalyukt Shivar, Gal Mukt Dharan, Adarsh Gaon). A catchment ranking in the top 10 may already have 50+ check dams built along its primary stream order. Building additional structures without checking existing storage saturation risks drying up downstream reservoirs.
3. **Panchayat Social Readiness & Maintenance**:
   - Sustainable watershed management requires active Village Water & Sanitation Committees (VWSC). Without community de-silting agreements, check dams silt up within 3–5 monsoon seasons.

---

## 6. Deliverables & Data Products Summary

All outputs are generated reproducibly and verified by automated unit tests:
- **Consensus Audit Table**: [`data/processed/jaldrishti_consensus_priority_audit.csv`](file:///c:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/data/processed/jaldrishti_consensus_priority_audit.csv)
- **Engine Script**: [`src/jaldrishti/consensus_audit_engine.py`](file:///c:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/src/jaldrishti/consensus_audit_engine.py)
- **Unit Test Suite**: [`tests/test_consensus_ranking.py`](file:///c:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/tests/test_consensus_ranking.py) (All 5 tests passing).
