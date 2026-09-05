import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import data
import gis_engine

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION & THEME
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="TerraSense GIS Operations Hub",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

data.init_db()

# Custom CSS for high-contrast disaster operations styling
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 10px 14px;
        border-left: 4px solid #1976d2;
    }
    .status-chip {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 13px;
        margin-right: 8px;
    }
    .status-chip-critical { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
    .status-chip-warning { background: #fff3e0; color: #e65100; border: 1px solid #ffcc80; }
    .status-chip-stable { background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SIDEBAR CONTROLS & SCENARIO INJECTOR
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("⛰️ TerraSense Hub")
    st.caption("AI-Powered Geospatial Flash Flood & Landslide Warning System")
    
    st.divider()
    st.subheader("📍 Ward Monitoring Selector")
    ward_options = gis_engine.get_all_ward_options()
    selected_ward = st.selectbox(
        "Active Operational Sector",
        options=list(ward_options.keys()),
        format_func=lambda w: ward_options[w],
        index=list(ward_options.keys()).index(4) if 4 in ward_options else 0,
        help="Switch monitored ward to inspect local topography, safe shelters, and secondary hazard zones."
    )
    
    gis_data = gis_engine.get_ward_gis(selected_ward)
    st.caption(f"**Sector:** {gis_data['valley_sector']} | **Slope Angle:** {gis_data['slope_angle_deg']}°")
    
    st.divider()
    st.subheader("🗺️ GIS Layer Visibility")
    show_epicenter = st.checkbox("🔴 Primary Hazard Epicenter", value=True)
    show_nearby_alert = st.checkbox("🟠 High Alert Nearby Buffer (1.2km)", value=True)
    show_safe_zones = st.checkbox("🛡️ Certified Safe Evacuation Shelters", value=True)
    show_routes = st.checkbox("🚶 Designated Safe Evacuation Corridors", value=True)
    show_infrastructure = st.checkbox("🏗️ Critical Infrastructure at Risk", value=True)

    layer_config = {
        "show_epicenter": show_epicenter,
        "show_nearby_alert": show_nearby_alert,
        "show_safe_zones": show_safe_zones,
        "show_routes": show_routes,
        "show_infrastructure": show_infrastructure
    }

    st.divider()
    st.subheader("🎛️ Demo Hardware & Scenario Injector")
    st.caption("Direct telemetry injection into hardware database:")
    
    # Preset Quick Injection Scenarios
    preset_choice = st.selectbox(
        "⚡ Load Hazard Preset Scenario",
        [
            "-- Select Scenario Preset --",
            "☀️ Dry Baseline (Nominal Safety)",
            "🌦️ Monsoon Saturation (Elevated)",
            "🌊 Cloudburst Surge (Flash Flood)",
            "⛰️ Slope Saturation (Landslide Imminent)",
            "🚨 Catastrophic Compound Event (Cloudburst + Slide)"
        ]
    )

    preset_values = {
        "☀️ Dry Baseline (Nominal Safety)": (0.0, 15.0),
        "🌦️ Monsoon Saturation (Elevated)": (28.0, 58.0),
        "🌊 Cloudburst Surge (Flash Flood)": (95.0, 68.0),
        "⛰️ Slope Saturation (Landslide Imminent)": (18.0, 96.0),
        "🚨 Catastrophic Compound Event (Cloudburst + Slide)": (125.0, 98.0)
    }

    default_rain = 0.0
    default_moist = 20.0
    if preset_choice in preset_values:
        default_rain, default_moist = preset_values[preset_choice]

    demo_rain = st.slider("Simulate Rainfall (mm/h)", 0.0, 150.0, float(default_rain))
    demo_moisture = st.slider("Simulate Moisture (%)", 0.0, 100.0, float(default_moist))

    if st.button("🚨 Inject Test Packet", type="primary", use_container_width=True):
        data.insert_telemetry(
            demo_rain,
            demo_moisture,
            ward_id=selected_ward,
            force_override=True,
            slope_angle_deg=gis_data["slope_angle_deg"]
        )
        st.success(f"Packet Injected for {ward_options[selected_ward]}!")
        st.rerun()

# ------------------------------------------------------------------------------
# INITIAL DATA FETCH & HAZARD STATE ASSESSMENT
# ------------------------------------------------------------------------------
initial_df = data.fetch_telemetry_history(25, ward_id=selected_ward)
if initial_df.empty:
    data.insert_telemetry(
        0.0, 20.0,
        ward_id=selected_ward,
        force_override=True,
        slope_angle_deg=gis_data["slope_angle_deg"]
    )
    initial_df = data.fetch_telemetry_history(25, ward_id=selected_ward)

latest_rec = initial_df.iloc[0]
init_risk = int(latest_rec['risk_score'])
init_moist = float(latest_rec['filtered_moisture'])
init_rain = float(latest_rec['raw_rainfall'])
init_fs = float(latest_rec.get('fs_value', 1.5))

# Determine initial alert tier: 'CRITICAL', 'WARNING', or 'STABLE'
if init_risk >= 75 or init_fs <= 1.0:
    current_tier = "CRITICAL"
elif init_risk >= 50 or init_fs <= 1.2:
    current_tier = "WARNING"
else:
    current_tier = "STABLE"

if "active_alert_tier" not in st.session_state:
    st.session_state["active_alert_tier"] = current_tier

# Classify hazard type
haz_code, haz_label, haz_color = data.classify_hazard(init_moist, init_rain, init_fs, init_risk)

# ------------------------------------------------------------------------------
# TOP HEADER & ALERT BANNERS
# ------------------------------------------------------------------------------
st.title("⛰️ TerraSense: Flash Flood & Landslide Operations Hub")

c_hdr1, c_hdr2 = st.columns([0.7, 0.3])
with c_hdr1:
    st.markdown(
        f"**Monitored Ward:** `{gis_data['name']}` | **Sensor Node:** `{gis_data['node_id']}` | **Base Elevation:** `{gis_data['elevation_base_m']}m`"
    )
with c_hdr2:
    if current_tier == "CRITICAL":
        st.error(f"🚨 ALERT TIER: CRITICAL RED\n{haz_label}")
    elif current_tier == "WARNING":
        st.warning(f"⚠️ ALERT TIER: WARNING ORANGE\n{haz_label}")
    else:
        st.success(f"✅ ALERT TIER: STABLE GREEN\n{haz_label}")

# Real-time message banner slot
banner_slot = st.empty()

# 6 Key Performance Metric Containers
kpi_slot = st.empty()

st.divider()

# ------------------------------------------------------------------------------
# MAIN CONTENT LAYOUT
# ------------------------------------------------------------------------------
left_col, right_col = st.columns([1.35, 0.85])

with left_col:
    map_hdr_col1, map_hdr_col2 = st.columns([0.75, 0.25])
    with map_hdr_col1:
        st.subheader("🗺️ Geospatial Disaster Operations Map")
    with map_hdr_col2:
        if st.button("🔄 Sync Map", use_container_width=True, help="Force re-sync of GIS Map elements"):
            st.rerun()

    # Dynamic status strip above map: Live sensor telemetry that updates continuously
    map_status_slot = st.empty()

    # --------------------------------------------------------------------------
    # STABILIZED MAP RENDERING (ZERO FLICKER ON TELEMETRY PACKETS)
    # The map is rendered using Folium and st_folium with state-gated persistence.
    # It only rebuilds when the alert tier, active ward, or layer visibility changes.
    # --------------------------------------------------------------------------
    disaster_map = gis_engine.create_stabilized_disaster_map(
        ward_id=selected_ward,
        risk_score=init_risk,
        moisture_pct=init_moist,
        fs_val=init_fs,
        rain_rate=init_rain,
        layer_config=layer_config
    )

    st_folium(
        disaster_map,
        width="100%",
        height=470,
        key=f"terrasense_map_w{selected_ward}_{st.session_state['active_alert_tier']}_{show_nearby_alert}_{show_safe_zones}_{show_routes}",
        returned_objects=[]
    )

    # --------------------------------------------------------------------------
    # SPATIAL INTELLIGENCE PANELS (Safe Shelters & Nearby High Alert Buffer)
    # --------------------------------------------------------------------------
    tab_shelters, tab_nearby = st.tabs([
        "🛡️ Safe Evacuation Zones & Routes",
        "⚠️ High Alert Nearby Regions & Corridors"
    ])

    with tab_shelters:
        st.markdown(f"#### Verified High-Elevation Refuge Sites for {gis_data['name']}")
        shelter_cols = st.columns(len(gis_data["safe_evacuation_zones"]))
        for idx, shelter in enumerate(gis_data["safe_evacuation_zones"]):
            with shelter_cols[idx]:
                badge = "🌟 PRIMARY SHELTER" if shelter.get("is_primary") else "REFUGE CAMP"
                st.markdown(f"""
                <div style='background:#f1f8e9; border:1px solid #c8e6c9; border-radius:6px; padding:10px; margin-bottom:10px;'>
                    <span style='background:#2e7d32; color:white; padding:2px 6px; border-radius:3px; font-size:10px; font-weight:bold;'>{badge}</span>
                    <h5 style='margin:6px 0 2px 0; color:#1b5e20;'>{shelter['name']}</h5>
                    <p style='font-size:12px; margin:2px 0;'><b>Elevation:</b> {shelter['elevation_m']}m AMSL (<b>+{shelter['elevation_above_hazard_m']}m</b> High Ground)</p>
                    <p style='font-size:12px; margin:2px 0;'><b>Capacity:</b> {shelter['capacity_persons']} Evacuees</p>
                    <p style='font-size:11px; color:#555; margin-top:4px;'><b>Provisions:</b> {", ".join(shelter['facilities'][:2])}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("##### 🚶 Active Evacuation Corridors")
        for corridor in gis_data["evacuation_corridors"]:
            st.info(
                f"**{corridor['name']}**: Length `{corridor['distance_km']} km` | "
                f"Est. Walk Time: `{corridor['est_walk_min']} mins` | Terrain: `{corridor['terrain_type']}`"
            )

    with tab_nearby:
        st.markdown(f"#### Secondary Hazard Buffers & At-Risk Infrastructure")
        st.warning(
            f"**Secondary Alert Buffer ({gis_data['nearby_high_alert']['buffer_radius_m']}m):** "
            f"{gis_data['nearby_high_alert']['description']}"
        )
        
        st.markdown("##### 🏗️ Critical Infrastructure in Alert Perimeter")
        infra_items = gis_data['nearby_high_alert'].get('critical_infrastructure', [])
        for item in infra_items:
            st.markdown(
                f"- **{item['name']}** ({item['type']}): `{item['status']}` — *{item['risk_warning']}*"
            )

        st.markdown("##### 📡 Cascading Multi-Ward Early Warning")
        for cw in gis_data['nearby_high_alert'].get('cascading_wards', []):
            st.write(
                f"• **{cw['name']}** ({cw['relation']}, {cw['distance_km']}km): "
                f"Estimated debris surge arrival in **{cw['surge_arrival_min']} minutes**."
            )

with right_col:
    st.subheader("📈 Real-Time Telemetry Stream")
    chart_slot = st.empty()
    
    st.divider()
    st.subheader("🔬 Geotechnical Stability Analysis")
    geo_slot = st.empty()

# ------------------------------------------------------------------------------
# FAST TELEMETRY REFRESH FRAGMENT (RUNS EVERY 3 SECONDS)
# NOTE: The map is intentionally NOT re-instantiated here.
# Telemetry metrics and charts update live every 3s without causing map flicker.
# If an alert threshold is crossed, it cleanly transitions the application.
# ------------------------------------------------------------------------------
@st.fragment(run_every="3s")
def update_telemetry_feed():
    df = data.fetch_telemetry_history(25, ward_id=selected_ward)
    if df.empty:
        return

    latest = df.iloc[0]
    avg_risk = int(latest['risk_score'])
    filtered_moist = float(latest['filtered_moisture'])
    raw_moist = float(latest['raw_moisture'])
    ari_val = float(latest['ari_score'])
    rain_rate = float(latest['raw_rainfall'])
    fs_val = float(latest.get('fs_value', 1.5))
    timestamp = latest['timestamp']

    # Moisture saturation rate (dTheta / dt)
    velocity = 0.0
    if len(df) > 1:
        df_sorted = df.sort_values(by='timestamp')
        velocity = df_sorted['filtered_moisture'].diff().mean()
        if pd.isna(velocity):
            velocity = 0.0

    # Classify hazard mode
    haz_code, haz_desc, haz_color = data.classify_hazard(filtered_moist, rain_rate, fs_val, avg_risk)

    # Check for Alert Tier State Transition
    if avg_risk >= 75 or fs_val <= 1.0:
        new_tier = "CRITICAL"
        status_msg = f"🚨 CRITICAL RED: Active Slope Shear Failure & Surge Inundation! Factor of Safety ({fs_val}) <= 1.0. Immediate evacuation to high-elevation shelters mandatory!"
        banner_type = "error"
    elif avg_risk >= 50 or fs_val <= 1.2:
        new_tier = "WARNING"
        status_msg = f"⚠️ WARNING ORANGE: Elevated Debris Runoff & Hydrostatic Pore Surcharge. Factor of Safety ({fs_val}) declining. High-alert nearby zones activated."
        banner_type = "warning"
    else:
        new_tier = "STABLE"
        status_msg = f"✅ STABLE GREEN: Operating within nominal geotechnical thresholds (Factor of Safety {fs_val} > 1.2)."
        banner_type = "success"

    # If alert tier changed, trigger single clean app rerun to adapt map perimeters
    if new_tier != st.session_state.get("active_alert_tier"):
        st.session_state["active_alert_tier"] = new_tier
        st.rerun(scope="app")

    # 1. Update Real-Time Status Banners
    with banner_slot.container():
        if banner_type == "error":
            st.error(status_msg)
        elif banner_type == "warning":
            st.warning(status_msg)
        else:
            st.success(status_msg)

    # 2. Update KPI Metrics Tiles
    with kpi_slot.container():
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Monitored Sector", latest['ward_name'].split(' - ')[0])
        c2.metric("Rainfall Rate", f"{rain_rate} mm/h")
        c3.metric("Filtered Saturation", f"{filtered_moist}%", delta=f"{round(velocity, 2)}%/pkt")
        c4.metric("Antecedent Rain (ARI)", f"{round(ari_val, 1)}")
        c5.metric("Factor of Safety (FS)", f"{fs_val}", delta="UNSTABLE" if fs_val <= 1.0 else "MARGINAL" if fs_val <= 1.2 else "STABLE")
        c6.metric("Hazard Risk Score", f"{avg_risk} / 100")

    # 3. Update Live Map Telemetry Chip (Above map, without rebuilding map DOM)
    with map_status_slot.container():
        tier_class = "status-chip-critical" if new_tier == "CRITICAL" else "status-chip-warning" if new_tier == "WARNING" else "status-chip-stable"
        st.markdown(f"""
        <div style='background:#f8f9fa; border:1px solid #e0e0e0; border-radius:6px; padding:6px 12px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <span class='status-chip {tier_class}'>{new_tier} ALERT</span>
                <span style='font-weight:600; font-size:13px;'>{haz_desc}</span>
            </div>
            <div style='font-size:12px; color:#666;'>
                🛰️ <b>Node:</b> {gis_data['node_id']} | 💧 <b>Moisture:</b> {filtered_moist}% | ⚖️ <b>FS:</b> {fs_val} | ⏱️ <b>Packet:</b> {str(timestamp).split()[-1]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Update Time-Series Telemetry Chart
    with chart_slot.container():
        chart_df = df.sort_values(by='timestamp')[['timestamp', 'raw_moisture', 'filtered_moisture', 'ari_score', 'fs_value']]
        chart_df = chart_df.set_index('timestamp')
        st.line_chart(chart_df, height=330)

    # 5. Update Geotechnical Stability Panel
    with geo_slot.container():
        fs_percentage = min(100, int((fs_val / 1.5) * 100))
        st.progress(fs_percentage / 100.0, text=f"Slope Equilibrium Ratio: {fs_val} FS (Baseline: 1.50)")
        
        g1, g2 = st.columns(2)
        with g1:
            st.caption(f"**Critical Slip Depth:** 2.0 m")
            st.caption(f"**Cohesion (c'):** 12.0 kPa")
        with g2:
            st.caption(f"**Slope Beta (β):** {gis_data['slope_angle_deg']}°")
            st.caption(f"**Friction Angle (φ):** 28.0°")

# Invoke the fast telemetry loop
update_telemetry_feed()