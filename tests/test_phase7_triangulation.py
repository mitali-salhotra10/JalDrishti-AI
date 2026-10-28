"""
test_phase7_triangulation.py - Automated Quality Assurance Suite for Phase 7
Multi-Evidence Triangulation and Infrastructure Saturation.

Validates:
1. GSDA Raw Data Integrity and SHA-256 Hash.
2. Catchment Infrastructure Ledger Schema, Invariants, and Zero-Fabrication Policy.
3. Multi-Evidence Assessment Schema, Tier 1 Cardinality, and Category Validity.
4. Separate Screening of MAR vs. SWH.
5. Bit-for-bit Immutability of Phase 3 and Phase 4 Baseline Artifacts.
"""

import hashlib
import os
import pandas as pd
import pytest

# Constants & Paths
RAW_GSDA_PATH = "data/raw/ground_water_level_manual_quarterly_maharashtra_1970_2025.csv"
EXPECTED_GSDA_SIZE = 91492435
EXPECTED_GSDA_HASH = "5003c9030b34df310f0bdd0527df022b9b0e73aa780b5bbacc88cc49d1be0eb6"

INFRASTRUCTURE_LEDGER_PATH = "data/processed/jaldrishti_infrastructure_by_catchment.csv"
EVIDENCE_ASSESSMENT_PATH = "data/processed/jaldrishti_phase7_evidence_assessment.csv"

# Baseline hashes for immutability verification
BASELINE_HASHES = {
    "data/processed/jaldrishti_mcda_scenario_rankings.csv": "692b7dc9b7d56e5a964a452348c3086906f0e1d1630e26a6761306a2f875e982",
    "data/processed/jaldrishti_consensus_priority_audit.csv": "85bece275a30aca3fd7aca0d81ef226179e6bb702f96a95b81e3f76669696ccb",
    "data/processed/jaldrishti_watersheds_with_village_indicators_v2.csv": "93585556df7f91825e1efe4664d224e3fc2a4c437317e815efa8c6f9b01a4843",
    "data/processed/jaldrishti_scored_watersheds.shp": "b600ca7cf8decf872b11cdcc2bb947c6ea9c7748bd2451d90c4b268f0339e372",
}


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def test_gsda_raw_file_integrity_and_hash():
    """Verify GSDA raw CSV exists, matches expected size and SHA-256 hash."""
    assert os.path.exists(RAW_GSDA_PATH), f"Raw GSDA dataset not found at {RAW_GSDA_PATH}"
    actual_size = os.path.getsize(RAW_GSDA_PATH)
    assert actual_size == EXPECTED_GSDA_SIZE, f"GSDA file size mismatch: {actual_size} vs {EXPECTED_GSDA_SIZE}"
    actual_hash = compute_sha256(RAW_GSDA_PATH)
    assert actual_hash == EXPECTED_GSDA_HASH, f"GSDA SHA-256 mismatch: {actual_hash} vs {EXPECTED_GSDA_HASH}"


def test_catchment_infrastructure_ledger_schema_and_zero_fabrication():
    """Verify catchment infrastructure ledger has 518 rows, required columns, and zero fabrication policy."""
    assert os.path.exists(INFRASTRUCTURE_LEDGER_PATH), f"Missing ledger at {INFRASTRUCTURE_LEDGER_PATH}"
    df = pd.read_csv(INFRASTRUCTURE_LEDGER_PATH)
    assert len(df) == 518, f"Expected 518 catchments, found {len(df)}"

    required_cols = [
        "HYBAS_ID",
        "sub_area_km2",
        "structure_count_total",
        "designed_storage_capacity_m3",
        "designed_storage_capacity_m3_per_km2",
        "inventory_status",
        "inventory_confidence",
        "inventory_data_policy",
        "cgwb_monitoring_well_count",
        "gsda_monitoring_well_count",
        "total_monitoring_well_count",
        "monitoring_network_coverage_flag",
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column {col} in infrastructure ledger"

    # Strict Zero-Fabrication Verification
    assert (df["structure_count_total"] == 0).all(), "Fabricated structure counts detected!"
    assert (df["designed_storage_capacity_m3"] == 0.0).all(), "Fabricated storage capacity detected!"
    assert (df["inventory_status"] == "INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS").all(), \
        "Missing explicit inventory unavailable status!"

    # Multi-Agency Monitoring Network Coverage Verification
    monitored_catchments = df[df["total_monitoring_well_count"] > 0]
    assert len(monitored_catchments) == 459, \
        f"Expected 459 catchments with combined well monitoring, found {len(monitored_catchments)}"
    assert (df["total_monitoring_well_count"] >= df["cgwb_monitoring_well_count"]).all()
    assert (df["total_monitoring_well_count"] >= df["gsda_monitoring_well_count"]).all()


def test_evidence_assessment_schema_and_shortlist_preservation():
    """Verify evidence assessment schema, row count, and exact preservation of baseline shortlist counts."""
    assert os.path.exists(EVIDENCE_ASSESSMENT_PATH), f"Missing assessment at {EVIDENCE_ASSESSMENT_PATH}"
    df = pd.read_csv(EVIDENCE_ASSESSMENT_PATH)
    assert len(df) == 518, f"Expected 518 catchments, found {len(df)}"

    required_cols = [
        "HYBAS_ID",
        "sub_area_km2",
        "preliminary_screening_score",
        "score_S1_Equal_Pillars",
        "score_S2_AHP_Expert",
        "score_S4_Managed_Aquifer_Recharge",
        "rank_S4_Managed_Aquifer_Recharge",
        "score_S5_Surface_Water_Harvesting",
        "rank_S5_Surface_Water_Harvesting",
        "consensus_priority_tier_revised",
        "shortlist_surface_water_harvesting",
        "shortlist_managed_aquifer_recharge",
        "shortlist_robust_consensus",
        "evidence_confidence_level",
        "provisional_action_category_MAR",
        "provisional_screening_rationale_MAR",
        "provisional_action_category_SWH",
        "provisional_screening_rationale_SWH",
        "screening_disclaimer",
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column {col} in evidence assessment"

    # Tier 1 Count Preservation
    tier1 = df[df["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")]
    assert len(tier1) == 76, f"Expected 76 Consensus Tier 1 catchments, found {len(tier1)}"

    # Specialized Shortlist Cardinality Preservation
    assert df["shortlist_surface_water_harvesting"].sum() == 20, "SWH shortlist cardinality altered!"
    assert df["shortlist_managed_aquifer_recharge"].sum() == 20, "MAR shortlist cardinality altered!"
    assert df["shortlist_robust_consensus"].sum() == 20, "Robust consensus shortlist cardinality altered!"


def test_provisional_action_categories_and_divergence():
    """Verify action categories A-D validity and clear separation between MAR and SWH."""
    df = pd.read_csv(EVIDENCE_ASSESSMENT_PATH)
    tier1 = df[df["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")]

    valid_mar_categories = [
        "Category A: Potential New Infrastructure Assessment (MAR)",
        "Category B: Maintenance, Desilting & Restoration Assessment",
        "Category C: Mixed or Conflicting Evidence Requiring Field Assessment",
        "Category D: Insufficient Evidence",
    ]
    valid_swh_categories = [
        "Category A: Potential New Infrastructure Assessment (SWH)",
        "Category B: Maintenance, Desilting & Restoration Assessment",
        "Category C: Mixed or Conflicting Evidence Requiring Field Assessment",
        "Category D: Insufficient Evidence",
    ]

    for cat in tier1["provisional_action_category_MAR"]:
        assert cat in valid_mar_categories, f"Invalid MAR category: {cat}"

    for cat in tier1["provisional_action_category_SWH"]:
        assert cat in valid_swh_categories, f"Invalid SWH category: {cat}"

    # Verify MAR and SWH do NOT collapse into identical classifications
    mar_counts = tier1["provisional_action_category_MAR"].value_counts()
    swh_counts = tier1["provisional_action_category_SWH"].value_counts()
    assert not mar_counts.equals(swh_counts), "MAR and SWH action categories must not be identical!"

    # In SWH, 75 of 76 Tier 1 catchments qualify for Category A based on surface runoff deficit/slope
    assert swh_counts["Category A: Potential New Infrastructure Assessment (SWH)"] == 75

    # In MAR, exactly 12 catchments with confirmed decadal water-table depletion qualify for Category A
    # (56 are Category C due to rising water tables or inconclusive trends, and 8 are Category D)
    assert mar_counts["Category A: Potential New Infrastructure Assessment (MAR)"] == 12
    assert mar_counts["Category C: Mixed or Conflicting Evidence Requiring Field Assessment"] == 56
    assert mar_counts["Category D: Insufficient Evidence"] == 8


def test_baseline_artifacts_remain_unaltered():
    """Confirm all Phase 3 and Phase 4 baseline files remain bit-for-bit identical."""
    for filepath, expected_hash in BASELINE_HASHES.items():
        assert os.path.exists(filepath), f"Baseline file missing: {filepath}"
        actual_hash = compute_sha256(filepath)
        assert actual_hash == expected_hash, (
            f"Baseline file corrupted or modified! File: {filepath}\n"
            f"Expected SHA-256: {expected_hash}\n"
            f"Actual SHA-256:   {actual_hash}"
        )
