# Customer Segmentation with Actionable Business Insights

## Project Overview
This project presents an end-to-end Machine Learning solution designed to segment retail customers based on their annual income and spending behavior. By applying **K-Means Clustering**, **Ridge Regression**, and **Logistic Regression**, the project extracts meaningful customer profiles and translates model outcomes into strategic business strategies.

---

## Key Objectives
1. **Unsupervised Customer Segmentation:** Group customers using K-Means clustering after evaluating optimal $k$ via Elbow Curve and Silhouette Analysis.
2. **Predictive Spending Modeling:** Predict continuous spending scores using Ridge Regression with hyperparameter tuning.
3. **Purchase Likelihood Classification:** Forecast high-spending behavior using Logistic Regression optimized via GridSearchCV.
4. **Actionable Business Insights:** Provide targeted marketing and retention strategies for each customer persona.

---

## Dataset Description
The analysis utilizes the **Mall Customer Segmentation Dataset** (`Mall_Customers.csv`), consisting of 200 customer records with the following parameters:

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| `CustomerID` | Numerical | Unique identifier for each customer |
| `Gender` | Categorical | Customer gender (Male / Female) |
| `Age` | Numerical | Customer age in years |
| `AnnualIncome` | Numerical | Annual income of customer (in $k$) |
| `SpendingScore` | Numerical | Score assigned by mall based on behavior (1-100) |

---

## Machine Learning Pipeline & Methodology

```text
Mall_Customers.csv ➔ Data Preprocessing & Scaling (StandardScaler)
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
  K-Means Clustering   Ridge Regression  Logistic Regression
 (Customer Segments) (Predict Spending) (High-Spender Alert)
         │                │                │
         └────────────────┼────────────────┘
                          ▼
             Actionable Business Insights