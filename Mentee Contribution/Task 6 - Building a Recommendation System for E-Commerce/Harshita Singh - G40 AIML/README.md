# E-Commerce Recommendation System — ML Model Comparison

Implementing and comparing regression, classification, and clustering algorithms to support product recommendations, purchase-likelihood prediction, and customer segmentation for an e-commerce business.

## Project Structure

```
.
├── Ecommerce_recommendation_system.ipynb   # Main notebook: EDA, models, tuning, evaluation
├── ecommerce_customer_data.csv             # Dataset used
├── requirements.txt                        # Python dependencies
└── README.md
```

## Objective

Build and compare machine learning models to help an e-commerce business:

- Predict customer ratings (**Regression**)
- Predict purchase likelihood (**Classification**)
- Segment customers by behavior (**Clustering**)
- Improve model performance via **hyperparameter tuning**
- Compare models using appropriate **evaluation metrics**

## Dataset

`ecommerce_customer_data.csv` contains 350 customer records with the following columns:

| Column | Description |
|---|---|
| `Customer ID` | Unique customer identifier |
| `Gender` | Customer gender |
| `Age` | Customer age |
| `City` | Customer location |
| `Membership Type` | Bronze / Silver / Gold |
| `Total Spend` | Total amount spent by the customer |
| `Items Purchased` | Number of items purchased |
| `Average Rating` | Customer's average product rating |
| `Discount Applied` | Whether a discount was applied |
| `Days Since Last Purchase` | Recency of last purchase |
| `Satisfaction Level` | Satisfied / Neutral / Unsatisfied |

**Note:** This dataset is customer-level (not transaction-level), so the task mapping is adapted slightly from the original spec — see the notebook's intro cell for details (e.g. `Purchase_Status` is derived from `Satisfaction Level` since no direct purchase flag exists).

## Approach

### Part A — Regression
Linear Regression and Ridge Regression predict `Average Rating` from spend, items purchased, age, discount usage, and recency. Evaluated with MAE, MSE, RMSE, R².

### Part B — Classification
Logistic Regression predicts `Purchase_Status` (Satisfied vs Not Satisfied) as a purchase-likelihood proxy. Evaluated with Accuracy, Precision, Recall, F1-Score, ROC-AUC.

> Note: `Average Rating` is deliberately excluded as a feature here to avoid label leakage — see the notebook for details on why, and a caveat on this dataset's near-deterministic synthetic structure.

### Part C — Clustering
K-Means segments customers using spend, items purchased, rating, recency, and discount usage. Best K selected via Elbow Method + Silhouette Score.

### Part D — Hyperparameter Tuning
GridSearchCV tunes:
- Ridge Regression: `alpha`
- Logistic Regression: `C`, `penalty`, `solver`
- K-Means: `n_clusters` (via elbow/silhouette sweep)

### Part E — Model Comparison & Business Alignment
Comparison tables across all three models, mapped to business value (recommendation quality, targeted campaigns, customer segmentation), plus a final conclusion and recommendation.

## How to Run

```bash
pip install -r requirements.txt
jupyter notebook Ecommerce_recommendation_system.ipynb
```

## Deliverables Checklist

- [x] Python notebook
- [x] Dataset used
- [x] Data preprocessing steps
- [x] Exploratory Data Analysis
- [x] Regression model implementation
- [x] Classification model implementation
- [x] Clustering model implementation
- [x] Hyperparameter tuning results
- [x] Model comparison table
- [x] Business interpretation
- [x] Final conclusion and recommendation
