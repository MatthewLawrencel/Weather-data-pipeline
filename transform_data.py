import pandas as pd
from datetime import datetime, timezone

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the extracted weather data."""

    if df.empty:
        print("No data to clean.")
        return df

    df = df.drop_duplicates()

    df = df.fillna({
        "temperature_c": 0.0,
        "humidity_%": 0.0,
        "wind_speed_m_s": 0.0,
        "feels_like_c": 0.0,
        "time": datetime.now(timezone.utc),
        "extracted_at": datetime.now(timezone.utc)
    })

    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    df["extracted_at"] = pd.to_datetime(df["extracted_at"], utc=True, errors="coerce")

    # Computed feels_like
    df["feels_like_c"] = df["temperature_c"] - ((100 - df["humidity_%"]) / 5)

    df = df[
        ["city", "time", "temperature_c", "humidity_%", "wind_speed_m_s", "feels_like_c", "extracted_at"]
    ]

    return df


if __name__ == "__main__":
    from extract_data import extract_all_cities

    print("Fetching raw weather data...")
    raw_df = extract_all_cities()

    print("Raw data:")
    print(raw_df)

    print("\nCleaning data...")
    clean_df = clean_weather_data(raw_df)

    clean_df.to_csv("data/cleaned_weather.csv", index=False)
    print("\nCleaned data saved!")

