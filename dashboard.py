import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
from PIL import Image
import os

# ----------------------------
# STREAMLIT PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Indian Weather Dashboard",
    page_icon="🌦️",  # your site icon
    layout="wide"
)

st.title("🌦️ Indian Weather Dashboard")
st.write("Displays the latest weather data loaded into PostgreSQL.")


# ----------------------------
# DATABASE CONNECTION
# ----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    st.error("❌ DATABASE_URL is missing. Set it before running the dashboard.")
    st.stop()

engine = create_engine(DATABASE_URL)


# ----------------------------
# FETCH DATA FROM POSTGRES
# ----------------------------
@st.cache_data(ttl=300)
def fetch_data():
    try:
        query = text("SELECT * FROM weather_reports ORDER BY extracted_at DESC")
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()


df = fetch_data()

if df.empty:
    st.warning("⚠ No weather data available in the database.")
    st.stop()


# ----------------------------
# CITY DROPDOWN
# ----------------------------
cities = df["city"].unique()
selected_city = st.selectbox("Choose City", cities)


# ----------------------------
# FILTER CITY DATA
# ----------------------------
city_df = df[df["city"] == selected_city].copy()

# Ensure timestamps are datetime
city_df["extracted_at"] = pd.to_datetime(city_df["extracted_at"], errors="coerce")


# ----------------------------
# CITY WEATHER TABLE
# ----------------------------
st.subheader("📊 City Weather Details")

st.dataframe(
    city_df,
    height=230,
    width="stretch"     # FIXES Streamlit width error
)


# ----------------------------
# TEMPERATURE TREND
# ----------------------------
st.subheader("🌡 Temperature Trend")

fig_temp = px.line(
    city_df,
    x="extracted_at",
    y="temperature_c",
    markers=True,
    title=f"Temperature Trend - {selected_city}",
)
st.plotly_chart(fig_temp, use_container_width=True)


# ----------------------------
# HUMIDITY TREND
# ----------------------------
st.subheader("💧 Humidity Trend")

fig_hum = px.line(
    city_df,
    x="extracted_at",
    y="humidity_%",
    markers=True,
    title=f"Humidity Trend - {selected_city}",
)
st.plotly_chart(fig_hum, use_container_width=True)


# ----------------------------
# WIND SPEED TREND
# ----------------------------
st.subheader("🌬 Wind Speed Trend")

fig_wind = px.line(
    city_df,
    x="extracted_at",
    y="wind_speed_m_s",
    markers=True,
    title=f"Wind Speed Trend - {selected_city}",
)
st.plotly_chart(fig_wind, use_container_width=True)

