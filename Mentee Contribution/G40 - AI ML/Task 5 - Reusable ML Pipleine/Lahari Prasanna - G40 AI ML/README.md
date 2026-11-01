# Mini Project 2 — Reusable Customer Churn Prediction Pipeline

**Student:** Lahari Prasanna Desetty
**Phase:** Phase 1 — ML Engineering Fundamentals
**Model:** RandomForestClassifier via scikit-learn Pipeline

---

## Project Overview

This project builds a **reusable, production-ready machine learning pipeline** using scikit-learn to predict customer churn for a subscription-based business.

The pipeline handles the full end-to-end ML workflow — from raw data loading to model evaluation and reusable prediction — without any manual preprocessing of train or test data separately.

---

## Business Problem

A subscription business wants to identify customers who are likely to cancel their service (churn). Early prediction allows the business to take proactive retention actions such as offering discounts, improving support, or suggesting better plans — reducing customer loss and protecting revenue.

---

## Project Structure

```
Mini_Project_2_Customer_Churn_Pipeline/
│
├── customer_churn_pipeline.ipynb   ← Main notebook with full pipeline code
├── customer_churn.csv              ← Dataset (Telco Customer Churn, adapted)
├── customer_churn_pipeline.pkl     ← Saved reusable pipeline (joblib)
├── decision_log.md                 ← All technical decisions explained
├── model_evaluation_report.md      ← Full evaluation results and interpretation
└── README.md                       ← This file
```

---

## Dataset

**Source:** Telco Customer Churn — Kaggle (blastchar/telco-customer-churn)
**Rows:** 7,043 customers
**Columns used:** 11 (as per assignment specification)

| Column | Type | Description |
|---|---|---|
| CustomerID | Categorical | Unique customer identifier (dropped before training) |
| Gender | Categorical | Customer gender |
| Age | Numerical | Customer age (18–70) |
| Tenure | Numerical | Months the customer has stayed |
| MonthlyCharges | Numerical | Monthly subscription amount |
| TotalCharges | Numerical | Total amount paid (had 11 hidden missing values) |
| ContractType | Categorical | Month-to-month, One year, Two year |
| PaymentMethod | Categorical | Electronic check, Mailed check, Bank transfer, Credit card |
| InternetService | Categorical | DSL, Fiber optic, No |
| SupportTickets | Numerical | Number of support issues raised (0–10) |
| Churn | Target | Yes or No |

---

## Pipeline Architecture

```
Raw Customer Data
        ↓
  Remove CustomerID
        ↓
  Train-Test Split (80:20, stratified)
        ↓
  ColumnTransformer
  ├── Numerical columns (Age, Tenure, MonthlyCharges, TotalCharges, SupportTickets)
  │       ├── SimpleImputer (strategy=median)
  │       └── StandardScaler
  └── Categorical columns (Gender, ContractType, PaymentMethod, InternetService)
          ├── SimpleImputer (strategy=most_frequent)
          └── OneHotEncoder (handle_unknown=ignore)
        ↓
  RandomForestClassifier (random_state=42)
        ↓
  Evaluation (Accuracy, Confusion Matrix, Classification Report)
        ↓
  Save Pipeline → customer_churn_pipeline.pkl
        ↓
  Load & Predict on New Customer Data
```

---

## Model Results

| Metric | Value |
|---|---|
| Accuracy | 78.50% |
| Precision (Churn=Yes) | 0.62 |
| Recall (Churn=Yes) | 0.50 |
| F1-score (Churn=Yes) | 0.55 |
| True Positives | 186 |
| False Negatives | 188 |

**Recall** is the most critical metric for this business problem — missing a churner costs more than incorrectly flagging a loyal customer.

---

## How to Run

### Step 1 — Open the notebook in Google Colab
Upload `customer_churn_pipeline.ipynb` and `customer_churn.csv` to Google Colab.

### Step 2 — Run all cells in order
Each cell is clearly labelled. Run them top to bottom — no manual preprocessing is required.

### Step 3 — Reuse the saved pipeline
```python
import joblib
import pandas as pd

# Load the saved pipeline
loaded_pipeline = joblib.load("customer_churn_pipeline.pkl")

# Predict for a new customer
new_customer = pd.DataFrame({
    "Gender": ["Female"],
    "Age": [32],
    "Tenure": [5],
    "MonthlyCharges": [850],
    "TotalCharges": [4250],
    "ContractType": ["Month-to-month"],
    "PaymentMethod": ["Electronic check"],
    "InternetService": ["Fiber optic"],
    "SupportTickets": [3]
})

prediction = loaded_pipeline.predict(new_customer)
print("Churn Prediction:", prediction[0])
```

The pipeline automatically handles all preprocessing — no manual cleaning, scaling, or encoding needed.

---

## Key Technical Decisions

| Decision | Choice | Reason |
|---|---|---|
| Removed column | CustomerID | Identifier with no predictive value |
| Split ratio | 80:20 | Sufficient training data with reliable test evaluation |
| Stratification | stratify=y | Preserves 73/27 churn ratio in both splits |
| Numerical imputation | Median | Robust to outliers in TotalCharges |
| Categorical imputation | Most frequent | Preserves natural category distribution |
| Encoding | OneHotEncoder | Converts text categories to numeric 0/1 columns |
| Scaling | StandardScaler | Normalises columns on very different scales |
| Model | RandomForestClassifier | Handles non-linear patterns, robust, good for classification |
| Saving | joblib | Saves complete pipeline for future reuse |

Full details in `decision_log.md`.

---

## Important Notes

- The pipeline is fitted **only on training data** — no data leakage
- `TotalCharges` had 11 hidden missing values (blank spaces) fixed using `pd.to_numeric(errors="coerce")` — handled inside the pipeline by `SimpleImputer`
- The `.pkl` file contains the complete pipeline — preprocessing + model — in one reusable file
- All random operations use `random_state=42` or `np.random.seed(42)` for full reproducibility

---

## Summary

> This project builds a reusable customer churn prediction pipeline using scikit-learn. The pipeline handles missing values, scales numerical columns, encodes categorical columns using OneHotEncoder, trains a RandomForestClassifier, evaluates the model, and saves the complete workflow for future use. The same pipeline can be reused to predict churn for any new customer data without manually repeating any preprocessing steps.
