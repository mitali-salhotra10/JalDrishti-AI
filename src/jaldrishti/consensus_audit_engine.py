# JalDrishti-AI: MCDA Consensus Ranking Audit & Intervention Shortlisting Engine
# Implements Robust Multi-Criteria Consensus, Intervention-Specific Shortlists (SWH vs MAR),
# and Audits Discrepancies in Naive Mean-Rank Aggregation.
# Author: JalDrishti-AI Engineering Team

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

def get_project_root() -> Path:
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists() or (parent / "data").exists():
            return parent
    return Path.cwd()

def run_consensus_audit(
    project_root: Path = None,
    rankings_csv: Path = None,
    watershed_v2_csv: Path = None,
    out_audit_csv: Path = None
):
    if project_root is None:
        project_root = get_project_root()

    processed_dir = project_root / "data" / "processed"
    if rankings_csv is None:
        rankings_csv = processed_dir / "jaldrishti_mcda_scenario_rankings.csv"
    if watershed_v2_csv is None:
        watershed_v2_csv = processed_dir / "jaldrishti_watersheds_with_village_indicators_v2.csv"
    if out_audit_csv is None:
        out_audit_csv = processed_dir / "jaldrishti_consensus_priority_audit.csv"

    print("=" * 75)
    print("JALDRISHTI-AI: CONSENSUS RANKING AUDIT & INTERVENTION SHORTLISTING")
    print("=" * 75)

    df_rankings = pd.read_csv(rankings_csv)
    df_w2 = pd.read_csv(watershed_v2_csv)
    print(f"Loaded {len(df_rankings)} scenario rankings and {len(df_w2)} watershed physical records")

    # Merge physical indicators onto rankings table
    ind_cols_to_merge = [
        "HYBAS_ID", "village_rainfall_baseline_mean_mm", "village_rainfall_cv_pct",
        "village_drought_years_count", "village_cropland_pct", "village_natural_veg_pct",
        "village_slope_mean_deg", "village_elevation_mean_m", "run_mm_syr",
        "village_clay_0_5cm_g_kg", "village_sand_0_5cm_g_kg", "village_soc_0_5cm_dg_kg",
        "village_infiltration_proxy"
    ]
    df_merged = df_rankings.merge(df_w2[ind_cols_to_merge], on="HYBAS_ID", how="left")

    # Define Planning Scenarios (excluding pure unweighted Shannon Entropy which is distorted by coastal runoff)
    # Core Planning Scenarios:
    # 1. S1_Equal_Pillars
    # 2. S2_AHP_Expert
    # 3. S4_Managed_Aquifer_Recharge (MAR)
    # 4. S5_Surface_Water_Harvesting (SWH)
    # 5. S6_Robust_Core_Ex_Border (filled with S2 rank for partial borders to maintain array length)
    # 6. S7_Winsorized_AHP
    planning_scenarios = [
        "rank_S1_Equal_Pillars",
        "rank_S2_AHP_Expert",
        "rank_S4_Managed_Aquifer_Recharge",
        "rank_S5_Surface_Water_Harvesting",
        "rank_S7_Winsorized_AHP"
    ]

    rank_matrix = df_merged[planning_scenarios].values

    # 1. Compute Robust Consensus Metrics
    print("Computing robust non-parametric consensus metrics across planning scenarios...")
    # Median Rank: Highly resistant to single-scenario outlier skew
    df_merged["rank_median_planning"] = np.round(np.median(rank_matrix, axis=1), 2)
    # Mean Rank across planning scenarios
    df_merged["rank_mean_planning"] = np.round(np.mean(rank_matrix, axis=1), 2)
    # Standard deviation of ranks across planning scenarios
    df_merged["rank_std_planning"] = np.round(np.std(rank_matrix, axis=1), 2)
    # Interquartile Range (IQR = 75th percentile - 25th percentile)
    q75 = np.percentile(rank_matrix, 75, axis=1)
    q25 = np.percentile(rank_matrix, 25, axis=1)
    df_merged["rank_iqr_planning"] = np.round(q75 - q25, 2)

    # Frequency of appearance in top percentiles (out of 5 core planning scenarios)
    # Top 10% = rank <= 52
    df_merged["top10pct_count_planning"] = np.sum(rank_matrix <= 52, axis=1)
    # Top 20% = rank <= 104
    df_merged["top20pct_count_planning"] = np.sum(rank_matrix <= 104, axis=1)
    # Top 25% = rank <= 130
    df_merged["top25pct_count_planning"] = np.sum(rank_matrix <= 130, axis=1)

    # 2. Transparent Multi-Tier Consensus Classification
    # Consensus Rule:
    # Tier 1 (High Consensus Priority): Appears in Top 20% (rank <= 104) in at least 4 out of 5 planning scenarios, AND median rank <= 104.
    # Tier 2 (Moderate / Intervention-Specific): Appears in Top 20% in 2 or 3 scenarios, OR median rank <= 180.
    # Tier 3 (Low Priority / Maintenance): All remaining catchments.
    def assign_robust_tier(row):
        t20_cnt = row["top20pct_count_planning"]
        med_r = row["rank_median_planning"]
        if t20_cnt >= 4 and med_r <= 104:
            return "Consensus Tier 1: Robust Priority (Multi-Scenario)"
        elif t20_cnt >= 2 or med_r <= 180:
            return "Consensus Tier 2: Specialized / Moderate Priority"
        else:
            return "Consensus Tier 3: Low Priority / Conservation"

    df_merged["consensus_priority_tier_revised"] = df_merged.apply(assign_robust_tier, axis=1)

    tier_counts = df_merged["consensus_priority_tier_revised"].value_counts()
    print("\nRevised Consensus Priority Tier Distribution:")
    for tier, count in tier_counts.items():
        print(f" - {tier:45s}: {count:3d} ({count/518*100:.2f}%)")

    # 3. Formulate Candidate Shortlists (Top 20 each)
    # Shortlist A: Surface Water Harvesting (SWH)
    # Ranked by S5 (Surface Water Harvesting Focus), prioritizing high clay, cropland, and runoff
    top20_swh = df_merged.nsmallest(20, "rank_S5_Surface_Water_Harvesting").copy()
    top20_swh_ids = set(top20_swh["HYBAS_ID"])

    # Shortlist B: Managed Aquifer Recharge (MAR)
    # Ranked by S4 (Managed Aquifer Recharge Focus), prioritizing permeable textures and drought stress
    top20_mar = df_merged.nsmallest(20, "rank_S4_Managed_Aquifer_Recharge").copy()
    top20_mar_ids = set(top20_mar["HYBAS_ID"])

    # Shortlist C: Robust Multi-Scenario Consensus
    # Sorted by median rank ascending, tie-break on top20 count descending and rank IQR ascending
    top20_consensus = df_merged.sort_values(
        by=["rank_median_planning", "top20pct_count_planning", "rank_iqr_planning"],
        ascending=[True, False, True]
    ).head(20).copy()
    top20_consensus_ids = set(top20_consensus["HYBAS_ID"])

    # Assign Shortlist Flags in Master Table
    df_merged["shortlist_surface_water_harvesting"] = df_merged["HYBAS_ID"].isin(top20_swh_ids)
    df_merged["shortlist_managed_aquifer_recharge"] = df_merged["HYBAS_ID"].isin(top20_mar_ids)
    df_merged["shortlist_robust_consensus"] = df_merged["HYBAS_ID"].isin(top20_consensus_ids)

    # 4. Export Master Audit Table
    df_merged.to_csv(out_audit_csv, index=False)
    print(f"\n[SUCCESS] Exported consensus audit table to: {out_audit_csv}")
    print(f"Shape: {df_merged.shape[0]} rows x {df_merged.shape[1]} columns")

    # 5. Print Shortlist Comparisons
    print("\n" + "=" * 75)
    print("TOP-10 CANDIDATE SHORTLIST: SURFACE WATER HARVESTING (SWH)")
    print("Criteria: Impoundment suitability (high clay vertisols, high runoff depth, cropland)")
    print("=" * 75)
    swh_cols = ["HYBAS_ID", "sub_area_km2", "rank_S5_Surface_Water_Harvesting", "rank_S2_AHP_Expert", "village_clay_0_5cm_g_kg", "village_cropland_pct", "run_mm_syr"]
    print(top20_swh[swh_cols].head(10).to_string(index=False))

    print("\n" + "=" * 75)
    print("TOP-10 CANDIDATE SHORTLIST: MANAGED AQUIFER RECHARGE (MAR)")
    print("Criteria: Subsurface infiltration (permeable sand/silt, rolling terrain, drought)")
    print("=" * 75)
    mar_cols = ["HYBAS_ID", "sub_area_km2", "rank_S4_Managed_Aquifer_Recharge", "rank_S2_AHP_Expert", "village_sand_0_5cm_g_kg", "village_infiltration_proxy", "village_drought_years_count"]
    print(top20_mar[mar_cols].head(10).to_string(index=False))

    print("\n" + "=" * 75)
    print("TOP-10 CANDIDATE SHORTLIST: ROBUST MULTI-SCENARIO CONSENSUS")
    print("Criteria: Minimum median rank, low rank dispersion across diverse planning models")
    print("=" * 75)
    con_cols = ["HYBAS_ID", "sub_area_km2", "rank_median_planning", "rank_iqr_planning", "top20pct_count_planning", "rank_S1_Equal_Pillars", "rank_S2_AHP_Expert", "rank_S5_Surface_Water_Harvesting"]
    print(top20_consensus[con_cols].head(10).to_string(index=False))

    # Overlap between SWH and MAR
    overlap_swh_mar = top20_swh_ids.intersection(top20_mar_ids)
    print(f"\nDirect Top-20 Overlap between SWH and MAR: {len(overlap_swh_mar)} catchments")
    if len(overlap_swh_mar) > 0:
        print(f"Shared catchments: {overlap_swh_mar}")

    return df_merged, top20_swh, top20_mar, top20_consensus

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JalDrishti-AI Consensus Ranking Audit")
    parser.add_argument("--root", type=str, default=None, help="Project root directory")
    args = parser.parse_args()
    root_path = Path(args.root) if args.root else None
    run_consensus_audit(project_root=root_path)
