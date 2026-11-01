README.md

\# Customer Churn Prediction using Reusable ML Pipeline



**# Project Objective**

Build a reusable machine learning pipeline using scikit-learn to predict customer churn for a subscription-based telecom company.



**# Dataset:**



Source:= Kaggle data set (Telco Customer Churn)

Records:= 7,043 customers

Target:=Churn (1 = Churned, 0 = Stayed).



**# Technology Stack:**



* &#x20;Python 3.x
* &#x20;pandas, numPy (Data manipulation)
* &#x20;matplotlib, seaborn (Visualization)
* &#x20;scikit-learn (Pipeline, RandomForest, Preprocessing)
* &#x20;joblib (Model saving)
* 

**# Pipeline Architecture:**



Raw Data → Train-Test Split (80:20) → Preprocessing (Imputer + Scaler + OneHotEncoder) → 

&#x20;RandomForestClassifier → Evaluation → Saved Model (.pkl)





