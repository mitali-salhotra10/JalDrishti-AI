# JalDrishti-AI: Advanced MCDA Sensitivity Analysis & Ranking Stability Engine
# Implements Multi-Scenario Comparative Weighting, Normalization Analysis, and Consensus Ranking
# Author: JalDrishti-AI Engineering Team

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kendalltau, pearsonr

def get_project_root() -> Path:
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists() or (parent / "data").exists():
            return parent
    return Path.cwd()

def winsorized_min_max(vals: np.ndarray, direction: str, p_low: float = 1.0, p_high: float = 99.0) -> np.ndarray:
    """
    Min-max normalization with 1st-99th percentile winsorization to prevent
    extreme outliers (e.g., coastal rainfall >3500mm or steep scarps >35°) from distorting plateau scores.
    """
    q_low = np.percentile(vals, p_low)
    q_high = np.percentile(vals, p_high)
    clipped = np.clip(vals, q_low, q_high)
    rng = q_high - q_low if q_high > q_low else 1.0
    if direction == "benefit":
        return (clipped - q_low) / rng
    else: # cost
        return (q_high - clipped) / rng

def standard_min_max(vals: np.ndarray, direction: str) -> np.ndarray:
    """Standard Min-Max normalization."""
    v_min = np.min(vals)
    v_max = np.max(vals)
    rng = v_max - v_min if v_max > v_min else 1.0
    if direction == "benefit":
        return (vals - v_min) / rng
    else: # cost
        return (v_max - vals) / rng

def compute_shannon_entropy_weights(R: np.ndarray) -> np.ndarray:
    """Computes Shannon Entropy weights from normalized matrix R."""
    m, n = R.shape
    eps = 1e-12
    col_sums = np.sum(R, axis=0) + eps
    P = R / col_sums
    k = 1.0 / np.log(m)
    P_safe = np.where(P > 0, P, eps)
    E = -k * np.sum(P_safe * np.log(P_safe), axis=0)
    D = 1.0 - E
    D = np.maximum(D, 0.0)
    if np.sum(D) == 0:
        return np.ones(n) / n
    return D / np.sum(D)

def run_sensitivity_pipeline(
    project_root: Path = None,
    input_csv: Path = None,
    out_rankings_csv: Path = None,
    out_summary_csv: Path = None
):
    if project_root is None:
        project_root = get_project_root()

    processed_dir = project_root / "data" / "processed"
    if input_csv is None:
        input_csv = processed_dir / "jaldrishti_watersheds_with_village_indicators_v2.csv"
    if out_rankings_csv is None:
        out_rankings_csv = processed_dir / "jaldrishti_mcda_scenario_rankings.csv"
    if out_summary_csv is None:
        out_summary_csv = processed_dir / "jaldrishti_mcda_scenario_summary.csv"

    print("=" * 75)
    print("JALDRISHTI-AI: ADVANCED MCDA SENSITIVITY & STABILITY ENGINE")
    print("=" * 75)

    df_raw = pd.read_csv(input_csv)
    n_basins = len(df_raw)
    print(f"Loaded {n_basins} catchments from {input_csv.name}")

    # Core metadata to retain
    meta_cols = [
        "HYBAS_ID", "sub_area_km2", "up_area_km2", "preliminary_screening_score",
        "village_coverage_pct", "village_coverage_flag"
    ]
    df_out = df_raw[meta_cols].copy()

    # 1. Define Candidate Indicators by Pillar
    pillars = {
        "Climate_Stress": [
            ("village_rainfall_baseline_mean_mm", "cost", "Baseline Mean Rain (mm)"),
            ("village_rainfall_cv_pct", "benefit", "Rainfall Inter-Annual CV (%)"),
            ("village_drought_years_count", "benefit", "Drought Frequency Count"),
            ("village_rainfall_anomaly_2025_pct", "cost", "Rainfall Anomaly 2025 (%)")
        ],
        "Agricultural_Demand": [
            ("village_cropland_pct", "benefit", "Cropland Fraction (%)"),
            ("village_natural_veg_pct", "cost", "Natural Vegetation Buffer (%)"),
            ("village_built_up_pct", "benefit", "Built-up Land Fraction (%)")
        ],
        "Topographic_Runoff": [
            ("village_slope_mean_deg", "benefit", "Catchment Mean Slope (deg)"),
            ("run_mm_syr", "benefit", "Natural Runoff Depth (mm)"),
            ("village_elevation_mean_m", "benefit", "Catchment Mean Elevation (m)")
        ],
        "Soil_Infiltration_Storage": [
            ("village_clay_0_5cm_g_kg", "benefit", "Topsoil Clay Content (g/kg)"),
            ("village_sand_0_5cm_g_kg", "cost", "Topsoil Sand Content (g/kg)"),
            ("village_soc_0_5cm_dg_kg", "benefit", "Soil Organic Carbon (dg/kg)")
        ]
    }

    # Handle missing values via median imputation for the transboundary catchment
    all_crit_cols = []
    for p_name, ind_list in pillars.items():
        for col, _, _ in ind_list:
            if col not in all_crit_cols:
                all_crit_cols.append(col)

    df_imputed = df_raw.copy()
    for c in all_crit_cols:
        med = df_imputed[c].median()
        df_imputed[c] = df_imputed[c].fillna(med)

    # 2. Normalize Indicators (both Standard and Winsorized)
    norm_standard = {}
    norm_winsorized = {}
    for p_name, ind_list in pillars.items():
        for col, direction, _ in ind_list:
            vals = df_imputed[col].values
            norm_standard[col] = standard_min_max(vals, direction)
            norm_winsorized[col] = winsorized_min_max(vals, direction)

    # 3. Define Sensitivity Scenarios
    scenarios = {}

    # Scenario 1: Equal Pillar Weights (25% to each of the 4 pillars)
    scenarios["S1_Equal_Pillars"] = {
        "description": "Equal weights (25%) across all 4 pillars; equal within-pillar weights.",
        "pillar_weights": {"Climate_Stress": 0.25, "Agricultural_Demand": 0.25, "Topographic_Runoff": 0.25, "Soil_Infiltration_Storage": 0.25},
        "within_weights": {
            "Climate_Stress": [0.25, 0.25, 0.25, 0.25],
            "Agricultural_Demand": [1/3, 1/3, 1/3],
            "Topographic_Runoff": [1/3, 1/3, 1/3],
            "Soil_Infiltration_Storage": [1/3, 1/3, 1/3]
        },
        "normalization": "standard",
        "filter_core": False
    }

    # Scenario 2: Expert / AHP Model
    # Documented Saaty Matrix: CR = 0.0015 < 0.10
    scenarios["S2_AHP_Expert"] = {
        "description": "Analytical Hierarchy Process (AHP) calibrated to state guidelines (Climate 35%, Ag 30%, Runoff 20%, Infiltration 15%).",
        "pillar_weights": {"Climate_Stress": 0.35, "Agricultural_Demand": 0.30, "Topographic_Runoff": 0.20, "Soil_Infiltration_Storage": 0.15},
        "within_weights": {
            "Climate_Stress": [0.35, 0.25, 0.25, 0.15],
            "Agricultural_Demand": [0.50, 0.30, 0.20],
            "Topographic_Runoff": [0.40, 0.40, 0.20],
            "Soil_Infiltration_Storage": [0.40, 0.30, 0.30]
        },
        "normalization": "standard",
        "filter_core": False
    }

    # Scenario 3: Shannon Entropy Objective Model
    # Compute column-wise entropy across all 13 indicators
    X_mat = np.column_stack([norm_standard[col] for col in all_crit_cols])
    w_ent = compute_shannon_entropy_weights(X_mat)
    # Group into pillars
    scenarios["S3_Shannon_Entropy"] = {
        "description": "Objective Shannon Entropy weights derived from information dispersion contrast across basins.",
        "direct_weights": dict(zip(all_crit_cols, w_ent)),
        "normalization": "standard",
        "filter_core": False
    }

    # Scenario 4: Managed Aquifer Recharge (MAR Focus)
    # Permeable soils, rolling terrain, acute drought demand
    # Modify soil direction: sand is benefit, clay is cost
    scenarios["S4_Managed_Aquifer_Recharge"] = {
        "description": "Subsurface Managed Aquifer Recharge (MAR): prioritizes permeable sandy strata, rolling relief, and acute drought frequency.",
        "pillar_weights": {"Climate_Stress": 0.30, "Agricultural_Demand": 0.20, "Topographic_Runoff": 0.15, "Soil_Infiltration_Storage": 0.35},
        "within_weights": {
            "Climate_Stress": [0.30, 0.30, 0.30, 0.10],
            "Agricultural_Demand": [0.50, 0.30, 0.20],
            "Topographic_Runoff": [0.30, 0.40, 0.30],
            "Soil_Infiltration_Storage": [0.20, 0.50, 0.30] # sand is benefit, clay is cost
        },
        "custom_soil_dirs": {"village_sand_0_5cm_g_kg": "benefit", "village_clay_0_5cm_g_kg": "cost"},
        "normalization": "standard",
        "filter_core": False
    }

    # Scenario 5: Surface Water Harvesting (SWH Focus)
    # Impoundment structures (farm ponds, check dams) require clay for low seepage and high runoff
    scenarios["S5_Surface_Water_Harvesting"] = {
        "description": "Surface Water Harvesting (SWH): prioritizes impermeable vertisols (low seepage), high runoff depth, and cropland density.",
        "pillar_weights": {"Climate_Stress": 0.20, "Agricultural_Demand": 0.25, "Topographic_Runoff": 0.35, "Soil_Infiltration_Storage": 0.20},
        "within_weights": {
            "Climate_Stress": [0.35, 0.25, 0.25, 0.15],
            "Agricultural_Demand": [0.55, 0.25, 0.20],
            "Topographic_Runoff": [0.40, 0.45, 0.15],
            "Soil_Infiltration_Storage": [0.55, 0.20, 0.25] # clay 55% benefit, sand 20% cost
        },
        "normalization": "standard",
        "filter_core": False
    }

    # Scenario 6: Robust Core (Excluding partial/transboundary borders)
    scenarios["S6_Robust_Core_Ex_Border"] = {
        "description": "AHP weighting evaluated exclusively on the 402 full-coverage (>=90%) catchments to eliminate border edge-effects.",
        "pillar_weights": {"Climate_Stress": 0.35, "Agricultural_Demand": 0.30, "Topographic_Runoff": 0.20, "Soil_Infiltration_Storage": 0.15},
        "within_weights": {
            "Climate_Stress": [0.35, 0.25, 0.25, 0.15],
            "Agricultural_Demand": [0.50, 0.30, 0.20],
            "Topographic_Runoff": [0.40, 0.40, 0.20],
            "Soil_Infiltration_Storage": [0.40, 0.30, 0.30]
        },
        "normalization": "standard",
        "filter_core": True
    }

    # Scenario 7: Winsorized Normalization (1st-99th percentile) with AHP weights
    scenarios["S7_Winsorized_AHP"] = {
        "description": "AHP model with 1st-99th percentile winsorized normalization to mitigate coastal precipitation outliers.",
        "pillar_weights": {"Climate_Stress": 0.35, "Agricultural_Demand": 0.30, "Topographic_Runoff": 0.20, "Soil_Infiltration_Storage": 0.15},
        "within_weights": {
            "Climate_Stress": [0.35, 0.25, 0.25, 0.15],
            "Agricultural_Demand": [0.50, 0.30, 0.20],
            "Topographic_Runoff": [0.40, 0.40, 0.20],
            "Soil_Infiltration_Storage": [0.40, 0.30, 0.30]
        },
        "normalization": "winsorized",
        "filter_core": False
    }

    # 4. Compute Scores and Ranks for Each Scenario
    score_columns = []
    rank_columns = []

    for s_name, s_cfg in scenarios.items():
        norm_dict = norm_winsorized if s_cfg["normalization"] == "winsorized" else norm_standard

        # Handle custom indicator directions if needed (e.g. for MAR)
        if "custom_soil_dirs" in s_cfg:
            s_norm = norm_dict.copy()
            for col, d in s_cfg["custom_soil_dirs"].items():
                s_norm[col] = standard_min_max(df_imputed[col].values, d)
        else:
            s_norm = norm_dict

        if "direct_weights" in s_cfg:
            # Shannon Entropy direct indicator weights
            weights = np.array([s_cfg["direct_weights"][c] for c in all_crit_cols])
            X_cols = np.column_stack([s_norm[c] for c in all_crit_cols])
            score = np.dot(X_cols, weights) * 100.0
        else:
            # Explicit Pillar Hierarchical Weighting
            score = np.zeros(n_basins)
            for p_name, p_w in s_cfg["pillar_weights"].items():
                ind_list = pillars[p_name]
                w_within = np.array(s_cfg["within_weights"][p_name])
                P_cols = np.column_stack([s_norm[col] for col, _, _ in ind_list])
                p_sub_index = np.dot(P_cols, w_within)
                score += p_w * p_sub_index
            score *= 100.0

        # Filtering for core scenario
        if s_cfg["filter_core"]:
            mask_core = df_raw["village_coverage_pct"] >= 90.0
            score_final = np.where(mask_core, score, np.nan)
            rank_series = pd.Series(score_final).rank(ascending=False, method="min", na_option="bottom").astype("Int64")
        else:
            score_final = score
            rank_series = pd.Series(score_final).rank(ascending=False, method="min").astype(int)

        score_col = f"score_{s_name}"
        rank_col = f"rank_{s_name}"
        df_out[score_col] = np.round(score_final, 2)
        df_out[rank_col] = rank_series
        score_columns.append(score_col)
        rank_columns.append(rank_col)

    # 5. Consensus & Ranking Stability Metrics
    # Compute mean rank and rank variance across standard scenarios (S1, S2, S3, S4, S5, S7)
    std_rank_cols = [f"rank_{s}" for s in ["S1_Equal_Pillars", "S2_AHP_Expert", "S3_Shannon_Entropy", "S4_Managed_Aquifer_Recharge", "S5_Surface_Water_Harvesting", "S7_Winsorized_AHP"]]
    df_out["mean_rank_all_scenarios"] = np.round(df_out[std_rank_cols].mean(axis=1), 2)
    df_out["rank_std_all_scenarios"] = np.round(df_out[std_rank_cols].std(axis=1), 2)

    # Consensus Priority Tier: Top 20% mean rank across all scenarios
    q20_rank = df_out["mean_rank_all_scenarios"].quantile(0.20)
    q50_rank = df_out["mean_rank_all_scenarios"].quantile(0.50)

    def assign_consensus_tier(mean_r):
        if mean_r <= q20_rank:
            return "Consensus Tier 1: Persistent High Priority"
        elif mean_r <= q50_rank:
            return "Consensus Tier 2: Moderate Sensitivity"
        else:
            return "Consensus Tier 3: Low Priority"

    df_out["consensus_priority_tier"] = df_out["mean_rank_all_scenarios"].apply(assign_consensus_tier)

    # Export master rankings CSV
    df_out.to_csv(out_rankings_csv, index=False)
    print(f"\n[SUCCESS] Saved comprehensive scenario rankings to: {out_rankings_csv}")
    print(f"Shape: {df_out.shape[0]} rows x {df_out.shape[1]} columns")

    # 6. Compute Cross-Scenario Rank Correlation Matrix
    corr_matrix = pd.DataFrame(index=std_rank_cols, columns=std_rank_cols, dtype=float)
    for c1 in std_rank_cols:
        for c2 in std_rank_cols:
            rho, _ = spearmanr(df_out[c1], df_out[c2])
            corr_matrix.loc[c1, c2] = np.round(rho, 4)

    print("\nSpearman Rank Correlation Matrix Across Scenarios:")
    print(corr_matrix.to_string())

    # 7. Compute Top-10 and Top-20 Jaccard Overlap
    print("\nTop-20 Ranking Overlap (Jaccard Index) vs S2 (AHP Expert):")
    top20_ahp = set(df_out.nsmallest(20, "rank_S2_AHP_Expert")["HYBAS_ID"])
    jaccard_results = []
    for r_col in std_rank_cols:
        top20_other = set(df_out.nsmallest(20, r_col)["HYBAS_ID"])
        inter = len(top20_ahp.intersection(top20_other))
        union = len(top20_ahp.union(top20_other))
        jaccard = inter / union if union > 0 else 1.0
        jaccard_results.append({
            "Scenario": r_col.replace("rank_", ""),
            "Shared_with_AHP_Top20": inter,
            "Jaccard_Top20": round(jaccard, 3)
        })
        print(f" - {r_col:35s}: {inter:2d}/20 shared (Jaccard = {jaccard:.2f})")

    # 8. Identify the Persistently High-Priority Watersheds (Top-20 consensus)
    robust_catchments = df_out.nsmallest(20, "mean_rank_all_scenarios")[
        ["HYBAS_ID", "sub_area_km2", "mean_rank_all_scenarios", "rank_std_all_scenarios",
         "rank_S1_Equal_Pillars", "rank_S2_AHP_Expert", "rank_S4_Managed_Aquifer_Recharge", "rank_S5_Surface_Water_Harvesting"]
    ]
    print("\nTop-10 Persistently High-Priority Watersheds Across Scenarios:")
    print(robust_catchments.head(10).to_string(index=False))

    # 9. Create Summary Table
    summary_records = []
    for s_name, s_cfg in scenarios.items():
        summary_records.append({
            "Scenario_ID": s_name,
            "Description": s_cfg["description"],
            "Normalization": s_cfg["normalization"],
            "Filtered_Core_Basins": s_cfg["filter_core"],
            "Mean_Score": round(df_out[f"score_{s_name}"].mean(), 2),
            "Std_Score": round(df_out[f"score_{s_name}"].std(), 2),
            "Min_Score": round(df_out[f"score_{s_name}"].min(), 2),
            "Max_Score": round(df_out[f"score_{s_name}"].max(), 2),
            "Correlation_with_AHP_Rho": round(spearmanr(df_out["rank_S2_AHP_Expert"], df_out[f"rank_{s_name}"]).statistic, 4) if not s_cfg["filter_core"] else np.nan
        })
    df_summary = pd.DataFrame(summary_records)
    df_summary.to_csv(out_summary_csv, index=False)
    print(f"\n[SUCCESS] Saved scenario summary to: {out_summary_csv}")

    return df_out, df_summary, corr_matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JalDrishti-AI MCDA Sensitivity Engine")
    parser.add_argument("--root", type=str, default=None, help="Project root directory")
    args = parser.parse_args()
    root_path = Path(args.root) if args.root else None
    run_sensitivity_pipeline(project_root=root_path)
