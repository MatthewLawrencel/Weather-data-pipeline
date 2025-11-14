cat > extract_data.py <<'PY'
import requests
import pandas as pd
from datetime import datetime, timezone
import os
from pathlib import Path

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_CSV = DATA_DIR / "indian_weather_raw.csv"

CITIES = {
    "Bengaluru": (12.9716, 77.5946), "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707), "Kolkata": (22.5726, 88.3639),
    "Delhi": (28.6139, 77.2090), "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567), "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873), "Lucknow": (26.8467, 80.9462),
    "Chandigarh": (30.7333, 76.7794), "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577), "Patna": (25.5941, 85.1376),
    "Nagpur": (21.1458, 79.0882), "Visakhapatnam": (17.6868, 83.2185),
    "Surat": (21.1702, 72.8311), "Mysuru": (11.0168, 76.9558),
    "Vadodara": (22.3072, 73.1812), "Guwahati": (26.1445, 91.7362)
}

def fetch_weather(city, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    d = r.json()
    return {
        "city": city,
        "time": datetime.now(timezone.utc),
        "temperature_c": d["main"]["temp"],
        "humidity_%": d["main"]["humidity"],
        "wind_speed_m_s": d["wind"]["speed"],
        "feels_like_c": d["main"]["feels_like"],
        "extracted_at": datetime.now(timezone.utc),
    }

def extract_all_cities():
    records = []
    print("\nExtracting weather for 20 cities...\n")
    for city, (lat, lon) in CITIES.items():
        try:
            rec = fetch_weather(city, lat, lon)
            records.append(rec)
            print(city, ": Success")
        except Exception as e:
            print(city, ": Failed", e)
    df = pd.DataFrame(records)
    df.to_csv(RAW_CSV, index=False)
    print("\nSaved raw CSV:", RAW_CSV)
    return df

if __name__ == "__main__":
    extract_all_cities()
PY
