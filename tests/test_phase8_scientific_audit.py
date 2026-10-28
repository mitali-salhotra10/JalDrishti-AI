"""
test_phase8_scientific_audit.py - Automated Scientific Quality Assurance & Regression Suite
Phase 8: Scientific Audit and Final MCDA Validation.

Validates:
1. Groundwater-depth trend sign interpretation (Theil-Sen slope in mbgl).
2. MAR Category Assignment and Rationale Audit (12 Category A, 56 Category C, 8 Category D in Tier 1).
3. Zero-Fabrication Audit (absence of hallucinated catchment IDs).
4. Strict Separation of MAR and SWH decision rules.
5. Unknown MRSAC infrastructure inventory policy enforcement.
6. Bit-for-bit Immutability of Phase 3 and Phase 4 baseline scores and ranks.
"""

import hashlib
import os
import numpy as np
import pandas as pd
import pytest
from scipy.stats import theilslopes

# Baseline hashes for immutability verification
BASELINE_HASHES = {
    "data/processed/jaldrishti_mcda_scenario_rankings.csv": "692b7dc9b7d56e5a964a452348c3086906f0e1d1630e26a6761306a2f875e982",
    "data/processed/jaldrishti_consensus_priority_audit.csv": "85bece275a30aca3fd7aca0d81ef226179e6bb702f96a95b81e3f76669696ccb",
    "data/processed/jaldrishti_watersheds_with_village_indicators_v2.csv": "93585556df7f91825e1efe4664d224e3fc2a4c437317e815efa8c6f9b01a4843",
    "data/processed/jaldrishti_scored_watersheds.shp": "b600ca7cf8decf872b11cdcc2bb947c6ea9c7748bd2451d90c4b268f0339e372",
}

EVIDENCE_ASSESSMENT_PATH = "data/processed/jaldrishti_phase7_evidence_assessment.csv"
INFRASTRUCTURE_LEDGER_PATH = "data/processed/jaldrishti_infrastructure_by_catchment.csv"


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def test_groundwater_depth_trend_sign_mathematics():
    """
    Verify Theil-Sen slope sign convention in meters below ground level (mbgl):
    - Increasing depth over time (water table dropping) -> positive slope (> 0).
    - Decreasing depth over time (water table rising)   -> negative slope (< 0).
    """
    years = np.array([2015, 2017, 2019, 2021, 2023], dtype=float)

    # Synthetic depleting well: depth deepens from 5.0m to 10.0m bgl
    depleting_levels = np.array([5.0, 6.2, 7.5, 8.8, 10.0], dtype=float)
    slope_depleting = theilslopes(depleting_levels, years)[0]
    assert slope_depleting > 0, f"Depleting well should have positive slope, got {slope_depleting}"
    assert np.isclose(slope_depleting, 0.625, atol=0.05)

    # Synthetic recovering well: depth rises from 10.0m to 5.0m bgl
    recovering_levels = np.array([10.0, 8.8, 7.5, 6.2, 5.0], dtype=float)
    slope_recovering = theilslopes(recovering_levels, years)[0]
    assert slope_recovering < 0, f"Recovering well should have negative slope, got {slope_recovering}"
    assert np.isclose(slope_recovering, -0.625, atol=0.05)


def test_zero_hallucinated_catchment_ids_audit():
    """
    Audit previously reported suspect catchment IDs (4081028710, 4081031300, 4081031730, 4081041160, 4081042780).
    Confirms they are recognized as non-existent and NOT present in the 518 Level 8 catchment database.
    """
    df_eval = pd.read_csv(EVIDENCE_ASSESSMENT_PATH)
    all_hybas = set(df_eval["HYBAS_ID"])
    assert len(all_hybas) == 518, f"Expected 518 unique catchments, found {len(all_hybas)}"

    hallucinated_ids = [4081028710, 4081031300, 4081031730, 4081041160, 4081042780]
    for hid in hallucinated_ids:
        assert hid not in all_hybas, f"Hallucinated ID {hid} unexpectedly present in actual dataset!"


def test_mar_action_category_assignment_logic():
    """
    Verify corrected MAR action category assignments for Consensus Tier 1 (N = 76):
    - Category A: exactly 12 catchments with confirmed decadal depletion (gw_depth_trend > 0).
    - Category C: exactly 56 catchments (40 with recovering water tables + 16 with inconclusive trends).
    - Category D: exactly 8 catchments with low coverage (<50%) or < 2 wells.
    """
    df_eval = pd.read_csv(EVIDENCE_ASSESSMENT_PATH)
    tier1 = df_eval[df_eval["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")].copy()
    assert len(tier1) == 76, f"Expected 76 Tier 1 catchments, found {len(tier1)}"

    mar_counts = tier1["provisional_action_category_MAR"].value_counts()
    assert mar_counts.get("Category A: Potential New Infrastructure Assessment (MAR)", 0) == 12
    assert mar_counts.get("Category C: Mixed or Conflicting Evidence Requiring Field Assessment", 0) == 56
    assert mar_counts.get("Category D: Insufficient Evidence", 0) == 8

    # Ensure all 12 Category A catchments have positive depth trend (true depletion)
    cat_a = tier1[tier1["provisional_action_category_MAR"].str.startswith("Category A")]
    assert len(cat_a) == 12
    for _, r in cat_a.iterrows():
        assert pd.notna(r["gw_depth_trend_median_m_yr"]), f"Catchment {r['HYBAS_ID']} has NaN trend in Cat A"
        assert r["gw_depth_trend_median_m_yr"] > 0, f"Catchment {r['HYBAS_ID']} has non-positive trend in Cat A: {r['gw_depth_trend_median_m_yr']}"

    # Ensure recovering catchments (trend < 0) are in Category C
    recovering = tier1[tier1["gw_depth_trend_median_m_yr"] < 0]
    assert len(recovering) == 40
    for _, r in recovering.iterrows():
        assert r["provisional_action_category_MAR"] == "Category C: Mixed or Conflicting Evidence Requiring Field Assessment", \
            f"Catchment {r['HYBAS_ID']} with recovering water table improperly classified: {r['provisional_action_category_MAR']}"


def test_separation_of_mar_and_swh_rules():
    """
    Verify complete hydrogeological separation of MAR and SWH screening logic:
    - SWH is governed by surface runoff, clay impermeability, and cropland draft (NOT groundwater trend).
    - SWH Category A has 75 catchments; MAR Category A has 12 catchments.
    """
    df_eval = pd.read_csv(EVIDENCE_ASSESSMENT_PATH)
    tier1 = df_eval[df_eval["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")]

    swh_counts = tier1["provisional_action_category_SWH"].value_counts()
    mar_counts = tier1["provisional_action_category_MAR"].value_counts()

    assert swh_counts["Category A: Potential New Infrastructure Assessment (SWH)"] == 75
    assert swh_counts["Category D: Insufficient Evidence"] == 1
    assert not mar_counts.equals(swh_counts), "MAR and SWH screening rules improperly collapsed!"


def test_unknown_mrsac_inventory_policy_enforcement():
    """
    Confirm that missing MRSAC structure inventory is explicitly treated as UNKNOWN,
    and never interpreted as zero physical infrastructure on the ground.
    """
    df_infra = pd.read_csv(INFRASTRUCTURE_LEDGER_PATH)
    assert len(df_infra) == 518

    # Verify inventory status flag and policy
    assert (df_infra["inventory_status"] == "INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS").all()
    assert (df_infra["inventory_confidence"] == "UNKNOWN").all()
    assert (df_infra["inventory_data_policy"] == "ABSENT_INVENTORY_IS_NOT_ZERO_INFRASTRUCTURE").all()

    # Ensure Category B (maintenance/desilting) is not spuriously assigned without structure data
    df_eval = pd.read_csv(EVIDENCE_ASSESSMENT_PATH)
    assert (df_eval["provisional_action_category_MAR"] != "Category B: Maintenance, Desilting & Restoration Assessment").all()
    assert (df_eval["provisional_action_category_SWH"] != "Category B: Maintenance, Desilting & Restoration Assessment").all()


def test_baseline_mcda_scores_and_rankings_immutability():
    """
    Verify that all Phase 3 and Phase 4 baseline artifacts remain bit-for-bit identical,
    and that evidence assessment scores exactly replicate the baseline audit table.
    """
    for filepath, expected_hash in BASELINE_HASHES.items():
        assert os.path.exists(filepath), f"Missing baseline file: {filepath}"
        actual_hash = compute_sha256(filepath)
        assert actual_hash == expected_hash, f"Hash mismatch for {filepath}: {actual_hash} vs {expected_hash}"

    df_eval = pd.read_csv(EVIDENCE_ASSESSMENT_PATH)
    df_audit = pd.read_csv("data/processed/jaldrishti_consensus_priority_audit.csv")

    assert (df_eval["HYBAS_ID"] == df_audit["HYBAS_ID"]).all()
    assert np.allclose(df_eval["preliminary_screening_score"], df_audit["preliminary_screening_score"])
    assert np.allclose(df_eval["score_S4_Managed_Aquifer_Recharge"], df_audit["score_S4_Managed_Aquifer_Recharge"])
    assert np.allclose(df_eval["score_S5_Surface_Water_Harvesting"], df_audit["score_S5_Surface_Water_Harvesting"])
    assert (df_eval["rank_S4_Managed_Aquifer_Recharge"] == df_audit["rank_S4_Managed_Aquifer_Recharge"]).all()
    assert (df_eval["rank_S5_Surface_Water_Harvesting"] == df_audit["rank_S5_Surface_Water_Harvesting"]).all()
    assert (df_eval["consensus_priority_tier_revised"] == df_audit["consensus_priority_tier_revised"]).all()
