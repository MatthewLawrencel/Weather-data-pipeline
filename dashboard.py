cat > dashboard.py <<'PY'
import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

st.title("🌦 India Weather Dashboard")

if not DATABASE_URL:
    st.error("❌ DATABASE_URL not found. Set environment variable.")
    st.stop()

engine = create_engine(DATABASE_URL)

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM weather_reports ORDER BY extracted_at DESC", engine)

df = load_data()

st.subheader("Latest Weather Data")
st.dataframe(df, width="container")

city_list = df["city"].unique()

city = st.selectbox("Select city:", city_list)

st.subheader(f"📊 Weather Trends for {city}")

city_df = df[df["city"] == city].sort_values("extracted_at")

st.line_chart(
    city_df,
    x="extracted_at",
    y=["temperature_c", "humidity_%", "wind_speed_m_s"],
    width="container"
)
PY
