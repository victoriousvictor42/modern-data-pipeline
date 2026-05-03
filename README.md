🚀 E-Commerce Data Modernization & Predictive Logistics
End-to-End Cloud Data Pipeline | BigQuery | dbt | Random Forest AI

📌 Executive Summary
This project demonstrates a full-scale Data Modernization of a legacy e-commerce system. I migrated siloed on-premise data to a Google Cloud Platform (GCP) data warehouse, engineered a Feature Store using modern SQL practices, and deployed a Machine Learning model to predict logistics bottlenecks.

🛠️ Tech Stack
Infrastructure: Google Cloud BigQuery (Data Warehouse).

Ingestion: Python (Pandas, Google Cloud SDK).

Transformation: dbt (Data Build Tool) style SQL for modular modeling.

AI/ML: Scikit-Learn (Random Forest Classifier).

Visualization: Matplotlib & Seaborn for Exploratory Data Analysis (EDA).

🏗️ The Pipeline Architecture
Ingestion: Automated the extraction of "dirty" legacy CSV files into a centralized BigQuery raw dataset.

Modernization (ELT): Used SQL CTEs to clean inconsistent timestamps and standardize delivery status metrics.

Feature Engineering: Materialized an olist_orders_features table to track customer loyalty and average delivery spreads.

Predictive Analytics: Built an AI model to flag high-risk "Late" orders, achieving actionable insights into logistics efficiency.

📊 Key Insights from EDA
Logistics Bottleneck: Identified that the 75th percentile of deliveries exceeds 38 days, highlighting a critical area for operational improvement.

Delivery Spread: The mean delivery time is 27.4 days, which serves as the primary feature for our Churn Prediction model.

📈 Impact
By identifying late orders before they occur, this system allows logistics managers in a high-growth environment (like Nairobi's e-commerce sector) to intervene early, reducing customer churn and improving brand trust.
