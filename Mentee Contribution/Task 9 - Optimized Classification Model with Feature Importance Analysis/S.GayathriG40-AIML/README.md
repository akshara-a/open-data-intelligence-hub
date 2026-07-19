# Optimized Classification Model with Feature Importance Analysis

## Project Title

**Predicting E-Commerce Purchase Likelihood Using an Optimized Classification Model**

---

## Project Overview

This project aims to predict whether an e-commerce customer will complete a purchase based on their browsing behavior and session information.

Different machine learning classification models are trained, evaluated, and compared. The best-performing model is optimized using hyperparameter tuning, and feature importance analysis is performed to identify the factors that most influence purchase decisions.

---

## Business Problem

Many customers visit e-commerce websites but do not complete a purchase.

This project helps identify customers who are most likely to purchase, allowing businesses to:

* Improve conversion rates
* Personalize marketing campaigns
* Reduce unnecessary advertising costs
* Target potential buyers effectively

---

## Dataset

**Dataset:** Online Shoppers Purchasing Intention Dataset

The dataset contains customer browsing sessions with features such as:

* Administrative
* Informational
* ProductRelated
* ProductRelated_Duration
* BounceRates
* ExitRates
* PageValues
* SpecialDay
* Month
* OperatingSystems
* Browser
* Region
* TrafficType
* VisitorType
* Weekend
* Revenue (Target Variable)

Target Variable:

* **0** → Customer did not purchase
* **1** → Customer completed a purchase

---

## Technologies Used

* Python
* Jupyter Notebook
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Joblib

---

## Project Workflow

1. Data Loading
2. Data Understanding
3. Data Cleaning
4. Exploratory Data Analysis (EDA)
5. Data Preprocessing
6. Train-Test Split
7. Baseline Model Training
8. Model Evaluation
9. Hyperparameter Optimization
10. Feature Importance Analysis
11. Threshold Analysis
12. Business Recommendations

---

## Machine Learning Models

The following classification models were implemented:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier

The Random Forest model was further optimized using **GridSearchCV**.

---

## Evaluation Metrics

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC
* Confusion Matrix

---

## Feature Importance

Feature importance analysis was performed using the optimized Random Forest model.

The most influential features help explain customer purchasing behavior and support better business decisions.

---

## Business Recommendations

Based on the model results:

* Target customers with a high purchase probability.
* Send personalized product recommendations.
* Offer discounts to interested customers.
* Improve customer engagement on product pages.
* Use remarketing campaigns for potential buyers.

---

## Project Files

```
Task 9/
│── purchase_prediction_analysis.ipynb
│── purchase_prediction_model.pkl
│── feature_importance.csv
│── customer_purchase_predictions.csv
│── README.md
```

---

## Future Improvements

* Implement XGBoost for comparison.
* Apply SMOTE for handling class imbalance.
* Use SHAP values for better model interpretability.
* Deploy the model using Streamlit or Flask.

---

## Conclusion

This project successfully predicts customer purchase likelihood using machine learning classification models.

After comparing multiple models, the optimized Random Forest model achieved the best overall performance. Feature importance analysis provided valuable insights into customer behavior, helping businesses improve marketing strategies and increase conversion rates.
