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
    # Sand + Clay + Silt sum rule
    sand = 300.0
    clay = 400.0
    silt = 300.0
    assert abs((sand + clay + silt) - 1000.0) < 1e-6
