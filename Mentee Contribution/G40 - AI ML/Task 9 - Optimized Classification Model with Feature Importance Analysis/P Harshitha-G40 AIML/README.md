# Predicting E-Commerce Purchase Likelihood Using an Optimized Classification Model

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 1. Executive Summary

In e-commerce operations, converting website visitors into paying buyers is paramount. This project implements an **end-to-end Machine Learning Classification Pipeline** to predict whether a customer will complete a purchase based on browsing behavior, historical interactions, engagement depth, and demographic profiles.

Using an **Optimized Random Forest Classification Pipeline**, we achieved an **Accuracy of 88.67%**, **Precision of 82.35%**, **Recall of 79.55%**, **F1-Score of 0.8092**, and an **ROC-AUC score of 0.9493** on unseen testing data.

---

## 2. Final Project Question Answered

> **Which classification model should the e-commerce company use to identify customers who are likely to purchase, how much did hyperparameter optimization improve its performance, which features influenced the predictions, and how can the company use these findings to improve conversion rates?**

### Empirical Answer:
1. **Selected Model**: The company should deploy the **Optimized Random Forest Classifier** (`n_estimators=300`, `class_weight='balanced'`).
2. **Performance Gain**: Hyperparameter tuning via 5-Fold `GridSearchCV` improved the baseline Random Forest F1-Score from **0.7907 to 0.8092** (+1.85%), Recall from **0.7727 to 0.7955** (+2.28%), Precision from **0.8095 to 0.8235** (+1.40%), and ROC-AUC from **0.9419 to 0.9493** (+0.74%).
3. **Top Influential Features**:
   - `CartItems` (**34.09%** importance): Number of items in cart is the dominant intent signal.
   - `TimeOnSite` (**16.34%** importance): Active browsing duration.
   - `PreviousPurchases` (**10.62%** importance): Repeat buyer behavior.
   - `PagesViewed` (**9.12%** importance): Product discovery depth.
   - `DaysSinceLastVisit` (**6.18%** importance): Recency / churn risk indicator.
4. **Strategic Actions to Improve Conversion**:
   - Deploy exit-intent popups and automated cart recovery drip emails for cart items >= 1.
   - Segment customers into Low (<0.30), Medium (0.30–0.59), and High (>=0.60) likelihood tiers to eliminate ad spend waste on low-intent visitors.
   - Lower decision threshold to **0.40** during holiday campaigns to increase buyer recall to **97.73%**.

---

## 3. Project Structure

```text
Task-9-Purchase-Prediction/
│
├── data/
│   └── ecommerce_customer_data.csv        # Synthetic customer dataset (1,500 records)
│
├── notebooks/
│   ├── Purchase_Prediction.ipynb         # Interactive master Jupyter Notebook
│   └── purchase_prediction_analysis.ipynb # Alternative executable notebook
│
├── src/
│   ├── generate_dataset.py               # Reproducible data generator
│   ├── data_preprocessing.py             # Pipeline & ColumnTransformer definition
│   ├── exploratory_analysis.py           # EDA plotting routines
│   ├── model_training.py                 # Baseline model builders
│   ├── model_evaluation.py               # Metrics, ROC, CM & Threshold analysis
│   ├── hyperparameter_tuning.py          # 5-Fold GridSearchCV optimization
│   ├── feature_importance.py             # Feature importance extraction & actions
│   ├── create_notebook.py                # Notebook builder script
│   ├── generate_pdf_reports.py           # PDF report generator
│   ├── generate_presentation.py          # PowerPoint presentation builder
│   
│
├── models/
│   └── purchase_prediction_model.pkl     # Final serialized Scikit-Learn pipeline
│
├── reports/
│   ├── figures/                          # Saved EDA, CM, ROC, and sensitivity plots
│   ├── feature_importance_report.md      # Feature importance analysis deliverable
│   ├── feature_importance_report.pdf     # PDF Feature report
│   ├── business_recommendations.md       # Strategic business recommendations deliverable
│   └── business_recommendations.pdf      # PDF Business recommendations
│
├── presentation/
│   └── mini_project_5_presentation.pptx # 10-slide PowerPoint presentation
│__app.py
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
```

---

## 4. Model Comparison Table (Deliverable 2)

| Model | Optimization Status | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | Baseline | 0.8633 | 0.7816 | 0.7727 | 0.7771 | 0.9255 |
| Decision Tree | Baseline | 0.8267 | 0.7093 | 0.6932 | 0.7011 | 0.7885 |
| Random Forest | Baseline | 0.8767 | 0.8095 | 0.7727 | 0.7907 | 0.9419 |
| Gradient Boosting | Baseline | 0.8900 | 0.8276 | 0.8182 | 0.8229 | 0.9472 |
| Decision Tree | Optimized | 0.8633 | 0.7609 | 0.7955 | 0.7778 | 0.9168 |
| **Selected Model (Random Forest)** | **Optimized** | **0.8867** | **0.8235** | **0.7955** | **0.8092** | **0.9493** |

---

## 5. Hyperparameter Optimization Summary (Deliverable 3)

- **Model Optimized**: Scikit-Learn `RandomForestClassifier` Pipeline
- **Search Method Used**: 5-Fold `GridSearchCV`
- **Optimization Metric**: F1-Score (to balance precision and recall)
- **Best Parameter Combination**:
  - `n_estimators`: `300`
  - `max_depth`: `None`
  - `min_samples_split`: `2`
  - `min_samples_leaf`: `1`
  - `class_weight`: `'balanced'`
- **Cross-Validation Score (F1)**: **0.8143**
- **Test-Set Score (F1)**: **0.8092** (ROC-AUC: **0.9493**)

---

## 6. How to Run the Project

### Environment Setup
```bash
# 1. Install required dependencies
py -3 -m pip install -r requirements.txt

# 2. Execute end-to-end ML pipeline
py -3 app.py

# 3. Generate PDF reports and Presentation slides
py -3 src/generate_pdf_reports.py
py -3 src/generate_presentation.py
```

---

## 7. License

Distributed under the MIT License. See `LICENSE` for more information.
