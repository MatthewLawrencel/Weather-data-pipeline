import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os


# Page Config

st.set_page_config(
    page_title="Indian Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)


# Title

st.title("🌦️ Indian Weather Dashboard")
st.markdown("### Live Weather Insights from 20 Major Indian Cities")


# Database Connection

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    st.error("❌ DATABASE_URL not found. Please set the environment variable.")
    st.stop()

engine = create_engine(DATABASE_URL)

@st.cache_data(ttl=300)
def load_weather_data():
    query = "SELECT * FROM weather_reports ORDER BY extracted_at DESC"
    return pd.read_sql(query, engine)


# Load Data

try:
    df = load_weather_data()
except Exception as e:
    st.error(f"❌ Failed to load data from database:\n\n{e}")
    st.stop()

if df.empty:
    st.warning("⚠️ No weather data found in the database.")
    st.stop()


# Sidebar Filters

st.sidebar.header("🔍 Filter Data")
selected_city = st.sidebar.selectbox("Choose City", sorted(df["city"].unique()))

city_df = df[df["city"] == selected_city]


# Display City Data

st.subheader(f"🏙️ Weather Summary: **{selected_city}**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Temperature (°C)", f"{city_df.iloc[0]['temperature_c']:.1f}")
col2.metric("💧 Humidity (%)", f"{city_df.iloc[0]['humidity_%']:.1f}")
col3.metric("🌬️ Wind Speed (m/s)", f"{city_df.iloc[0]['wind_speed_m_s']:.1f}")
col4.metric("🥵 Feels Like (°C)", f"{city_df.iloc[0]['feels_like_c']:.1f}")

st.divider()


# Data Table

st.subheader("📘 Detailed Data Table")
st.dataframe(city_df, height=300, width="stretch")  # ✨ FIXED (no more errors)

st.divider()


# Line Chart (Temperature Trend)

st.subheader("📈 Temperature Trend Over Time")

fig = px.line(
    city_df,
    x="extracted_at",
    y="temperature_c",
    title=f"Temperature Trend — {selected_city}",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)


# Humidity Chart

st.subheader("💧 Humidity Trend")

fig2 = px.area(
    city_df,
    x="extracted_at",
    y="humidity_%",
    title=f"Humidity Trend — {selected_city}",
)

st.plotly_chart(fig2, use_container_width=True)


# Footer

st.markdown("---")
st.markdown("Made with ❤️ by Matthew · Powered by Streamlit + Neon DB")

