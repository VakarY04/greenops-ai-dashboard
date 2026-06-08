import pandas as pd

# Load the raw dataset from your facilitator
try:
    df = pd.read_csv('data/cloud_usage_dataset.csv', parse_dates=['date'])
    print("Successfully loaded raw dataset!")
except FileNotFoundError:
    print("Error: Could not find 'data/cloud_usage_dataset.csv'. Please make sure it's in your data folder!")
    exit()

# Run the Hurdle 1 carbon math
df['co2e_kg'] = (df['cpu_hours'] * 0.0002) + (df['storage_gb'] * 0.00006 / 30) + (df['data_transfer_gb'] * 0.001)

# Save the newly calculated data as the enriched file
df.to_csv('data/cloud_usage_enriched.csv', index=False)
print("Success! 'data/cloud_usage_enriched.csv' has been created in your data folder.")