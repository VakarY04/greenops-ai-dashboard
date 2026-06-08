import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI

app = FastAPI(title="GreenOps API")

# Use environment variables for paths to make the code cloud-portable
DATASET_PATH = os.getenv("DATASET_PATH", "data/cloud_usage_enriched.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "model/co2e_model.pkl")

# Load data and model artifacts securely
df = pd.read_csv(DATASET_PATH, parse_dates=['date'])
model = joblib.load(MODEL_PATH)

@app.get('/health')
def health():
    """
    Returns liveness probe status.
    """
    return {"status": "ok"}

@app.get('/metrics/summary')
def get_summary():
    """
    Calculates and returns total CO2e, total cost, top emitting team, and top region.
    """
    total_co2e = float(df['co2e_kg'].sum())
    total_cost = float(df['cost_usd'].sum())
    top_team = str(df.groupby('team')['co2e_kg'].sum().idxmax())
    top_region = str(df.groupby('region')['co2e_kg'].sum().idxmax())
    
    return {
        "total_co2e_kg": total_co2e,
        "total_cost_usd": total_cost,
        "top_emitting_team": top_team,
        "top_emitting_region": top_region
    }

@app.get('/metrics/daily')
def get_daily():
    """
    Returns daily aggregated carbon emissions array for UI charts.
    """
    daily = df.groupby('date')['co2e_kg'].sum().reset_index()
    daily = daily.sort_values('date')
    return [
        {"date": row['date'].strftime('%Y-%m-%d'), "co2e_kg": float(row['co2e_kg'])}
        for _, row in daily.iterrows()
    ]

@app.get('/forecast')
def get_forecast():
    """
    Generates a forward-looking 30-day forecast using the trained model artifact.
    """
    daily = df.groupby('date')['co2e_kg'].sum().reset_index()
    daily = daily.sort_values('date').reset_index(drop=True)
    
    last_known_emissions = daily['co2e_kg'].iloc[-1] if len(daily) > 0 else 35.0
    last_date = daily['date'].max() if len(daily) > 0 else pd.Timestamp.now()
    
    predictions = []
    for i in range(1, 31):
        future_date = last_date + pd.Timedelta(days=i)
        feature_vector = np.array([[last_known_emissions, last_known_emissions, last_known_emissions, future_date.dayofweek]])
        pred_val = float(model.predict(feature_vector)[0])
        
        predictions.append({
            "date": future_date.strftime('%Y-%m-%d'),
            "predicted_co2e_kg": max(0.0, pred_val)
        })
    return predictions

@app.get('/green-score')
def get_green_score():
    """
    Calculates the average daily CO2e footprint, maps it to a sustainability 
    grade (A-F), and determines the simulated CI/CD pipeline gate status.
    """
    daily = df.groupby('date')['co2e_kg'].sum().reset_index()
    avg_daily = float(daily['co2e_kg'].mean())
    
    # Evaluate thresholds based on the Green Score engineering specifications
    if avg_daily < 2.0:
        grade, action, gate = "A", "Excellent - no action needed", "PASS"
    elif avg_daily < 5.0:
        grade, action, gate = "B", "Good - minor optimisation advised", "PASS"
    elif avg_daily < 10.0:
        grade, action, gate = "C", "Moderate - review VM sizing", "PASS"
    elif avg_daily < 20.0:
        grade, action, gate = "D", "Poor - immediate rightsizing required", "WARNING"
    else:
        grade, action, gate = "F", "Critical - pipeline soft gate triggered", "BLOCKED"
        
    return {
        "grade": grade,
        "avg_daily_co2e": round(avg_daily, 2),
        "action": action,
        "gate": gate
    }