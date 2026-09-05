import time
import random
import data
import gis_engine

SCENARIOS = {
    "1": {
        "name": "STABLE_DRY",
        "rain_base": 0.0,
        "rain_variance": 1.5,
        "moisture_drain": -0.15
    },
    "2": {
        "name": "MONSOON_ACCUMULATION",
        "rain_base": 18.0,
        "rain_variance": 5.0,
        "moisture_absorption": 0.25
    },
    "3": {
        "name": "CLOUD_BURST_EVENT",
        "rain_base": 85.0,
        "rain_variance": 20.0,
        "moisture_absorption": 1.10
    },
    "4": {
        "name": "SLOPE_DRAINAGE",
        "rain_base": 0.0,
        "rain_variance": 0.5,
        "moisture_drain": -0.60
    }
}

def run_simulation():
    data.init_db()
    print("=====================================================")
    print("⛰️ TerraSense Physics Environment Emulator Active")
    print("=====================================================")
    
    # Optional Ward Selector
    print("Available Wards:")
    for w_id, w_name in gis_engine.get_all_ward_options().items():
        print(f"  {w_id}: {w_name}")
        
    ward_choice = input("\nEnter Ward ID to simulate [Default=4]: ").strip()
    try:
        target_ward = int(ward_choice) if ward_choice else 4
    except ValueError:
        target_ward = 4
        
    gis = gis_engine.get_ward_gis(target_ward)
    print(f"Selected: {gis['name']} (Slope: {gis['slope_angle_deg']}°)")

    print("\nSelect Scenario Mode:")
    print("1: Clear / Dry Weather (Stable)")
    print("2: Steady Monsoon Rain (Gradual Saturation)")
    print("3: Flash Cloudburst Event (Rapid Flood & Failure)")
    print("4: Post-Rain Drainage")
    print("5: 🛑 MANUAL OVERRIDE MODE (Control purely via Streamlit Sidebar)")
    
    choice = input("\nEnter Mode (1-5) [Default=2]: ").strip()
    
    if choice == "5":
        print("\n🛑 Manual Control Enabled! `sim.py` is paused.")
        print("Use the sliders and 'Inject Test Packet' button in Streamlit to control data manually.\n")
        while True:
            time.sleep(10)

    active_scenario = SCENARIOS.get(choice, SCENARIOS["2"])
    
    print(f"\n🚀 Running Scenario: {active_scenario['name']} for Ward {target_ward}...")
    print("Pushing telemetry packets every 3s. Press Ctrl+C to stop.\n")

    current_raw_moisture = 42.0

    while True:
        # 1. Compute realistic rainfall
        rain_noise = random.uniform(-active_scenario["rain_variance"], active_scenario["rain_variance"])
        raw_rain = max(0.0, active_scenario["rain_base"] + rain_noise)
        
        # 2. Physics-based moisture adjustment
        if "moisture_absorption" in active_scenario:
            delta = (raw_rain * 0.02) + active_scenario["moisture_absorption"] + random.uniform(-0.05, 0.05)
        else:
            delta = active_scenario["moisture_drain"] + random.uniform(-0.05, 0.05)

        current_raw_moisture = max(10.0, min(98.0, current_raw_moisture + delta))
        jittered_moisture = current_raw_moisture + random.uniform(-0.8, 0.8)

        # 3. Insert into database
        data.insert_telemetry(
            raw_rain,
            jittered_moisture,
            ward_id=target_ward,
            slope_angle_deg=gis["slope_angle_deg"]
        )
        
        print(f"[{gis['node_id']} - {active_scenario['name']}] Rain: {round(raw_rain, 1)} mm/h | Soil Moisture: {round(jittered_moisture, 1)}%")
        time.sleep(3)

if __name__ == "__main__":
    run_simulation()