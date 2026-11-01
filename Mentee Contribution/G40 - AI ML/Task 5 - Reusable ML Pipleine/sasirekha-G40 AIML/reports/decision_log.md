# Decision Log

| Decision Area | Decision Taken | Reason |
|---------------|----------------|--------|
| Dataset | E-Commerce Customer Churn Dataset | Suitable customer-level churn dataset |
| Target Variable | Churn | Binary classification target |
| Removed Column | CustomerID | Identifier only; no predictive value |
| Train-Test Split | 80:20 | Standard evaluation split |
| Stratification | Yes | Maintains churn class distribution |
| Numerical Missing Values | Median Imputation | Robust to outliers |
| Categorical Missing Values | Most Frequent Imputation | Preserves common category |
| Numerical Scaling | StandardScaler | Standardizes feature scales |
| Categorical Encoding | OneHotEncoder | Converts text to numeric features |
| ML Model | RandomForestClassifier | Accurate and handles nonlinear relationships |
| Pipeline | sklearn Pipeline | Ensures reusable preprocessing and modeling |
| Model Saving | Joblib | Enables future reuse without retraining |