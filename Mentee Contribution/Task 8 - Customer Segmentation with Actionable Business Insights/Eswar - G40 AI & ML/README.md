# Task 8: Customer Segmentation with Actionable Business Insights

This project segments e-commerce customers into actionable business groups using **K-Means clustering**, supported by **regression** (predicting customer rating), **classification** (predicting purchase likelihood), and **hyperparameter tuning**.

## Files in this Folder

| File | Description |
|---|---|
| `Customer_Segmentation.ipynb` | Full analysis notebook — EDA, preprocessing, clustering, regression, classification, tuning, business insights |
| `customer_data.csv` | Synthetic e-commerce customer dataset (1,200 customers) used as the source data |
| `customer_segments.csv` | Output file: each customer mapped to their cluster and business segment name |
| `business_insights.md` | Full write-up of segment characteristics, revenue contribution, and recommended business actions |
| `requirements.txt` | Python dependencies needed to run the notebook |

## Dataset

The dataset (`customer_data.csv`) contains 1,200 synthetic customers with the following columns:

- `CustomerID`, `Age`, `Gender`, `AnnualIncome`
- `TotalSpending`, `PurchaseFrequency`, `AverageOrderValue`
- `DaysSinceLastPurchase`, `WebsiteVisits`, `DiscountUsage`, `CustomerRating`
- `WillPurchaseAgain` (classification target: 1 = likely to purchase again, 0 = not)

## Methodology

1. **EDA** — distributions, correlations, recency-vs-frequency analysis, outlier checks.
2. **Preprocessing** — missing value imputation, IQR-based outlier capping, categorical encoding, RFM feature engineering, scaling.
3. **Clustering** — K-Means with `k` selected via the elbow method and silhouette score (final k=5, silhouette ≈ 0.46).
4. **Segment Profiling** — each cluster is profiled on RFM + discount usage + rating, then assigned a business name (High-Value Loyal, At-Risk, Discount-Driven, New & Promising, Low-Engagement).
5. **Regression** — Linear and Ridge Regression predict `CustomerRating`; Ridge is tuned with `GridSearchCV`.
6. **Classification** — Logistic Regression predicts `WillPurchaseAgain`; tuned with `GridSearchCV`, evaluated with confusion matrix, F1-score, and ROC-AUC.
7. **Business Insights** — each segment's characteristics are translated into concrete marketing/retention actions (see `business_insights.md`).

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook Customer_Segmentation.ipynb
```

Run all cells top to bottom — the notebook loads `customer_data.csv` directly from this folder.

## Key Results

- **5 customer segments** identified, clearly separated on recency, frequency, and monetary value.
- **High-Value Loyal** customers make up 18% of the customer base but generate **46% of revenue**.
- **At-Risk** customers (avg. 147 days since last purchase) represent **26% of revenue** at risk of churn — the top priority for win-back campaigns.
- Regression model achieves R² ≈ 0.61 predicting customer rating.
- Classification model achieves F1 ≈ 0.95 predicting purchase likelihood.

Full segment-by-segment recommendations are in [`business_insights.md`](./business_insights.md).
