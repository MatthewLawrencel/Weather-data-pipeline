import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import plotly.express as px

# Page Settings
st.set_page_config(
    page_title="Indian Weather Dashboard",
    page_icon="🌦️",
    layout="wide",
)

st.markdown("""
    <h1 style='text-align: center; color: #4A90E2;'>🌦️ Indian Weather Dashboard</h1>
    <p style='text-align: center; font-size:18px; color: grey;'>
        Real-time weather insights for 20 major Indian cities
    </p>
""", unsafe_allow_html=True)

# Load Data
DATABASE_URL = os.getenv("DATABASE_URL")

@st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    return pd.read_sql("SELECT * FROM weather_reports", engine)

df = load_data()

# Sidebar Filters

st.sidebar.header("🔍 Filters")
selected_city = st.sidebar.selectbox("Select City", df["city"].unique())
city_df = df[df["city"] == selected_city]


# Metrics Row

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌡 Temperature (°C)",
        value=round(city_df["temperature_c"].iloc[0], 2)
    )

with col2:
    st.metric(
        label="💧 Humidity (%)",
        value=round(city_df["humidity_%"].iloc[0], 2)
    )

with col3:
    st.metric(
        label="🌬 Wind Speed (m/s)",
        value=round(city_df["wind_speed_m_s"].iloc[0], 2)
    )

with col4:
    st.metric(
        label=" Feels Like (°C)",
        value=round(city_df["feels_like_c"].iloc[0], 2)
    )

st.markdown("---")


# City Data Table

st.subheader(f"📍 Weather Details for **{selected_city}**")
st.dataframe(city_df, height=200, width="auto")

# -------------------------
# Temperature Bar Chart
# -------------------------
st.subheader("🌡 Temperature Comparison Across All Cities")

fig1 = px.bar(
    df,
    x="city",
    y="temperature_c",
    color="temperature_c",
    color_continuous_scale="Blues",
    title="City-wise Temperature Distribution",
    height=500
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Humidity Chart
# -------------------------
st.subheader("💧 Humidity Levels Across Cities")

fig2 = px.line(
    df,
    x="city",
    y="humidity_%",
    markers=True,
    title="Humidity % by City",
    color="city"
)
st.plotly_chart(fig2, use_container_width=True)


# Footer

st.markdown(
    """
    <hr>
    <p style='text-align:center; color:grey'>
        Built with ❤️ using Streamlit | Weather Data Pipeline Project
    </p>
    """,
    unsafe_allow_html=True
)

