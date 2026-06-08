import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV using pandas with date parsing
df = pd.read_csv('data/cloud_usage_dataset.csv', parse_dates=['date'])

# 2. Print shape, data types, and the first 10 rows
print("--- Dataset Shape ---")
print(df.shape)
print("\n--- Data Types ---")
print(df.dtypes)
print("\n--- First 10 Rows ---")
print(df.head(10))

# 3. Check for null values
print("\n--- Null Values Count ---")
print(df.isnull().sum())

# 4. Print total cost and average daily cost
total_cost = df['cost_usd'].sum()
# Grouping by date ensures we get the true average across unique billing days
avg_daily_cost = df.groupby('date')['cost_usd'].sum().mean() 

print(f"\nTotal Cost: ${total_cost:,.2nd}")
print(f"Average Daily Cost: ${avg_daily_cost:,.2nd}")

#CO2e
# 5. Create the co2e_kg column using the provided mathematical formula
df['co2e_kg'] = (df['cpu_hours'] * 0.0002) + (df['storage_gb'] * 0.00006 / 30) + (df['data_transfer_gb'] * 0.001)

# 6. Print total CO2e for the entire dataset period
total_co2e = df['co2e_kg'].sum()
print(f"\nTotal CO2e Baseline: {total_co2e:,.2nd} kg")

# 7. Group by service_type and print CO2e per service category
print("\n--- CO2e by Service Type ---")
print(df.groupby('service_type')['co2e_kg'].sum())

# 8. Group by team and print CO2e per team
print("\n--- CO2e by Team ---")
print(df.groupby('team')['co2e_kg'].sum())

#Visualization
# 9. Plot a line chart of daily CO2e over time
daily_co2e = df.groupby('date')['co2e_kg'].sum()

plt.figure(figsize=(10, 5))
plt.plot(daily_co2e.index, daily_co2e.values, color='#007acc', linewidth=2)
plt.title('Daily CO2e Emissions Over Time')
plt.xlabel('Date')
plt.ylabel('Emissions (kg CO2e)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('data/daily_co2e_trend.png') # 11. Save as PNG
plt.close()

# 10. Plot a bar chart of CO2e by region
regional_co2e = df.groupby('region')['co2e_kg'].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
regional_co2e.plot(kind='bar', color=['#007acc', '#4caf50', '#ff9800'])
plt.title('Total CO2e Emissions by Cloud Region')
plt.xlabel('Region')
plt.ylabel('Emissions (kg CO2e)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/regional_co2e.png') # 11. Save as PNG
plt.close()

#Save Clean Dataset & Version Control
df.to_csv('data/cloud_usage_enriched.csv', index=False)
print("\nEnriched dataset successfully saved!")