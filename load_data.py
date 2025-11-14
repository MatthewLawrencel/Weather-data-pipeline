# load_data.py
import os
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

TRANSFORMED_CSV = Path("data/indian_weather_transformed.csv")
DATABASE_URL = os.getenv("DATABASE_URL")

def create_table_if_not_exists(engine):
    create_sql = """
    CREATE TABLE IF NOT EXISTS weather_reports (
        city TEXT,
        lat DOUBLE PRECISION,
        lon DOUBLE PRECISION,
        time TIMESTAMPTZ,
        temperature_c DOUBLE PRECISION,
        feels_like_c DOUBLE PRECISION,
        humidity_pct DOUBLE PRECISION,
        wind_speed_m_s DOUBLE PRECISION,
        extracted_at TIMESTAMPTZ
    );
    """
    with engine.connect() as conn:
        conn.execute(text(create_sql))
        conn.commit()

def load_to_postgres():
    if not TRANSFORMED_CSV.exists():
        raise FileNotFoundError(f"{TRANSFORMED_CSV} not found; run transform first.")

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set.")

    df = pd.read_csv(TRANSFORMED_CSV)

    # convert datetimes before insert
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    df["extracted_at"] = pd.to_datetime(df["extracted_at"], utc=True, errors="coerce")

    engine = create_engine(DATABASE_URL)

    # ensure table exists & has correct schema
    create_table_if_not_exists(engine)

    # truncate then append
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE weather_reports;"))
        conn.commit()

    # to_sql will insert rows; use if_exists='append'
    df.to_sql("weather_reports", engine, if_exists="append", index=False)
    print(f"Successfully loaded {len(df)} rows into weather_reports")

if __name__ == "__main__":
    try:
        load_to_postgres()
    except Exception as e:
        print("Database load failed:", e)

