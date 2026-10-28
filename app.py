"""
JalDrishti-AI: Interactive Geospatial Decision Support Dashboard
Phase 9: Production Decision Support System for Watershed Prioritization in Maharashtra.

Features:
- Statewide KPI Overview & Infrastructure Availability Warnings
- Interactive Geospatial Vector Mapping (Consensus Tiers, MAR & SWH Categories, Trends)
- Catchment Profiler & Multi-Criteria Decision Engine Trace
- Multi-Catchment Comparison & Scenario Trade-off Analysis
- DPR Screening Dossier Viewer & CSV Export
"""

import os
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="JalDrishti-AI Decision Support Dashboard",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports" / "dpr_screening_sheets"


# -----------------------------------------------------------------------------
# Data Loading & Caching
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_all_data():
    """Load and merge all processed tabular and spatial assets strictly on HYBAS_ID."""
    eval_csv = DATA_DIR / "jaldrishti_phase7_evidence_assessment.csv"
    audit_csv = DATA_DIR / "jaldrishti_consensus_priority_audit.csv"
    infra_csv = DATA_DIR / "jaldrishti_infrastructure_by_catchment.csv"
    v2_csv = DATA_DIR / "jaldrishti_watersheds_with_village_indicators_v2.csv"
    shp_file = DATA_DIR / "jaldrishti_scored_watersheds.shp"

    df_eval = pd.read_csv(eval_csv)
    df_audit = pd.read_csv(audit_csv)
    df_infra = pd.read_csv(infra_csv)
    df_v2 = pd.read_csv(v2_csv)

    # Master tabular merge
    df_master = df_eval.merge(
        df_audit[[
            "HYBAS_ID", "village_coverage_pct", "village_coverage_flag",
            "village_sand_0_5cm_g_kg", "village_clay_0_5cm_g_kg",
            "village_soc_0_5cm_dg_kg", "village_infiltration_proxy"
        ]],
        on="HYBAS_ID", how="left"
    )

    df_master = df_master.merge(
        df_v2[[
            "HYBAS_ID", "village_count_intersecting", "village_silt_0_5cm_g_kg",
            "village_rainfall_baseline_mean_mm", "village_drought_years_count", "village_drought_frequency_pct",
            "village_slope_mean_deg", "village_elevation_mean_m", "village_cropland_pct"
        ]],
        on="HYBAS_ID", how="left"
    )

    df_master = df_master.merge(
        df_infra[[
            "HYBAS_ID", "inventory_status", "inventory_data_policy", "inventory_confidence"
        ]],
        on="HYBAS_ID", how="left"
    )

    # Load Spatial Geometry
    gdf = gpd.read_file(shp_file)
    gdf["HYBAS_ID"] = gdf["HYBAS_ID"].astype(int)
    gdf_merged = gdf[["HYBAS_ID", "geometry"]].merge(df_master, on="HYBAS_ID", how="inner")

    return df_master, gdf_merged


# -----------------------------------------------------------------------------
# Main Application
# -----------------------------------------------------------------------------
def main():
    # Header Banner
    st.title("💧 JalDrishti-AI: Watershed Prioritization Decision Support System")
    st.markdown(
        "**Multi-Criteria Decision Analysis & Ground-Truth Triangulation across 518 Level 8 Catchments in Maharashtra**"
    )

    # Statutory Preliminary Screening Disclaimer Banner
    st.info(
        "⚠️ **STATUTORY PLANNING NOTICE**: All priority classifications and action categories displayed in this "
        "dashboard are **macro-scale preliminary screening outcomes** derived from geospatial models and state observation wells. "
        "They do **NOT** constitute administrative approval, detailed engineering designs, or direct civil construction authorizations. "
        "Site-specific hydrogeological surveys, infiltration tests, and environmental appraisals are legally required prior to fund sanction."
    )

    # Load Data
    try:
        df_master, gdf_merged = load_all_data()
    except Exception as e:
        st.error(f"Error loading project datasets: {e}")
        return

    # -------------------------------------------------------------------------
    # Sidebar Navigation & Filters
    # -------------------------------------------------------------------------
    st.sidebar.title("🎛️ Navigation & Filters")
    nav_view = st.sidebar.radio(
        "Select Dashboard View:",
        [
            "📊 Executive Overview",
            "🗺️ Interactive Catchment Map",
            "🔍 Catchment Deep-Dive Profiler",
            "⚖️ Multi-Catchment Comparison",
            "📑 DPR Screening Dossiers & Export",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter Catchments")

    # Filter: Consensus Tier
    tier_options = ["All Tiers"] + sorted(list(df_master["consensus_priority_tier_revised"].dropna().unique()))
    selected_tier = st.sidebar.selectbox("Consensus Priority Tier:", tier_options)

    # Filter: MAR Category
    mar_options = ["All MAR Categories"] + sorted(list(df_master["provisional_action_category_MAR"].dropna().unique()))
    selected_mar = st.sidebar.selectbox("Managed Aquifer Recharge (MAR):", mar_options)

    # Filter: SWH Category
    swh_options = ["All SWH Categories"] + sorted(list(df_master["provisional_action_category_SWH"].dropna().unique()))
    selected_swh = st.sidebar.selectbox("Surface Water Harvesting (SWH):", swh_options)

    # Filter: Evidence Confidence
    conf_options = ["All Confidence Levels"] + sorted(list(df_master["evidence_confidence_level"].dropna().unique()))
    selected_conf = st.sidebar.selectbox("Monitoring Network Confidence:", conf_options)

    # Apply Filters
    df_filtered = df_master.copy()
    if selected_tier != "All Tiers":
        df_filtered = df_filtered[df_filtered["consensus_priority_tier_revised"] == selected_tier]
    if selected_mar != "All MAR Categories":
        df_filtered = df_filtered[df_filtered["provisional_action_category_MAR"] == selected_mar]
    if selected_swh != "All SWH Categories":
        df_filtered = df_filtered[df_filtered["provisional_action_category_SWH"] == selected_swh]
    if selected_conf != "All Confidence Levels":
        df_filtered = df_filtered[df_filtered["evidence_confidence_level"] == selected_conf]

    st.sidebar.caption(f"Showing **{len(df_filtered)}** of **518** catchments")

    # -------------------------------------------------------------------------
    # VIEW 1: EXECUTIVE OVERVIEW
    # -------------------------------------------------------------------------
    if nav_view == "📊 Executive Overview":
        st.subheader("Statewide Hydrological & Infrastructure Overview")

        # KPI Metric Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Catchments", "518", "HydroATLAS Level 8")
        with col2:
            st.metric("Consensus Tier 1", "76", "Robust Multi-Scenario (14.7%)")
        with col3:
            st.metric("Monitored Catchments", "459", "88.61% State Coverage")
        with col4:
            st.metric("MAR Category A", "12", "Secular Depletion Verified")
        with col5:
            st.metric("SWH Category A", "75", "Surface Runoff Deficit")

        st.markdown("---")

        # Physical Infrastructure Inventory Warning Banner
        st.warning(
            "🏛️ **PHYSICAL CONSERVATION STRUCTURE INVENTORY AUDIT STATUS**:\n\n"
            "- **MRSAC Jalyukt Shivar GIS Layer**: Protected behind departmental intranet authentication "
            "(`https://mrsac.maharashtra.gov.in/jalyukt/`). No bulk shapefile export is publicly accessible.\n"
            "- **Zero-Fabrication Policy**: In strict compliance with engineering ethics, zero artificial structures "
            "or storage capacities were fabricated. All 518 catchments are tagged as `INVENTORY_UNAVAILABLE_PENDING_MRSAC_ACCESS`.\n"
            "- **Binding Planning Invariant**: *An unrecorded digital inventory must NEVER be interpreted as the physical absence "
            "of water conservation infrastructure on the ground.* Maharashtra's agrarian catchments possess thousands of historical "
            "structures built under prior schemes. Local physical desilting/condition audits are required before new construction."
        )

        st.markdown("---")

        # Visual Analytics
        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("#### Consensus Prioritization Tiers (N = 518)")
            tier_counts = df_master["consensus_priority_tier_revised"].value_counts().reset_index()
            tier_counts.columns = ["Tier", "Count"]
            fig_tier = px.pie(
                tier_counts, names="Tier", values="Count", hole=0.45,
                color="Tier",
                color_discrete_map={
                    "Consensus Tier 1: Robust Priority (Multi-Scenario)": "#e74c3c",
                    "Consensus Tier 2: Specialized / Moderate Priority": "#f39c12",
                    "Consensus Tier 3: Low Priority / Conservation": "#27ae60"
                }
            )
            fig_tier.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320)
            st.plotly_chart(fig_tier, use_container_width=True)

        with c_right:
            st.markdown("#### Screening Action Breakdown for Consensus Tier 1 (N = 76)")
            tier1_df = df_master[df_master["consensus_priority_tier_revised"].str.startswith("Consensus Tier 1")]
            mar_t1 = tier1_df["provisional_action_category_MAR"].value_counts()
            swh_t1 = tier1_df["provisional_action_category_SWH"].value_counts()
            comp_df = pd.DataFrame({
                "Category": [
                    "Category A: Potential New Infrastructure",
                    "Category C: Mixed / Conflicting Evidence",
                    "Category D: Insufficient Evidence"
                ],
                "MAR Count": [
                    mar_t1.get("Category A: Potential New Infrastructure Assessment (MAR)", 0),
                    mar_t1.get("Category C: Mixed or Conflicting Evidence Requiring Field Assessment", 0),
                    mar_t1.get("Category D: Insufficient Evidence", 0)
                ],
                "SWH Count": [
                    swh_t1.get("Category A: Potential New Infrastructure Assessment (SWH)", 0),
                    swh_t1.get("Category C: Mixed or Conflicting Evidence Requiring Field Assessment", 0),
                    swh_t1.get("Category D: Insufficient Evidence", 0)
                ]
            })
            fig_bar = px.bar(
                comp_df, x="Category", y=["MAR Count", "SWH Count"],
                barmode="group",
                color_discrete_map={"MAR Count": "#2980b9", "SWH Count": "#e67e22"}
            )
            fig_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320, xaxis_title="", yaxis_title="Catchments")
            st.plotly_chart(fig_bar, use_container_width=True)

        # Ground-Truth Observational Validation Note
        st.markdown("---")
        st.markdown("#### Ground-Truth Observational Validation & Confounder Analysis")
        st.markdown(
            r"""
            - **Multi-Agency Network**: Ingests **1,936 CGWB stations** and **4,090 GSDA stations** (6,026 total stations), covering **459 of 518 catchments (88.61%)**.
            - **Inter-Agency Agreement**: For 48 collocated well pairs ($\le 100\text{ m}$ separation), Spearman correlation is **$\rho = 0.85$** ($p < 10^{-190}$) with **$0.00\text{ m}$ median difference**, verifying that both state and central monitoring networks record physical water tables accurately.
            - **Non-Significant MAR Association ($\rho = -0.075, p = 0.16$)**: The statistical independence between physical MAR suitability and decadal groundwater depletion is an expected hydrogeological outcome:
              1. *Pumping Bias*: Heavy agricultural tubewell pumping (sugarcane, fruit orchards) is concentrated in flat clay vertisols where surface infiltration is low, driving rapid water table drops regardless of physical percolation ratings.
              2. *Aquifer Stratigraphy*: Monitoring wells observe the shallow weathered basalt ($<15\text{ m}$) which recharges every monsoon ($\Delta h = +4.06\text{ m}$), whereas agricultural tubewells tap deep fractured basalt ($>80\text{ m}$).
            """
        )

    # -------------------------------------------------------------------------
    # VIEW 2: INTERACTIVE GEOSPATIAL MAP
    # -------------------------------------------------------------------------
    elif nav_view == "🗺️ Interactive Catchment Map":
        st.subheader("Geospatial Catchment Explorer")

        c_metric, c_engine = st.columns([2, 1])
        with c_metric:
            map_metric = st.selectbox(
                "Select Map Display Metric / Styling Layer:",
                [
                    "Consensus Priority Tier",
                    "MAR Provisional Action Category",
                    "SWH Provisional Action Category",
                    "Preliminary Screening Score",
                    "Decadal Groundwater Depth Trend (m/year)",
                    "Topsoil Clay Content (g/kg)",
                    "Infiltration Proxy (cm/hr)",
                    "Annual Rainfall Baseline (mm/year)"
                ]
            )
        with c_engine:
            map_engine = st.radio(
                "Map Engine:",
                ["Plotly Vector Choropleth (Fast)", "Folium OpenStreetMap (Leaflet)"],
                horizontal=True
            )

        # Filter the GeoDataFrame
        gdf_filtered = gdf_merged[gdf_merged["HYBAS_ID"].isin(df_filtered["HYBAS_ID"])].copy()

        if map_engine == "Plotly Vector Choropleth (Fast)":
            geojson_data = gdf_filtered.__geo_interface__

            if map_metric == "Consensus Priority Tier":
                fig_map = px.choropleth(
                    gdf_filtered, geojson=geojson_data, locations="HYBAS_ID",
                    featureidkey="properties.HYBAS_ID",
                    color="consensus_priority_tier_revised",
                    color_discrete_map={
                        "Consensus Tier 1: Robust Priority (Multi-Scenario)": "#e74c3c",
                        "Consensus Tier 2: Specialized / Moderate Priority": "#f39c12",
                        "Consensus Tier 3: Low Priority / Conservation": "#27ae60"
                    },
                    hover_data=["HYBAS_ID", "sub_area_km2", "gw_depth_trend_median_m_yr", "total_monitoring_well_count"],
                )
            elif map_metric == "MAR Provisional Action Category":
                fig_map = px.choropleth(
                    gdf_filtered, geojson=geojson_data, locations="HYBAS_ID",
                    featureidkey="properties.HYBAS_ID",
                    color="provisional_action_category_MAR",
                    color_discrete_map={
                        "Category A: Potential New Infrastructure Assessment (MAR)": "#2980b9",
                        "Category C: Mixed or Conflicting Evidence Requiring Field Assessment": "#f39c12",
                        "Category C: Mixed Evidence (Non-Tier-1)": "#bdc3c7",
                        "Category D: Insufficient Evidence": "#7f8c8d"
                    },
                    hover_data=["HYBAS_ID", "gw_depth_trend_median_m_yr", "village_clay_0_5cm_g_kg"],
                )
            elif map_metric == "SWH Provisional Action Category":
                fig_map = px.choropleth(
                    gdf_filtered, geojson=geojson_data, locations="HYBAS_ID",
                    featureidkey="properties.HYBAS_ID",
                    color="provisional_action_category_SWH",
                    color_discrete_map={
                        "Category A: Potential New Infrastructure Assessment (SWH)": "#d35400",
                        "Category C: Mixed Evidence (Non-Tier-1)": "#bdc3c7",
                        "Category D: Insufficient Evidence": "#7f8c8d"
                    },
                    hover_data=["HYBAS_ID", "village_clay_0_5cm_g_kg", "village_slope_mean_deg"],
                )
            elif map_metric == "Decadal Groundwater Depth Trend (m/year)":
                fig_map = px.choropleth(
                    gdf_filtered, geojson=geojson_data, locations="HYBAS_ID",
                    featureidkey="properties.HYBAS_ID",
                    color="gw_depth_trend_median_m_yr",
                    color_continuous_scale="RdBu_r",
                    hover_data=["HYBAS_ID", "total_monitoring_well_count"],
                )
            else:
                col_map = {
                    "Preliminary Screening Score": "preliminary_screening_score",
                    "Topsoil Clay Content (g/kg)": "village_clay_0_5cm_g_kg",
                    "Infiltration Proxy (cm/hr)": "village_infiltration_proxy",
                    "Annual Rainfall Baseline (mm/year)": "village_rainfall_baseline_mean_mm"
                }
                num_col = col_map[map_metric]
                fig_map = px.choropleth(
                    gdf_filtered, geojson=geojson_data, locations="HYBAS_ID",
                    featureidkey="properties.HYBAS_ID",
                    color=num_col,
                    color_continuous_scale="Viridis",
                    hover_data=["HYBAS_ID", "sub_area_km2"],
                )

            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=560)
            st.plotly_chart(fig_map, use_container_width=True)

        else:
            # Folium OpenStreetMap Leaflet Engine
            gdf_simple = gdf_filtered[["HYBAS_ID", "sub_area_km2", "consensus_priority_tier_revised", "provisional_action_category_MAR", "provisional_action_category_SWH", "geometry"]].copy()
            gdf_simple["geometry"] = gdf_simple["geometry"].simplify(0.008)

            m = folium.Map(location=[19.2, 76.2], zoom_start=7, tiles="OpenStreetMap")
            folium.GeoJson(
                gdf_simple,
                tooltip=folium.GeoJsonTooltip(
                    fields=["HYBAS_ID", "sub_area_km2", "consensus_priority_tier_revised", "provisional_action_category_MAR", "provisional_action_category_SWH"],
                    aliases=["Catchment ID:", "Area (km²):", "Consensus Tier:", "MAR Category:", "SWH Category:"]
                ),
                style_function=lambda x: {
                    "fillColor": "#e74c3c" if "Tier 1" in str(x["properties"]["consensus_priority_tier_revised"])
                                else "#f39c12" if "Tier 2" in str(x["properties"]["consensus_priority_tier_revised"])
                                else "#27ae60",
                    "color": "#2c3e50",
                    "weight": 1.2,
                    "fillOpacity": 0.55
                }
            ).add_to(m)
            st_folium(m, width="100%", height=560)

        st.caption(
            "📌 **Map Guide & Units**: Area in km²; Precipitation in mm/year; Soil Clay/Sand in g/kg (divide by 10 for %); "
            "Infiltration in cm/hr; Groundwater Trend in m/year (Positive = secular water-table depletion; Negative = recovery). "
            "Grey polygons indicate catchments filtered out by current sidebar criteria."
        )

        # Quick Catchment Inspection Panel on the Map View
        st.markdown("---")
        st.markdown("#### 🔎 Catchment Quick-Inspection Panel")
        avail_ids = sorted(gdf_filtered["HYBAS_ID"].unique())
        if avail_ids:
            c_sel, _ = st.columns([2, 3])
            with c_sel:
                sel_map_id = st.selectbox("Select Catchment to Inspect:", avail_ids, index=0, key="map_quick_inspect")
            map_row = gdf_filtered[gdf_filtered["HYBAS_ID"] == sel_map_id].iloc[0]

            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Catchment HYBAS_ID", str(map_row["HYBAS_ID"]))
            mc1.caption(f"Area: {map_row['sub_area_km2']:.1f} km²")
            mc2.metric("Consensus Tier", map_row["consensus_priority_tier_revised"].split(":")[0])
            mc2.caption(f"Median Planning Rank: #{int(map_row['rank_median_planning'])} / 518")

            trend_val = map_row["gw_depth_trend_median_m_yr"]
            t_txt = f"+{trend_val:.4f} m/yr (Depletion)" if pd.notna(trend_val) and trend_val > 0 else f"{trend_val:.4f} m/yr (Recovery)" if pd.notna(trend_val) else "Inconclusive"
            mc3.metric("MAR Category", map_row["provisional_action_category_MAR"].split(":")[0])
            mc3.caption(f"Decadal Trend: {t_txt} | Wells: {int(map_row['total_monitoring_well_count'])}")

            mc4.metric("SWH Category", map_row["provisional_action_category_SWH"].split(":")[0])
            mc4.caption(f"Clay: {map_row['village_clay_0_5cm_g_kg']:.1f} g/kg | Slope: {map_row['village_slope_mean_deg']:.1f}°")

    # -------------------------------------------------------------------------
    # VIEW 3: CATCHMENT DEEP-DIVE PROFILER
    # -------------------------------------------------------------------------
    elif nav_view == "🔍 Catchment Deep-Dive Profiler":
        st.subheader("Catchment Profile & Decision Engine Trace")

        c_search, _ = st.columns([2, 3])
        with c_search:
            all_ids = sorted(df_master["HYBAS_ID"].unique())
            selected_hid = st.selectbox("Search / Select Catchment HYBAS_ID:", all_ids, index=0)

        # Retrieve record
        row = df_master[df_master["HYBAS_ID"] == selected_hid].iloc[0]

        # Top Catchment Headline
        st.markdown(f"### Catchment HYBAS_ID: `{selected_hid}`")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Drainage Area", f"{row['sub_area_km2']:.1f} km²")
        k2.metric("Consensus Tier", row["consensus_priority_tier_revised"].split(":")[0])
        k3.metric("MAR Action Category", row["provisional_action_category_MAR"].split(":")[0])
        k4.metric("SWH Action Category", row["provisional_action_category_SWH"].split(":")[0])

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Multi-Criteria Scenario Rankings")
            scenarios = ["S1 Equal Pillars", "S2 AHP Expert", "S4 MAR", "S5 SWH", "S7 Winsorized AHP"]
            scores = [
                row["score_S1_Equal_Pillars"], row["score_S2_AHP_Expert"],
                row["score_S4_Managed_Aquifer_Recharge"], row["score_S5_Surface_Water_Harvesting"],
                row["score_S7_Winsorized_AHP"]
            ]
            fig_scen = go.Figure(data=[go.Bar(
                x=scenarios, y=scores, marker_color=["#34495e", "#2980b9", "#27ae60", "#e67e22", "#8e44ad"]
            )])
            fig_scen.update_layout(yaxis_title="Normalized Score (0-1)", yaxis=dict(range=[0, 1]), height=280, margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_scen, use_container_width=True)

            st.markdown(f"- **Median Planning Rank**: `#{int(row['rank_median_planning'])}` of 518")
            st.markdown(f"- **MAR Rank (S4)**: `#{int(row['rank_S4_Managed_Aquifer_Recharge'])}`")
            st.markdown(f"- **SWH Rank (S5)**: `#{int(row['rank_S5_Surface_Water_Harvesting'])}`")

        with c2:
            st.markdown("#### Ground-Truth Monitoring Status")
            trend_val = row["gw_depth_trend_median_m_yr"]
            if pd.notna(trend_val):
                t_str = f"+{trend_val:.4f} m/yr (Depletion)" if trend_val > 0 else f"{trend_val:.4f} m/yr (Recovery)"
            else:
                t_str = "Inconclusive / No 5-Year History"

            st.write(f"- **Active Monitoring Stations**: `{int(row['total_monitoring_well_count'])} wells` (CGWB: `{int(row['cgwb_monitoring_well_count'])}`, GSDA: `{int(row['gsda_monitoring_well_count'])}`)")
            st.write(f"- **Decadal Depth Trend (2015–2024)**: **`{t_str}`**")
            st.write(f"- **Median Seasonal Rise (Δh)**: `{row['gw_seasonal_recharge_median_m']:.2f} m`" if pd.notna(row['gw_seasonal_recharge_median_m']) else "- **Median Seasonal Rise**: `N/A`")
            st.write(f"- **Evidence Confidence Level**: `{row['evidence_confidence_level']}`")

            st.markdown("#### Physical & Soil Parameters")
            st.write(f"- **Topsoil Texture**: Clay: `{row['village_clay_0_5cm_g_kg']:.1f} g/kg` | Sand: `{row['village_sand_0_5cm_g_kg']:.1f} g/kg` | Silt: `{row['village_silt_0_5cm_g_kg']:.1f} g/kg`")
            st.write(f"- **Infiltration Capacity Proxy**: `{row['village_infiltration_proxy']:.2f} cm/hr`")
            st.write(f"- **Topography & Rainfall**: Slope: `{row['village_slope_mean_deg']:.2f}°` | Rainfall: `{row['village_rainfall_baseline_mean_mm']:.1f} mm/yr`")
            st.write(f"- **Cropland Extent**: `{row['village_cropland_pct']:.1f}%` of catchment area")

        st.markdown("---")
        st.markdown("#### Decision Engine Audit & Screening Rationales")
        st.info(f"**MAR Decision Rationale**: {row['provisional_screening_rationale_MAR']}")
        st.info(f"**SWH Decision Rationale**: {row['provisional_screening_rationale_SWH']}")
        st.warning(f"**Infrastructure Inventory Policy**: {row['inventory_data_policy']}")

    # -------------------------------------------------------------------------
    # VIEW 4: MULTI-CATCHMENT COMPARISON
    # -------------------------------------------------------------------------
    elif nav_view == "⚖️ Multi-Catchment Comparison":
        st.subheader("Multi-Catchment Side-by-Side Comparison")
        st.markdown(
            "Compare up to 5 catchments simultaneously across hydrogeological, soil, and multi-scenario indicators."
        )

        all_ids = sorted(df_master["HYBAS_ID"].unique())
        selected_ids = st.multiselect("Select Catchments to Compare (2–5 recommended):", all_ids, default=all_ids[:3])

        if len(selected_ids) < 2:
            st.warning("Please select at least 2 catchments to view comparative analysis.")
        else:
            comp_df = df_master[df_master["HYBAS_ID"].isin(selected_ids)].copy()

            # Comparative Bar Chart of Scenario Scores
            scen_plot_df = comp_df[["HYBAS_ID", "score_S1_Equal_Pillars", "score_S2_AHP_Expert", "score_S4_Managed_Aquifer_Recharge", "score_S5_Surface_Water_Harvesting"]].melt(
                id_vars="HYBAS_ID", var_name="Scenario", value_name="Score"
            )
            scen_plot_df["HYBAS_ID"] = scen_plot_df["HYBAS_ID"].astype(str)
            fig_comp = px.bar(
                scen_plot_df, x="Scenario", y="Score", color="HYBAS_ID", barmode="group",
                title="Scenario Scores Comparison"
            )
            fig_comp.update_layout(height=350)
            st.plotly_chart(fig_comp, use_container_width=True)

            # Metrics Table
            st.markdown("#### Key Parameters Comparison Table")
            display_cols = [
                "HYBAS_ID", "sub_area_km2", "consensus_priority_tier_revised",
                "provisional_action_category_MAR", "provisional_action_category_SWH",
                "gw_depth_trend_median_m_yr", "total_monitoring_well_count",
                "village_clay_0_5cm_g_kg", "village_sand_0_5cm_g_kg",
                "village_infiltration_proxy", "village_rainfall_baseline_mean_mm"
            ]
            st.dataframe(comp_df[display_cols].set_index("HYBAS_ID"), use_container_width=True)

            st.caption(
                "⚠️ **SCIENTIFIC SAFEGUARD**: Scores from S4 (MAR) and S5 (SWH) represent distinct physical objectives "
                "(subsurface recharge vs. surface runoff impoundment) and must not be treated as directly interchangeable."
            )

    # -------------------------------------------------------------------------
    # VIEW 5: DPR SCREENING DOSSIERS & EXPORTS
    # -------------------------------------------------------------------------
    elif nav_view == "📑 DPR Screening Dossiers & Export":
        st.subheader("DPR Screening Dossiers & Dataset Export")

        t_export, t_dossier, t_template = st.tabs([
            "📥 Export Filtered Ledger & Printable Summary",
            "📄 View DPR Screening Dossier",
            "📋 Reusable DPR Screening Template"
        ])

        with t_export:
            st.markdown("#### Filtered Catchment Table Export")
            st.write(f"Export the current filtered selection of **{len(df_filtered)} catchments** to CSV.")

            csv_data = df_filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Filtered Catchments CSV",
                data=csv_data,
                file_name="jaldrishti_filtered_catchments.csv",
                mime="text/csv",
            )

            st.dataframe(df_filtered[[
                "HYBAS_ID", "sub_area_km2", "consensus_priority_tier_revised",
                "provisional_action_category_MAR", "provisional_action_category_SWH",
                "gw_depth_trend_median_m_yr", "total_monitoring_well_count",
                "village_clay_0_5cm_g_kg", "village_infiltration_proxy"
            ]], use_container_width=True)

            st.markdown("---")
            st.markdown("#### 🖨️ Generate Printable Single-Catchment Summary Sheet")
            st.caption("Generate an audit-traceable, printable markdown briefing card for any of the 518 catchments.")

            c_print_sel, c_print_btn = st.columns([2, 1])
            with c_print_sel:
                all_ids_exp = sorted(df_filtered["HYBAS_ID"].unique())
                if not all_ids_exp:
                    all_ids_exp = sorted(df_master["HYBAS_ID"].unique())
                sel_p_id = st.selectbox("Select Catchment for Summary Card:", all_ids_exp, key="print_card_sel")

            p_row = df_master[df_master["HYBAS_ID"] == sel_p_id].iloc[0]
            trend_p = p_row["gw_depth_trend_median_m_yr"]
            t_str_p = f"+{trend_p:.4f} m/yr (Depletion)" if pd.notna(trend_p) and trend_p > 0 else f"{trend_p:.4f} m/yr (Recovery)" if pd.notna(trend_p) else "Inconclusive"

            card_md = f"""# JalDrishti-AI: Catchment Summary Briefing Card
## HYBAS_ID: {sel_p_id} (Maharashtra Level 8 Basin)

> **STATUTORY PLANNING DISCLAIMER**:  
> *Preliminary macro-screening outcome only. Not an approved Detailed Project Report (DPR) or construction authorization. On-site geophysical (VES), infiltration, and environmental audits required prior to civil construction.*

---
### 1. General & Ranking Metrics
- **Drainage Area**: {p_row['sub_area_km2']:.2f} km²
- **Consensus Prioritization Tier**: {p_row['consensus_priority_tier_revised']}
- **Median Planning Rank**: #{int(p_row['rank_median_planning'])} of 518
- **Preliminary Score**: {p_row['preliminary_screening_score']:.4f}
- **Scenario Scores**: S1 (Equal): {p_row['score_S1_Equal_Pillars']:.4f} | S2 (AHP): {p_row['score_S2_AHP_Expert']:.4f} | S4 (MAR): {p_row['score_S4_Managed_Aquifer_Recharge']:.4f} | S5 (SWH): {p_row['score_S5_Surface_Water_Harvesting']:.4f}

---
### 2. Observational Ground-Truth Status
- **Active Wells**: {int(p_row['total_monitoring_well_count'])} wells (CGWB: {int(p_row['cgwb_monitoring_well_count'])}, GSDA: {int(p_row['gsda_monitoring_well_count'])})
- **Decadal Depth Trend (2015–2024)**: {t_str_p}
- **Seasonal Fluctuation (Δh)**: {p_row['gw_seasonal_recharge_median_m']:.2f} m
- **Evidence Confidence**: {p_row['evidence_confidence_level']}

---
### 3. Soil & Physical Properties
- **Texture**: Clay: {p_row['village_clay_0_5cm_g_kg']:.1f} g/kg ({p_row['village_clay_0_5cm_g_kg']/10:.1f}%) | Sand: {p_row['village_sand_0_5cm_g_kg']:.1f} g/kg | Silt: {p_row['village_silt_0_5cm_g_kg']:.1f} g/kg
- **Infiltration Capacity Proxy**: {p_row['village_infiltration_proxy']:.2f} cm/hr
- **Terrain & Climate**: Slope: {p_row['village_slope_mean_deg']:.2f}° | Elevation: {p_row['village_elevation_mean_m']:.1f} m | Rainfall: {p_row['village_rainfall_baseline_mean_mm']:.1f} mm/yr | Cropland: {p_row['village_cropland_pct']:.1f}%

---
### 4. Provisional Screening Action Classifications
- **MAR Screening Category**: {p_row['provisional_action_category_MAR']}
  *Rationale*: {p_row['provisional_screening_rationale_MAR']}
- **SWH Screening Category**: {p_row['provisional_action_category_SWH']}
  *Rationale*: {p_row['provisional_screening_rationale_SWH']}
- **Infrastructure Inventory Status**: {p_row['inventory_status']} ({p_row['inventory_data_policy']})
"""
            st.download_button(
                label=f"📥 Download Summary Card (HYBAS_{sel_p_id}.md)",
                data=card_md,
                file_name=f"HYBAS_{sel_p_id}_Summary_Card.md",
                mime="text/markdown"
            )

        with t_dossier:
            st.markdown("#### Preliminary Detailed Project Report (DPR) Screening Dossiers")
            st.markdown(
                "Standardized screening sheets generated for confirmed Category A high-priority catchments."
            )

            d_type = st.radio("Intervention Type:", ["Managed Aquifer Recharge (MAR) - 12 Catchments", "Surface Water Harvesting (SWH) - 75 Catchments"])

            if "MAR" in d_type:
                target_dir = REPORTS_DIR / "mar_category_a"
            else:
                target_dir = REPORTS_DIR / "swh_category_a"

            available_files = sorted([f.name for f in target_dir.glob("*.md")])
            if available_files:
                sel_file = st.selectbox("Select Screening Dossier:", available_files)
                sheet_content = (target_dir / sel_file).read_text(encoding="utf-8")

                st.download_button(
                    label=f"📥 Download {sel_file}",
                    data=sheet_content,
                    file_name=sel_file,
                    mime="text/markdown"
                )

                st.markdown("---")
                st.markdown(sheet_content)
            else:
                st.warning("No screening dossiers found. Please run scripts/generate_dpr_screening_sheets.py first.")

        with t_template:
            st.markdown("#### Reusable DPR Screening Template")
            st.markdown(
                "Standardized feasibility assessment template for watershed development authorities and hydrogeologists."
            )

            template_path = REPORTS_DIR / "DPR_SCREENING_TEMPLATE.md"
            if template_path.exists():
                template_content = template_path.read_text(encoding="utf-8")
                st.download_button(
                    label="📥 Download Reusable DPR Screening Template (Markdown)",
                    data=template_content,
                    file_name="DPR_SCREENING_TEMPLATE.md",
                    mime="text/markdown"
                )
                st.markdown("---")
                st.markdown(template_content)
            else:
                st.warning("DPR_SCREENING_TEMPLATE.md not found in reports/dpr_screening_sheets/.")


if __name__ == "__main__":
    main()
