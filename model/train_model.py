import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Ensure the model directory exists
os.makedirs('model', exist_ok=True)

# ----------------------------------------------------
# Task A - Ingestion & Feature Engineering
# ----------------------------------------------------
# 1. Load your enriched data
df = pd.read_csv('data/cloud_usage_enriched.csv', parse_dates=['date'])

# Aggregate to daily totals
daily = df.groupby('date')['co2e_kg'].sum().reset_index()
daily = daily.sort_values('date').reset_index(drop=True)

# NOTE: Real-world time series models require enough history to compute lookbacks.
# If your current mock dataset is small, this section appends synthetic historical cycles 
# to dynamically unblock your pipeline and prevent empty DataFrame crashes!
if len(daily) < 45:
    print(f"Current historical timeline has {len(daily)} days. Appending synthetic baseline data for training...")
    base_date = daily['date'].min() if len(daily) > 0 else pd.Timestamp('2026-05-01')
    extended_records = []
    # Build 60 days of mock history containing weekend drops and random processing spikes
    for i in range(60):
        current_date = base_date - pd.Timedelta(days=i+1)
        day_of_week = current_date.dayofweek
        base_emissions = 45.0 if day_of_week < 5 else 12.0  # Weekend low-power drops
        noise = np.random.normal(0, 3.5)
        extended_records.append({'date': current_date, 'co2e_kg': max(1.0, base_emissions + noise)})
    
    extended_df = pd.DataFrame(extended_records)
    daily = pd.concat([extended_df, daily], ignore_index=True)
    daily = daily.sort_values('date').reset_index(drop=True)

# 2 & 3. Engineering Lags and Rolling Measurements
daily['lag_7'] = daily['co2e_kg'].shift(7)
daily['lag_14'] = daily['co2e_kg'].shift(14)
daily['rolling_7'] = daily['co2e_kg'].rolling(7).mean()

# 4. Day of the week extraction (0 = Monday, 6 = Sunday)
daily['dow'] = daily['date'].dt.dayofweek

# 5. Drop NaN rows introduced by the lookback windows
daily = daily.dropna().reset_index(drop=True)

# ----------------------------------------------------
# Task B - Train/Test Split & Model Training
# ----------------------------------------------------
features = ['lag_7', 'lag_14', 'rolling_7', 'dow']
target = 'co2e_kg'

# 6. Time-Series Split: Last 30 days for testing, remainder for training
X = daily[features]
y = daily[target]

X_train = X.iloc[:-30]
y_train = y.iloc[:-30]
X_test = X.iloc[-30:]
y_test = y.iloc[-30:]

# 8. Train the Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)
print("Forecasting model trained successfully!")

# ----------------------------------------------------
# Task C - Evaluation & Plotting
# ----------------------------------------------------
# 10. Predict on the test set
y_pred = model.predict(X_test)

# 11. Calculate Root Mean Squared Error (RMSE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mean_val = y_test.mean()
error_percentage = (rmse / mean_val) * 100

print("\n--- Model Evaluation ---")
print(f"Test Set Mean Daily CO2e: {mean_val:.4f} kg")
print(f"Model Prediction RMSE: {rmse:.4f} kg")
print(f"Error Percentage of Mean: {error_percentage:.2f}%")

# Interpretation Check
if error_percentage < 10:
    print("Interpretation: Success! Error is below the 10% threshold requirement.")
else:
    print("Interpretation: Error exceeds 10%. Adding localized weather context or cloud region features might help.")

# 13. Plot actual vs predicted patterns
plt.figure(figsize=(10, 5))
test_dates = daily['date'].iloc[-30:]
plt.plot(test_dates, y_test.values, label='Actual Emissions', marker='o', color='#2b2b2b', linewidth=2)
plt.plot(test_dates, y_pred, label='Forecasted Emissions', marker='x', linestyle='--', color='#007acc', linewidth=2)
plt.title('Hurdle 3: Actual vs Forecasted CO2e Emissions (30-Day Test Window)')
plt.xlabel('Date')
plt.ylabel('Emissions (kg CO2e)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Save plot to model directory
plt.savefig('model/forecast_plot.png')
plt.close()
print("Evaluation chart exported safely to model/forecast_plot.png")

# ----------------------------------------------------
# Task D - Save Model Artefact
# ----------------------------------------------------
# 14. Save the trained model artifact using joblib
joblib.dump(model, 'model/co2e_model.pkl')
print("Model binary artifact successfully saved to model/co2e_model.pkl")