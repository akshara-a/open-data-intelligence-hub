# Customer Segmentation with Actionable Business Insights

## Overview
RFM-based K-Means clustering to segment e-commerce customers, combined with
Ridge Regression (customer rating prediction) and Logistic Regression
(purchase likelihood prediction).

## Files
- `customer_segmentation_rfm.ipynb` – full notebook (EDA, clustering, regression, classification, tuning)
- `customer_segmentation_data.csv` – synthetic dataset (1500 customers, 13 columns)
- `eda_charts_task8.png` – spending/recency/frequency distributions, correlation heatmap
- `elbow_silhouette_task8.png` – elbow method + silhouette score comparison across K=2–7
- `segment_profile_task8.csv` – per-cluster profile with business segment names
- `model_comparison_task8.csv` – baseline vs tuned performance table
- `business_insights_task8.md` – full write-up: methodology, results, business recommendations

## Summary of Results
| Model | Metric | Baseline | Tuned | Selected |
|---|---|---|---|---|
| K-Means (K=4) | Silhouette | – | 0.338 | Yes |
| Ridge Regression | R² | 0.264 | 0.265 | Yes |
| Logistic Regression | F1 | 0.819 | 0.814 | Baseline (see notes) |

Four segments identified: **High-Value Loyal Customers**, **At-Risk Customers**,
**New and Promising Customers**, **Low-Engagement Customers** — each with
specific business actions detailed in `business_insights_task8.md`.