# Building a Recommendation System for E-Commerce

## Project Overview

This project implements multiple machine learning algorithms to build an e-commerce recommendation system that predicts customer value, purchase/campaign likelihood, and segments customers for personalized recommendations and targeted marketing.

## Dataset

`Ecommerce.csv` — a customer-level e-commerce behavioral dataset (10,000 customers, 14 columns) containing RFM (Recency, Frequency, Monetary) metrics and engagement data: session counts, page views, clicks, wishlist adds, cart abandonment rate, returns, an existing 5-tier segment label, and campaign response.

The dataset is customer-level (one row per customer) rather than interaction-level (one row per user-product pair), so it has no explicit `Rating` or `Purchase Status` column. The three ML tasks are mapped onto the closest real columns available:

| Task | Target Used | Stands In For |
|---|---|---|
| Regression | `Monetary` (total customer value) | Rating |
| Classification | `Campaign_Response` (0/1) | Purchase Status |
| Clustering | Customer segments (unchanged) | Customer segments |

## Approach

| ML Task | Algorithm | Target / Goal | Metrics Used |
|---|---|---|---|
| Regression | Ridge Regression | Predict customer monetary value | MAE, RMSE, R² |
| Classification | Logistic Regression | Predict campaign response likelihood | Accuracy, Precision, Recall, F1 |
| Clustering | K-Means | Segment customers | Inertia, Silhouette Score |

All models are tuned with `GridSearchCV`:
- **Ridge:** `alpha` ∈ [0.01, 0.1, 1, 10, 100]
- **Logistic Regression:** `C` ∈ [0.01, 0.1, 1, 10], `solver` ∈ [liblinear, lbfgs], `max_iter` ∈ [100, 200, 500]
- **K-Means:** `n_clusters` ∈ [2, 10], selected via Elbow Method + Silhouette Score

## Results

| ML Task | Best Result | Business Use |
|---|---|---|
| Regression | R² ≈ 0.87 (tuned Ridge, α=100) | Prioritize high-value customers for premium recommendations |
| Classification | F1 ≈ 0.56 (tuned Logistic Regression) | Target likely responders with marketing spend |
| Clustering | Silhouette ≈ 0.47 (k=2) | Design different retention strategies per segment |

K-Means at k=5 was also validated against the dataset's existing Iron/Copper/Silver/Gold/Platinum labels and recovered them almost perfectly — confirming the behavioral features capture the same signal the original tiers were built on.

## Conclusion

No single algorithm wins outright — each answers a different business question. Ridge Regression is the most accurate predictor of customer value, Logistic Regression gives a usable but imperfect ranking of campaign responders, and K-Means clustering gives the clearest, most actionable segmentation. A production system would combine all three: cluster for strategy, classify for targeting, and regress for sizing investment per customer.

## Files

| File | Description |
|---|---|
| `Ecommerce.csv` | Dataset used for all three models |
| `multi_algo_recommendation.ipynb` | Full notebook: preprocessing, all three models, tuning, evaluation, plots |
| `Multi-Algorithm_Recommendation_System_Comparison_Report.docx` | Final written report (problem statement through conclusion) |
| `README.md` | This file |
