# Task 6 - Recommendation System Decision Log and Evaluation Report

## 1. Project Overview
- Project: ML Algorithms for E-Commerce Recommendation System
- Dataset: Synthetic e-commerce dataset (2000 rows) matching required schema
- Models: Ridge Regression, Logistic Regression, K-Means Clustering

## 2. Part A - Regression (Rating Prediction)
- Model: Ridge Regression
- Best alpha (GridSearchCV): 10.0
- Test R2 Score: 0.435
- Test RMSE: 0.586
- Business Use: Predicts which products a user is likely to rate highly, feeding the recommendation section.

## 3. Part B - Classification (Purchase Prediction)
- Model: Logistic Regression
- Best Params (GridSearchCV): {'C': 0.1, 'max_iter': 1000, 'penalty': 'l2', 'solver': 'lbfgs'}
- Test Accuracy: 0.807
- Test F1-Score: 0.864
- Business Use: Flags users likely to purchase for targeted discounts, email campaigns, and cart recovery.

## 4. Part C - Clustering (Customer Segmentation)
- Model: K-Means
- Optimal K (via Silhouette Analysis): 2
- Silhouette Score: 0.214
- Business Use: Groups customers into segments (frequent buyers, discount-sensitive, high-value, browsers) for targeted marketing.

## 5. Hyperparameter Tuning Summary
| Model | Method | Result |
|---|---|---|
| Ridge Regression | GridSearchCV | alpha=10.0 |
| Logistic Regression | GridSearchCV | {'C': 0.1, 'max_iter': 1000, 'penalty': 'l2', 'solver': 'lbfgs'} |
| K-Means | Silhouette Search | k=2 |

## 6. Business Interpretation
- Regression identifies products worth recommending based on predicted satisfaction.
- Classification prioritizes which users to target with offers/campaigns to drive conversion.
- Clustering enables differentiated marketing strategy per customer type.
- Combined, these three models form the backbone of a personalized recommendation system.

## 7. Final Conclusion
The tuned Ridge Regression model explained a moderate share of rating variance (R2 above),
the tuned Logistic Regression model reliably distinguished buyers from non-buyers (F1 above),
and K-Means clustering revealed distinct, actionable customer segments (Silhouette score above).
Together, these models allow the business to recommend the right products, to the right users,
at the right time, while tailoring marketing strategy per customer segment.
