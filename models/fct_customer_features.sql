-- Creating the Feature Store for AI Churn Prediction
WITH raw_orders AS (
    SELECT 
        customer_id,
        order_id,
        order_status,
        -- Modernization: Standardizing "dirty" date strings to BigQuery Timestamps
        PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', order_purchase_timestamp) as purchase_at,
        PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', order_delivered_customer_date) as delivered_at
    FROM {{ source('raw_ecommerce', 'olist_orders') }}
),

feature_engineering AS (
    SELECT 
        customer_id,
        COUNT(order_id) as total_orders,
        -- Calculate the average days to deliver (A key feature for Churn AI)
        AVG(TIMESTAMP_DIFF(delivered_at, purchase_at, DAY)) as avg_delivery_time_days
    FROM raw_orders
    WHERE order_status = 'delivered'
    GROUP BY 1
)

SELECT * FROM feature_engineering
