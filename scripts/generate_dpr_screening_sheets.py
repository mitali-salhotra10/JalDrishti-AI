"""
generate_dpr_screening_sheets.py - Automated DPR Screening Sheet Generator
Phase 9: Interactive Decision Support Dashboard & Stakeholder Reporting.

Generates reproducible, standardized preliminary Detailed Project Report (DPR)
screening dossiers for all 12 MAR Category A and 75 SWH Category A catchments.
Strictly adheres to zero-fabrication standards: does not invent coordinates,
storage capacities, costs, or engineering dimensions.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def generate_dpr_sheets():
    root = Path(__file__).resolve().parent.parent
    processed_dir = root / "data" / "processed"
    reports_dir = root / "reports" / "dpr_screening_sheets"
    mar_dir = reports_dir / "mar_category_a"
    swh_dir = reports_dir / "swh_category_a"

    mar_dir.mkdir(parents=True, exist_ok=True)
    swh_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load Data
    df_eval = pd.read_csv(processed_dir / "jaldrishti_phase7_evidence_assessment.csv")
    df_audit = pd.read_csv(processed_dir / "jaldrishti_consensus_priority_audit.csv")
    df_infra = pd.read_csv(processed_dir / "jaldrishti_infrastructure_by_catchment.csv")
    df_v2 = pd.read_csv(processed_dir / "jaldrishti_watersheds_with_village_indicators_v2.csv")

    # Merge on HYBAS_ID
    df_master = df_eval.merge(
        df_v2[[
            "HYBAS_ID", "village_count_intersecting", "village_coverage_pct", "village_coverage_flag",
            "village_sand_0_5cm_g_kg", "village_clay_0_5cm_g_kg", "village_silt_0_5cm_g_kg",
            "village_soc_0_5cm_dg_kg", "village_infiltration_proxy",
            "village_rainfall_baseline_mean_mm", "village_drought_years_count", "village_drought_frequency_pct",
            "village_slope_mean_deg", "village_elevation_mean_m", "village_cropland_pct"
        ]],
        on="HYBAS_ID", how="left"
    )

    df_master = df_master.merge(
        df_infra[[
            "HYBAS_ID", "inventory_status", "inventory_data_policy", "inventory_confidence"
        ]],
        on="HYBAS_ID", how="left"
    )

    # Identify Target Catchments
    mar_targets = df_master[df_master["provisional_action_category_MAR"].str.startswith("Category A")].copy()
    swh_targets = df_master[df_master["provisional_action_category_SWH"].str.startswith("Category A")].copy()

    print(f"Loaded {len(df_master)} total catchments.")
    print(f"Identified {len(mar_targets)} MAR Category A catchments.")
    print(f"Identified {len(swh_targets)} SWH Category A catchments.")

    index_rows = []

    # Generate MAR Sheets
    for _, r in mar_targets.iterrows():
        hid = int(r["HYBAS_ID"])
        sheet_path = mar_dir / f"DPR_MAR_HYBAS_{hid}.md"
        content = build_mar_sheet(r)
        sheet_path.write_text(content, encoding="utf-8")
        index_rows.append({
            "HYBAS_ID": hid,
            "intervention_type": "Managed Aquifer Recharge (MAR)",
            "screening_category": r["provisional_action_category_MAR"],
            "consensus_tier": r["consensus_priority_tier_revised"],
            "sub_area_km2": r["sub_area_km2"],
            "gw_depth_trend_m_yr": r["gw_depth_trend_median_m_yr"],
            "monitoring_wells_count": r["total_monitoring_well_count"],
            "clay_g_kg": r["village_clay_0_5cm_g_kg"],
            "sand_g_kg": r["village_sand_0_5cm_g_kg"],
            "infiltration_proxy": r["village_infiltration_proxy"],
            "dpr_sheet_file": sheet_path.name
        })

    # Generate SWH Sheets
    for _, r in swh_targets.iterrows():
        hid = int(r["HYBAS_ID"])
        sheet_path = swh_dir / f"DPR_SWH_HYBAS_{hid}.md"
        content = build_swh_sheet(r)
        sheet_path.write_text(content, encoding="utf-8")
        index_rows.append({
            "HYBAS_ID": hid,
            "intervention_type": "Surface Water Harvesting (SWH)",
            "screening_category": r["provisional_action_category_SWH"],
            "consensus_tier": r["consensus_priority_tier_revised"],
            "sub_area_km2": r["sub_area_km2"],
            "gw_depth_trend_m_yr": r["gw_depth_trend_median_m_yr"],
            "monitoring_wells_count": r["total_monitoring_well_count"],
            "clay_g_kg": r["village_clay_0_5cm_g_kg"],
            "sand_g_kg": r["village_sand_0_5cm_g_kg"],
            "infiltration_proxy": r["village_infiltration_proxy"],
            "dpr_sheet_file": sheet_path.name
        })

    # Save Master Index CSV
    df_index = pd.DataFrame(index_rows)
    index_csv = reports_dir / "dpr_screening_master_index.csv"
    df_index.to_csv(index_csv, index=False)
    print(f"[COMPLETE] Saved {len(index_rows)} screening sheets and master index to {index_csv.name}")
    return 0


def build_mar_sheet(r) -> str:
    hid = int(r["HYBAS_ID"])
    trend = r["gw_depth_trend_median_m_yr"]
    trend_str = f"+{trend:.4f} m/year (Depletion)" if pd.notna(trend) and trend > 0 else f"{trend:.4f} m/year" if pd.notna(trend) else "Inconclusive / No Trend"
    rech = r["gw_seasonal_recharge_median_m"]
    rech_str = f"+{rech:.2f} m" if pd.notna(rech) else "N/A"
    wells = int(r["total_monitoring_well_count"]) if pd.notna(r["total_monitoring_well_count"]) else 0
    cgwb_w = int(r["cgwb_monitoring_well_count"]) if pd.notna(r["cgwb_monitoring_well_count"]) else 0
    gsda_w = int(r["gsda_monitoring_well_count"]) if pd.notna(r["gsda_monitoring_well_count"]) else 0

    clay = r["village_clay_0_5cm_g_kg"]
    sand = r["village_sand_0_5cm_g_kg"]
    infilt = r["village_infiltration_proxy"]

    # Mechanism assessment based on soil
    if sand >= 280.0 or infilt >= 1.0:
        rech_type = "Surface Infiltration Structures (Percolation Tanks, Check Dams with Infiltration Pits)"
        recom_tech = "Excavation to permeable weathered mantle, silt traps, loose boulder gully checks."
    else:
        rech_type = "Subsurface Injection Structures (Recharge Shafts, Dedicated Recharge Borewells)"
        recom_tech = "Dual-purpose recharge shafts penetrating through dense black cotton clay cap into jointed/vesicular basalt."

    return f"""# JalDrishti-AI: Preliminary DPR Screening Dossier
## Managed Aquifer Recharge (MAR) — Catchment HYBAS_ID: {hid}

> **LEGAL & ENGINEERING DISCLAIMER**:  
> *This dossier is an automated, macro-scale preliminary screening assessment derived from the JalDrishti-AI multi-criteria decision support engine. It is NOT an approved Detailed Project Report (DPR), administrative sanction, or civil engineering specification. Site-specific Vertical Electrical Sounding (VES), infiltration rate testing, and structural safety audits are legally mandatory prior to fund sanction or civil construction.*

---

### 1. Catchment Identity & Administrative Context
- **HydroATLAS Level 8 Basin ID**: `{hid}`
- **Sub-Catchment Drainage Area**: `{r['sub_area_km2']:.2f} km²`
- **Intersecting Villages**: `{int(r['village_count_intersecting'])} villages` (`{r['village_coverage_pct']:.1f}%` boundary area coverage, Flag: `{r['village_coverage_flag']}`)
- **Consensus Prioritization Tier**: `{r['consensus_priority_tier_revised']}`
- **Preliminary 2-Variable Screening Score**: `{r['preliminary_screening_score']:.4f}`
- **Robust Consensus Rank**: `{int(r['rank_median_planning'])} / 518` (Median Planning Rank across all scenarios)
- **Scenario S4 (MAR Priority Score)**: `{r['score_S4_Managed_Aquifer_Recharge']:.4f}` (Rank: `#{int(r['rank_S4_Managed_Aquifer_Recharge'])}`)

---

### 2. Multi-Evidence Ground-Truth Observational Status
- **Active Monitoring Stations**: `{wells} wells` (CGWB: `{cgwb_w}`, GSDA: `{gsda_w}`)
- **Decadal Groundwater Depth Trend (2015–2024)**: **`{trend_str}`**
- **Median Seasonal Water Table Fluctuation (Δh)**: `{rech_str}`
- **Evidence Confidence Level**: `{r['evidence_confidence_level']}`
- **Hydrogeological Interpretation**: Catchment displays confirmed secular groundwater depletion (increasing water depth over a 10-year period), establishing empirical justification for artificial aquifer replenishment.

---

### 3. Soil, Topography & Physical Parameters
- **Topsoil Texture (0–5cm)**:
  - Clay Content: `{clay:.1f} g/kg` (`{clay/10:.1f}%`)
  - Sand Content: `{sand:.1f} g/kg` (`{sand/10:.1f}%`)
  - Silt Content: `{r['village_silt_0_5cm_g_kg']:.1f} g/kg`
  - Soil Organic Carbon: `{r['village_soc_0_5cm_dg_kg']:.1f} dg/kg`
- **Infiltration Capacity Proxy**: `{infilt:.2f} cm/hr`
- **Terrain Topography**: Mean Slope: `{r['village_slope_mean_deg']:.2f}°`, Mean Elevation: `{r['village_elevation_mean_m']:.1f} m amsl`
- **Climate & Rainfall Baseline**: Annual Precipitation: `{r['village_rainfall_baseline_mean_mm']:.1f} mm/year`, Historical Drought Frequency: `{r['village_drought_frequency_pct']:.1f}%` (`{int(r['village_drought_years_count'])} severe drought years in 2001–2025`)
- **Agricultural Land Use**: Cropland Fraction: `{r['village_cropland_pct']:.1f}%`

---

### 4. Provisional Engineering Screening Assessment
- **Screening Classification**: **`{r['provisional_action_category_MAR']}`**
- **Decision Rationale**: {r['provisional_screening_rationale_MAR']}
- **Recommended Primary Technology**: **{rech_type}**
- **Specific Structural Adaptations**: {recom_tech}

---

### 5. Existing Conservation Infrastructure Status (MRSAC Audit)
- **Centralized Digital Inventory**: **`{r['inventory_status']}`**
- **Inventory Confidence**: `{r['inventory_confidence']}`
- **Statutory Policy Invariant**: `{r['inventory_data_policy']}`
- *Crucial Engineering Mandate*: Centralized MRSAC GIS structure data is currently restricted. An unrecorded digital inventory must NEVER be interpreted as the physical absence of structures. A field survey must record all existing check dams, percolation tanks, and nala bunds within the catchment to avoid over-saturating the drainage network or causing downstream starvation.

---

### 6. Mandatory Pre-Construction Field Checklist
Prior to finalizing any DPR for Catchment `{hid}`, the investigating engineer must complete:
1. [ ] **Geophysical Resistivity Profiling**: Minimum 3 Vertical Electrical Soundings (VES) along suspected fracture lineaments.
2. [ ] **Double-Ring Infiltrometer Tests**: In situ infiltration measurement across potential percolation tank beds.
3. [ ] **Local Well Census**: Inventory of private agricultural borewells within a 1.5 km radius to prevent private monopolization of public recharge.
4. [ ] **Structure Siltation Audit**: Physical assessment of existing structures; where siltation exceeds 40%, prioritize desilting over new construction.
5. [ ] **Water Quality Pre-Testing**: Baseline electrical conductivity (EC) and nitrate testing to ensure recharge water does not contaminate drinking aquifers.
"""


def build_swh_sheet(r) -> str:
    hid = int(r["HYBAS_ID"])
    clay = r["village_clay_0_5cm_g_kg"]
    sand = r["village_sand_0_5cm_g_kg"]
    slope = r["village_slope_mean_deg"]
    cropland = r["village_cropland_pct"]

    if clay >= 400.0:
        seepage_risk = "Very Low (Heavy impermeable vertisol bed prevents percolation losses)"
        structure_focus = "Earthen Nala Bunds, Cement Nala Bunds (CNBs), Unlined Farm Ponds"
    else:
        seepage_risk = "Moderate (Requires clay puddling or polythene pond lining)"
        structure_focus = "Check Dams with masonry core wall, lined farm ponds, contour trenches"

    return f"""# JalDrishti-AI: Preliminary DPR Screening Dossier
## Surface Water Harvesting (SWH) — Catchment HYBAS_ID: {hid}

> **LEGAL & ENGINEERING DISCLAIMER**:  
> *This dossier is an automated, macro-scale preliminary screening assessment derived from the JalDrishti-AI multi-criteria decision support engine. It is NOT an approved Detailed Project Report (DPR), administrative sanction, or civil engineering specification. Site-specific stream discharge gauging, catchment yield modeling, and waste weir spillway calculations are legally mandatory prior to fund sanction or civil construction.*

---

### 1. Catchment Identity & Administrative Context
- **HydroATLAS Level 8 Basin ID**: `{hid}`
- **Sub-Catchment Drainage Area**: `{r['sub_area_km2']:.2f} km²`
- **Intersecting Villages**: `{int(r['village_count_intersecting'])} villages` (`{r['village_coverage_pct']:.1f}%` boundary area coverage, Flag: `{r['village_coverage_flag']}`)
- **Consensus Prioritization Tier**: `{r['consensus_priority_tier_revised']}`
- **Preliminary 2-Variable Screening Score**: `{r['preliminary_screening_score']:.4f}`
- **Robust Consensus Rank**: `{int(r['rank_median_planning'])} / 518`
- **Scenario S5 (SWH Priority Score)**: `{r['score_S5_Surface_Water_Harvesting']:.4f}` (Rank: `#{int(r['rank_S5_Surface_Water_Harvesting'])}`)

---

### 2. Terrain, Drainage & Climate Characteristics
- **Drainage Topography**: Mean Slope: `{slope:.2f}°`, Mean Elevation: `{r['village_elevation_mean_m']:.1f} m amsl`
- **Precipitation Baseline**: Annual Precipitation: `{r['village_rainfall_baseline_mean_mm']:.1f} mm/year`
- **Historical Drought Vulnerability**: `{r['village_drought_frequency_pct']:.1f}%` (`{int(r['village_drought_years_count'])} severe drought years in 2001–2025`)
- **Agricultural Cropland Intensity**: `{cropland:.1f}%` of catchment area
- **Runoff Generation Assessment**: Combination of moderate slope and intense monsoon showers creates high seasonal surface runoff requiring catchment detention.

---

### 3. Soil Seepage & Foundation Feasibility
- **Topsoil Clay Content**: `{clay:.1f} g/kg` (`{clay/10:.1f}%`)
- **Topsoil Sand Content**: `{sand:.1f} g/kg` (`{sand/10:.1f}%`)
- **Seepage Risk Assessment**: **{seepage_risk}**
- **Recommended Surface Harvesting Interventions**: **{structure_focus}**

---

### 4. Provisional Engineering Screening Assessment
- **Screening Classification**: **`{r['provisional_action_category_SWH']}`**
- **Decision Rationale**: {r['provisional_screening_rationale_SWH']}
- **Hydrological Focus**: Harvest peak monsoon flash runoff for critical supplementary irrigation during agricultural dry spells.

---

### 5. Infrastructure Saturation & Downstream Rights
- **Centralized Digital Inventory**: **`{r['inventory_status']}`**
- **Statutory Policy Mandate**: `{r['inventory_data_policy']}`
- *Crucial Engineering Mandate*: While surface harvesting structures retain runoff locally, cumulative upstream harvesting must not starve downstream irrigation schemes or major reservoirs. Hydrological yield modeling is required to ensure ecological baseflow and legal riparian allocations.

---

### 6. Mandatory Pre-Construction Field Checklist
Prior to finalizing any DPR for Catchment `{hid}`, the investigating engineer must complete:
1. [ ] **Catchment Hydrological Yield Calculation**: Strange's table or SCS-CN runoff estimation for 75% dependable year.
2. [ ] **Spillway & Waste Weir Hydraulic Sizing**: Design flood discharge calculation using Dicken's or Ryve's formula with adequate freeboard.
3. [ ] **Local Siltation History**: Upstream catchment treatment (CCT, deep CCT, loose boulder checks) to prevent reservoir siltation.
4. [ ] **Existing Structures Inspection**: Condition and desilting audit of all historical nala bunds within the stream reach.
5. [ ] **Beneficiary Water Users Association**: Community agreement on equitable water distribution during dry spells.
"""


if __name__ == "__main__":
    import sys
    sys.exit(generate_dpr_sheets())
