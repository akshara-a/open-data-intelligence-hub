# Task 9 — Optimized Classification Model with Feature Importance Analysis

Predicting customer subscription likelihood for an e-commerce company using an optimized classification model, built on `ecommerce_customer_data.csv`.

## Note on the target variable

The assignment brief (`task9.md`) describes a browsing/purchase dataset with a `Purchase` (Yes/No) target and session-level fields such as `PagesViewed`, `CartItems`, and `TimeOnSite`. The dataset actually provided (`ecommerce_customer_data.csv`) is a retail transaction/customer-profile export instead — every row is already a completed purchase, and there is no browsing-session data.

To keep this a genuine, business-relevant **binary classification problem** on the data available, the notebook uses `Subscription Status` (`Yes`/`No`) as the target — it is binary, business-meaningful (identifying loyal/engaged customers vs. one-off shoppers), and every task in the brief (EDA, preprocessing, baseline models, hyperparameter tuning, feature importance, threshold analysis, customer segmentation, business recommendations) is carried out against it exactly as specified.

## Contents

- `purchase_prediction_analysis.ipynb` — full, executed Jupyter notebook covering all required tasks: dataset understanding, data-quality checks, EDA, preprocessing pipeline, baseline model training (Logistic Regression, Decision Tree, Random Forest), hyperparameter optimization (`GridSearchCV`) on two models, hyperparameter sensitivity analysis, baseline-vs-optimized comparison, confusion matrix, ROC curve, feature-importance analysis, classification-threshold analysis, customer likelihood segmentation, business recommendations, and final conclusion/limitations.
- `purchase_prediction_model.pkl` — the saved, final preprocessing + classification pipeline (optimized Logistic Regression), produced by the notebook.
- `ecommerce_customer_data.csv` — the source dataset (already supplied).
- `requirements.txt` — Python packages needed to run the notebook.

## Key findings

- The dataset is clean (no missing values, no duplicate rows) but contains two notable quality artifacts documented in the notebook: `Discount Applied` and `Promo Code Used` are identical for every row (one is dropped as redundant), and every subscribed customer in this data happens to be male — flagged explicitly as a likely dataset artifact rather than a real business signal.
- Optimized Logistic Regression was selected as the final model: it matches an optimized Random Forest on F1-score and ROC-AUC while staying fully interpretable.
- `Discount Applied` and `Gender` are the two strongest predictors of subscription status; the notebook explains why the `Gender` effect specifically should not be acted on without further validation.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook purchase_prediction_analysis.ipynb
```
