import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import data

st.set_page_config(page_title="TerraSense GIS Operations Hub", layout="wide")

st.title("⛰️ TerraSense: Flash Flood & Landslide Early Warning System")
st.markdown("**Node ID:** TS-NODE-04 | **Location:** Ward 4 - Kullu Valley (Pandoh Bypass)")

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.header("🎛️ Demo Hardware Controls")
    st.caption("Inject scenarios directly into telemetry database:")
    
    demo_rain = st.slider("Simulate Rainfall (mm/h)", 0.0, 150.0, 0.0)
    demo_moisture = st.slider("Simulate Moisture (%)", 0.0, 100.0, 10.0)
    
    if st.button("🚨 Inject Test Packet", type="primary"):
        data.insert_telemetry(demo_rain, demo_moisture, ward_id=4, force_override=True)
        st.success("Test Packet Injected!")

# ---------------------------------------------------------
# PAGE CONTAINERS
# ---------------------------------------------------------
kpi_slot = st.empty()
banner_slot = st.empty()

st.divider()

left_col, right_col = st.columns([1.2, 0.8])

with left_col:
    st.subheader("MAP VIEW")
    map_slot = st.empty()

with right_col:
    st.subheader("📈 Filtered Telemetry Stream")
    chart_slot = st.empty()

# ---------------------------------------------------------
# REAL-TIME FRAGMENT LOOP
# ---------------------------------------------------------
@st.fragment(run_every="3s")
def update_telemetry_feed():
    df = data.fetch_telemetry_history(20)

    if df.empty:
        with kpi_slot.container():
            st.info("⚡ Waiting for telemetry stream... Use sidebar injector or `sim.py`.")
        return

    latest = df.iloc[0]

    # Calculate Saturation Velocity (dTheta / dt)
    velocity = 0.0
    if len(df) > 1:
        df_sorted = df.sort_values(by='timestamp')
        velocity = df_sorted['filtered_moisture'].diff().mean()
        if pd.isna(velocity):
            velocity = 0.0

    avg_risk = int(latest['risk_score'])
    filtered_moisture = latest['filtered_moisture']
    ari_val = latest['ari_score']
    rain_rate = latest['raw_rainfall']
    fs_val = latest.get('fs_value', 1.5)

    # Dynamic Map Render based on Hazard Risk Level
    hazard_center = [31.7580, 77.0620]
    safe_assembly_pt = [31.7650, 77.0700]

    m = folium.Map(location=[31.7610, 77.0660], zoom_start=14, tiles="OpenStreetMap")

    folium.Marker(
        location=hazard_center,
        popup=f"<b>Ward 4 Node</b><br>Moisture: {filtered_moisture}%<br>FS: {fs_val}",
        icon=folium.Icon(color="red" if avg_risk >= 75 else "orange" if avg_risk >= 50 else "blue", icon="exclamation-triangle", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=safe_assembly_pt,
        popup="<b>SAFE ZONE:</b> Kullu Secondary School",
        icon=folium.Icon(color="green", icon="shield", prefix="fa")
    ).add_to(m)

    # Dynamic Hazard Buffer Circle on Critical Alert
    if avg_risk >= 75:
        folium.Circle(
            location=hazard_center,
            radius=500,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.35,
            popup="⚠️ ACTIVE LANDSLIDE HAZARD ZONE (500m Buffer)"
        ).add_to(m)
        route_color = "#FF0000"
    else:
        route_color = "#00FF00"

    evacuation_route = [hazard_center, [31.7600, 77.0640], [31.7630, 77.0670], safe_assembly_pt]
    folium.PolyLine(
        locations=evacuation_route,
        color=route_color,
        weight=5,
        opacity=0.85,
        tooltip="Active Safe Evacuation Corridor"
    ).add_to(m)

    with map_slot.container():
        st_folium(
            m,
            width="100%",
            height=430,
            key="terrasense_dynamic_gis_map",
            returned_objects=[]
        )

    # Status Alert Banners
    if avg_risk >= 75:
        status_msg = f"🚨 CRITICAL RED: Active Slope Failure Hazard! Factor of Safety ({fs_val}) <= 1.0 (Failure Imminent)."
        banner_type = "error"
    elif avg_risk >= 50:
        status_msg = f"⚠️ WARNING ORANGE: Elevated Debris Runoff. Factor of Safety ({fs_val}) Declining."
        banner_type = "warning"
    else:
        status_msg = f"✅ STABLE GREEN: Safe Operating Parameters (Factor of Safety {fs_val} > 1.2)."
        banner_type = "success"

    # KPI Metrics Banner
    with kpi_slot.container():
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Monitoring Ward", latest['ward_name'])
        c2.metric("Rainfall Rate", f"{rain_rate} mm/h")
        c3.metric("Filtered Saturation", f"{filtered_moisture}%", delta=f"{round(velocity, 2)}%/pkt")
        c4.metric("Antecedent Rain (ARI)", f"{ari_val}")
        c5.metric("Factor of Safety (FS)", f"{fs_val}")
        c6.metric("Risk Score", f"{avg_risk} / 100")

    with banner_slot.container():
        if banner_type == "error":
            st.error(status_msg)
        elif banner_type == "warning":
            st.warning(status_msg)
        else:
            st.success(status_msg)

    # Historical Telemetry Graph
    with chart_slot.container():
        chart_df = df.sort_values(by='timestamp')[['timestamp', 'raw_moisture', 'filtered_moisture', 'ari_score', 'fs_value']]
        chart_df = chart_df.set_index('timestamp')
        st.line_chart(chart_df, height=360)

update_telemetry_feed()