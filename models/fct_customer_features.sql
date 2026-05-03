-- Creating the Feature Store for AI Churn Prediction
-- This version works directly in BigQuery Console or a Python Client
WITH raw_orders AS (
    SELECT 
        customer_id,
        order_id,
        order_status,
        -- Correcting data types for Modernization
        SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', order_purchase_timestamp) as purchase_at,
        SAFE.PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', order_delivered_customer_date) as delivered_at
    FROM `project-id.raw_ecommerce.olist_orders` -- Hardcoded path for Notebooks
),

feature_store AS (
    SELECT 
        customer_id,
        COUNT(order_id) as total_orders,
        AVG(TIMESTAMP_DIFF(delivered_at, purchase_at, DAY)) as avg_delivery_time
    FROM raw_orders
    WHERE order_status = 'delivered'
    GROUP BY 1
)

SELECT * FROM feature_store
