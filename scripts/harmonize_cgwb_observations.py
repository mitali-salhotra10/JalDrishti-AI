# JalDrishti-AI: CGWB Groundwater Observation Harmonization Pipeline
# Author: JalDrishti-AI Engineering Team
# License: Apache-2.0
"""
Harmonizes raw Central Ground Water Board (CGWB) quarterly manual observation records
downloaded from the National Water Data Portal (NWDP / NWIC, Ministry of Jal Shakti)
into the standardized 14-column JalDrishti-AI ingestion schema.
Filters strictly to the 2015-2024 decadal target window, enforces unambiguous station
identification, filters unphysical or duplicate values, and generates an auditable,
traceable exclusion summary ledger.
"""

import sys
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

# Bounding box for Maharashtra State
MH_LAT_MIN, MH_LAT_MAX = 15.6, 22.1
MH_LON_MIN, MH_LON_MAX = 72.6, 80.9

TARGET_COLUMNS = [
    "station_id",
    "station_name",
    "district",
    "taluka",
    "latitude",
    "longitude",
    "well_type",
    "aquifer_type",
    "observation_year",
    "observation_date",
    "water_level_mbgl",
    "pre_monsoon_wl_mbgl",
    "post_monsoon_wl_mbgl",
    "measurement_qc_flag"
]

def clean_name(val: str) -> str:
    if pd.isna(val):
        return "UNKNOWN"
    return str(val).strip().replace(" ", "_").replace("/", "_").replace("-", "_")

def harmonize_cgwb_datasets(
    raw_dir: Path,
    output_csv: Path,
    exclusion_csv: Path,
    start_year: int = 2015,
    end_year: int = 2024
):
    print("=" * 78)
    print("JALDRISHTI-AI: CGWB OBSERVATION HARMONIZATION PIPELINE")
    print("=" * 78)

    file_1991_2020 = raw_dir / "gwl_manual_quarterly_cgwb_mh_1991_2020.csv"
    file_2021_2025 = raw_dir / "gwl_manual_quarterly_cgwb_mh_2021_2025.csv"

    if not file_1991_2020.exists() or not file_2021_2025.exists():
        print(f"[ERROR] Required raw files missing in {raw_dir}:")
        print(f"  - {file_1991_2020.name}: {'FOUND' if file_1991_2020.exists() else 'MISSING'}")
        print(f"  - {file_2021_2025.name}: {'FOUND' if file_2021_2025.exists() else 'MISSING'}")
        return 1

    print(f"Loading raw CGWB files from {raw_dir}...")
    df_91 = pd.read_csv(file_1991_2020)
    df_21 = pd.read_csv(file_2021_2025)
    print(f"  Loaded {len(df_91):,} rows from {file_1991_2020.name}")
    print(f"  Loaded {len(df_21):,} rows from {file_2021_2025.name}")

    total_raw_rows = len(df_91) + len(df_21)
    df_all = pd.concat([df_91, df_21], ignore_index=True)
    print(f"Total raw observations combined: {total_raw_rows:,}")

    # Track sequential exclusions
    exclusion_records = []
    current_count = total_raw_rows

    # 1. Parse timestamps
    df_all["parsed_datetime"] = pd.to_datetime(
        df_all["Data Acquisition Time"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )
    # Fallback parsing for dates without time
    mask_nat = df_all["parsed_datetime"].isna()
    if mask_nat.sum() > 0:
        df_all.loc[mask_nat, "parsed_datetime"] = pd.to_datetime(
            df_all.loc[mask_nat, "Data Acquisition Time"],
            format="%d-%m-%Y",
            errors="coerce"
        )

    # Exclusion: Unparseable date
    unparseable_dates = df_all["parsed_datetime"].isna().sum()
    df_valid_dates = df_all[df_all["parsed_datetime"].notna()].copy()
    current_count -= unparseable_dates
    exclusion_records.append({
        "stage": 1,
        "filter_criterion": "Unparseable Date / Malformed Timestamp",
        "records_excluded": int(unparseable_dates),
        "records_remaining": int(current_count),
        "pct_of_original": round(unparseable_dates / total_raw_rows * 100, 4)
    })

    # 2. Filter to target temporal window (start_year to end_year)
    df_valid_dates["obs_year"] = df_valid_dates["parsed_datetime"].dt.year
    outside_prior = (df_valid_dates["obs_year"] < start_year).sum()
    outside_post = (df_valid_dates["obs_year"] > end_year).sum()
    total_outside_window = outside_prior + outside_post

    df_window = df_valid_dates[
        (df_valid_dates["obs_year"] >= start_year) & 
        (df_valid_dates["obs_year"] <= end_year)
    ].copy()
    current_count -= total_outside_window
    exclusion_records.append({
        "stage": 2,
        "filter_criterion": f"Outside Decadal Window ({start_year}-{end_year})",
        "records_excluded": int(total_outside_window),
        "records_remaining": int(current_count),
        "pct_of_original": round(total_outside_window / total_raw_rows * 100, 4)
    })

    # 3. Measurement value validation
    val_col = "Groundwater Level Quarterly Manual (meter)"
    df_window["wl_numeric"] = pd.to_numeric(df_window[val_col], errors="coerce")
    null_wl = df_window["wl_numeric"].isna().sum()
    negative_wl = (df_window["wl_numeric"] < 0).sum()
    total_invalid_wl = null_wl + negative_wl

    df_valid_wl = df_window[df_window["wl_numeric"].notna() & (df_window["wl_numeric"] >= 0)].copy()
    current_count -= total_invalid_wl
    exclusion_records.append({
        "stage": 3,
        "filter_criterion": "Missing (NaN) or Negative Depth Value",
        "records_excluded": int(total_invalid_wl),
        "records_remaining": int(current_count),
        "pct_of_original": round(total_invalid_wl / total_raw_rows * 100, 4)
    })

    # 4. Coordinate validity & bounding box check
    df_valid_wl["lat_numeric"] = pd.to_numeric(df_valid_wl["Latitude"], errors="coerce")
    df_valid_wl["lon_numeric"] = pd.to_numeric(df_valid_wl["Longitude"], errors="coerce")

    invalid_coords = (
        df_valid_wl["lat_numeric"].isna() | 
        df_valid_wl["lon_numeric"].isna() |
        (~df_valid_wl["lat_numeric"].between(MH_LAT_MIN, MH_LAT_MAX)) |
        (~df_valid_wl["lon_numeric"].between(MH_LON_MIN, MH_LON_MAX))
    ).sum()

    df_valid_coords = df_valid_wl[
        df_valid_wl["lat_numeric"].notna() & 
        df_valid_wl["lon_numeric"].notna() &
        df_valid_wl["lat_numeric"].between(MH_LAT_MIN, MH_LAT_MAX) &
        df_valid_wl["lon_numeric"].between(MH_LON_MIN, MH_LON_MAX)
    ].copy()
    current_count -= invalid_coords
    exclusion_records.append({
        "stage": 4,
        "filter_criterion": f"Invalid Coordinates or Outside MH Envelope [{MH_LAT_MIN}-{MH_LAT_MAX}N, {MH_LON_MIN}-{MH_LON_MAX}E]",
        "records_excluded": int(invalid_coords),
        "records_remaining": int(current_count),
        "pct_of_original": round(invalid_coords / total_raw_rows * 100, 4)
    })

    # 5. Build deterministic unique station key and deduplicate on (station_id, observation_date)
    # Using District LGD Code, District, Tehsil, Station name, and coordinates
    df_valid_coords["dist_lgd"] = df_valid_coords["District LGD Code"].fillna(0).astype(int).astype(str)
    df_valid_coords["dist_clean"] = df_valid_coords["District"].apply(clean_name).str.upper()
    df_valid_coords["tehsil_clean"] = df_valid_coords["Tehsil"].apply(clean_name).str.upper()
    df_valid_coords["station_clean"] = df_valid_coords["Station"].apply(clean_name)
    df_valid_coords["lat_str"] = df_valid_coords["lat_numeric"].round(4).astype(str)
    df_valid_coords["lon_str"] = df_valid_coords["lon_numeric"].round(4).astype(str)

    df_valid_coords["station_id"] = (
        "CGWB_" + 
        df_valid_coords["dist_lgd"] + "_" + 
        df_valid_coords["dist_clean"] + "_" + 
        df_valid_coords["tehsil_clean"] + "_" + 
        df_valid_coords["station_clean"] + "_" + 
        df_valid_coords["lat_str"] + "_" + 
        df_valid_coords["lon_str"]
    )

    df_valid_coords["obs_date_str"] = df_valid_coords["parsed_datetime"].dt.strftime("%Y-%m-%d")

    duplicate_obs = df_valid_coords.duplicated(subset=["station_id", "obs_date_str"], keep="first").sum()
    df_clean = df_valid_coords.drop_duplicates(subset=["station_id", "obs_date_str"], keep="first").copy()
    current_count -= duplicate_obs
    exclusion_records.append({
        "stage": 5,
        "filter_criterion": "Duplicate Station-Date Observation (Retained First)",
        "records_excluded": int(duplicate_obs),
        "records_remaining": int(current_count),
        "pct_of_original": round(duplicate_obs / total_raw_rows * 100, 4)
    })

    # 6. Map to target 14-column template schema
    df_clean["station_name"] = df_clean["Station"].str.strip()
    df_clean["district"] = df_clean["District"].str.strip()
    df_clean["taluka"] = df_clean["Tehsil"].str.strip()
    df_clean["latitude"] = df_clean["lat_numeric"]
    df_clean["longitude"] = df_clean["lon_numeric"]
    df_clean["well_type"] = "Observation_Well"
    # Documented aquifer information is not explicit in CGWB quarterly file -> set to Unknown per policy
    df_clean["aquifer_type"] = "Unknown"
    df_clean["observation_year"] = df_clean["obs_year"]
    df_clean["observation_date"] = df_clean["obs_date_str"]
    df_clean["water_level_mbgl"] = df_clean["wl_numeric"]
    df_clean["pre_monsoon_wl_mbgl"] = np.nan
    df_clean["post_monsoon_wl_mbgl"] = np.nan
    df_clean["measurement_qc_flag"] = "Valid"

    df_output = df_clean[TARGET_COLUMNS].copy()

    # Save outputs
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_output.to_csv(output_csv, index=False)
    print(f"\n[SAVED] Mapped ingestion dataset saved to {output_csv.name}")
    print(f"  Rows: {len(df_output):,}, Columns: {len(df_output.columns)}")
    print(f"  Distinct Monitoring Stations: {df_output['station_id'].nunique():,}")
    print(f"  Observation Date Range: {df_output['observation_date'].min()} to {df_output['observation_date'].max()}")

    # Save exclusion ledger
    df_exclusions = pd.DataFrame(exclusion_records)
    exclusion_csv.parent.mkdir(parents=True, exist_ok=True)
    df_exclusions.to_csv(exclusion_csv, index=False)
    print(f"\n[SAVED] Exclusion ledger saved to {exclusion_csv.name}")
    print(df_exclusions.to_string(index=False))

    print("\n[COMPLETE] Harmonization finished successfully.")
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Harmonize CGWB raw observation datasets")
    parser.add_argument("--raw-dir", type=str, default="data/raw", help="Path to raw data directory")
    parser.add_argument("--output", type=str, default="data/raw/cgwb_maharashtra_observation_wells.csv", help="Output CSV path")
    parser.add_argument("--exclusions", type=str, default="data/processed/cgwb_ingestion_exclusion_summary.csv", help="Exclusion summary CSV path")
    parser.add_argument("--start-year", type=int, default=2015, help="Start year of decadal window")
    parser.add_argument("--end-year", type=int, default=2024, help="End year of decadal window")
    args = parser.parse_args()

    sys.exit(harmonize_cgwb_datasets(
        raw_dir=Path(args.raw_dir),
        output_csv=Path(args.output),
        exclusion_csv=Path(args.exclusions),
        start_year=args.start_year,
        end_year=args.end_year
    ))
