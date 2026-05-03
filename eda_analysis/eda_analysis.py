# Secure Authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your_credentials.json"
client = bigquery.Client()

# 1. Create the Dataset if it doesn't exist
dataset_id = f"{client.project}.raw_ecommerce"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"  # Explicitly setting location to match your error

try:
    client.create_dataset(dataset, timeout=30)
    print(f"Created dataset {dataset_id}")
except Exception:
    print(f"Dataset {dataset_id} already exists")

# 2. Upload the Mock Data we just generated
df = pd.read_csv('olist_orders_dataset.csv')
table_ref = f"{dataset_id}.olist_orders"

job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
job.result()  # Wait for upload

print(f"✅ Success! Table {table_ref} is now live in BigQuery.")

client = bigquery.Client()
project_id = client.project
dataset_id = f"{project_id}.raw_ecommerce"

# Create tables in the cloud
create_table_query = f"""
CREATE OR REPLACE TABLE `{dataset_id}.olist_orders_features` AS
WITH raw_orders AS (
    SELECT
        customer_id,
        order_id,
        order_status,
        SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', order_purchase_timestamp) as purchase_at,
        SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', order_delivered_customer_date) as delivered_at
    FROM `{dataset_id}.olist_orders`
)
SELECT
    customer_id,
    COUNT(order_id) as total_orders,
    -- Handling potential NULLs for clean AI training
    AVG(TIMESTAMP_DIFF(delivered_at, purchase_at, DAY)) as avg_delivery_time
FROM raw_orders
WHERE order_status = 'delivered'
  AND delivered_at IS NOT NULL
GROUP BY 1
"""

query_job = client.query(create_table_query)
query_job.result()  # This waits for the cloud to finish the job
print(f"✅ Feature Store Table '{dataset_id}.olist_orders_features' is now ready for AI!")

# creating the visualizations
# 1. Load and Standardize Dates
df = pd.read_csv('olist_orders_dataset.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])

# 2. Engineering the Logistics Metrics
# 'Delivery Spread' measures the total customer wait time
df['delivery_time_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days

# 'Bottlenecks' are defined as orders exceeding the 75th percentile (the slowest 25%)
bottleneck_limit = df['delivery_time_days'].quantile(0.75)
df['is_bottleneck'] = df['delivery_time_days'] > bottleneck_limit

# 3. Visualization for Stakeholders
plt.figure(figsize=(14, 6))

# Plot A: The Delivery Spread
plt.subplot(1, 2, 1)
sns.kdeplot(df['delivery_time_days'], fill=True, color="dodgerblue")
plt.axvline(df['delivery_time_days'].mean(), color='red', linestyle='--', label='Average Delay')
plt.title('Analysis of Delivery Spreads')
plt.xlabel('Days to Deliver')
plt.legend()

# Plot B: Bottleneck Identification
plt.subplot(1, 2, 2)
sns.boxplot(x='is_bottleneck', y='delivery_time_days', data=df, palette="Reds")
plt.title(f'Logistics Bottlenecks (> {bottleneck_limit:.0f} Days)')
plt.show()

# 4. Impact Summary
print(f"Mean Delivery Spread: {df['delivery_time_days'].mean():.1f} days")
print(f"Logistics Bottleneck Threshold: {bottleneck_limit} days")
