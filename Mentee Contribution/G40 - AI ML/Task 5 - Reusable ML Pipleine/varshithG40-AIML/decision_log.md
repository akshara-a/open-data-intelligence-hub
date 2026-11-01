# Decision Log

| Decision Area | Decision Taken | Reason |
|---------------|----------------|--------|
| Removed column | Removed CustomerID | It is an identifier and does not carry predictive signal |
| Missing numeric values | Used median imputation | Median is robust to outliers and preserves central tendency |
| Missing categorical values | Used most frequent imputation | Keeps the most common category pattern and avoids introducing noise |
| Encoding | Used OneHotEncoder | Categorical variables must be converted to numeric form for the model |
| Scaling | Used StandardScaler | Numerical features are standardized to a common scale |
| Model | Used Logistic Regression | It is simple, interpretable, and works well as a baseline churn model |
| Split | Used 80:20 train-test split | This provides a reasonable validation setup for a small dataset |
| Stratification | Used stratify=y | This preserves the class distribution between train and test sets |
| Reusability | Saved the full pipeline with joblib | The preprocessing steps and trained model can be reused for future predictions without rewriting code |
| Business interpretation | High-risk customers can be targeted for retention campaigns | Early intervention can reduce churn and improve revenue retention |