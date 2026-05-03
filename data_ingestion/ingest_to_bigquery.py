import os
from google.cloud import bigquery
import pandas as pd

# 1. Setup Connection (Modernization Step)
# Ensure you have your Google Credentials JSON file path set
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private_id.json"

try:
    client = bigquery.Client()
    print("Cloud Connection Established! You are ready to migrate.")
except Exception as e:
    print(f"Connection failed: {e}")

# 2. Defining our "Silos" and their corresponding Cloud Tables
data_silos = {
    "sales_db": ["olist_orders_dataset.csv", "olist_order_items_dataset.csv"],
    "marketing_crm": ["olist_customers_dataset.csv"],
    "logistics_sys": ["olist_geolocation_dataset.csv"]
}

dataset_id = "olist-data-modernization.raw_ecommerce"

def upload_silo_data():
    for silo, files in data_silos.items():
        print(f"Migrating data from Silo: {silo}...")
        for file in files:
            table_name = file.replace(".csv", "")
            table_ref = f"{dataset_id}.{table_name}"

            # Load "Dirty" Data locally to simulate pre-processing
            df = pd.read_csv(file)

            # Basic Engineering check: ensure no empty critical IDs
            df = df.dropna(subset=[df.columns[0]])

            # Upload to Cloud Warehouse
            job = client.load_table_from_dataframe(df, table_ref)
            job.result()  # Wait for the job to complete
            print(f" Successfully migrated {table_name} to BigQuery.")

if __name__ == "__main__":
    upload_silo_data()
