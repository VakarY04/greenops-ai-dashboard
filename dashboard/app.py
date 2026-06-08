import streamlit as st
import pandas as pd
import requests

# Page UI configurations using your preferred blue-beige accents
st.set_page_config(page_title="GreenOps AI Sustainability Dashboard", layout="wide")

st.markdown("<h1 style='color: #007acc;'>GreenOps AI Sustainability Dashboard</h1>", unsafe_allow_html=True)
st.subheader("Cloud Infrastructure Carbon Accounting & Predictive Systems")
st.markdown("---")

API_URL = "http://127.0.0.1:8000"

# Fetch general summary metrics from the running backend API
try:
    summary_res = requests.get(f"{API_URL}/metrics/summary").json()
    daily_res = requests.get(f"{API_URL}/metrics/daily").json()
    
    # 1. Top row KPI summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Carbon Footprint", value=f"{summary_res['total_co2e_kg']:.2f} kg CO2e")
    with col2:
        st.metric(label="Total Aggregated Cost", value=f"${summary_res['total_cost_usd']:.2f} USD")
    with col3:
        st.metric(label="Highest-Emission Team", value=summary_res['top_emitting_team'])
        
    st.markdown("<br>", unsafe_allow_html=True) # visual structural layout spacing
    
    # 2. Historical Daily Carbon Trend Data
    st.subheader("Historical Daily CO2e Emission Trends")
    daily_df = pd.DataFrame(daily_res)
    daily_df['date'] = pd.to_datetime(daily_df['date'])
    daily_df.set_index('date', inplace=True)
    st.line_chart(daily_df)
    
    st.markdown("---")
    
    # 3. AI Time-Series Forecast Actions
    st.subheader("Predictive Infrastructure Analysis")
    if st.button("Show 30-Day Forecast"):
        with st.spinner("Querying forecasting model artifact..."):
            forecast_res = requests.get(f"{API_URL}/forecast").json()
            forecast_df = pd.DataFrame(forecast_res)
            forecast_df['date'] = pd.to_datetime(forecast_df['date'])
            forecast_df.set_index('date', inplace=True)
            
            st.success("Next-quarter carbon targets loaded successfully!")
            st.line_chart(forecast_df)

except requests.exceptions.ConnectionError:
    st.error("Error: Could not connect to the FastAPI backend service. Please make sure uvicorn is running on port 8000!")