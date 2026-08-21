# Decision Log

| Decision Area | Decision Taken | Reason |
|---------------|----------------|--------|
| Removed customerID | Identifier only | Does not help prediction |
| Missing Values | Median & Most Frequent | Robust preprocessing |
| Scaling | StandardScaler | Normalize numeric features |
| Encoding | OneHotEncoder | Convert categorical data |
| Model | RandomForestClassifier | Good for classification |
| Train-Test Split | 80:20 | Evaluate on unseen data |
| Stratification | Yes | Preserve churn ratio |
| Pipeline Saved | joblib | Reusable ML workflow |
