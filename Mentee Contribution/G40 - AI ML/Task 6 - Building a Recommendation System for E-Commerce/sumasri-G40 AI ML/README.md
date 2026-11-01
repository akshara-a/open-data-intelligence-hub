# Building a Recommendation System for E-Commerce

## Task 6

### Objective
This project implements multiple machine learning algorithms for an e-commerce recommendation system. The objective is to predict customer ratings, predict purchase likelihood, segment customers, and compare model performance.

---

## Dataset

Dataset Used: E-commerce Customer Behavior Dataset

Features include:

- Customer ID
- Gender
- Age
- City
- Membership Type
- Total Spend
- Items Purchased
- Average Rating
- Discount Applied
- Days Since Last Purchase
- Satisfaction Level

---

## Machine Learning Models

### 1. Regression
- Ridge Regression
- Metrics:
  - MAE
  - MSE
  - RMSE
  - R² Score

### 2. Classification
- Logistic Regression
- Metrics:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC-AUC

### 3. Clustering
- K-Means Clustering
- Evaluation:
  - Elbow Method
  - Silhouette Score

### 4. Hyperparameter Tuning
- GridSearchCV
- Ridge Regression
- Logistic Regression
- K-Means Optimization

---

## Project Structure

- Ecommerce_Recommendation_System.ipynb
- README.md
- model_comparison.md
- requirements.txt
- ecommerce_data.csv

---

## Business Outcome

- Predict customer ratings.
- Predict purchase likelihood.
- Segment customers.
- Improve recommendation quality.
- Support personalized marketing strategies.
# Model Comparison

| Model | ML Task | Evaluation Metrics | Business Value |
|--------|----------|--------------------|----------------|
| Ridge Regression | Rating Prediction | MAE, RMSE, R² | Predict customer ratings |
| Logistic Regression | Purchase Prediction | Accuracy, Precision, Recall, F1, ROC-AUC | Predict purchase likelihood |
| K-Means Clustering | Customer Segmentation | Inertia, Silhouette Score | Customer segmentation |

## Summary

- Ridge Regression predicts customer ratings.
- Logistic Regression predicts purchase likelihood.
- K-Means groups customers into meaningful segments.
- Hyperparameter tuning improves model performance.