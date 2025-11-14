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
        "wind_speed_m_s": 0.0,
        "feels_like_c": 0.0,
    })

    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    df["extracted_at"] = pd.to_datetime(df["extracted_at"], utc=True, errors="coerce")

    df = df[
        ["city", "time", "temperature_c", "humidity_%", "wind_speed_m_s", "feels_like_c", "extracted_at"]
    ]

    return df


if __name__ == "__main__":
    from extract_data import extract_all_cities
    raw_df = extract_all_cities()

    print("Raw:")
    print(raw_df)

    cleaned = clean_weather_data(raw_df)
    print("\nCleaned:")
    print(cleaned)

