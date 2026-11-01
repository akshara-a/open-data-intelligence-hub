# Predicting E-Commerce Purchase Likelihood Using an Optimized Classification Model

## Overview
Binary classification project predicting whether an e-commerce visitor will complete a purchase,
based on browsing behavior, transaction history, engagement, and demographics. Includes EDA,
preprocessing, baseline model comparison (Logistic Regression, Decision Tree, Random Forest),
hyperparameter optimization, feature-importance analysis, threshold analysis, and business
recommendations.

## Folder structure
```
mini-project-5/
├── data/
│   └── ecommerce_customer_data.csv          # synthetic dataset used in the analysis
├── notebooks/
│   └── purchase_prediction_analysis.ipynb   # full, executed analysis notebook
├── models/
│   └── purchase_prediction_model.pkl        # saved preprocessing + classifier pipeline
├── reports/
│   ├── model_comparison_table.csv
│   ├── feature_importance_report.csv
│   └── threshold_analysis.csv
├── presentation/
│   └── mini_project_5_presentation.pptx
├── requirements.txt
└── README.md
```

## Note on the dataset
No dataset was supplied with the project brief, so a structured synthetic dataset (6,000 rows) was
generated with realistic feature distributions and a purchase probability that depends on cart
items, prior purchases, engagement, discounts, and recency — mirroring the relationships a real
e-commerce dataset would exhibit. Swap in a real dataset by replacing
`data/ecommerce_customer_data.csv` with the same column names (or updating the notebook's column
lists) and re-running.

## How to reproduce
```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/purchase_prediction_analysis.ipynb
```

## Key result (this run)
- **Selected model:** Optimized Logistic Regression (highest F1-score on the held-out test set)
- **Test performance:** Accuracy 0.761 · Precision 0.782 · Recall 0.882 · F1 0.829 · ROC-AUC 0.827
- **Top predictive features:** time on site, days since last visit, discount usage, previous
  purchases, cart items

Exact numbers vary slightly between runs since the dataset is randomly generated each time — see
`reports/model_comparison_table.csv` for the numbers from the last executed run.

## Loading the saved model
```python
import joblib
model = joblib.load("models/purchase_prediction_model.pkl")
predictions = model.predict(new_customers_df)
probabilities = model.predict_proba(new_customers_df)[:, 1]
```
`new_customers_df` must contain the same raw columns as `data/ecommerce_customer_data.csv`
(minus `CustomerID` and `Purchase`) — the saved pipeline handles imputation, scaling, and encoding.
