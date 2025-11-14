cat > load_data.py <<'PY'
import os
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

CSV = Path("data/indian_weather_transformed.csv")
DATABASE_URL = os.getenv("DATABASE_URL")

def load():
    engine = create_engine(DATABASE_URL)
    df = pd.read_csv(CSV)

    create_sql = """
    CREATE TABLE IF NOT EXISTS weather_reports (
        city TEXT,
        temperature_c DOUBLE PRECISION,
        "humidity_%" DOUBLE PRECISION,
        wind_speed_m_s DOUBLE PRECISION,
        feels_like_c DOUBLE PRECISION,
        time TIMESTAMPTZ,
        extracted_at TIMESTAMPTZ
    );
    """

    with engine.connect() as c:
        c.execute(text(create_sql))
        c.execute(text("TRUNCATE weather_reports;"))
        c.commit()

    df.to_sql("weather_reports", engine, if_exists="append", index=False)
    print("Loaded", len(df), "rows")

if __name__ == "__main__":
    load()
PY
