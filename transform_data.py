from extract_data import extract_all_cities

import pandas as pd
from datetime import datetime, timezone


def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        print("No data to clean.")
        return df

    df = df.drop_duplicates()

    df = df.fillna({
        "temperature_c": 0.0,
        "humidity_%": 0.0,
        "wind_speed_m_s": 0.0
    })

    df["extracted_at"] = pd.to_datetime(df["extracted_at"], utc=True, errors="coerce")

    df["time"] = datetime.now(timezone.utc)

    df["feels_like_c"] = df["temperature_c"] - ((100 - df["humidity_%"]) / 5)

    df = df[
        ["city", "time", "temperature_c", "humidity_%", "wind_speed_m_s", "feels_like_c", "extracted_at"]
    ]

    return df


if __name__ == "__main__":
    raw_df = extract_all_cities()
    print(" Raw data:")
    print(raw_df)

    clean_df = clean_weather_data(raw_df)
    print("\n Cleaned & transformed data:")
    print(clean_df)
