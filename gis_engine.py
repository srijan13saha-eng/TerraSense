import folium
from folium import plugins

# ==============================================================================
# TERRASENSE GEOSPATIAL DATABASE: WARDS, HAZARDS, SHELTERS & HIGH-ALERT ZONES
# ==============================================================================

WARDS_GIS = {
    4: {
        "ward_id": 4,
        "name": "Ward 4 - Kullu Valley (Pandoh Bypass)",
        "valley_sector": "Pandoh Bypass / Beas Lower Gorge",
        "center": [31.7610, 77.0660],
        "zoom": 14,
        "node_id": "TS-NODE-04",
        "elevation_base_m": 1210,
        "slope_angle_deg": 38.0,
        "soil_type": "Weathered Phyllite & Saturated Sandy Silt",
        "primary_threats": ["Active Dip-Slope Landslide", "Beas Nullah Flash Inundation"],
        
        # Primary Hazard Epicenter
        "hazard_epicenter": {
            "coords": [31.7580, 77.0620],
            "label": "TS-NODE-04: KM 118 Cut-Slope Section",
            "type": "Landslide & Flash Surge Epicenter",
            "critical_radius_m": 480,
            "description": "High shear strain slope with high landslide and debris flow propensity."
        },
        
        # High Alert Nearby Regions (Secondary Threat Perimeters)
        "nearby_high_alert": {
            "buffer_radius_m": 1200,
            "name": "Ward 4 Secondary Hazard Buffer & Surge Basin",
            "description": "Adjoining cut-slopes, downstream surge corridor, and road infrastructure subject to secondary collapse.",
            # Downstream Flash Flood Surge Corridor (Polygon along riverbed)
            "surge_corridor": [
                [31.7585, 77.0615],
                [31.7560, 77.0600],
                [31.7530, 77.0580],
                [31.7500, 77.0560],
                [31.7485, 77.0575],
                [31.7515, 77.0605],
                [31.7550, 77.0625],
                [31.7580, 77.0635]
            ],
            # Critical Infrastructure in danger within nearby zone
            "critical_infrastructure": [
                {
                    "name": "Pandoh Bypass Bridge (KM 119)",
                    "coords": [31.7545, 77.0595],
                    "type": "Bridge / Transit Choke Point",
                    "risk_warning": "HIGH: Pier scour & debris jamming hazard",
                    "status": "RESTRICTED ACCESS"
                },
                {
                    "name": "Valley Electric Substation 33kV",
                    "coords": [31.7535, 77.0640],
                    "type": "Power Infrastructure",
                    "risk_warning": "CRITICAL: Flood water ingress & slope toe undercut",
                    "status": "EMERGENCY SHUTOFF READY"
                },
                {
                    "name": "NH-21 Highway Nullah Culvert",
                    "coords": [31.7615, 77.0585],
                    "type": "Drainage Culvert",
                    "risk_warning": "MODERATE: Mudflow & boulder accumulation",
                    "status": "MONITORED"
                }
            ],
            # Cascading Alert to Neighboring Wards
            "cascading_wards": [
                {"ward_id": 5, "name": "Ward 5 (Bhuntar Confluence)", "distance_km": 14.2, "relation": "Downstream Catchment", "surge_arrival_min": 25},
                {"ward_id": 3, "name": "Ward 3 (Aut / Larji)", "distance_km": 8.5, "relation": "Upstream Reservoir Sector", "surge_arrival_min": 15}
            ]
        },
        
        # Certified Safe Evacuation Zones (High Elevation / Geotechnically Stable)
        "safe_evacuation_zones": [
            {
                "id": "SAFE-01",
                "name": "Kullu Senior Secondary School & Indoor Sports Hall",
                "coords": [31.7665, 77.0720],
                "elevation_m": 1285,
                "elevation_above_hazard_m": 75,
                "capacity_persons": 550,
                "facilities": ["Emergency Medical Post", "Independent Solar Genset", "Satellite Comms", "Potable Water Reservoir"],
                "status": "PRIMARY ACTIVE SHELTER",
                "is_primary": True
            },
            {
                "id": "SAFE-02",
                "name": "Sultanpur High Ground Community Center & Helipad",
                "coords": [31.7710, 77.0650],
                "elevation_m": 1315,
                "elevation_above_hazard_m": 105,
                "capacity_persons": 400,
                "facilities": ["Elevated Helipad", "Air Evacuation Staging", "SDRF Stockpile", "Dry Rations (7 Days)"],
                "status": "HIGH-ALTITUDE REFUGE",
                "is_primary": False
            },
            {
                "id": "SAFE-03",
                "name": "District Disaster Relief Staging Base (Ridge Top)",
                "coords": [31.7630, 77.0780],
                "elevation_m": 1298,
                "elevation_above_hazard_m": 88,
                "capacity_persons": 700,
                "facilities": ["Mass Triage Tent", "NDRF Forward Headquarters", "Heavy Ambulance Access"],
                "status": "SECONDARY MASS CAMP",
                "is_primary": False
            }
        ],
        
        # Designated Safe Evacuation Corridors (Routed away from flood channels & slope toes)
        "evacuation_corridors": [
            {
                "name": "Corridor Alpha: Primary Ridge Route to Senior Secondary School",
                "destination": "SAFE-01",
                "path": [
                    [31.7580, 77.0620],  # Hazard Node
                    [31.7605, 77.0645],  # Diverge uphill via bypass link
                    [31.7630, 77.0675],  # High ridge road (above flood level)
                    [31.7650, 77.0700],  # School approach avenue
                    [31.7665, 77.0720]   # Safe Zone 1 Entrance
                ],
                "distance_km": 1.4,
                "est_walk_min": 18,
                "terrain_type": "Paved Ridge Link (No Slope Toe Exposure)"
            },
            {
                "name": "Corridor Bravo: High Terrace Route to Sultanpur Helipad",
                "destination": "SAFE-02",
                "path": [
                    [31.7580, 77.0620],  # Hazard Node
                    [31.7620, 77.0630],  # North slope diversion track
                    [31.7660, 77.0638],  # Upper terrace contour path
                    [31.7710, 77.0650]   # Sultanpur Helipad
                ],
                "distance_km": 1.7,
                "est_walk_min": 24,
                "terrain_type": "Terraced Jeep Track (Elevated Stable Bedrock)"
            }
        ]
    },

    1: {
        "ward_id": 1,
        "name": "Ward 1 - Old Manali (Beas Upper Reach)",
        "valley_sector": "Upper Beas Basin / Manalsu Stream Confluence",
        "center": [32.2530, 77.1850],
        "zoom": 14,
        "node_id": "TS-NODE-01",
        "elevation_base_m": 2050,
        "slope_angle_deg": 41.0,
        "soil_type": "Granitic Moraine & Glacial Debris",
        "primary_threats": ["Glacial Cloudburst Inundation", "Steep Scree Slope Failure"],
        "hazard_epicenter": {
            "coords": [32.2510, 77.1810],
            "label": "TS-NODE-01: Manalsu Nullah Gorge",
            "type": "Flash Torrent & Boulder Roll Zone",
            "critical_radius_m": 420,
            "description": "Narrow gorge prone to sudden torrent surges and stream bank erosion."
        },
        "nearby_high_alert": {
            "buffer_radius_m": 1100,
            "name": "Upper Beas Runout Buffer",
            "description": "Low-lying riverside pathways, commercial shops along the stream bank.",
            "surge_corridor": [
                [32.2520, 77.1810],
                [32.2500, 77.1830],
                [32.2470, 77.1860],
                [32.2450, 77.1890],
                [32.2435, 77.1880],
                [32.2460, 77.1840],
                [32.2490, 77.1810]
            ],
            "critical_infrastructure": [
                {
                    "name": "Club House Footbridge",
                    "coords": [32.2490, 77.1845],
                    "type": "Pedestrian Suspension Bridge",
                    "risk_warning": "HIGH: Flash torrent clearance < 0.8m",
                    "status": "CLOSURE ENFORCED"
                }
            ],
            "cascading_wards": [
                {"ward_id": 2, "name": "Ward 2 (Naggar / Left Bank)", "distance_km": 19.5, "relation": "Downstream River Reach", "surge_arrival_min": 35}
            ]
        },
        "safe_evacuation_zones": [
            {
                "id": "SAFE-101",
                "name": "Old Manali High Ridge Temple Ground (Manu Temple Plateau)",
                "coords": [32.2580, 77.1815],
                "elevation_m": 2180,
                "elevation_above_hazard_m": 130,
                "capacity_persons": 450,
                "facilities": ["Community Dining Hall", "First Aid Center", "High Ground Shelter"],
                "status": "ACTIVE SAFE HAVEN",
                "is_primary": True
            }
        ],
        "evacuation_corridors": [
            {
                "name": "Manu Temple Uphill Evacuation Path",
                "destination": "SAFE-101",
                "path": [
                    [32.2510, 77.1810],
                    [32.2540, 77.1812],
                    [32.2580, 77.1815]
                ],
                "distance_km": 0.9,
                "est_walk_min": 15,
                "terrain_type": "Cobblestone Village Climb"
            }
        ]
    },

    2: {
        "ward_id": 2,
        "name": "Ward 2 - Naggar / Left Bank (Slope Cut Corridor)",
        "valley_sector": "Naggar Heritage Ridge / Left Bank Highway",
        "center": [32.1420, 77.1700],
        "zoom": 14,
        "node_id": "TS-NODE-02",
        "elevation_base_m": 1760,
        "slope_angle_deg": 36.0,
        "soil_type": "Colluvial Silt & Fractured Quartzite",
        "primary_threats": ["Road Widening Cut-Slope Landslide", "Debris Torrents"],
        "hazard_epicenter": {
            "coords": [32.1400, 77.1680],
            "label": "TS-NODE-02: Naggar-Manali Road Cut KM 14",
            "type": "Rotational Slope Slump",
            "critical_radius_m": 450,
            "description": "Progressive slope movement over roadway toe excavation."
        },
        "nearby_high_alert": {
            "buffer_radius_m": 1150,
            "name": "Naggar Highway High-Alert Buffer",
            "description": "Adjacent apple orchards on unstable terraces and highway links.",
            "surge_corridor": [
                [32.1410, 77.1670],
                [32.1380, 77.1650],
                [32.1350, 77.1630],
                [32.1340, 77.1650],
                [32.1370, 77.1680]
            ],
            "critical_infrastructure": [
                {
                    "name": "Naggar Castle Access Hairpin",
                    "coords": [32.1435, 77.1710],
                    "type": "Mountain Road Switchback",
                    "risk_warning": "MODERATE: Retaining wall settlement",
                    "status": "ONE-WAY TRAFFIC"
                }
            ],
            "cascading_wards": [
                {"ward_id": 4, "name": "Ward 4 (Kullu / Pandoh)", "distance_km": 28.0, "relation": "Downstream Valley Hub", "surge_arrival_min": 60}
            ]
        },
        "safe_evacuation_zones": [
            {
                "id": "SAFE-201",
                "name": "Naggar Heritage High Plateau (Govt College Ground)",
                "coords": [32.1460, 77.1740],
                "elevation_m": 1840,
                "elevation_above_hazard_m": 80,
                "capacity_persons": 500,
                "facilities": ["Reinforced Concrete Hall", "Ambulance Station", "Clean Water Storage"],
                "status": "SAFE HIGH GROUND",
                "is_primary": True
            }
        ],
        "evacuation_corridors": [
            {
                "name": "Naggar Upper Plateau Safe Link",
                "destination": "SAFE-201",
                "path": [
                    [32.1400, 77.1680],
                    [32.1425, 77.1710],
                    [32.1460, 77.1740]
                ],
                "distance_km": 1.1,
                "est_walk_min": 16,
                "terrain_type": "Paved Ascending Link Road"
            }
        ]
    },

    3: {
        "ward_id": 3,
        "name": "Ward 3 - Aut & Larji Catchment (Hydro Surge Sector)",
        "valley_sector": "Aut Tunnel Bypass / Larji Reservoir",
        "center": [31.7240, 77.2100],
        "zoom": 14,
        "node_id": "TS-NODE-03",
        "elevation_base_m": 960,
        "slope_angle_deg": 44.0,
        "soil_type": "Dolomitic Limestone & Jointed Gneiss",
        "primary_threats": ["Reservoir Backwater Surge", "Tunnel Portal Rockfall"],
        "hazard_epicenter": {
            "coords": [31.7220, 77.2080],
            "label": "TS-NODE-03: Larji Dam Backwater Gate",
            "type": "Hydraulic Surge & Slope Surcharge",
            "critical_radius_m": 500,
            "description": "Severe backwater elevation causing toe liquefaction."
        },
        "nearby_high_alert": {
            "buffer_radius_m": 1300,
            "name": "Aut Gorge Inundation Buffer",
            "description": "Tunnel portal approaches and downstream river plain.",
            "surge_corridor": [
                [31.7230, 77.2070],
                [31.7200, 77.2050],
                [31.7160, 77.2020],
                [31.7150, 77.2040],
                [31.7180, 77.2080]
            ],
            "critical_infrastructure": [
                {
                    "name": "Aut Tunnel North Portal",
                    "coords": [31.7250, 77.2095],
                    "type": "Highway Tunnel Portal",
                    "risk_warning": "HIGH: Flash debris inundation at portal entry",
                    "status": "EVACUATION ESCORT ONLY"
                }
            ],
            "cascading_wards": [
                {"ward_id": 4, "name": "Ward 4 (Pandoh Bypass)", "distance_km": 8.5, "relation": "Downstream Reservoir Tail", "surge_arrival_min": 15}
            ]
        },
        "safe_evacuation_zones": [
            {
                "id": "SAFE-301",
                "name": "Aut High School Emergency Shelter",
                "coords": [31.7290, 77.2150],
                "elevation_m": 1080,
                "elevation_above_hazard_m": 120,
                "capacity_persons": 600,
                "facilities": ["Elevated Sports Ground", "Emergency Telephony", "Field Hospital"],
                "status": "PRIMARY DISASTER SHELTER",
                "is_primary": True
            }
        ],
        "evacuation_corridors": [
            {
                "name": "Aut Hill Ascent Corridor",
                "destination": "SAFE-301",
                "path": [
                    [31.7220, 77.2080],
                    [31.7255, 77.2115],
                    [31.7290, 77.2150]
                ],
                "distance_km": 1.3,
                "est_walk_min": 20,
                "terrain_type": "Zig-zag Uphill Asphalt Road"
            }
        ]
    },

    5: {
        "ward_id": 5,
        "name": "Ward 5 - Bhuntar Confluence (Riverine Floodplain)",
        "valley_sector": "Beas & Parvati River Confluence / Airport Plain",
        "center": [31.8790, 77.1540],
        "zoom": 14,
        "node_id": "TS-NODE-05",
        "elevation_base_m": 1090,
        "slope_angle_deg": 18.0,
        "soil_type": "Alluvial Silt & River Cobbles",
        "primary_threats": ["Dual-River Flash Flood Inundation", "Embankment Overtopping"],
        "hazard_epicenter": {
            "coords": [31.8770, 77.1510],
            "label": "TS-NODE-05: Beas-Parvati River Junction",
            "type": "River Confluence Flash Flood Core",
            "critical_radius_m": 550,
            "description": "Rapid hydraulic head rise from combined mountain river torrents."
        },
        "nearby_high_alert": {
            "buffer_radius_m": 1400,
            "name": "Bhuntar Floodplain High Alert Perimeter",
            "description": "Low-lying residential sectors, market street, and airport boundary.",
            "surge_corridor": [
                [31.8780, 77.1500],
                [31.8740, 77.1470],
                [31.8700, 77.1440],
                [31.8680, 77.1460],
                [31.8720, 77.1520]
            ],
            "critical_infrastructure": [
                {
                    "name": "Kullu-Manali Airport (Bhuntar Runway 34)",
                    "coords": [31.8760, 77.1550],
                    "type": "Aviation Transport Hub",
                    "risk_warning": "CRITICAL: Embankment breach would submerge runway",
                    "status": "FLIGHT OPERATIONS SUSPENDED"
                },
                {
                    "name": "Hathithan Double-Span Bridge",
                    "coords": [31.8810, 77.1520],
                    "type": "River Bridge",
                    "risk_warning": "HIGH: Hydrodynamic tree-trunk battering",
                    "status": "RESTRICTED TO HEAVY RESCUE"
                }
            ],
            "cascading_wards": [
                {"ward_id": 4, "name": "Ward 4 (Pandoh Bypass)", "distance_km": 14.2, "relation": "Downstream Gorge Feed", "surge_arrival_min": 25}
            ]
        },
        "safe_evacuation_zones": [
            {
                "id": "SAFE-501",
                "name": "Bhuntar Upper Ridge Sports Complex & Camp",
                "coords": [31.8860, 77.1620],
                "elevation_m": 1180,
                "elevation_above_hazard_m": 90,
                "capacity_persons": 850,
                "facilities": ["Helicopter Landing Pad", "NDRF Base", "Water Purification Units"],
                "status": "PRIMARY EVACUATION COMPLEX",
                "is_primary": True
            }
        ],
        "evacuation_corridors": [
            {
                "name": "Bhuntar Upper Ridge High Escape Path",
                "destination": "SAFE-501",
                "path": [
                    [31.8770, 77.1510],
                    [31.8810, 77.1560],
                    [31.8860, 77.1620]
                ],
                "distance_km": 1.6,
                "est_walk_min": 22,
                "terrain_type": "Elevated Bypass Highway to Ridge"
            }
        ]
    }
}

def get_ward_gis(ward_id: int):
    """Retrieve full GIS spatial dictionary for a given ward (fallback to Ward 4)."""
    return WARDS_GIS.get(ward_id, WARDS_GIS[4])

def get_all_ward_options():
    """Returns mapping of {ward_id: display_name} for Streamlit selectbox."""
    return {w_id: data["name"] for w_id, data in WARDS_GIS.items()}

# ==============================================================================
# FOLIUM MAP BUILDER WITH HIGH-ALERT BUFFERS & SAFE EVACUATION ZONES
# ==============================================================================

def create_stabilized_disaster_map(
    ward_id: int,
    risk_score: int,
    moisture_pct: float,
    fs_val: float,
    rain_rate: float,
    layer_config: dict = None
) -> folium.Map:
    """
    Constructs an interactive GIS map featuring:
    1. Primary Hazard Epicenter (Active Slope / Flood Inundation)
    2. High-Alert Nearby Regions (Buffer circle, downstream surge corridor, critical infrastructure)
    3. Safe Evacuation Zones (High-elevation shelters with capacities and readiness)
    4. Safe Evacuation Corridors (Protected paths routed away from hazard zones)
    5. Cascading neighboring ward hazard alerts
    """
    if layer_config is None:
        layer_config = {
            "show_epicenter": True,
            "show_nearby_alert": True,
            "show_safe_zones": True,
            "show_routes": True,
            "show_infrastructure": True
        }

    gis = get_ward_gis(ward_id)
    center = gis["center"]
    epicenter = gis["hazard_epicenter"]
    nearby = gis["nearby_high_alert"]
    shelters = gis["safe_evacuation_zones"]
    corridors = gis["evacuation_corridors"]

    # Determine Alert Level Tier
    is_critical = risk_score >= 75 or fs_val <= 1.0
    is_warning = (risk_score >= 50 and not is_critical) or (fs_val <= 1.2 and not is_critical)

    # Base Folium Map centered on the active ward
    m = folium.Map(
        location=center,
        zoom_start=gis["zoom"],
        tiles="OpenStreetMap",
        control_scale=True,
        prefer_canvas=True
    )

    # --------------------------------------------------------------------------
    # 1. HIGH ALERT NEARBY REGIONS (Secondary Hazard Perimeter & Surge Corridor)
    # --------------------------------------------------------------------------
    if layer_config.get("show_nearby_alert", True):
        # Amber / Orange Buffer Circle covering secondary slope collapses & runouts
        if is_critical or is_warning:
            buffer_color = "#FF4500" if is_critical else "#FFA500"
            buffer_opacity = 0.18 if is_critical else 0.12
            border_weight = 3 if is_critical else 2

            folium.Circle(
                location=epicenter["coords"],
                radius=nearby["buffer_radius_m"],
                color=buffer_color,
                weight=border_weight,
                dash_array="6, 6",
                fill=True,
                fill_color=buffer_color,
                fill_opacity=buffer_opacity,
                tooltip=f"<b>HIGH ALERT NEARBY ZONE ({nearby['buffer_radius_m']}m Buffer)</b><br>Secondary Slope Instability & Runout Risk",
                popup=folium.Popup(f"""
                    <div style='width:240px; font-family:sans-serif;'>
                        <h4 style='color:#E65100; margin-bottom:4px;'>⚠️ HIGH ALERT NEARBY ZONE</h4>
                        <p style='font-size:12px; margin:2px 0;'><b>Perimeter:</b> {nearby['buffer_radius_m']}m Secondary Warning Buffer</p>
                        <p style='font-size:11px; color:#555;'>{nearby['description']}</p>
                        <div style='background:#FFF3E0; border-left:3px solid #FF9800; padding:4px 8px; margin-top:6px; font-size:11px;'>
                            <b>Instruction:</b> Secondary zone on high alert. Avoid riverbank corridors and cut-slopes.
                        </div>
                    </div>
                """, max_width=280)
            ).add_to(m)

            # Downstream Flash Flood Surge Corridor (Polygon along watercourse)
            if "surge_corridor" in nearby and nearby["surge_corridor"]:
                folium.Polygon(
                    locations=nearby["surge_corridor"],
                    color="#D84315" if is_critical else "#FB8C00",
                    weight=2,
                    dash_array="4, 4",
                    fill=True,
                    fill_color="#FF5722",
                    fill_opacity=0.28 if is_critical else 0.15,
                    tooltip="<b>DOWNSTREAM SURGE CORRIDOR</b> (Flash Flood Inundation Path)",
                    popup=folium.Popup("""
                        <div style='width:220px; font-family:sans-serif;'>
                            <h4 style='color:#BF360C; margin-bottom:4px;'>🌊 FLASH FLOOD SURGE CORRIDOR</h4>
                            <p style='font-size:11px;'>Active hydraulic flow path. Rapid inundation risk within 15-30 mins of cloudburst event.</p>
                        </div>
                    """, max_width=250)
                ).add_to(m)

    # --------------------------------------------------------------------------
    # 2. CRITICAL INFRASTRUCTURE AT RISK (Within Nearby High-Alert Zone)
    # --------------------------------------------------------------------------
    if layer_config.get("show_infrastructure", True) and "critical_infrastructure" in nearby:
        for infra in nearby["critical_infrastructure"]:
            infra_icon_color = "red" if is_critical else "orange" if is_warning else "gray"
            folium.Marker(
                location=infra["coords"],
                tooltip=f"<b>INFRASTRUCTURE:</b> {infra['name']}",
                popup=folium.Popup(f"""
                    <div style='width:230px; font-family:sans-serif;'>
                        <h4 style='margin-bottom:4px;'>🏗️ {infra['name']}</h4>
                        <p style='font-size:12px; margin:2px 0;'><b>Category:</b> {infra['type']}</p>
                        <p style='font-size:11px; color:#C62828;'><b>Alert:</b> {infra['risk_warning']}</p>
                        <p style='font-size:11px;'><b>Status:</b> <code>{infra['status']}</code></p>
                    </div>
                """, max_width=260),
                icon=folium.Icon(color=infra_icon_color, icon="industry", prefix="fa")
            ).add_to(m)

    # --------------------------------------------------------------------------
    # 3. PRIMARY HAZARD EPICENTER (Red Alert Core Zone)
    # --------------------------------------------------------------------------
    if layer_config.get("show_epicenter", True):
        # Hazard Center Marker
        node_color = "red" if is_critical else "orange" if is_warning else "blue"
        folium.Marker(
            location=epicenter["coords"],
            tooltip=f"<b>{gis['node_id']} Hazard Epicenter</b> (Risk: {risk_score}/100)",
            popup=folium.Popup(f"""
                <div style='width:240px; font-family:sans-serif;'>
                    <h3 style='color:{'#D32F2F' if is_critical else '#F57C00' if is_warning else '#1976D2'}; margin:0 0 6px 0;'>
                        {'🚨 DISASTER EPICENTER' if is_critical else '⚠️ WARNING SECTOR' if is_warning else 'ℹ️ MONITORING STATION'}
                    </h3>
                    <p style='font-size:12px; margin:3px 0;'><b>Station ID:</b> {gis['node_id']}</p>
                    <p style='font-size:12px; margin:3px 0;'><b>Hazard Class:</b> {epicenter['type']}</p>
                    <p style='font-size:12px; margin:3px 0;'><b>Filtered Moisture:</b> {moisture_pct}%</p>
                    <p style='font-size:12px; margin:3px 0;'><b>Factor of Safety (FS):</b> {fs_val}</p>
                    <p style='font-size:12px; margin:3px 0;'><b>Rainfall Rate:</b> {rain_rate} mm/h</p>
                    <p style='font-size:12px; margin:3px 0;'><b>Slope Angle:</b> {gis['slope_angle_deg']}°</p>
                    <div style='background:#FFEBEE; color:#C62828; padding:5px 8px; border-radius:4px; margin-top:6px; font-size:11px; font-weight:bold;'>
                        {'CRITICAL: Immediate evacuation required!' if is_critical else 'WARNING: Slope surcharge observed.' if is_warning else 'NORMAL: Slope parameters stable.'}
                    </div>
                </div>
            """, max_width=270),
            icon=folium.Icon(color=node_color, icon="exclamation-triangle", prefix="fa")
        ).add_to(m)

        # Primary Hazard Perimeter (Red Circle on Warning/Critical)
        if is_critical or is_warning:
            folium.Circle(
                location=epicenter["coords"],
                radius=epicenter["critical_radius_m"],
                color="#D32F2F" if is_critical else "#F57C00",
                weight=3,
                fill=True,
                fill_color="#D32F2F" if is_critical else "#F57C00",
                fill_opacity=0.38 if is_critical else 0.22,
                tooltip=f"<b>ACTIVE HAZARD FOOTPRINT ({epicenter['critical_radius_m']}m)</b>",
                popup="<b>ACTIVE DISASTER IMPACT ZONE:</b> Immediate structural exclusion area."
            ).add_to(m)

    # --------------------------------------------------------------------------
    # 4. CERTIFIED SAFE EVACUATION ZONES (High Elevation Shelters)
    # --------------------------------------------------------------------------
    if layer_config.get("show_safe_zones", True):
        for shelter in shelters:
            is_prim = shelter.get("is_primary", False)
            facilities_list = "".join([f"<li>{fac}</li>" for fac in shelter["facilities"]])
            
            folium.Marker(
                location=shelter["coords"],
                tooltip=f"<b>SAFE REFUGE:</b> {shelter['name']} (+{shelter['elevation_above_hazard_m']}m High Ground)",
                popup=folium.Popup(f"""
                    <div style='width:260px; font-family:sans-serif;'>
                        <div style='background:#E8F5E9; border-left:4px solid #2E7D32; padding:6px 10px; margin-bottom:8px;'>
                            <h4 style='color:#1B5E20; margin:0 0 4px 0;'>🛡️ SAFE EVACUATION ZONE</h4>
                            <span style='font-size:11px; color:#2E7D32; font-weight:bold;'>{shelter['status']}</span>
                        </div>
                        <h4 style='margin:4px 0 6px 0; color:#1b2838;'>{shelter['name']}</h4>
                        <p style='font-size:12px; margin:2px 0;'><b>Elevation:</b> {shelter['elevation_m']}m AMSL (<b>+{shelter['elevation_above_hazard_m']}m</b> above hazard)</p>
                        <p style='font-size:12px; margin:2px 0;'><b>Shelter Capacity:</b> <span style='color:#2E7D32; font-weight:bold;'>{shelter['capacity_persons']} Persons</span></p>
                        <p style='font-size:12px; margin:4px 0 2px 0;'><b>Emergency Provisions:</b></p>
                        <ul style='font-size:11px; color:#333; margin:2px 0 6px 16px; padding:0;'>
                            {facilities_list}
                        </ul>
                        <div style='background:#2E7D32; color:white; text-align:center; padding:5px 8px; border-radius:4px; font-size:11px; font-weight:bold;'>
                            VERIFIED GEOTECHNICALLY STABLE HIGH GROUND
                        </div>
                    </div>
                """, max_width=290),
                icon=folium.Icon(color="green", icon="shield" if is_prim else "home", prefix="fa")
            ).add_to(m)

    # --------------------------------------------------------------------------
    # 5. DESIGNATED SAFE EVACUATION CORRIDORS (Escape Routes)
    # --------------------------------------------------------------------------
    if layer_config.get("show_routes", True):
        for idx, corridor in enumerate(corridors):
            # Dynamic Route Color: Brilliant Emerald Green for safe egress corridor
            route_color = "#00C853" if is_critical else "#2E7D32" if is_warning else "#4CAF50"
            route_weight = 6 if is_critical else 4
            route_opacity = 0.95 if is_critical else 0.80

            folium.PolyLine(
                locations=corridor["path"],
                color=route_color,
                weight=route_weight,
                opacity=route_opacity,
                dash_array="8, 6" if not is_critical else None,
                tooltip=f"<b>SAFE EVACUATION CORRIDOR</b>: {corridor['name']} ({corridor['distance_km']} km, ~{corridor['est_walk_min']} min)",
                popup=folium.Popup(f"""
                    <div style='width:230px; font-family:sans-serif;'>
                        <h4 style='color:#2E7D32; margin-bottom:4px;'>🚶 ACTIVE EVACUATION CORRIDOR</h4>
                        <p style='font-size:12px; margin:2px 0;'><b>Path:</b> {corridor['name']}</p>
                        <p style='font-size:12px; margin:2px 0;'><b>Length:</b> {corridor['distance_km']} km</p>
                        <p style='font-size:12px; margin:2px 0;'><b>Est. Walk Time:</b> {corridor['est_walk_min']} minutes</p>
                        <p style='font-size:11px; color:#555;'><b>Terrain:</b> {corridor['terrain_type']}</p>
                        <div style='background:#E8F5E9; color:#1B5E20; padding:4px 6px; border-radius:4px; font-size:11px; margin-top:4px;'>
                            ✓ Bypasses River Surge & Debris Runout
                        </div>
                    </div>
                """, max_width=260)
            ).add_to(m)

    # --------------------------------------------------------------------------
    # 6. CASCADING ADJACENT WARD WARNING PINS
    # --------------------------------------------------------------------------
    if (is_critical or is_warning) and "cascading_wards" in nearby:
        for casc in nearby["cascading_wards"]:
            cw_id = casc["ward_id"]
            if cw_id in WARDS_GIS:
                c_data = WARDS_GIS[cw_id]
                folium.Marker(
                    location=c_data["center"],
                    tooltip=f"<b>CASCADING ALERT:</b> {casc['name']} ({casc['relation']})",
                    popup=folium.Popup(f"""
                        <div style='width:220px; font-family:sans-serif;'>
                            <h4 style='color:#E65100; margin-bottom:4px;'>📡 ADJOINING SECTOR ALERT</h4>
                            <p style='font-size:12px; margin:2px 0;'><b>Target:</b> {casc['name']}</p>
                            <p style='font-size:11px; margin:2px 0;'><b>Relation:</b> {casc['relation']}</p>
                            <p style='font-size:11px; margin:2px 0;'><b>Surge Arrival Est:</b> ~{casc['surge_arrival_min']} mins</p>
                            <div style='background:#FFF3E0; color:#E65100; font-size:11px; padding:3px 6px; margin-top:4px;'>
                                Secondary sirens & alerts dispatched.
                            </div>
                        </div>
                    """, max_width=250),
                    icon=folium.Icon(color="orange", icon="broadcast-tower", prefix="fa")
                ).add_to(m)

    return m

