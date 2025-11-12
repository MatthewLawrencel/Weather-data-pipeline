# Weather Data Engineering Pipeline  

---     
  Weather Data Extraction, Transformation, and Visualization using Python, PostgreSQL, and Streamlit

---

## Overview

This project demonstrates a complete **Data Engineering workflow**:
- **Extract** real-time weather data for multiple Indian cities using the OpenWeatherMap API  
- **Transform & clean** data into a structured format using `pandas`
- **Load** the cleaned data into a **PostgreSQL (Neon Cloud)** database
- **Visualize** the latest data interactively using **Streamlit**

The pipeline shows how to build a real-world, cloud-connected ETL system — from API to dashboard — using only Python and open-source tools.

---

## Project Architecture

OpenWeatherMap API → extract_data.py → PostgreSQL (Neon) → Streamlit Dashboard

---


---

## Tech Stack

| Layer | Tool / Library |
|-------|----------------|
| Language | Python 3.12 |
| Data Processing | Pandas |
| Database | PostgreSQL (via Neon Cloud) |
| ORM / DB Interface | SQLAlchemy |
| Visualization | Streamlit |
| Environment | Ubuntu 24.04 + venv |

---


---

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/MatthewLawrencel/Weather-data-pipeline.git
cd Weather-data-pipeline

```

### Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```
### API and Database Configuration

##### OpenWeatherMap API Key
Create an account at https://openweathermap.org/api
Copy your API key and export it:
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

**PostgreSQL Database (Neon)**
Create a free account on https://neon.tech
Create a new Postgres project → copy the connection string
Export it in your terminal:
```bash
export DATABASE_URL="postgresql://neondb_owner:your_password@your_host/neondb?sslmode=require"
```
### **Extract and Load Data**
```bash
Extracting live weather data for 20 Indian cities...
Bengaluru: Success
Mumbai: Success
...
Extracted 20 records.
```
### **Launching the Dashboard**
```bash
streamlit run dashboard.py

```
### Live Link
https://dashboardpy-hjqvid62w2a8dksutykte9.streamlit.app/

### Author
Matthew Lawrence L

lawrence82773824@gmail.com
