# Building a Recommendation System for E-Commerce

## Project Overview

This project implements multiple machine learning algorithms to build an e-commerce recommendation system that predicts customer ratings, purchase likelihood, and segments customers for personalized recommendations and targeted marketing.

Instead of relying on a single algorithm, three complementary approaches are used together:

- **Regression** — predict how much rating a user may give a product
- **Classification** — predict whether a user is likely to purchase a product
- **Clustering** — group similar customers based on behavior

## Dataset

`Ecommerce.csv` contains customer, product, rating, and purchase-related information:

| Column | Description |
|---|---|
| User_ID | Unique ID of the customer |
| Product_ID | Unique ID of the product |
| Product_Category | Category of the product |
| Rating | Rating given by the user (1–5) |
| Price | Price of the product |
| Purchase_Status | Whether the user purchased the product (1) or not (0) |
| Number_of_Views | How many times the user viewed the product |
| Cart_Status | Whether the user added the product to cart |
| Time_Spent | Time spent by the user on the product page (minutes) |
| Previous_Purchases | Number of previous purchases by the user |

A production dataset was not supplied for this task, so a synthetic dataset (6,000 rows) was generated with realistic, correlated behavior (more cart activity and time-on-page increase the odds of a higher rating and a purchase), so the models have genuine signal to learn from rather than pure noise.

## Approach

### 1. Regression — Ridge Regression
- **Target:** `Rating`
- **Why Ridge:** its L2 penalty controls overfitting better than plain Linear Regression once one-hot encoded category features are added
- **Tuning:** `GridSearchCV` over `alpha ∈ {0.01, 0.1, 1, 10, 100}`
- **Metrics:** MAE, RMSE, R²

### 2. Classification — Logistic Regression
- **Target:** `Purchase_Status`
- **Tuning:** `GridSearchCV` over `C`, `solver`, `max_iter`
- **Metrics:** Accuracy, Precision, Recall, F1 Score, Confusion Matrix

### 3. Clustering — K-Means
- **Input:** customer-level aggregated behavior (views, purchases, avg rating, avg time spent, total spend, cart adds)
- **Choosing k:** Elbow Method + Silhouette Score across `k = 2..6`
- **Metrics:** Inertia, Silhouette Score

## Results Summary

| ML Task | Algorithm | Target / Goal | Metrics Used | Business Use |
|---|---|---|---|---|
| Regression | Ridge Regression | Predict product rating | MAE, RMSE, R² | Recommend highly rated products |
| Classification | Logistic Regression | Predict purchase likelihood | Accuracy, Precision, Recall, F1 | Target likely buyers |
| Clustering | K-Means | Segment customers | Inertia, Silhouette Score | Create customer groups |

Full numeric results, charts, and business interpretation are in `Multi-Algorithm_Recommendation_System_Comparison_Report.docx` and reproduced step-by-step in `multi_algo_recommendation.ipynb`.

## Tools & Libraries

- Python
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn (models, `GridSearchCV`, evaluation metrics)

## Files in this Submission

| File | Description |
|---|---|
| `Ecommerce.csv` | Dataset used for all three models |
| `multi_algo_recommendation.ipynb` | Full, executed notebook: preprocessing → regression → classification → clustering → tuning → comparison |
| `Multi-Algorithm_Recommendation_System_Comparison_Report.docx` | Final written report with business interpretation and conclusion |
| `README.md` | This file |

## How to Run

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
jupyter notebook multi_algo_recommendation.ipynb
```

## Key Takeaways

- No single ML technique is sufficient for a complete recommendation system — regression, classification, and clustering each answer a different business question.
- Clustering gave the clearest, most directly actionable segmentation (high-value vs. low-engagement customers).
- Classification is best used for a small, high-confidence list of likely buyers rather than broad targeting.
- Regression works best as one supporting signal inside a broader recommendation ranking rather than a standalone predictor.
