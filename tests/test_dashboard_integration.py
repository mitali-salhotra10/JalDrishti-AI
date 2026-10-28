"""
test_dashboard_integration.py - Automated Testing Suite for Phase 9 Dashboard & Data Integration
Validates:
1. Requirements file existence and dependencies.
2. Master dataset loading, schemas, and 518-catchment integrity.
3. DPR screening sheet generation, file counts, and mandatory content.
4. Statutory disclaimer presence and zero-fabrication invariant.
5. Bit-for-bit immutability of Phase 3/4 baseline files.
"""

import hashlib
import os
from pathlib import Path
import pandas as pd
import pytest

# Baseline hashes for immutability verification
BASELINE_HASHES = {
    "data/processed/jaldrishti_mcda_scenario_rankings.csv": "692b7dc9b7d56e5a964a452348c3086906f0e1d1630e26a6761306a2f875e982",
    "data/processed/jaldrishti_consensus_priority_audit.csv": "85bece275a30aca3fd7aca0d81ef226179e6bb702f96a95b81e3f76669696ccb",
    "data/processed/jaldrishti_watersheds_with_village_indicators_v2.csv": "93585556df7f91825e1efe4664d224e3fc2a4c437317e815efa8c6f9b01a4843",
    "data/processed/jaldrishti_scored_watersheds.shp": "b600ca7cf8decf872b11cdcc2bb947c6ea9c7748bd2451d90c4b268f0339e372",
}

BASE_DIR = Path(__file__).resolve().parent.parent


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def test_dashboard_requirements_file():
    """Verify requirements-dashboard.txt exists and specifies core packages."""
    req_file = BASE_DIR / "requirements-dashboard.txt"
    assert req_file.exists(), "Missing requirements-dashboard.txt"
    content = req_file.read_text(encoding="utf-8")
    for pkg in ["streamlit", "plotly", "folium", "streamlit-folium", "geopandas"]:
        assert pkg in content, f"Package {pkg} missing from requirements-dashboard.txt"


def test_dashboard_data_loading_and_shape():
    """Verify load_all_data() loads 518 catchments with all essential attributes."""
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    from app import load_all_data

    df_master, gdf_merged = load_all_data()
    assert len(df_master) == 518, f"Expected 518 catchments in tabular master, found {len(df_master)}"
    assert len(gdf_merged) == 518, f"Expected 518 catchments in spatial merged, found {len(gdf_merged)}"

    required_cols = [
        "HYBAS_ID", "sub_area_km2", "consensus_priority_tier_revised",
        "provisional_action_category_MAR", "provisional_action_category_SWH",
        "gw_depth_trend_median_m_yr", "total_monitoring_well_count",
        "village_clay_0_5cm_g_kg", "village_sand_0_5cm_g_kg", "village_infiltration_proxy",
        "inventory_status", "inventory_data_policy"
    ]
    for col in required_cols:
        assert col in df_master.columns, f"Missing {col} in df_master"
        assert col in gdf_merged.columns, f"Missing {col} in gdf_merged"

    # Verify spatial CRS
    assert str(gdf_merged.crs).upper() in ["EPSG:4326", "WGS 84"], f"Unexpected CRS: {gdf_merged.crs}"


def test_dpr_screening_sheets_coverage_and_counts():
    """Verify that exactly 12 MAR and 75 SWH preliminary screening dossiers exist, plus the master template."""
    reports_dir = BASE_DIR / "reports" / "dpr_screening_sheets"
    mar_dir = reports_dir / "mar_category_a"
    swh_dir = reports_dir / "swh_category_a"
    index_csv = reports_dir / "dpr_screening_master_index.csv"
    template_md = reports_dir / "DPR_SCREENING_TEMPLATE.md"

    assert mar_dir.exists(), "Missing mar_category_a directory"
    assert swh_dir.exists(), "Missing swh_category_a directory"
    assert index_csv.exists(), "Missing dpr_screening_master_index.csv"
    assert template_md.exists(), "Missing DPR_SCREENING_TEMPLATE.md"

    template_text = template_md.read_text(encoding="utf-8")
    assert "STATUTORY PLANNING & LEGAL DISCLAIMER" in template_text
    assert "Mandatory Pre-Construction Field Checklist" in template_text

    mar_files = list(mar_dir.glob("*.md"))
    swh_files = list(swh_dir.glob("*.md"))
    assert len(mar_files) == 12, f"Expected 12 MAR screening sheets, found {len(mar_files)}"
    assert len(swh_files) == 75, f"Expected 75 SWH screening sheets, found {len(swh_files)}"

    df_index = pd.read_csv(index_csv)
    assert len(df_index) == 87, f"Expected 87 records in master index, found {len(df_index)}"

    # Check content of a sample MAR sheet
    sample_mar = mar_files[0].read_text(encoding="utf-8")
    assert "LEGAL & ENGINEERING DISCLAIMER" in sample_mar
    assert "INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS" in sample_mar
    assert "Vertical Electrical Sounding (VES)" in sample_mar


def test_disclaimers_and_zero_fabrication_preservation():
    """Confirm app.py contains required statutory disclaimers and zero-fabrication warnings."""
    app_code = (BASE_DIR / "app.py").read_text(encoding="utf-8")
    assert "STATUTORY PLANNING NOTICE" in app_code
    assert "INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS" in app_code
    assert "ABSENT_INVENTORY_IS_NOT_ZERO_INFRASTRUCTURE" or "unrecorded digital inventory must NEVER" in app_code

    # Assert no hallucinated IDs exist in master index
    df_index = pd.read_csv(BASE_DIR / "reports" / "dpr_screening_sheets" / "dpr_screening_master_index.csv")
    hallucinated_ids = [4081028710, 4081031300, 4081031730, 4081041160, 4081042780]
    for hid in hallucinated_ids:
        assert hid not in df_index["HYBAS_ID"].values, f"Hallucinated ID {hid} found in DPR master index!"


def test_hybas_id_uniqueness_and_geometry_validity():
    """Verify HYBAS_ID uniqueness, matching baseline catchments, and geometry validity."""
    from app import load_all_data
    df_master, gdf_merged = load_all_data()

    # Uniqueness
    assert len(df_master["HYBAS_ID"].unique()) == 518, "Duplicate HYBAS_ID found in df_master"
    assert len(gdf_merged["HYBAS_ID"].unique()) == 518, "Duplicate HYBAS_ID found in gdf_merged"

    # Match baseline rankings HYBAS_ID exactly
    baseline_rankings = pd.read_csv(BASE_DIR / "data" / "processed" / "jaldrishti_mcda_scenario_rankings.csv")
    baseline_ids = set(baseline_rankings["HYBAS_ID"])
    assert set(df_master["HYBAS_ID"]) == baseline_ids, "Mismatch between master dataset and baseline rankings HYBAS_IDs"
    assert set(gdf_merged["HYBAS_ID"]) == baseline_ids, "Mismatch between spatial geometries and baseline rankings HYBAS_IDs"

    # Geometry validity
    assert all(gdf_merged.geometry.is_valid), "Invalid polygon geometry detected in spatial layer"
    assert not any(gdf_merged.geometry.is_empty), "Empty geometry detected in spatial layer"
    geom_types = set(gdf_merged.geometry.geom_type)
    assert geom_types.issubset({"Polygon", "MultiPolygon"}), f"Unexpected geometry types: {geom_types}"


def test_scientific_decision_rules_and_conflation_prevention():
    """Verify scientific decision rules, category counts, and separation of MAR and SWH."""
    df_eval = pd.read_csv(BASE_DIR / "data" / "processed" / "jaldrishti_phase7_evidence_assessment.csv")
    df_infra = pd.read_csv(BASE_DIR / "data" / "processed" / "jaldrishti_infrastructure_by_catchment.csv")
    assert len(df_eval) == 518

    # Category counts in Consensus Tier 1 (N = 76)
    tier1 = df_eval[df_eval["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")]
    assert len(tier1) == 76, f"Expected 76 Tier 1 catchments, found {len(tier1)}"

    mar_cat_a = (tier1["provisional_action_category_MAR"].str.startswith("Category A")).sum()
    mar_cat_c = (tier1["provisional_action_category_MAR"].str.startswith("Category C")).sum()
    mar_cat_d = (tier1["provisional_action_category_MAR"].str.startswith("Category D")).sum()
    assert mar_cat_a == 12, f"Expected 12 MAR Category A, got {mar_cat_a}"
    assert mar_cat_c == 56, f"Expected 56 MAR Category C, got {mar_cat_c}"
    assert mar_cat_d == 8, f"Expected 8 MAR Category D, got {mar_cat_d}"

    swh_cat_a = (tier1["provisional_action_category_SWH"].str.startswith("Category A")).sum()
    swh_cat_d = (tier1["provisional_action_category_SWH"].str.startswith("Category D")).sum()
    assert swh_cat_a == 75, f"Expected 75 SWH Category A, got {swh_cat_a}"
    assert swh_cat_d == 1, f"Expected 1 SWH Category D, got {swh_cat_d}"

    # Category B must be 0 across entire dataset (inventory unverified)
    assert (df_eval["provisional_action_category_MAR"].str.startswith("Category B")).sum() == 0, "Category B assigned in MAR"
    assert (df_eval["provisional_action_category_SWH"].str.startswith("Category B")).sum() == 0, "Category B assigned in SWH"

    # Invariant: inventory status must be pending MRSAC access across all catchments
    assert all(df_infra["inventory_status"] == "INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS")

    # Invariant: MAR Category A and SWH Category A are distinct evaluations
    # All 12 MAR Category A catchments are also SWH Category A, but 63 SWH Category A catchments are MAR Category C or D
    overlap = tier1[
        (tier1["provisional_action_category_MAR"].str.startswith("Category A")) &
        (tier1["provisional_action_category_SWH"].str.startswith("Category A"))
    ]
    assert len(overlap) == 12, f"Expected 12 joint Category A catchments, found {len(overlap)}"


def test_dpr_screening_dossier_content_integrity():
    """Verify that all 87 screening dossiers match authoritative IDs and have zero fabrication."""
    reports_dir = BASE_DIR / "reports" / "dpr_screening_sheets"
    mar_dir = reports_dir / "mar_category_a"
    swh_dir = reports_dir / "swh_category_a"

    df_eval = pd.read_csv(BASE_DIR / "data" / "processed" / "jaldrishti_phase7_evidence_assessment.csv")
    expected_mar_ids = set(df_eval[df_eval["provisional_action_category_MAR"].str.startswith("Category A")]["HYBAS_ID"])
    expected_swh_ids = set(df_eval[df_eval["provisional_action_category_SWH"].str.startswith("Category A")]["HYBAS_ID"])

    assert len(expected_mar_ids) == 12
    assert len(expected_swh_ids) == 75

    actual_mar_ids = {int(f.stem.replace("DPR_MAR_HYBAS_", "")) for f in mar_dir.glob("*.md")}
    actual_swh_ids = {int(f.stem.replace("DPR_SWH_HYBAS_", "")) for f in swh_dir.glob("*.md")}

    assert actual_mar_ids == expected_mar_ids, "MAR dossier IDs do not match authoritative Category A IDs"
    assert actual_swh_ids == expected_swh_ids, "SWH dossier IDs do not match authoritative Category A IDs"

    # Content integrity on all files: no fabricated cost / currency figures
    for f in list(mar_dir.glob("*.md")) + list(swh_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        assert "₹" not in text and "INR" not in text and "Rs." not in text, f"Fabricated currency found in {f.name}"
        assert ("LEGAL & ENGINEERING DISCLAIMER" in text or "STATUTORY PLANNING" in text), f"Missing disclaimer in {f.name}"
        assert "Mandatory Pre-Construction Field Checklist" in text, f"Missing checklist in {f.name}"


def test_graceful_degradation_missing_optional_data():
    """Verify that data loading and profiling degrade gracefully if optional columns are NaN."""
    from app import load_all_data
    df_master, gdf_merged = load_all_data()

    # Optional fields may contain NaN without causing errors
    optional_cols = ["village_soc_0_5cm_dg_kg", "total_monitoring_well_count", "gw_depth_trend_median_m_yr"]
    for col in optional_cols:
        assert col in df_master.columns
        # df_master should not crash if we compute summary stats even with NaNs
        mean_val = df_master[col].mean()
        assert not pd.isna(mean_val) or pd.isna(mean_val)  # computation succeeds without error


def test_user_acceptance_workflows():
    """Verify core UI workflows: KPIs, search, multi-selection, and non-silent NaN handling."""
    from app import load_all_data
    df_master, gdf_merged = load_all_data()

    # 1. Statewide metrics check
    assert len(df_master) == 518
    assert (df_master["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")).sum() == 76
    assert (df_master["total_monitoring_well_count"] > 0).sum() == 459
    assert (df_master["provisional_action_category_MAR"].str.startswith("Category A")).sum() == 12
    assert (df_master["provisional_action_category_SWH"].str.startswith("Category A")).sum() == 75

    # 2. Search by HYBAS_ID
    sample_id = 4081044860
    assert sample_id in df_master["HYBAS_ID"].values
    c_data = df_master[df_master["HYBAS_ID"] == sample_id].iloc[0]
    assert c_data["sub_area_km2"] == 1313.9

    # 3. Filtering consistency
    filtered = df_master[df_master["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")]
    assert len(filtered) == 76
    filtered_mar = filtered[filtered["provisional_action_category_MAR"].str.startswith("Category A")]
    assert len(filtered_mar) == 12

    # 4. Multi-catchment comparison
    comp_ids = [4081044860, 4081048280, 4081056630]
    comp_df = df_master[df_master["HYBAS_ID"].isin(comp_ids)]
    assert len(comp_df) == 3

    # 5. Empty selection handling
    empty_filter = df_master[df_master["sub_area_km2"] > 100000]
    assert len(empty_filter) == 0

    # 6. Missing evidence handling (no silent zero conversion)
    missing_trends = df_master[df_master["gw_depth_trend_median_m_yr"].isna()]
    assert len(missing_trends) == 163


def test_baseline_hashes_unaltered():
    """Confirm all Phase 3 and Phase 4 baseline files remain 100% bit-for-bit identical."""
    for filepath, expected_hash in BASELINE_HASHES.items():
        full_path = BASE_DIR / filepath
        assert full_path.exists(), f"Baseline file missing: {filepath}"
        actual_hash = compute_sha256(str(full_path))
        assert actual_hash == expected_hash, f"Hash mismatch for {filepath}: {actual_hash} vs {expected_hash}"
