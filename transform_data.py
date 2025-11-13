import pandas as pd
from datetime import datetime, timezone

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the extracted weather data.
    """
    if df.empty:
        print("No data to clean.")
        return df

    #  Drop duplicates
    df = df.drop_duplicates()

    #  Fill missing values
    df = df.fillna({
        "temperature_c": 0.0,
        "humidity_%": 0.0,
        "wind_speed_m_s": 0.0,
        "feels_like_c": 0.0,
        "time": None,
        "extracted_at": None
    })

    # Convert time columns to timezone-aware datetimes
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
    else:
        df["time"] = datetime.now(timezone.utc)  # fallback if no time column exists

    df["extracted_at"] = pd.to_datetime(df["extracted_at"], utc=True, errors="coerce")

    # Add computed column
    df["feels_like_c"] = df["temperature_c"] - ((100 - df["humidity_%"]) / 5)

    # Re-order columns
    df = df[
        ["city", "time", "temperature_c", "humidity_%", "wind_speed_m_s", "feels_like_c", "extracted_at"]
    ]

    return df


if __name__ == "__main__":
    
    from extract_data import extract_all_cities as extract_weather_data

    print(" Fetching raw weather data...")
    raw_df = extract_weather_data()
    print(" Raw data:")
    print(raw_df)

    print("\n Cleaning data...")
    clean_df = clean_weather_data(raw_df)
    print("\n Cleaned data:")
    print(clean_df)

