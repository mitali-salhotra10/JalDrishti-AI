# JalDrishti-AI: Unit Tests for Consensus Ranking Audit & Intervention Shortlisting
# Tests consensus recalculations, SWH vs MAR divergence, and shortlist schema integrity

import pytest
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_consensus_audit_file_integrity():
    """Verify that jaldrishti_consensus_priority_audit.csv exists and has 518 unique catchments."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_consensus_priority_audit.csv"
    assert csv_path.exists(), f"Consensus audit CSV not found at {csv_path}"
    df = pd.read_csv(csv_path)
    assert len(df) == 518, f"Expected 518 rows, found {len(df)}"
    assert df["HYBAS_ID"].nunique() == 518, "HYBAS_ID must be 100% unique"

def test_median_rank_bounds_and_validity():
    """Verify that rank_median_planning is populated, bounded in [1, 518], and non-null."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_consensus_priority_audit.csv"
    df = pd.read_csv(csv_path)
    assert "rank_median_planning" in df.columns
    assert df["rank_median_planning"].notna().all(), "Median rank must have zero nulls"
    assert df["rank_median_planning"].min() >= 1.0
    assert df["rank_median_planning"].max() <= 518.0

def test_shortlist_cardinality():
    """Verify that all three intervention shortlists have exactly 20 candidate catchments."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_consensus_priority_audit.csv"
    df = pd.read_csv(csv_path)
    
    for col in [
        "shortlist_surface_water_harvesting",
        "shortlist_managed_aquifer_recharge",
        "shortlist_robust_consensus"
    ]:
        assert col in df.columns, f"Missing shortlist column: {col}"
        count = df[col].sum()
        assert count == 20, f"Expected exactly 20 catchments in {col}, found {count}"

def test_swh_vs_mar_geological_divergence():
    """
    Verify physical hydrogeological divergence:
    - SWH catchments must have significantly higher clay than MAR catchments.
    - MAR catchments must have significantly higher sand & infiltration proxy than SWH catchments.
    """
    csv_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_consensus_priority_audit.csv"
    df = pd.read_csv(csv_path)
    
    swh = df[df["shortlist_surface_water_harvesting"]]
    mar = df[df["shortlist_managed_aquifer_recharge"]]
    
    mean_clay_swh = swh["village_clay_0_5cm_g_kg"].mean()
    mean_clay_mar = mar["village_clay_0_5cm_g_kg"].mean()
    assert mean_clay_swh > mean_clay_mar, f"SWH mean clay ({mean_clay_swh:.1f}) should exceed MAR ({mean_clay_mar:.1f})"
    
    mean_sand_mar = mar["village_sand_0_5cm_g_kg"].mean()
    mean_sand_swh = swh["village_sand_0_5cm_g_kg"].mean()
    assert mean_sand_mar > mean_sand_swh, f"MAR mean sand ({mean_sand_mar:.1f}) should exceed SWH ({mean_sand_swh:.1f})"
    
    mean_inf_mar = mar["village_infiltration_proxy"].mean()
    mean_inf_swh = swh["village_infiltration_proxy"].mean()
    assert mean_inf_mar > mean_inf_swh, f"MAR infiltration proxy ({mean_inf_mar:.2f}) should exceed SWH ({mean_inf_swh:.2f})"

def test_revised_consensus_tiers():
    """Verify revised consensus priority tiers are populated and sum to 518."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_consensus_priority_audit.csv"
    df = pd.read_csv(csv_path)
    assert "consensus_priority_tier_revised" in df.columns
    tier_counts = df["consensus_priority_tier_revised"].value_counts()
    assert tier_counts.sum() == 518
    assert "Consensus Tier 1: Robust Priority (Multi-Scenario)" in tier_counts
    tier1_cnt = tier_counts["Consensus Tier 1: Robust Priority (Multi-Scenario)"]
    assert 50 <= tier1_cnt <= 100, f"Expected 50-100 Tier 1 catchments, found {tier1_cnt}"
