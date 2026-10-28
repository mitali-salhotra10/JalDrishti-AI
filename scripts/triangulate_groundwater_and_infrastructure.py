# JalDrishti-AI: Multi-Evidence Triangulation and Infrastructure Saturation Pipeline
# Author: JalDrishti-AI Engineering Team
# License: Apache-2.0
"""
Triangulates official CGWB and GSDA groundwater observation records with HydroATLAS
Level 8 catchments and formalizes the infrastructure inventory availability audit.
Produces:
1. data/processed/jaldrishti_infrastructure_by_catchment.csv
2. data/processed/jaldrishti_phase7_evidence_assessment.csv
Categorizes Consensus Tier 1 catchments into provisional screening action categories
(A: Potential New Infrastructure, B: Maintenance/Desilting, C: Mixed Evidence, D: Insufficient Evidence)
while strictly preserving all baseline rankings, scores, and keeping MAR and SWH separate.
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np

TARGET_METRIC_CRS = "EPSG:32643"  # UTM Zone 43N

def get_project_root() -> Path:
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists() or (parent / "data").exists():
            return parent
    return Path.cwd()

def triangulate_evidence(project_root: Path = None) -> int:
    if project_root is None:
        project_root = get_project_root()

    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"

    print("=" * 78)
    print("JALDRISHTI-AI: MULTI-EVIDENCE TRIANGULATION & INFRASTRUCTURE SATURATION")
    print("=" * 78)

    # 1. Load Catchments
    basins_shp = processed_dir / "jaldrishti_scored_watersheds.shp"
    if not basins_shp.exists():
        print(f"[ERROR] Catchment shapefile missing at {basins_shp}")
        return 1
    gdf_basins = gpd.read_file(basins_shp)
    gdf_basins_utm = gdf_basins.to_crs(TARGET_METRIC_CRS)
    n_basins = len(gdf_basins)
    print(f"Loaded {n_basins} Level 8 catchments from {basins_shp.name}")

    # 2. Load Consensus Priority Audit Table (Baseline)
    audit_csv = processed_dir / "jaldrishti_consensus_priority_audit.csv"
    if not audit_csv.exists():
        print(f"[ERROR] Consensus audit CSV missing at {audit_csv}")
        return 1
    df_audit = pd.read_csv(audit_csv)
    print(f"Loaded {len(df_audit)} catchments from {audit_csv.name}")

    # 3. Load CGWB Observations
    cgwb_csv = raw_dir / "cgwb_maharashtra_observation_wells.csv"
    if not cgwb_csv.exists():
        print(f"[ERROR] Harmonized CGWB CSV missing at {cgwb_csv}")
        return 1
    df_cgwb = pd.read_csv(cgwb_csv)
    st_cgwb = df_cgwb.groupby("station_id")[["latitude", "longitude"]].first().reset_index()
    gdf_cgwb = gpd.GeoDataFrame(
        st_cgwb,
        geometry=gpd.points_from_xy(st_cgwb["longitude"], st_cgwb["latitude"]),
        crs="EPSG:4326"
    ).to_crs(TARGET_METRIC_CRS)
    cgwb_joined = gpd.sjoin(gdf_cgwb, gdf_basins_utm[["HYBAS_ID", "geometry"]], how="inner", predicate="within")
    cgwb_counts = cgwb_joined.groupby("HYBAS_ID").size().to_dict()
    print(f"Mapped {len(cgwb_joined)} CGWB stations across {len(cgwb_counts)} catchments.")

    # 4. Load GSDA Observations
    gsda_csv = raw_dir / "ground_water_level_manual_quarterly_maharashtra_1970_2025.csv"
    if not gsda_csv.exists():
        print(f"[ERROR] GSDA CSV missing at {gsda_csv}")
        return 1
    df_gsda = pd.read_csv(gsda_csv, encoding="latin-1", low_memory=False)
    df_gsda.columns = df_gsda.columns.str.strip()
    df_gsda["dt"] = pd.to_datetime(df_gsda["Date of Monitoring"], format="%d-%m-%Y", errors="coerce")
    gsda_dec = df_gsda[(df_gsda["dt"] >= "2015-01-01") & (df_gsda["dt"] <= "2024-12-31")].copy()
    gsda_dec["wl"] = pd.to_numeric(gsda_dec["Water Level, m bgl"], errors="coerce")
    gsda_valid = gsda_dec[gsda_dec["wl"].notna() & (gsda_dec["wl"] >= 0)].copy()

    st_gsda = gsda_valid.groupby("Well ID")[["Latitude", "Longitude"]].first().reset_index()
    st_gsda.rename(columns={"Latitude": "latitude", "Longitude": "longitude", "Well ID": "gsda_well_id"}, inplace=True)
    gdf_gsda = gpd.GeoDataFrame(
        st_gsda,
        geometry=gpd.points_from_xy(st_gsda["longitude"], st_gsda["latitude"]),
        crs="EPSG:4326"
    ).to_crs(TARGET_METRIC_CRS)
    gsda_joined = gpd.sjoin(gdf_gsda, gdf_basins_utm[["HYBAS_ID", "geometry"]], how="inner", predicate="within")
    gsda_counts = gsda_joined.groupby("HYBAS_ID").size().to_dict()
    print(f"Mapped {len(gsda_joined)} GSDA wells across {len(gsda_counts)} catchments.")

    # 5. Load Groundwater Results (Validation Results from Phase 6)
    gw_res_csv = processed_dir / "jaldrishti_groundwater_validation_results.csv"
    df_gw_res = pd.read_csv(gw_res_csv) if gw_res_csv.exists() else pd.DataFrame()
    gw_trends = df_gw_res.set_index("HYBAS_ID")["gw_depth_trend_median_m_yr"].to_dict() if len(df_gw_res) > 0 else {}
    gw_recharge = df_gw_res.set_index("HYBAS_ID")["gw_seasonal_recharge_median_m"].to_dict() if len(df_gw_res) > 0 else {}

    # 6. Check MRSAC Jalyukt Shivar GIS Layer Availability
    mrsac_shp = raw_dir / "mrsac_jalyukt_shivar_structures.shp"
    mrsac_available = mrsac_shp.exists()
    print(f"\nMRSAC Jalyukt Shivar Layer Availability: {'AVAILABLE' if mrsac_available else 'UNAVAILABLE (AUTHENTICATION RESTRICTED)'}")
    if not mrsac_available:
        print("  Notice: Official shapefile is not present in data/raw/. In accordance with engineering")
        print("  ethics, NO structures or capacities are fabricated. All 518 catchments are explicitly")
        print("  flagged as INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS with zero recorded capacity.")
        print("  MANDATE: Absent inventory data must NOT be interpreted as zero physical infrastructure on the ground.")

    # 7. Build Catchment-Level Infrastructure & Coverage Table
    infra_rows = []
    for idx, row in df_audit.iterrows():
        hybas_id = int(row["HYBAS_ID"])
        sub_area = float(row["sub_area_km2"])

        cgwb_w = cgwb_counts.get(hybas_id, 0)
        gsda_w = gsda_counts.get(hybas_id, 0)
        total_w = cgwb_w + gsda_w

        if cgwb_w > 0 and gsda_w > 0:
            cov_flag = "CGWB_AND_GSDA"
        elif gsda_w > 0:
            cov_flag = "GSDA_ONLY"
        elif cgwb_w > 0:
            cov_flag = "CGWB_ONLY"
        else:
            cov_flag = "NO_MONITORING_WELL"

        gw_trend = gw_trends.get(hybas_id, np.nan)
        gw_rech = gw_recharge.get(hybas_id, np.nan)

        infra_rows.append({
            "HYBAS_ID": hybas_id,
            "sub_area_km2": sub_area,
            "structure_count_total": 0,
            "structure_count_check_dam": 0,
            "structure_count_percolation_tank": 0,
            "structure_count_farm_pond": 0,
            "structure_count_other": 0,
            "designed_storage_capacity_m3": 0.0,
            "designed_storage_capacity_m3_per_km2": 0.0,
            "pct_structures_with_known_capacity": 0.0,
            "pct_structures_with_known_status": 0.0,
            "pct_structures_with_damage_or_silt_status": 0.0,
            "inventory_status": "INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS",
            "inventory_confidence": "UNKNOWN",
            "inventory_data_policy": "ABSENT_INVENTORY_IS_NOT_ZERO_INFRASTRUCTURE",
            "cgwb_monitoring_well_count": cgwb_w,
            "gsda_monitoring_well_count": gsda_w,
            "total_monitoring_well_count": total_w,
            "monitoring_network_coverage_flag": cov_flag,
            "gw_depth_trend_median_m_yr": gw_trend,
            "gw_seasonal_recharge_median_m": gw_rech
        })

    df_infra = pd.DataFrame(infra_rows)
    out_infra_csv = processed_dir / "jaldrishti_infrastructure_by_catchment.csv"
    df_infra.to_csv(out_infra_csv, index=False)
    print(f"\n[SAVED] Catchment infrastructure ledger saved to {out_infra_csv.name}")
    print(f"  Rows: {len(df_infra)}, Columns: {len(df_infra.columns)}")

    # 8. Develop Evidence Assessment & Provisional Action Screening Categories
    # Assesses Consensus Tier 1 catchments (and all catchments) into screening categories A-D
    assessment_rows = []
    for idx, row in df_audit.iterrows():
        hybas_id = int(row["HYBAS_ID"])
        tier_rev = str(row.get("consensus_priority_tier_revised", "Tier 3: Moderate Priority"))
        is_tier1 = "Tier 1" in tier_rev

        sub_area = float(row["sub_area_km2"])
        clay = float(row["village_clay_0_5cm_g_kg"]) if pd.notna(row["village_clay_0_5cm_g_kg"]) else 350.0
        sand = float(row["village_sand_0_5cm_g_kg"]) if pd.notna(row["village_sand_0_5cm_g_kg"]) else 250.0
        infilt = float(row["village_infiltration_proxy"]) if pd.notna(row["village_infiltration_proxy"]) else 1.0
        drought_yrs = float(row["village_drought_years_count"]) if pd.notna(row["village_drought_years_count"]) else 0.0
        cropland = float(row["village_cropland_pct"]) if pd.notna(row["village_cropland_pct"]) else 50.0
        slope = float(row["village_slope_mean_deg"]) if pd.notna(row["village_slope_mean_deg"]) else 3.0
        cov_str = str(row["village_coverage_flag"]).strip()
        is_low_cov = (cov_str in ["partial_border", "transboundary_uncovered"]) or (float(row.get("village_coverage_pct", 100)) < 50.0)

        cgwb_w = cgwb_counts.get(hybas_id, 0)
        gsda_w = gsda_counts.get(hybas_id, 0)
        total_w = cgwb_w + gsda_w

        gw_trend = gw_trends.get(hybas_id, np.nan)
        gw_rech = gw_recharge.get(hybas_id, np.nan)

        # Confidence level in evidence
        if is_low_cov or total_w == 0:
            conf_level = "Low (Missing Local Monitoring or Low Village Coverage)"
        elif total_w >= 3 and pd.notna(gw_trend):
            conf_level = "High (Dense Well Network & Decadal Trend)"
        else:
            conf_level = "Moderate (Intermediate Network Coverage)"

        # Provisional Action Categorization for Managed Aquifer Recharge (MAR)
        # Evaluated as screening outcomes requiring field hydrogeological appraisal.
        # Trend sign: Positive slope = depth below ground level increasing = water table depleting.
        #             Negative slope = depth below ground level decreasing = water table rising/recovering.
        if is_low_cov or total_w < 2:
            cat_mar = "Category D: Insufficient Evidence"
            rat_mar = "Catchment has low village data coverage (<50%) or sparse monitoring (<2 wells); observational network required before screening."
        elif not is_tier1:
            cat_mar = "Category C: Mixed Evidence (Non-Tier-1)"
            rat_mar = "Non-Tier-1 catchment; baseline screening priority is moderate or low."
        else:  # is_tier1 and sufficient monitoring (>= 2 wells, >= 50% coverage)
            if pd.notna(gw_trend) and gw_trend > 0:
                cat_mar = "Category A: Potential New Infrastructure Assessment (MAR)"
                if sand >= 280.0 or infilt >= 1.0:
                    rat_mar = "Tier 1 priority with observed decadal water-table depletion (depth trend > 0) and favorable infiltration capacity; field appraisal recommended for percolation tanks/check dams."
                else:
                    rat_mar = "Tier 1 priority with observed decadal water-table depletion (depth trend > 0) in clay vertisol terrain; slow surface infiltration indicates field appraisal should evaluate subsurface recharge shafts/borewells into fractured basalt."
            elif pd.notna(gw_trend) and gw_trend < 0:
                cat_mar = "Category C: Mixed or Conflicting Evidence Requiring Field Assessment"
                rat_mar = "Tier 1 macro-model priority conflicts with observed decadal water-table rise/recovery (depth trend < 0); field survey required to verify local recharge, canal influence, or extraction rates before civil works."
            else:
                cat_mar = "Category C: Mixed or Conflicting Evidence Requiring Field Assessment"
                rat_mar = "Tier 1 priority with active monitoring wells, but decadal depth trend is statistically inconclusive (<5 observation years); seasonal fluctuation monitoring and local hydrogeological survey required."

        # Provisional Action Categorization for Surface Water Harvesting (SWH)
        # Criteria: Independent of groundwater depth trend; based on surface runoff, clay impermeability, and cropland draft
        if is_low_cov:
            cat_swh = "Category D: Insufficient Evidence"
            rat_swh = "Low village mapping coverage (<50%); requires border/field baseline verification."
        elif not is_tier1:
            cat_swh = "Category C: Mixed Evidence (Non-Tier-1)"
            rat_swh = "Non-Tier-1 catchment; moderate surface water harvesting screening priority."
        else:  # is_tier1 and adequate coverage
            if clay < 280.0:
                cat_swh = "Category C: Mixed or Conflicting Evidence Requiring Field Assessment"
                rat_swh = "Consensus priority is high, but coarse/permeable soils present high seepage risk for unlined earthen structures; pond lining or gully plugs required."
            elif clay >= 380.0 and cropland >= 60.0:
                cat_swh = "Category A: Potential New Infrastructure Assessment (SWH)"
                rat_swh = "Impermeable clay vertisols and heavy agricultural draft provide suitable conditions for surface water harvesting structures (check dams, unlined farm ponds); field site appraisal recommended."
            else:
                cat_swh = "Category A: Potential New Infrastructure Assessment (SWH)"
                rat_swh = "Moderate-to-high clay content supports earthen surface water harvesting; site engineering survey recommended for structure siting and waste weir design."

        # Copy baseline scores and ranks to preserve them bit-for-bit
        record = {
            "HYBAS_ID": hybas_id,
            "sub_area_km2": sub_area,
            "preliminary_screening_score": row["preliminary_screening_score"],
            "score_S1_Equal_Pillars": row["score_S1_Equal_Pillars"],
            "score_S2_AHP_Expert": row["score_S2_AHP_Expert"],
            "score_S4_Managed_Aquifer_Recharge": row["score_S4_Managed_Aquifer_Recharge"],
            "rank_S4_Managed_Aquifer_Recharge": row["rank_S4_Managed_Aquifer_Recharge"],
            "score_S5_Surface_Water_Harvesting": row["score_S5_Surface_Water_Harvesting"],
            "rank_S5_Surface_Water_Harvesting": row["rank_S5_Surface_Water_Harvesting"],
            "score_S7_Winsorized_AHP": row["score_S7_Winsorized_AHP"],
            "rank_median_planning": row["rank_median_planning"],
            "consensus_priority_tier_revised": tier_rev,
            "shortlist_surface_water_harvesting": row["shortlist_surface_water_harvesting"],
            "shortlist_managed_aquifer_recharge": row["shortlist_managed_aquifer_recharge"],
            "shortlist_robust_consensus": row["shortlist_robust_consensus"],
            "cgwb_monitoring_well_count": cgwb_w,
            "gsda_monitoring_well_count": gsda_w,
            "total_monitoring_well_count": total_w,
            "gw_depth_trend_median_m_yr": gw_trend,
            "gw_seasonal_recharge_median_m": gw_rech,
            "evidence_confidence_level": conf_level,
            "provisional_action_category_MAR": cat_mar,
            "provisional_screening_rationale_MAR": rat_mar,
            "provisional_action_category_SWH": cat_swh,
            "provisional_screening_rationale_SWH": rat_swh,
            "screening_disclaimer": "PRELIMINARY_SCREENING_ONLY_NOT_A_CONSTRUCTION_APPROVAL"
        }
        assessment_rows.append(record)

    df_assessment = pd.DataFrame(assessment_rows)
    out_assessment_csv = processed_dir / "jaldrishti_phase7_evidence_assessment.csv"
    df_assessment.to_csv(out_assessment_csv, index=False)
    print(f"[SAVED] Phase 7 evidence assessment saved to {out_assessment_csv.name}")
    print(f"  Rows: {len(df_assessment)}, Columns: {len(df_assessment.columns)}")

    # Print summary of Consensus Tier 1 categorizations
    tier1_df = df_assessment[df_assessment["consensus_priority_tier_revised"].str.contains("Tier 1", na=False)]
    print(f"\n--- CONSENSUS TIER 1 ACTION CATEGORIZATION (N = {len(tier1_df)} catchments) ---")
    print("Managed Aquifer Recharge (MAR) Categories:")
    print(tier1_df["provisional_action_category_MAR"].value_counts().to_string())
    print("\nSurface Water Harvesting (SWH) Categories:")
    print(tier1_df["provisional_action_category_SWH"].value_counts().to_string())

    print("\n[COMPLETE] Multi-evidence triangulation finished successfully.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JalDrishti-AI Multi-Evidence Triangulation Pipeline")
    parser.add_argument("--root", type=str, default=None, help="Project root directory")
    args = parser.parse_args()

    root_path = Path(args.root) if args.root else None
    sys.exit(triangulate_evidence(project_root=root_path))
