import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from datetime import datetime
import pytz

st.set_page_config(page_title="Indian Weather Dashboard", page_icon="🌦️", layout="wide")

# ✅ 1️⃣ Try environment variable directly (no secrets.toml)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    st.error("""
    ❌ Database URL not found.

    ➤ Run this first in your terminal before launching Streamlit:
    export DATABASE_URL="postgresql://neondb_owner:npg_61kPBWhFtCEg@ep-red-forest-a1nxle5r.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    """)
    st.stop()

# ✅ 2️⃣ Create database engine
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    st.error(f"⚠️ Failed to connect to database: {e}")
    st.stop()

# ✅ 3️⃣ Load weather data
@st.cache_data(ttl=900)
def load_data():
    query = "SELECT * FROM weather_reports ORDER BY extracted_at DESC;"
    return pd.read_sql(query, engine)

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Could not load data: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ No weather data found yet. Try running the ETL first.")
    st.stop()

# ✅ Dashboard UI
st.title("🌦️ Indian Weather Dashboard")
st.caption("Real-time weather data for major Indian cities (via Neon PostgreSQL).")

# 🕒 Show last update time
last_updated = pd.to_datetime(df["extracted_at"].max()).tz_localize("UTC").tz_convert("Asia/Kolkata")
st.caption(f"🕒 Last Updated: {last_updated.strftime('%d %B %Y, %I:%M %p')} IST")

city = st.selectbox("🏙️ Select a City", sorted(df["city"].unique()))
filtered_df = df[df["city"] == city].sort_values("extracted_at", ascending=False).head(1)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Temp (°C)", round(filtered_df["temperature_c"].iloc[0], 1))
col2.metric("💧 Humidity (%)", filtered_df["humidity_%"].iloc[0])
col3.metric("🌬️ Wind (m/s)", filtered_df["wind_speed_m_s"].iloc[0])
col4.metric("🥵 Feels Like (°C)", round(filtered_df["feels_like_c"].iloc[0], 1))

st.subheader("📋 Latest Weather Data")
st.dataframe(df, use_container_width=True)
