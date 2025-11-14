cat > transform_data.py <<'PY'
import pandas as pd
from pathlib import Path

RAW_CSV = Path("data/indian_weather_raw.csv")
TRANSFORMED = Path("data/indian_weather_transformed.csv")

def clean_weather_data(df):
    df = df.drop_duplicates().reset_index(drop=True)

    df["feels_like_c"] = df["temperature_c"] - ((100 - df["humidity_%"]) / 5)

    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    df["extracted_at"] = pd.to_datetime(df["extracted_at"], utc=True, errors="coerce")

    return df

if __name__ == "__main__":
    df = pd.read_csv(RAW_CSV)
    df_clean = clean_weather_data(df)
    df_clean.to_csv(TRANSFORMED, index=False)
    print("Saved:", TRANSFORMED)
PY
