# E-Commerce Purchase Prediction

## Mini Project 5

---

## Project Overview

This project develops a machine learning model to predict whether a customer will purchase a product based on browsing behavior, customer interactions, and product-related attributes. The objective is to help businesses identify potential buyers, improve marketing strategies, optimize customer engagement, and increase overall conversion rates.

The project includes complete data preprocessing, exploratory data analysis (EDA), feature engineering, model training, hyperparameter tuning, evaluation, feature importance analysis, and business recommendations.

---

## Key Results

| Metric | Value |
|---------|-------|
| Best Model | Random Forest (Optimized) |
| Accuracy | **99.72%** |
| Precision | **100.00%** |
| Recall | **98.75%** |
| F1-Score | **99.37%** |
| ROC-AUC Score | **99.55%** |

---

# Dataset

## Dataset Statistics

| Metric | Value |
|---------|-------|
| Total Records | 25,000 Customer Sessions |
| Total Features | 29 |
| Numerical Features | 13 |
| Categorical Features | 16 |
| Purchase Rate | 22.46% (5,616 Purchases) |
| Non-Purchase Rate | 77.54% (19,384 Non-Purchases) |
| Target Variable | purchased |

---

## Important Features

| Feature | Description |
|---------|-------------|
| customer_id | Unique customer identifier |
| session_id | Unique browsing session |
| device_type | Device used by customer |
| user_type | Registered or non-registered user |
| marketing_channel | Marketing source |
| product_category | Product category |
| unit_price | Product price |
| quantity | Quantity purchased |
| discount_percent | Discount percentage |
| pages_viewed | Number of pages viewed |
| time_on_site_sec | Time spent browsing |
| added_to_cart | Product added to cart |
| rating | Product rating |
| review_helpful_votes | Helpful review votes |
| purchased | Target variable |

---

# Project Structure

```
mini-project-5/
│
├── data/
│   └── ecommerce_customer_data.csv
│
├── notebooks/
│   └── purchase_prediction_analysis.ipynb
│
├── models/
│   └── purchase_prediction_model.pkl
│
├── reports/
│   ├── feature_importance_report.pdf
│   ├── business_recommendations.pdf
│   └── model_comparison_table.csv
│
├── presentation/
│   └── mini_project_5_presentation.pptx
│
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/mini-project-5.git
cd mini-project-5
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Required Libraries

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- joblib
- scipy

---

# Workflow

The project follows these major steps:

1. Load the dataset.
2. Perform data cleaning and preprocessing.
3. Conduct Exploratory Data Analysis (EDA).
4. Encode categorical variables.
5. Split the dataset into training and testing sets.
6. Build machine learning pipelines.
7. Train multiple classification models.
8. Perform hyperparameter tuning using RandomizedSearchCV.
9. Evaluate models using classification metrics.
10. Compare model performance.
11. Analyze feature importance.
12. Generate business recommendations.

---

# Models Implemented

- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- Optimized Random Forest using RandomizedSearchCV

---

# Model Evaluation Metrics

The following metrics were used to evaluate the classification models:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC Score
- Confusion Matrix
- Classification Report

---

# Best Model Performance

| Metric | Score |
|---------|-------|
| Accuracy | 99.72% |
| Precision | 100.00% |
| Recall | 98.75% |
| F1-Score | 99.37% |
| ROC-AUC | 99.55% |

The Optimized Random Forest model achieved the highest performance among all evaluated models.

---

# Feature Importance

The top five most influential features identified by the Random Forest model are:

1. Review Helpful Votes
2. Product Rating
3. Unit Price
4. Time on Site
5. Location

These features contribute the most toward predicting customer purchasing behavior.

---

# Business Recommendations

Based on the analysis, the following recommendations are suggested:

- Improve the customer review collection system.
- Display helpful reviews prominently.
- Focus on maintaining high product ratings.
- Personalize marketing campaigns based on customer behavior.
- Optimize discount strategies for price-sensitive customers.
- Increase customer engagement through better website navigation.
- Encourage user registration and loyalty programs.

---

# Files Included

| File | Description |
|------|-------------|
| purchase_prediction_analysis.ipynb | Complete project implementation |
| purchase_prediction_model.pkl | Saved trained model |
| feature_importance_report.pdf | Feature importance analysis |
| business_recommendations.pdf | Business recommendation report |
| model_comparison_table.csv | Comparison of all classification models |
| mini_project_5_presentation.pptx | Project presentation |
| README.md | Project documentation |

---

# Future Improvements

- Deploy the model using Flask or Streamlit.
- Integrate real-time customer prediction.
- Implement recommendation systems.
- Add customer lifetime value prediction.
- Develop churn prediction models.
- Build a complete customer analytics dashboard.

---

# Conclusion

This project demonstrates how machine learning can accurately predict customer purchasing behavior using historical browsing and transaction data. The Optimized Random Forest model achieved an accuracy of **99.72%**, making it suitable for business applications such as personalized marketing, customer segmentation, and conversion optimization.

The feature importance analysis revealed that customer reviews and product ratings are the strongest predictors of purchase decisions, highlighting the importance of customer trust and engagement in e-commerce platforms.

---

# Author

**Mini Project 5 – E-Commerce Purchase Prediction**

Machine Learning Classification Project
