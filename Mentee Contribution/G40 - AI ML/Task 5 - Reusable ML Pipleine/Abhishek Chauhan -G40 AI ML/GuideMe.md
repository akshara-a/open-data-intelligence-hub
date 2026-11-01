# Customer Churn Prediction — Reusable ML Pipeline

A production-ready, reusable machine learning pipeline built with **scikit-learn** to predict customer churn risk for a subscription-based business.

---

## Project Overview

Customer churn is when a customer stops using a service. This pipeline predicts which customers are likely to churn so the business can take early action — offering discounts, improving support, or sending retention offers.

The pipeline is **fully reusable**: train it once, save it as a `.pkl` file, and use it to predict churn for any new customer without repeating preprocessing steps.

---

## Dataset

| Property | Detail |
|---|---|
| File | `churn.csv` |
| Rows | 36,992 customers |
| Columns | 24 |
| Target | `churn_risk_score` → renamed to `churn` (0 = No Churn, 1 = Churn) |

### Features Used

**Numerical (6)**

| Column | Description |
|---|---|
| `age` | Customer age |
| `days_since_last_login` | Days since the customer last logged in |
| `avg_time_spent` | Average time spent on the platform |
| `avg_transaction_value` | Average value of transactions |
| `avg_frequency_login_days` | Average number of days between logins |
| `points_in_wallet` | Loyalty points balance |

**Categorical (11)**

| Column | Description |
|---|---|
| `gender` | Customer gender (`Unknown` treated as NaN) |
| `region_category` | Region type — City / Town / Village |
| `membership_category` | Membership tier — No / Basic / Silver / Gold / Platinum |
| `joined_through_referral` | Whether referred (`?` treated as NaN) |
| `preferred_offer_types` | Type of offers preferred |
| `medium_of_operation` | Device used — Desktop / Smartphone / Both (`?` treated as NaN) |
| `internet_option` | Internet type — Wi-Fi / Mobile Data / Fiber Optic |
| `used_special_discount` | Whether customer used a discount — Yes / No |
| `offer_application_preference` | Whether customer applies offers — Yes / No |
| `past_complaint` | Whether customer raised a complaint — Yes / No |
| `complaint_status` | Status of last complaint (`No Information Available` treated as NaN) |

**Dropped Columns (6)**

| Column | Reason |
|---|---|
| `Unnamed: 0` | Row index, not a feature |
| `security_no` | Unique identifier per customer |
| `referral_id` | Unique identifier per customer |
| `joining_date` | Raw date string, not parsed |
| `last_visit_time` | Raw time string, not parsed |
| `feedback` | Free-form text, not handled by this pipeline |

---

## Pipeline Architecture

```
churn.csv
    │
    ▼
Rename target column (churn_risk_score → churn)
    │
    ▼
Drop unnecessary columns
(Unnamed: 0, security_no, referral_id, joining_date, last_visit_time, feedback)
    │
    ▼
Fix data type issues
  ├── avg_frequency_login_days  →  convert string to float
  ├── joined_through_referral   →  replace '?' with NaN
  ├── medium_of_operation       →  replace '?' with NaN
  ├── gender                    →  replace 'Unknown' with NaN
  └── complaint_status          →  replace 'No Information Available' with NaN
    │
    ▼
Separate Features (X) and Target (y)
    │
    ▼
Train-Test Split  →  80% Train | 20% Test  (stratified)
    │
    ▼
ColumnTransformer
  ├── Numeric columns   →  Median Imputer  →  StandardScaler
  └── Categorical cols  →  MostFrequent Imputer  →  OneHotEncoder
    │
    ▼
RandomForestClassifier (100 trees, random_state=42)
    │
    ▼
Evaluation Dashboard (Confusion Matrix + Precision/Recall/F1 + Accuracy Gauge)
    │
    ▼
Feature Importance (Top 15)
    │
    ▼
Save Pipeline → customer_churn_pipeline.pkl
    │
    ▼
Predict for New Customer
```

---

## Project Structure

```
Customer_Churn_Pipeline/
│
├── churn.csv                        # Raw dataset
├── Customer_Churn_Pipeline.ipynb    # Main notebook
├── customer_churn_pipeline.pkl      # Saved pipeline (generated on run)
├── model_evaluation.png             # Evaluation dashboard plot (generated on run)
└── GuideMe.md                       # This file
```

---

## Notebook Walkthrough

| Step | Section | What it does |
|---|---|---|
| 1 | Import Libraries | Loads pandas, numpy, sklearn, matplotlib, seaborn, joblib |
| 2 | Load and Inspect Dataset | Reads CSV, checks shape, missing values, and target distribution |
| 3 | Drop Unnecessary Columns | Removes 6 identifier/raw-string columns |
| 4 | Fix Data Type Issues | Converts string column to float; replaces sentinel values with NaN |
| 5 | Separate Features and Target | Splits dataframe into X and y |
| 6 | Train-Test Split | 80:20 split, stratified on target |
| 7 | Define Feature Groups | Lists numeric (6) and categorical (11) columns |
| 8 | Preprocessing Pipelines | Builds numeric and categorical sub-pipelines, combines with ColumnTransformer |
| 9 | Full Reusable ML Pipeline | Wraps preprocessor + RandomForest into one Pipeline object |
| 10 | Train the Pipeline | Fits entire pipeline on training data only |
| 11 | Predict on Test Data | Generates predictions on unseen test set |
| 12 | Evaluate the Model | Plots 3-panel dashboard — confusion matrix, metric bars, accuracy gauge |
| 13 | Feature Importance | Shows top 15 features driving churn predictions |
| 14 | Save the Pipeline | Serialises full pipeline to `.pkl` using joblib |
| 15 | Load and Predict | Loads saved pipeline, predicts churn for a new customer |

---

## Model Evaluation

The evaluation step produces a **3-panel visual dashboard** saved as `model_evaluation.png`:

- **Panel 1 — Confusion Matrix**: heatmap showing True Negatives, False Positives, False Negatives, and True Positives
- **Panel 2 — Precision / Recall / F1**: grouped bar chart comparing metrics for both classes
- **Panel 3 — Accuracy Gauge**: semicircle gauge displaying overall accuracy (green ≥ 80%, orange ≥ 65%, red below)

> **Recall** for the Churn class is the most important metric — missing a customer who will churn is more costly than a false alarm.

---

## Key Design Decisions

| Decision | Choice | Reason |
|---|---|---|
| Target rename | `churn_risk_score` → `churn` | Cleaner column name throughout the notebook |
| Sentinel values | Replaced `'?'`, `'Unknown'`, `'No Information Available'` with `NaN` | Lets the pipeline imputer handle them consistently |
| Numeric imputation | Median | Robust to outliers in transaction and spending columns |
| Categorical imputation | Most frequent | Preserves dominant category pattern |
| Encoding | `OneHotEncoder` | Avoids false ordering that label encoding implies for multi-class columns |
| Scaling | `StandardScaler` | Prevents high-value columns from dominating the model |
| Model | `RandomForestClassifier (n=100)` | Handles nonlinear patterns, resistant to overfitting |
| Train-test split | 80:20, `stratify=y` | Preserves churn ratio in both sets |
| Pipeline structure | `Pipeline` + `ColumnTransformer` | Prevents data leakage; entire workflow reusable on new data |
| Saved artifact | `.pkl` via `joblib` | Full pipeline (preprocessing + model) saved as one object |

---

## How to Run

### 1. Install Dependencies

```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib
```

### 2. Place the Dataset

Put `churn.csv` in the same folder as `Customer_Churn_Pipeline.ipynb`.

### 3. Run the Notebook

Open the notebook in Jupyter and run all cells top to bottom.

---

## Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Data loading and manipulation |
| `numpy` | Numerical operations and NaN handling |
| `scikit-learn` | Pipeline, preprocessing, model, and evaluation |
| `matplotlib` | Plotting the evaluation dashboard |
| `seaborn` | Confusion matrix heatmap |
| `joblib` | Saving and loading the pipeline |

---

## Author

Submitted as part of **Mini Project 2 — Phase 1: ML Engineering Fundamentals**  
Open Data Intelligence Hub — Mentee Contribution, Task 5

---

## Decision Log

### Project
Reusable Customer Churn Prediction Pipeline using Scikit-learn

### Technical Decisions

| Decision Area | Decision Taken | Reason |
|---|---|---|
| Dataset | Used Customer Churn Dataset | Contains customer details and churn information required for prediction |
| Removed Columns | Removed `Unnamed: 0`, `security_no`, `referral_id`, `joining_date`, `last_visit_time`, `feedback` | These are unique identifiers or raw strings that do not provide useful learning information |
| Target Column | Used `churn` (renamed from `churn_risk_score`) | Represents whether the customer leaves the service or not |
| Train-Test Split | Used 80:20 split | 80% data used for training and 20% for testing model performance |
| Stratification | Used `stratify=y` | Maintains the same churn/non-churn ratio in both training and testing data |
| Sentinel Values | Replaced `'?'`, `'Unknown'`, `'No Information Available'` with `NaN` | Ensures the imputer handles unknowns consistently inside the pipeline |
| Missing Numerical Values | Used Median Imputation | Median is less affected by outliers compared to mean |
| Missing Categorical Values | Used Most Frequent Imputation | Replaces missing categories with the most common value |
| Feature Scaling | Used `StandardScaler` | Brings all numerical features into a common scale |
| Encoding Method | Used `OneHotEncoder` | Converts categorical text values into 0/1 numerical format without implying any order between categories |
| Preprocessing | Used `ColumnTransformer` | Applies different preprocessing methods to numeric and categorical column types separately |
| Model Selection | Used `RandomForestClassifier` | Handles classification problems, learns complex nonlinear patterns, and reduces overfitting through ensemble voting |
| Pipeline Creation | Used `sklearn Pipeline` | Combines preprocessing and model training into one reusable workflow, preventing data leakage |
| Evaluation | Used Accuracy, Confusion Matrix, Classification Report, and visual dashboard | Measures overall and per-class model performance |
| Model Saving | Used `joblib` | Saves the complete pipeline (preprocessing + model) for future predictions |

### Final Decision

A reusable machine learning pipeline was created that automatically performs:

- Missing value handling
- Sentinel value cleaning
- Feature scaling
- Categorical encoding
- Model training
- Visual evaluation
- Prediction

The saved pipeline can be reused for predicting churn of new customers without repeating any preprocessing steps.

---

## Business Insights

### Why Churn Prediction Matters

Every customer who leaves costs the business more than retaining them would have. Research consistently shows acquiring a new customer costs 5–7x more than keeping an existing one. Predicting churn early gives the business time to act.

### What the Model Enables

| Insight | Business Action |
|---|---|
| Customer predicted to churn | Trigger a personalised retention offer or discount |
| High churn probability score | Prioritise for proactive customer support outreach |
| Membership category linked to churn | Redesign lower-tier membership benefits |
| Past complaint linked to churn | Fast-track complaint resolution for at-risk customers |
| Low avg time spent linked to churn | Send re-engagement campaigns to inactive users |
| Preferred offer type identified | Personalise offers based on what each customer responds to |

### Key Metrics to Watch

**Recall** is the most important metric for this problem. A false negative — predicting "No Churn" for a customer who actually leaves — means a missed opportunity to retain them. A false positive — flagging someone who wasn't going to leave — costs only a small retention offer.

The business should aim to **maximise recall on the Churn class** even if it slightly lowers overall accuracy.

### How to Use the Pipeline in Production

1. Export new customer records in the same format as `churn.csv`
2. Load the saved pipeline: `joblib.load('customer_churn_pipeline.pkl')`
3. Run `.predict()` and `.predict_proba()` to get churn label and confidence score
4. Flag customers with churn probability above a threshold (e.g. 60%) for retention action
5. Retrain the pipeline periodically as new data accumulates to keep predictions fresh
