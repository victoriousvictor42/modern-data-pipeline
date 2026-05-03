from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. Pulling the Engineered Features from BigQuery
client = bigquery.Client()
query = f"""
SELECT
    customer_id,
    total_orders,
    avg_delivery_time,
    -- Label: If delivery > 7 days, it's 'Late' (1), else 'On-Time' (0)
    CASE WHEN avg_delivery_time > 7 THEN 1 ELSE 0 END as is_late
FROM `{client.project}.raw_ecommerce.olist_orders_features`
"""
# Note: Ensure you have  ran the SQL transformation to create 'olist_orders_features' first!
df_ai = client.query(query).to_dataframe()

# 2. Preparing Data for Random Forest
X = df_ai[['total_orders', 'avg_delivery_time']] # Our Features
y = df_ai['is_late'] # Our Target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Training the Model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 4. Evaluating the "Engineering" Quality
y_pred = model.predict(X_test)
print("--- AI Model Performance Report ---")
print(classification_report(y_test, y_pred))
