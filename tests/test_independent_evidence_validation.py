# JalDrishti-AI: Independent Evidence Validation Pipeline Unit Tests
# Author: JalDrishti-AI Engineering Team
# License: Apache-2.0

import pytest
import hashlib
import numpy as np
import pandas as pd
from pathlib import Path

from scripts.validate_independent_evidence import (
    get_project_root,
    compute_theil_sen_slope,
    validate_well_schema,
    validate_coordinates,
    filter_and_deduplicate,
    process_groundwater_observations,
    validate_independent_data,
    REQUIRED_CORE_COLUMNS
)

@pytest.fixture
def project_root():
    return get_project_root()

def test_template_file_integrity_and_zero_rows(project_root):
    template_path = project_root / "data" / "raw" / "templates" / "cgwb_maharashtra_observation_wells_template.csv"
    assert template_path.exists(), f"Template CSV missing at {template_path}"

    df = pd.read_csv(template_path)
    # Mandate zero fabricated data rows
    assert len(df) == 0, f"Template must contain 0 data rows, found {len(df)}"

    # Check required core headers
    for col in REQUIRED_CORE_COLUMNS:
        assert col in df.columns, f"Required core column '{col}' missing from template"

    # Check seasonal and timeseries headers
    expected_headers = [
        "station_id", "station_name", "district", "taluka", "latitude", "longitude",
        "well_type", "aquifer_type", "observation_year", "observation_date",
        "water_level_mbgl", "pre_monsoon_wl_mbgl", "post_monsoon_wl_mbgl", "measurement_qc_flag"
    ]
    for h in expected_headers:
        assert h in df.columns, f"Expected header '{h}' missing from template"

def test_schema_validation_rejection_rules():
    # Valid schema with seasonal fields
    df_valid = pd.DataFrame({
        "station_id": ["ST01"],
        "latitude": [18.5],
        "longitude": [74.0],
        "well_type": ["Dugwell"],
        "aquifer_type": ["Basalt_Fractured"],
        "measurement_qc_flag": ["Valid"],
        "observation_year": [2020],
        "pre_monsoon_wl_mbgl": [12.0],
        "post_monsoon_wl_mbgl": [4.0]
    })
    is_valid, errors = validate_well_schema(df_valid)
    assert is_valid, f"Expected valid schema, got errors: {errors}"

    # Missing core column
    df_missing_core = df_valid.drop(columns=["latitude"])
    is_valid, errors = validate_well_schema(df_missing_core)
    assert not is_valid
    assert any("latitude" in e for e in errors)

    # Missing both seasonal and timeseries columns
    df_no_measurements = df_valid.drop(columns=["observation_year", "pre_monsoon_wl_mbgl", "post_monsoon_wl_mbgl"])
    is_valid, errors = validate_well_schema(df_no_measurements)
    assert not is_valid
    assert any("either time-series" in e for e in errors)

def test_coordinate_bounds_and_numeric_validation():
    df_test = pd.DataFrame({
        "station_id": ["S_VALID", "S_DELHI", "S_KOLKATA", "S_CORRUPT"],
        "latitude": [18.5204, 28.6139, 22.5726, "corrupt_lat"],
        "longitude": [73.8567, 77.2090, 88.3639, 74.0],
        "well_type": ["Dugwell"] * 4,
        "aquifer_type": ["Basalt"] * 4,
        "measurement_qc_flag": ["Valid"] * 4
    })

    df_clean, dropped = validate_coordinates(df_test)
    assert len(df_clean) == 1, f"Expected 1 valid Maharashtra station, retained {len(df_clean)}"
    assert dropped == 3, f"Expected 3 dropped invalid stations, got {dropped}"
    assert df_clean["station_id"].iloc[0] == "S_VALID"

def test_qc_filtering_and_deduplication():
    df_test = pd.DataFrame({
        "station_id": ["ST01", "ST01", "ST02", "ST03", "ST04"],
        "observation_year": [2020, 2020, 2020, 2020, 2020],
        "measurement_qc_flag": ["Valid", "Valid", "Dry_Well", "Pumping_Affected", "Destroyed"]
    })

    df_clean, dropped = filter_and_deduplicate(df_test, exclude_flagged_qc=True)
    assert len(df_clean) == 1, f"Expected 1 clean record, got {len(df_clean)}"
    assert dropped == 4, f"Expected 4 dropped records, got {dropped}"
    assert df_clean["station_id"].iloc[0] == "ST01"

def test_seasonal_fluctuation_calculation():
    df_input = pd.DataFrame({
        "station_id": ["ST01", "ST02"],
        "latitude": [18.5, 19.2],
        "longitude": [74.0, 75.0],
        "well_type": ["Dugwell", "Dugwell"],
        "aquifer_type": ["Basalt", "Basalt"],
        "observation_year": [2021, 2021],
        "pre_monsoon_wl_mbgl": [15.0, 8.0],
        "post_monsoon_wl_mbgl": [5.0, 10.0],  # ST01: +10m rise, ST02: -2m deficit
        "measurement_qc_flag": ["Valid", "Valid"]
    })

    df_res = process_groundwater_observations(df_input, min_years=1)
    recharge_st01 = df_res[df_res["station_id"] == "ST01"]["seasonal_recharge_median_m"].iloc[0]
    recharge_st02 = df_res[df_res["station_id"] == "ST02"]["seasonal_recharge_median_m"].iloc[0]

    assert recharge_st01 == pytest.approx(10.0, abs=1e-5), f"Expected +10m recharge, got {recharge_st01}"
    assert recharge_st02 == pytest.approx(-2.0, abs=1e-5), f"Expected -2m recharge deficit, got {recharge_st02}"

def test_theil_sen_median_slope_calculation():
    # Linear deepening of water table: 1.5 m/year depletion
    years = np.array([2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
    levels = 10.0 + 1.5 * (years - 2015)
    slope = compute_theil_sen_slope(years, levels, min_years=5)
    assert slope == pytest.approx(1.5, abs=1e-4)

    # Recovering water table: -0.8 m/year
    levels_recovery = 25.0 - 0.8 * (years - 2015)
    slope_rec = compute_theil_sen_slope(years, levels_recovery, min_years=5)
    assert slope_rec == pytest.approx(-0.8, abs=1e-4)

    # Insufficient observation years (< 5 years) must return NaN
    years_short = np.array([2015, 2016, 2017, 2018])
    levels_short = np.array([10.0, 11.0, 12.0, 13.0])
    slope_short = compute_theil_sen_slope(years_short, levels_short, min_years=5)
    assert np.isnan(slope_short)

def test_pipeline_dry_run_mode_clean_exit(project_root):
    # Test dry run when template is passed
    template_path = project_root / "data" / "raw" / "templates" / "cgwb_maharashtra_observation_wells_template.csv"
    code_template = validate_independent_data(project_root=project_root, wells_csv=template_path)
    assert code_template == 0, f"Template execution must return exit code 0, got {code_template}"

def test_phase3_and_phase4_outputs_unaltered(project_root):
    # Check consensus audit table
    audit_path = project_root / "data" / "processed" / "jaldrishti_consensus_priority_audit.csv"
    assert audit_path.exists()
    df_audit = pd.read_csv(audit_path)
    assert len(df_audit) == 518
    assert len(df_audit.columns) == 46

    # Check scenario rankings table
    rank_path = project_root / "data" / "processed" / "jaldrishti_mcda_scenario_rankings.csv"
    assert rank_path.exists()
    df_rank = pd.read_csv(rank_path)
    assert len(df_rank) == 518
    assert len(df_rank.columns) == 23

    # Check that shortlists are intact
    assert "shortlist_surface_water_harvesting" in df_audit.columns
    assert "shortlist_managed_aquifer_recharge" in df_audit.columns
    assert "shortlist_robust_consensus" in df_audit.columns
    assert df_audit["shortlist_surface_water_harvesting"].sum() == 20
    assert df_audit["shortlist_managed_aquifer_recharge"].sum() == 20
    assert df_audit["shortlist_robust_consensus"].sum() == 20

def test_cgwb_raw_files_integrity_and_hashes(project_root):
    raw_dir = project_root / "data" / "raw"
    f91 = raw_dir / "gwl_manual_quarterly_cgwb_mh_1991_2020.csv"
    f21 = raw_dir / "gwl_manual_quarterly_cgwb_mh_2021_2025.csv"

    assert f91.exists(), f"Missing {f91}"
    assert f21.exists(), f"Missing {f21}"
    assert f91.stat().st_size == 13975547, f"Size mismatch for {f91.name}"
    assert f21.stat().st_size == 1754883, f"Size mismatch for {f21.name}"

    h91 = hashlib.sha256(f91.read_bytes()).hexdigest()
    h21 = hashlib.sha256(f21.read_bytes()).hexdigest()

    assert h91 == "8e2c13f5aa5af13245cd51056ba0062550967f869901a75a56733fd28e4de3c0"
    assert h21 == "5fd40cbfc51ad349e25cd7678e3bafdac732d470986ec1c55c39a23b174b04d0"

def test_cgwb_harmonized_dataset_integrity(project_root):
    harm_path = project_root / "data" / "raw" / "cgwb_maharashtra_observation_wells.csv"
    assert harm_path.exists(), f"Missing harmonized CSV at {harm_path}"

    df = pd.read_csv(harm_path)
    assert len(df) == 43752, f"Expected 43,752 harmonized rows, got {len(df)}"
    assert len(df.columns) == 14, f"Expected 14 columns, got {len(df.columns)}"
    assert df["station_id"].nunique() == 1936, f"Expected 1,936 unique stations, got {df['station_id'].nunique()}"

    # Verify no nulls in required columns
    for col in ["station_id", "station_name", "district", "taluka", "latitude", "longitude", "observation_date", "water_level_mbgl"]:
        assert df[col].isna().sum() == 0, f"Found unexpected NaNs in column '{col}'"

    # Verify coordinate bounds
    assert df["latitude"].between(15.6, 22.1).all(), "Coordinates outside latitude bounds"
    assert df["longitude"].between(72.6, 80.9).all(), "Coordinates outside longitude bounds"

def test_cgwb_exclusion_summary_ledger(project_root):
    excl_path = project_root / "data" / "processed" / "cgwb_ingestion_exclusion_summary.csv"
    assert excl_path.exists(), f"Missing exclusion ledger at {excl_path}"

    df_ex = pd.read_csv(excl_path)
    assert len(df_ex) == 5, f"Expected 5 exclusion stages, got {len(df_ex)}"
    # Final remaining records must match harmonized dataset length
    final_remaining = df_ex["records_remaining"].iloc[-1]
    assert final_remaining == 43752, f"Ledger final count mismatch: {final_remaining} vs 43,752"

def test_empirical_validation_execution_and_results(project_root):
    harm_path = project_root / "data" / "raw" / "cgwb_maharashtra_observation_wells.csv"
    res_code = validate_independent_data(project_root=project_root, wells_csv=harm_path)
    assert res_code == 0, f"Validation execution returned non-zero code {res_code}"

    res_csv = project_root / "data" / "processed" / "jaldrishti_groundwater_validation_results.csv"
    assert res_csv.exists(), f"Results CSV missing at {res_csv}"

    df_res = pd.read_csv(res_csv)
    assert len(df_res) == 370, f"Expected 370 covered catchments, got {len(df_res)}"
    assert df_res["gw_depth_trend_median_m_yr"].notna().sum() == 355, "Expected 355 evaluated catchments with trend"
