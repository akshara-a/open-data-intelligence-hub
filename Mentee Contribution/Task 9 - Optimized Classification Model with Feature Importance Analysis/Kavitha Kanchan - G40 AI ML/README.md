# 🛒 E-Commerce Purchase Likelihood Prediction

An optimized machine learning classification model to predict whether an e-commerce customer will complete a purchase based on browsing behavior and engagement metrics.

## 📌 Project Overview
- **Goal:** Predict customer purchase intent to optimize marketing spend and improve conversion rates.
- **Algorithms Used:** Logistic Regression, Decision Tree, Random Forest (Tuned with GridSearchCV).
- **Key Metrics:** Precision, Recall, F1-Score, ROC-AUC.

## 🛠️ Tech Stack
- Python 3.x
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-Learn

## 📊 Key Findings
- **Top Feature:** `TimeOnSite` and `Age` are the most critical features determining conversion.
- **Optimal Threshold:** Lowering classification threshold to `0.40` significantly improves **Recall** to capture potential buyers.