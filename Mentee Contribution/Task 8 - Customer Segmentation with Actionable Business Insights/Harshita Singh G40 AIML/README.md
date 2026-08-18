# Customer Segmentation with Actionable Business Insights

An end-to-end customer segmentation project for an e-commerce company: cluster
customers by behaviour (K-Means), predict customer rating (regression), predict
purchase likelihood (classification), and translate every result into a
concrete, segment-specific business action.

## Project Structure

```text
customer-segmentation-project/
│
├── data/
│   └── customer_data.csv              # 1,500-row synthetic dataset
│
├── notebooks/
│   └── customer_segmentation.ipynb    # full, executed analysis
│
├── src/
│   ├── data_preprocessing.py          # cleaning, outliers, RFM, scaling
│   ├── clustering.py                  # elbow/silhouette, K-Means, PCA, profiling
│   ├── regression.py                  # Linear + Ridge, GridSearchCV tuning
│   ├── classification.py              # Logistic Regression, GridSearchCV tuning
│   └── model_evaluation.py            # model comparison table builder
│
├── reports/
│   ├── customer_segments.csv          # segment profile + recommended action
│   ├── business_insights.md           # narrative business insights
│   ├── model_comparison_table.csv     # baseline vs tuned performance
│   └── visualizations/                # all charts (EDA, elbow, PCA, ROC, etc.)
│
├── build_notebook.py                  # regenerates the notebook end-to-end
├── README.md
└── requirements.txt
```

## How to Reproduce

```bash
pip install -r requirements.txt
jupyter notebook notebooks/customer_segmentation.ipynb
```

Or regenerate the executed notebook and all reports from scratch:

```bash
python build_notebook.py
```

## Approach

1. **EDA** — distributions, missing values, duplicates, correlation heatmap,
   recency-vs-frequency view.
2. **Preprocessing** — median imputation, percentile-capped outliers, RFM
   feature engineering, StandardScaler.
3. **Clustering** — K-Means, k chosen via elbow method + silhouette score
   (final k=5, silhouette ≈ 0.42), PCA 2D visualization, per-cluster profiling.
4. **Segment naming** — clusters are mapped to business-meaningful names
   (High-Value Loyal, New & Promising, Discount-Driven, At-Risk,
   Low-Engagement) using a deterministic rule based on spend, frequency,
   recency, and discount usage — not manual eyeballing.
5. **Regression** — Linear vs Ridge Regression predicting `CustomerRating`,
   with `GridSearchCV` tuning Ridge's `alpha`.
6. **Classification** — Logistic Regression predicting `PurchaseLikelihood`,
   with `GridSearchCV` tuning `C`; evaluated via F1, ROC-AUC, confusion matrix.
7. **Business insights** — each segment gets a specific recommended action,
   backed by its profile numbers, in `reports/business_insights.md`.

## Dataset

`data/customer_data.csv` is a realistic **synthetic** dataset (1,500 customers)
generated to match five latent behavioural segments, with injected missing
values and outliers so the preprocessing steps are meaningfully exercised.
It is not real customer data.

## Key Results

- K-Means silhouette score: **0.418** (k=5)
- Ridge Regression (tuned): RMSE ≈ 0.66, R² ≈ 0.23 for `CustomerRating`
- Logistic Regression (tuned): F1 ≈ 0.82, ROC-AUC ≈ 0.82 for `PurchaseLikelihood`
- Highest-revenue segment: **High-Value Loyal Customers** (~46% of revenue from 15% of customers)
