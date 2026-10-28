# JalDrishti-AI: Unit Tests for MCDA Sensitivity and Stability Framework
# Tests mathematical consistency, rank bounds, Saaty AHP CR, and scenario stability

import pytest
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_scenario_rankings_file_integrity():
    """Verify that jaldrishti_mcda_scenario_rankings.csv exists, has 518 rows, and unique keys."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_mcda_scenario_rankings.csv"
    assert csv_path.exists(), f"Scenario rankings CSV missing at {csv_path}"
    df = pd.read_csv(csv_path)
    assert len(df) == 518, f"Expected 518 rows, found {len(df)}"
    assert df["HYBAS_ID"].nunique() == 518, "HYBAS_ID must be 100% unique"
    assert "preliminary_screening_score" in df.columns, "Preliminary screening score must be preserved"

def test_scenario_score_and_rank_ranges():
    """Verify that all scenario scores fall in [0, 100] and ranks span [1, 518]."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_mcda_scenario_rankings.csv"
    df = pd.read_csv(csv_path)
    
    scenarios = ["S1_Equal_Pillars", "S2_AHP_Expert", "S3_Shannon_Entropy", "S4_Managed_Aquifer_Recharge", "S5_Surface_Water_Harvesting", "S7_Winsorized_AHP"]
    for s in scenarios:
        s_col = f"score_{s}"
        r_col = f"rank_{s}"
        assert s_col in df.columns and r_col in df.columns
        assert df[s_col].min() >= 0.0, f"{s_col} min below 0: {df[s_col].min()}"
        assert df[s_col].max() <= 100.0, f"{s_col} max above 100: {df[s_col].max()}"
        assert df[r_col].min() == 1, f"{r_col} min must be 1"
        assert df[r_col].max() == 518, f"{r_col} max must be 518"

def test_ahp_consistency_ratio():
    """Verify that Saaty pairwise comparison matrix produces CR < 0.10."""
    # Saaty pairwise matrix across the 4 pillars:
    # 1. Climate Stress, 2. Agricultural Demand, 3. Topographic Runoff, 4. Soil Infiltration
    A = np.array([
        [1.0,    1.25,   1.75,   2.25],
        [1/1.25, 1.0,    1.50,   2.00],
        [1/1.75, 1/1.50, 1.0,    1.333333],
        [1/2.25, 1/2.00, 1/1.333333, 1.0]
    ])
    
    # Eigenvalue calculation
    eigenvalues, eigenvectors = np.linalg.eig(A)
    max_idx = np.argmax(np.real(eigenvalues))
    lambda_max = np.real(eigenvalues[max_idx])
    
    n = 4
    CI = (lambda_max - n) / (n - 1)
    RI = 0.90 # Saaty Random Index for n=4
    CR = CI / RI
    
    assert CR < 0.10, f"AHP Consistency Ratio {CR:.4f} exceeds threshold 0.10"
    
    # Priority vector
    w = np.real(eigenvectors[:, max_idx])
    w = w / np.sum(w)
    assert np.isclose(np.sum(w), 1.0)
    assert np.isclose(w[0], 0.35, atol=0.03)

def test_preliminary_score_preservation_unaltered():
    """Verify that preliminary_screening_score is not overwritten or modified."""
    val_csv = PROJECT_ROOT / "data" / "interim" / "jaldrishti_watershed_validation_518_basins.csv"
    rankings_csv = PROJECT_ROOT / "data" / "processed" / "jaldrishti_mcda_scenario_rankings.csv"
    
    df_val = pd.read_csv(val_csv)
    df_rank = pd.read_csv(rankings_csv)
    
    slp = df_val["slp_dg_sav_deg"]
    slp_norm = (slp - 0.0) / (14.7 - 0.0)
    pre = df_val["pre_mm_syr"]
    rain_inv_norm = 1.0 - (pre - 465.0) / (4136.0 - 465.0)
    orig_score = (0.5 * slp_norm + 0.5 * rain_inv_norm) * 100.0
    
    delta = np.abs(df_rank["preliminary_screening_score"] - orig_score).max()
    assert delta < 1e-12, f"Preliminary score max delta ({delta}) exceeds tolerance 1e-12"

def test_winsorized_ahp_rank_stability():
    """Verify that winsorized normalisation maintains strong rank correlation with standard AHP."""
    rankings_csv = PROJECT_ROOT / "data" / "processed" / "jaldrishti_mcda_scenario_rankings.csv"
    df = pd.read_csv(rankings_csv)
    
    rho, _ = spearmanr(df["rank_S2_AHP_Expert"], df["rank_S7_Winsorized_AHP"])
    assert rho > 0.95, f"Expected rho > 0.95 between standard and winsorized AHP, found {rho:.4f}"

def test_consensus_priority_tiers():
    """Verify that consensus priority tiers are assigned and have plausible counts."""
    rankings_csv = PROJECT_ROOT / "data" / "processed" / "jaldrishti_mcda_scenario_rankings.csv"
    df = pd.read_csv(rankings_csv)
    
    assert "consensus_priority_tier" in df.columns
    tier_counts = df["consensus_priority_tier"].value_counts()
    assert "Consensus Tier 1: Persistent High Priority" in tier_counts
    tier1_count = tier_counts["Consensus Tier 1: Persistent High Priority"]
    assert 90 <= tier1_count <= 115, f"Expected ~104 Tier 1 catchments, found {tier1_count}"
