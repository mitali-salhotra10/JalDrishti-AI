# JalDrishti-AI: 7–10 Minute Live Academic Demonstration Script

**Document ID**: `JD-DOC-21-DEMO-SCRIPT`  
**Purpose**: Guided Script for University Technical Evaluation, Capstone Defense & Academic Viva  
**Target Duration**: 7 to 10 Minutes  
**Demonstrator**: Project Lead / Presenter  
**Required Setup**:
- Local terminal open at `C:\Users\MITALI SALHOTRA\OneDrive\Desktop\JalDrishti`
- Streamlit application running on `http://localhost:8501` (`streamlit run app.py`)
- Secondary window open with [`reports/dpr_screening_sheets/`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/reports/dpr_screening_sheets)

---

## Demonstration Overview Timeline

```
  00:00 ─── 01:00 : Introduction & Problem Statement
  01:00 ─── 02:15 : Data Pipeline & Spatial Ingestion
  02:15 ─── 03:30 : Multi-Scenario MCDA & Consensus Prioritisation
  03:30 ─── 04:45 : Empirical Groundwater Triangulation & Deccan Trap Paradox
  04:45 ─── 06:15 : Live Dashboard Walkthrough (Dual Map & Catchment Profiler)
  06:15 ─── 07:30 : Multi-Catchment Comparison & DPR Screening Dossier Viewer
  07:30 ─── 08:30 : Scientific Safeguards, Invariants & Limitations
  08:30 ─── 09:30 : Conclusion, Future Work & Q&A Transition
```

---

## Segment-by-Segment Script

### Segment 1: Introduction & Problem Statement (0:00 – 1:00)

- **What to Show on Screen**:
  - Presentation slide 1 or the top header banner of the Streamlit dashboard:  
    `💧 JalDrishti-AI: Watershed Prioritization Decision Support System`
- **Speaking Notes**:
  > *"Good morning/afternoon, esteemed committee members. Today I am presenting JalDrishti-AI, a scientifically defensible geospatial decision-support framework and interactive system developed for watershed prioritisation across Maharashtra, India.*
  >
  > *In Maharashtra, agriculture faces an acute hydrological dichotomy: the Western Ghats receive over 3,000 millimeters of rainfall that rapidly escapes to the sea as torrential runoff, while the vast Deccan Plateau rain-shadow suffers chronic drought and severe groundwater depletion in fractured basalt aquifers.*
  >
  > *Historically, public water conservation schemes—such as check dams and percolation tanks—have suffered from three fatal flaws: they are planned using political administrative units rather than natural hydrological basins; they conflate surface runoff capture with subsurface aquifer recharge; and they lack empirical ground-truth validation. JalDrishti-AI resolves these gaps across all 518 natural sub-basins of the state."*
- **Main Takeaway**:
  JalDrishti-AI bridges natural watershed hydrology, village administrative data, and hydrogeological reality.

---

### Segment 2: Data Pipeline & Spatial Ingestion (1:00 – 2:15)

- **What to Show on Screen**:
  - The architectural workflow diagram from Section 4 of [`README.md`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/README.md) or Section 6 of [`docs/20_FINAL_PROJECT_REPORT.md`](file:///C:/Users/MITALI%20SALHOTRA/OneDrive/Desktop/JalDrishti/docs/20_FINAL_PROJECT_REPORT.md).
- **Speaking Notes**:
  > *"To build this framework, we integrated multiple authoritative remote-sensing and ground-truth assets:*
  > *1. Macro-scale hydrological basins from WWF HydroATLAS Level 8, delineating 518 natural catchments averaging 594 square kilometers.*
  > *2. Micro-scale administrative data from 44,468 village revenue boundaries.*
  > *3. High-resolution environmental layers: 25 years of daily CHIRPS satellite rainfall, 30-meter NASA SRTM digital elevation models, 10-meter ESA WorldCover land use, and ISRIC SoilGrids 250-meter soil texture profiles.*
  >
  > *Using vectorized, area-weighted polygon intersection in UTM Zone 43N, we aggregated village socio-ecological metrics into natural hydrological boundaries. We strictly enforced soil physics mass conservation: topsoil sand, clay, and silt sum to exactly 1,000 g/kg across every single catchment."*
- **Main Takeaway**:
  True multi-scale integration with strict physical mass-conservation guarantees.

---

### Segment 3: Multi-Scenario MCDA & Consensus Prioritisation (2:15 – 3:30)

- **What to Show on Screen**:
  - Dashboard: Click on **View 1: 📊 Executive Overview**, scroll to the **Statewide KPI Scorecards** and the **Consensus Tier Donut Chart**.
- **Speaking Notes**:
  > *"Rather than relying on an arbitrary, single-weight formula, our Multi-Criteria Decision Analysis framework balances four distinct pillars: Climate Drought Stress, Land Use Demand, Terrain Runoff Potential, and Soil Infiltration Capacity.*
  >
  > *We formulated and tested seven distinct policy scenarios: Equal Pillars (S1), an AHP-derived Expert model with an AHP Consistency Ratio of 0.046 (S2), Drought Stress (S3), Managed Aquifer Recharge (S4), Surface Water Harvesting (S5), Agrarian Vulnerability (S6), and a 5th/95th percentile Winsorized model (S7).*
  >
  > *Because decision-makers often argue over weights, we introduced Consensus Prioritisation. Using the median planning rank and rank standard deviation across all seven scenarios, we classified the state into three tiers:*
  > *- Consensus Tier 1: Exactly 76 sub-basins (14.7% of the state) that consistently rank in the top 100 regardless of which scenario is prioritized.*
  > *- Consensus Tier 2: 109 specialized basins.*
  > *- Consensus Tier 3: 333 low-priority or baseline conservation basins."*
- **Main Takeaway**:
  Robust consensus eliminates single-weight bias and isolates 76 high-confidence priority targets.

---

### Segment 4: Empirical Groundwater Triangulation & Deccan Trap Paradox (3:30 – 4:45)

- **What to Show on Screen**:
  - Dashboard: Scroll down to the **Multi-Agency Observational Evidence Summary** card in Executive Overview, pointing out the 6,026 monitoring stations and decadal depth trend distribution.
- **Speaking Notes**:
  > *"Next, we subjected our macro-suitability models to independent empirical triangulation using 70,513 quarterly groundwater observation records from 6,026 government monitoring wells across the CGWB and GSDA spanning up to 55 years.*
  >
  > *First, we established the mathematical sign convention: groundwater is measured in meters below ground level (m bgl). A positive Theil-Sen slope ($\beta > 0$) means depth is increasing—indicating water-table depletion. A negative slope ($\beta < 0$) means depth is decreasing—indicating recovery.*
  >
  > *When we correlated physical MAR suitability with decadal depth trends across all 355 monitored catchments, we observed a weak, statistically non-significant correlation: Spearman $\rho = -0.0748, p = 0.1598$.*
  >
  > *Crucially, this is not a model failure—it reveals a fundamental hydrogeological reality of the Deccan Volcanic Province:*
  > *First, intensive agricultural pumping for cash crops like sugarcane occurs in flat, heavy clay vertisol plains where surface infiltration is slowest. Depletion is most acute where recharge is geologically hardest to achieve.*
  > *Second, shallow government dugwells recharge rapidly every monsoon ($\Delta h \approx +4.06\text{ m}$), whereas private tube-wells pump from deep fractured basalt (>80 m) that is disconnected from shallow recharge.*
  > *Therefore, physical suitability tells us where recharge is geologically viable, not where historical extraction has been most aggressive."*
- **Main Takeaway**:
  Independent empirical testing reveals the decoupled dual-aquifer dynamics of fractured basalts.

---

### Segment 5: Live Dashboard Walkthrough — Dual Map & Profiler (4:45 – 6:15)

- **What to Show on Screen**:
  - In Dashboard: Switch sidebar radio to **View 2: 🗺️ Interactive Catchment Map**.
  - Toggle between **Plotly Vector Choropleth** and **Folium OpenStreetMap Leaflet**.
  - Show the **Catchment Quick-Inspection Panel** on Folium.
  - Switch sidebar radio to **View 3: 🔍 Catchment Deep-Dive Profiler**.
  - Select Catchment `4081076330` (or `4081044860`).
- **Speaking Notes**:
  > *"Let us explore the operational system. Our dashboard features a Dual Map Engine:*
  > *1. High-speed Plotly WebGL vector choropleth for rapid thematic switching—coloring by Consensus Tiers, MAR Category, SWH Category, or Decadal Trends.*
  > *2. Folium OpenStreetMap Leaflet GIS engine, allowing field engineers to view real-world satellite terrain, roads, and village landmarks, with a click-to-inspect panel.*
  >
  > *Now let us look at the Catchment Profiler for basin 4081076330. In Card 1, you see its multi-scenario scores. In Card 2, you see its ground-truth observational record: 3 active monitoring wells, an acute decadal water table depletion of +0.805 meters per year, and an annual monsoon rise of +2.82 meters.*
  >
  > *In Card 3, soil texture reveals permeable sandy loam (sand $\ge 280\text{ g/kg}$). In Card 4, the transparent decision trace confirms why this basin was assigned MAR Category A: robust Tier 1 priority, verified water-table depletion, and viable surface infiltration."*
- **Main Takeaway**:
  Complete operational transparency from statewide choropleth down to individual well observations.

---

### Segment 6: Multi-Catchment Comparison & DPR Dossiers (6:15 – 7:30)

- **What to Show on Screen**:
  - Switch to **View 4: ⚖️ Multi-Catchment Comparison**. Add catchments `4081044860`, `4081048280`, and `4081056630`.
  - Switch to **View 5: 📑 DPR Screening Dossiers & Data Export**.
  - Open a generated MAR dossier (e.g., `DPR_MAR_HYBAS_4081044860.md`).
  - Show the **One-Click Download** buttons and the **Printable Summary Sheet** tab.
- **Speaking Notes**:
  > *"In View 4, planning officers can compare 2 to 5 catchments side-by-side across their radar scores and physical parameters before committing capital.*
  >
  > *In View 5, the system provides one-click export of filtered tabular datasets, printable executive summaries, and standardized preliminary DPR screening dossiers.*
  >
  > *Our automated batch generator produced 87 preliminary screening dossiers: 12 MAR Category A dossiers and 75 SWH Category A dossiers.*
  > *Notice that every single dossier contains zero fabricated budgets, zero hallucinated IDs, and zero invented coordinates. Instead, every dossier embeds our mandatory 5-point pre-construction checklist: geophysical VES resistivity profiling, double-ring infiltration tests, private borewell census, structure siltation audits, and water quality baselines."*
- **Main Takeaway**:
  Automated, reproducible transition from macro-screening to standardized field engineering briefs.

---

### Segment 7: Scientific Safeguards, Invariants & Limitations (7:30 – 8:30)

- **What to Show on Screen**:
  - Show Section 12 of `README.md` or Section 10 of `docs/19_PHASE10_RELEASE_READINESS_REPORT.md` (or terminal showing `pytest tests/ -v`).
- **Speaking Notes**:
  > *"To ensure rigorous scientific integrity, we implemented five non-negotiable safeguards:*
  > *1. Hydrogeological Separation: MAR and SWH are evaluated on separate criteria. SWH relies on clay vertisols ($\ge 380\text{ g/kg}$) to prevent seepage in unlined earthen bunds; MAR requires permeable soils or dedicated recharge shafts.*
  > *2. Zero Fabrication & Unknown MRSAC Inventory: Because the official MRSAC Jalyukt Shivar GIS portal requires state intranet credentials, we enforce the explicit invariant: 'unrecorded digital inventory must never be interpreted as zero physical structures.' Consequently, Category B (maintenance only) is strictly unassigned.*
  > *3. Baseline Immutability: All four Phase 3 and Phase 4 baseline datasets are cryptographically pinned with SHA-256 hashes and verified bit-for-bit.*
  > *4. No Silent Zeroes: Missing values remain explicit NaNs or 'Inconclusive'—they are never silently converted to zero.*
  > *5. Automated Testing: 52 automated tests cover our data loading, geometry validity, decision logic, and UI workflows."*
- **Main Takeaway**:
  Strict engineering invariants protect against false precision and data hallucination.

---

### Segment 8: Conclusion, Future Work & Q&A Transition (8:30 – 9:30)

- **What to Show on Screen**:
  - Summary slide or the top of `docs/20_FINAL_PROJECT_REPORT.md`.
- **Speaking Notes**:
  > *"In conclusion, JalDrishti-AI demonstrates how multi-scale geospatial data engineering, multi-scenario decision modeling, and empirical observational validation can elevate watershed planning from ad-hoc administrative spending to a transparent, scientifically defensible discipline.*
  >
  > *In future work, we aim to integrate authenticated MRSAC APIs to model structure-density saturation, ingest 12.5-meter ALOS PALSAR DEMs for automated micro-lineament extraction, and expand the pipeline to pan-India scale.*
  >
  > *Thank you for your time and attention. I am now ready to answer any questions from the committee."*
- **Main Takeaway**:
  Professional, confident conclusion inviting rigorous technical inquiry.

---

## Committee Q&A Preparation: Anticipated Technical Questions

### Q1: Why did your MAR suitability score show a negative/non-significant correlation with observed groundwater depletion?
**Answer**:
> *"This is one of the most significant hydrogeological findings of our study. In the Deccan Traps, intense agricultural pumping occurs in flat vertisol plains with high clay content (>400 g/kg). These areas have the most acute depletion, yet surface recharge is geologically constrained. Meanwhile, government dugwells tap the shallow weathered basalt which recharges rapidly during every monsoon (+4.06 m rise), whereas farmers pump from deeper fractured basalt (>80 m). Our physical suitability score accurately reflects where recharge is geologically viable, not where historical extraction has been most aggressive."*

### Q2: Why are there only 12 MAR Category A catchments when there are 75 SWH Category A catchments?
**Answer**:
> *"Because Managed Aquifer Recharge (MAR) and Surface Water Harvesting (SWH) have fundamentally opposite soil physics requirements. Over 70% of Maharashtra's plateau is covered in heavy black cotton clay vertisols. This impermeable clay is ideal for surface water harvesting because it prevents foundation seepage in earthen check dams and farm ponds. However, for surface percolation tanks, clay is an impermeable barrier that causes water to evaporate rather than infiltrate. The 56 Tier 1 catchments with heavy clay were appropriately classified as MAR Category C—flagging that they require subsurface recharge shafts or borewells rather than conventional surface percolation tanks."*

### Q3: Why did you not assign any catchments to Category B (Maintenance / Desilting)?
**Answer**:
> *"Assigning Category B requires verifiable spatial records of existing check dams, percolation tanks, and their siltation status. The official MRSAC Jalyukt Shivar GIS portal is protected behind Government of Maharashtra intranet credentials. We adopted the strict scientific invariant that 'absent digital records must never be assumed to equal zero physical structures.' Inventing structure counts would be unscientific and potentially dangerous; therefore, Category B remains unassigned until official institutional GIS access is granted."*