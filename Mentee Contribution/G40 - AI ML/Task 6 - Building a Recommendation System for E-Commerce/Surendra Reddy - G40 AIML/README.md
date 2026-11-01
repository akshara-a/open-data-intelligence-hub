# Task 6 - E-Commerce Recommendation System (Regression + Classification + Clustering)

## Overview
This project implements and compares three ML approaches to power an 
e-commerce recommendation system: Ridge Regression (rating prediction), 
Logistic Regression (purchase prediction), and K-Means Clustering 
(customer segmentation).

## Dataset
Synthetic e-commerce dataset (2000 rows) generated to match the required 
schema: User_ID, Product_ID, Category, Price, Rating, Browsing_Time, 
Previous_Purchases, Cart_Addition, Purchase_Status, Age, Gender, 
Location, Discount_Applied, Total_Spending.

## Results Summary

| Model | Task | Metric | Score |
|---|---|---|---|
| Ridge Regression | Rating Prediction | R² / RMSE | 0.435 / 0.586 |
| Logistic Regression | Purchase Prediction | Accuracy / F1 | 0.807 / 0.864 |
| K-Means Clustering | Customer Segmentation | Silhouette | 0.214 (k=4 used for business interpretability) |

## Hyperparameter Tuning
- Ridge alpha tuned via GridSearchCV → best alpha = 10.0
- Logistic Regression tuned via GridSearchCV → best C=0.1, solver=lbfgs
- K-Means k selected via Silhouette Analysis and Elbow Method

## Files
- `ecommerce_recommendation_system.ipynb` — full notebook
- `ecommerce_data.csv` — dataset
- `eda_charts.png` — exploratory analysis charts
- `elbow_method.png` — K-Means elbow curve
- `model_comparison.csv` — model comparison table
- `decision_log.md` — detailed decision log and business interpretation

## Business Value
- **Regression** → recommend products a user is likely to rate highly
- **Classification** → target likely buyers with discounts/campaigns
- **Clustering** → tailor marketing strategy per customer segment