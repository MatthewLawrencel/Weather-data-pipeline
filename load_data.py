import pandas as pd
from sqlalchemy import create_engine
from transform_data import clean_weather_data
from extract_data import extract_weather_data


def load_to_postgres(df: pd.DataFrame):
    """Load the cleaned weather data into PostgreSQL."""
    if df.empty:
        print("No data to load.")
        return

    # Database connection string
    engine = create_engine( "postgresql+psycopg2://neondb_owner:npg_39vLSiuZVelq@ep-weathered-queen-a1vi2p83-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")

    # Write to database table
    df.to_sql("weather_reports", engine, if_exists="append", index=False)
    print("Data successfully loaded into Neon PostgreSQL!")


if __name__ == "__main__":
    # Extract
    raw_df = extract_weather_data("Bengaluru")

    # Transform
    clean_df = clean_weather_data(raw_df)

    # Load
    load_to_postgres(clean_df)
