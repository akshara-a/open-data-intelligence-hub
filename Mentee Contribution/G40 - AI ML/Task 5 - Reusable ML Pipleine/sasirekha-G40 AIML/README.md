# Reusable Customer Churn Prediction Pipeline

## Student Name

Sasi Rekha

---

## Project Overview

This project builds a reusable Machine Learning Pipeline using scikit-learn to predict customer churn based on customer behavior.

The pipeline automatically:

- Loads customer data
- Handles missing values
- Encodes categorical variables
- Scales numerical features
- Trains a Random Forest Classifier
- Predicts customer churn
- Saves the trained pipeline for future use

---

## Dataset

Dataset Name:

E-Commerce Customer Churn Dataset

Rows:

5630

Columns:

20

Target Column:

Churn

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Joblib

---

## Machine Learning Workflow

Dataset
↓
Train-Test Split
↓
Missing Value Imputation
↓
Feature Scaling
↓
One-Hot Encoding
↓
Random Forest Classifier
↓
Model Evaluation
↓
Save Pipeline
↓
Predict New Customers

---

## Model

RandomForestClassifier

---

## Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

## Output

Saved reusable pipeline:

models/customer_churn_pipeline.pkl

---

## Conclusion

The reusable pipeline can preprocess new customer data automatically and predict whether a customer is likely to churn without requiring manual preprocessing.