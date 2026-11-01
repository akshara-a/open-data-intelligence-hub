# E-Commerce Recommendation System

Machine learning models built on customer browsing/purchase data to support
product recommendations: predicting ratings, predicting purchase likelihood,
and segmenting customers by behavior.

## What's in this repo

| File | Description |
|---|---|
| `Notebook.ipynb` | Full analysis: preprocessing, EDA, regression, classification, clustering, hyperparameter tuning |
| `ecommerce_user_behavior_8000.csv` | Raw dataset (8,000 browsing sessions) |
| `Business_Report.docx` | Non-technical summary of results and recommendations |

## Problem

An e-commerce platform wants to improve recommendations using its browsing
and purchase data. The notebook builds three models toward that goal:

1. **Regression** &mdash; predict the rating a customer would give a product
2. **Classification** &mdash; predict whether a session ends in a purchase
3. **Clustering** &mdash; group customers into behavioral segments

Each model is tuned with cross-validated hyperparameter search and evaluated
with the metrics appropriate to the task.

## Dataset

`ecommerce_user_behavior_8000.csv` contains one row per browsing session:

- `user_id`, `age`, `gender`, `device_type` &mdash; identifiers and demographics
- `time_on_site`, `pages_viewed`, `avg_session_time`, `bounce_rate` &mdash; engagement
- `previous_purchases`, `cart_items`, `discount_seen`, `ad_clicked`, `returning_user` &mdash; purchase and marketing signals
- `purchase` &mdash; whether the session converted (classification target)

The dataset does not include a rating column, so the notebook builds one
from a weighted combination of the existing features as a stand-in target
for the regression task. See the caveat below before trusting that model.

## Setup

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

Then open the notebook:

```bash
jupyter notebook Notebook.ipynb
```

Run all cells top to bottom &mdash; the dataset CSV needs to sit in the same
folder as the notebook.

## Results

| Model | Metric | Result |
|---|---|---|
| Ridge Regression (rating) | R² / RMSE | 0.998 / 0.03 |
| Logistic Regression (purchase, tuned) | Accuracy / F1 / ROC-AUC | 86.7% / 0.90 / 0.91 |
| K-Means (segmentation, k=4) | Silhouette Score | 0.16 |

Four customer segments came out of the clustering step:

- **Efficient Shoppers** (28%) &mdash; short sessions, low bounce, decent ratings
- **High-Value Loyal** (23%) &mdash; longest sessions, most repeat purchases, highest ratings
- **At-Risk Browsers** (24%) &mdash; very short sessions, high bounce, low ratings
- **Frustrated Browsers** (25%) &mdash; long sessions but still high bounce and low ratings

## Caveat on the rating model

Because this dataset has no real customer ratings, the rating column was
generated from a formula involving the other features, so the regression
model's near-perfect score reflects it recovering that formula rather than
predicting genuine customer sentiment. Retrain on real rating data before
using this model in production.

## Next steps

- Replace the synthetic rating with real customer feedback and retrain
- Try tree-based models (Random Forest, Gradient Boosting) as a stronger baseline
- Investigate the Frustrated Browsers segment for possible UX/checkout friction
- A/B test any recommendation ranking before full rollout
