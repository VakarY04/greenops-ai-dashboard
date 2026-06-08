import os
import io
import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load environment variables securely from your .env file
load_dotenv()
CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not CONN_STR:
    print("Error: AZURE_STORAGE_CONNECTION_STRING not found in your .env file!")
    exit()

# Initialize the Azure Client
client = BlobServiceClient.from_connection_string(CONN_STR)
blob_client = client.get_container_client("greenops-data").get_blob_client("cloud_usage_enriched.csv")

print("Fetching and verifying data from Azure Blob Storage...")
# Download the data directly from the cloud into memory
data = blob_client.download_blob().readall()
df = pd.read_csv(io.BytesIO(data))

print("\n--- Success! Data Retrieved ---")
print(f"Dataset Shape: {df.shape}")
print(f"Total Calculated CO2e: {df['co2e_kg'].sum():.4f} kg")