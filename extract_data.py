import requests
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
import os

#  OpenWeatherMap API key
API_KEY = "f0d17542f4b2710bec5278246688429e"

#  Neon PostgreSQL connection URL 
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://neondb_owner:npg_JvYhZ5OTi9Gy@ep-damp-rice-a1pcsqzf-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
)

# 20 Major Indian Cities with coordinates
CITIES = {
    "Bengaluru": (12.9716, 77.5946),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Delhi": (28.6139, 77.2090),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Chandigarh": (30.7333, 76.7794),
    "Bhopal": (23.2599, 77.4126),
    "Indore": (22.7196, 75.8577),
    "Patna": (25.5941, 85.1376),
    "Nagpur": (21.1458, 79.0882),
    "Visakhapatnam": (17.6868, 83.2185),
    "Surat": (21.1702, 72.8311),
    "Mysuru": (11.0168, 76.9558),
    "Vadodara": (22.3072, 73.1812),
    "Guwahati": (26.1445, 91.7362),
}

def fetch_weather(city, lat, lon):
    """Fetch weather data from OpenWeatherMap"""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "city": city,
        "temperature_c": data["main"]["temp"],
        "humidity_%": data["main"]["humidity"],
        "wind_speed_m_s": data["wind"]["speed"],
        "feels_like_c": data["main"]["feels_like"],
        "time": datetime.now(timezone.utc),
        "extracted_at": datetime.now(timezone.utc),
    }

def extract_all_cities():
    """Fetch weather for all 20 Indian cities"""
    all_data = []
    print("\nExtracting live weather data for 20 Indian cities...\n")

    for city, (lat, lon) in CITIES.items():
        try:
            record = fetch_weather(city, lat, lon)
            all_data.append(record)
            print(f"{city}: Success")
        except Exception as e:
            print(f"{city}: Failed ({e})")

    df = pd.DataFrame(all_data)
    print(f"\n Extracted {len(df)} records.")
    return df


def extract_weather_data(city):
    """Extract weather for a single city (used by transform_data.py)."""
    city = city.strip()
    if city not in CITIES:
        raise ValueError(f"{city} not in CITIES list.")

    lat, lon = CITIES[city]
    record = fetch_weather(city, lat, lon)
    return pd.DataFrame([record])

def load_to_postgres(df):
    """Load extracted data into Neon PostgreSQL"""
    if df.empty:
        print("No data to load.")
        return
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE weather_reports;"))
            conn.commit()

        df.to_sql("weather_reports", engine, if_exists="append", index=False)
        print(f"Successfully loaded {len(df)} rows into PostgreSQL.")
    except Exception as e:
        print(f"Database load failed: {e}")

if __name__ == "__main__":
    df = extract_all_cities()
    load_to_postgres(df)

