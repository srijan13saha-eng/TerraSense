import sqlite3
import pandas as pd
import math

DB_NAME = "terra_sense.db"

def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(telemetry)")
    columns = [column[1] for column in cursor.fetchall()]
    if columns and "fs_value" not in columns:
        cursor.execute("DROP TABLE IF EXISTS telemetry")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wards (
            ward_id INTEGER PRIMARY KEY,
            ward_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            raw_rainfall REAL,
            raw_moisture REAL,
            filtered_moisture REAL,
            ari_score REAL,
            fs_value REAL,
            risk_score INTEGER,
            ward_id INTEGER,
            FOREIGN KEY (ward_id) REFERENCES wards (ward_id)
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM wards')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO wards (ward_id, ward_name) VALUES (4, 'Ward 4 - Kullu Valley')")
        
    conn.commit()
    conn.close()

def calculate_factor_of_safety(moisture_pct, slope_angle_deg=35.0):
    """
    Geotechnical Infinite Slope Stability Equation.
    FS > 1.2 : Stable | FS 1.0 - 1.2 : Marginal | FS <= 1.0 : Failure Imminent
    """
    c_prime = 12.0  # Effective soil cohesion (kPa)
    gamma = 19.0    # Bulk unit weight of soil (kN/m^3)
    gamma_w = 9.81  # Unit weight of water (kN/m^3)
    z = 2.0         # Slip surface depth (meters)
    phi_deg = 28.0  # Internal friction angle of soil (degrees)
    
    beta = math.radians(slope_angle_deg)
    phi = math.radians(phi_deg)
    m = min(1.0, max(0.0, moisture_pct / 100.0))  # Saturation ratio
    
    num = c_prime + (gamma - (m * gamma_w)) * z * (math.cos(beta) ** 2) * math.tan(phi)
    den = gamma * z * math.sin(beta) * math.cos(beta)
    
    fs = num / den if den != 0 else 2.0
    return round(max(0.1, fs), 2)

def insert_telemetry(raw_rain, raw_moisture, ward_id=4, alpha=0.25, force_override=False):
    conn = get_connection()
    cursor = conn.cursor()
    
    if force_override:
        filtered_moisture = raw_moisture
        ari_score = raw_rain
    else:
        cursor.execute('''
            SELECT filtered_moisture, raw_rainfall 
            FROM telemetry 
            WHERE ward_id = ? 
            ORDER BY log_id DESC LIMIT 20
        ''', (ward_id,))
        history = cursor.fetchall()

        if history and history[0][0] is not None:
            prev_filtered = history[0][0]
            filtered_moisture = (alpha * raw_moisture) + ((1.0 - alpha) * prev_filtered)
        else:
            filtered_moisture = raw_moisture

        past_rains = [row[1] for row in history if row[1] is not None]
        weights = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        
        ari_score = raw_rain
        for i, rain_val in enumerate(past_rains[:len(weights)]):
            ari_score += rain_val * weights[i]

    # Geotechnical Factor of Safety
    fs_val = calculate_factor_of_safety(filtered_moisture)

    # Dynamic Risk Score (Moisture 50%, ARI 30%, FS Factor 20%)
    norm_moisture = min(100.0, filtered_moisture)
    norm_ari = min(100.0, (ari_score / 150.0) * 100.0)
    fs_risk = max(0.0, (1.5 - fs_val) / 1.0) * 100.0
    
    risk_score = int(min(100, max(0, (norm_moisture * 0.5) + (norm_ari * 0.3) + (fs_risk * 0.2))))

    cursor.execute('''
        INSERT INTO telemetry 
        (raw_rainfall, raw_moisture, filtered_moisture, ari_score, fs_value, risk_score, ward_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (round(raw_rain, 1), round(raw_moisture, 1), round(filtered_moisture, 1), round(ari_score, 1), fs_val, risk_score, ward_id))
    
    conn.commit()
    conn.close()

def fetch_telemetry_history(limit=25):
    try:
        conn = get_connection()
        query = f'''
            SELECT t.timestamp, t.raw_rainfall, t.raw_moisture, t.filtered_moisture, 
                   t.ari_score, t.fs_value, t.risk_score, w.ward_name
            FROM telemetry t
            JOIN wards w ON t.ward_id = w.ward_id
            ORDER BY t.log_id DESC LIMIT {limit}
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()