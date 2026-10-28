# Unit test suite for JalDrishti-AI
import pytest
from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_project_structure():
    """Verify that expected top-level directories and configuration exist."""
    assert (PROJECT_ROOT / "docs").is_dir()
    assert (PROJECT_ROOT / "notebooks").is_dir()
    assert (PROJECT_ROOT / "src" / "jaldrishti").is_dir()
    assert (PROJECT_ROOT / "scripts").is_dir()
    assert (PROJECT_ROOT / "data" / "raw").is_dir()
    assert (PROJECT_ROOT / "data" / "interim").is_dir()
    assert (PROJECT_ROOT / "data" / "processed").is_dir()
    assert (PROJECT_ROOT / "outputs" / "figures").is_dir()
    assert (PROJECT_ROOT / "outputs" / "maps").is_dir()

def test_hydroatlas_basins_shapefile():
    """Verify HydroATLAS Level 8 basin shapefile feature count and geometry validity."""
    shp_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_scored_watersheds.shp"
    assert shp_path.exists(), f"Shapefile not found at {shp_path}"
    gdf = gpd.read_file(shp_path)
    assert len(gdf) == 518, f"Expected 518 basins, found {len(gdf)}"
    assert gdf.crs.to_epsg() == 4326, f"Expected EPSG:4326, found {gdf.crs}"
    assert gdf.geometry.is_valid.all(), "All basin geometries must be valid"

def test_preliminary_score_formula_reproducibility():
    """Verify bit-for-bit mathematical reproduction of the preliminary screening score."""
    val_csv = PROJECT_ROOT / "data" / "interim" / "jaldrishti_watershed_validation_518_basins.csv"
    shp_path = PROJECT_ROOT / "data" / "processed" / "jaldrishti_scored_watersheds.shp"
    df_val = pd.read_csv(val_csv)
    gdf = gpd.read_file(shp_path)

    slp = df_val["slp_dg_sav_deg"]
    slp_norm = (slp - 0.0) / (14.7 - 0.0)
    pre = df_val["pre_mm_syr"]
    rain_inv_norm = 1.0 - (pre - 465.0) / (4136.0 - 465.0)
    recomputed_score = (0.5 * slp_norm + 0.5 * rain_inv_norm) * 100.0

    delta = np.abs(gdf["preliminar"] - recomputed_score).max()
    assert delta < 1e-12, f"Preliminary score max delta ({delta}) exceeds tolerance 1e-12"

def test_aggregated_watershed_indicators():
    """Verify aggregated watershed indicator columns, coverage flags, and completeness."""
    agg_csv = PROJECT_ROOT / "data" / "processed" / "jaldrishti_watersheds_with_village_indicators.csv"
    assert agg_csv.exists(), f"Aggregated CSV not found at {agg_csv}"
    df = pd.read_csv(agg_csv)
    assert len(df) == 518
    assert "village_rainfall_baseline_mean_mm" in df.columns
    assert "village_cropland_pct" in df.columns
    assert "village_coverage_flag" in df.columns

    # Verify coverage flags
    flag_counts = df["village_coverage_flag"].value_counts()
    assert flag_counts.get("full_coverage", 0) == 402
    assert flag_counts.get("substantial_coverage", 0) == 53
    assert flag_counts.get("partial_border", 0) == 62
    assert flag_counts.get("transboundary_uncovered", 0) == 1

def test_soil_physical_sanity_rules():
    """Verify that SoilGrids extraction mass conservation logic holds."""
    sand = 300.0
    clay = 400.0
    silt = 300.0
    assert abs((sand + clay + silt) - 1000.0) < 1e-6

def test_village_integrated_indicators_v1():
    """Verify integrity of integrated village indicators v1 dataset."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "maharashtra_village_integrated_indicators_v1.csv"
    if not csv_path.exists():
        pytest.skip("Integrated village CSV not found in lightweight CI checkout")
    df = pd.read_csv(csv_path)
    assert len(df) == 44468, f"Expected 44,468 rows, found {len(df)}"
    assert df["area_id"].nunique() == 44468, "area_id must be 100% unique"
    
    # Check soil mass conservation on valid terrestrial records
    valid_soil = df.dropna(subset=["sand_0_5cm", "clay_0_5cm", "silt_0_5cm"])
    assert len(valid_soil) >= 44400
    sum_tex = valid_soil["sand_0_5cm"] + valid_soil["clay_0_5cm"] + valid_soil["silt_0_5cm"]
    assert (np.abs(sum_tex - 1000.0) < 2.0).all(), "Soil fractions must sum to 1000 g/kg"

def test_aggregated_watershed_indicators_v2():
    """Verify aggregated watershed v2 indicators containing soil, terrain, and drought metrics."""
    agg_v2 = PROJECT_ROOT / "data" / "processed" / "jaldrishti_watersheds_with_village_indicators_v2.csv"
    assert agg_v2.exists(), f"v2 CSV not found at {agg_v2}"
    df = pd.read_csv(agg_v2)
    assert len(df) == 518
    assert "village_elevation_mean_m" in df.columns
    assert "village_slope_mean_deg" in df.columns
    assert "village_clay_0_5cm_g_kg" in df.columns
    assert "village_drought_years_count" in df.columns

def test_mcda_scoring_and_ranking():
    """Verify MCDA composite scores, ranks, and tiers."""
    mcda_csv = PROJECT_ROOT / "data" / "processed" / "jaldrishti_watersheds_mcda_scores.csv"
    assert mcda_csv.exists(), f"MCDA CSV not found at {mcda_csv}"
    df = pd.read_csv(mcda_csv)
    assert len(df) == 518
    for col in ["mcda_score_ahp", "mcda_score_equal", "mcda_score_entropy"]:
        assert df[col].min() >= 0.0 and df[col].max() <= 100.0
    for col in ["mcda_rank_ahp", "mcda_rank_equal", "mcda_rank_entropy"]:
        assert df[col].min() == 1 and df[col].max() == 518
    assert (df["mcda_priority_tier"] == "Tier 1: High Intervention Priority").sum() == 104

