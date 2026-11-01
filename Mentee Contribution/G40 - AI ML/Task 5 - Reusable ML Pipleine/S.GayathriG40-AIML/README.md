# Customer Churn Prediction Pipeline


## Project Overview

This project builds a reusable machine learning pipeline to predict customer churn using Scikit-learn.

The pipeline automatically handles preprocessing, model training, evaluation, and prediction.


## Objective

The objective is to identify customers who are likely to leave a subscription service.

This helps businesses take preventive actions to reduce customer loss.


## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Jupyter Notebook


## Machine Learning Model

RandomForestClassifier


## Pipeline Workflow


Customer Churn Dataset

↓

Data Cleaning

↓

Train-Test Split

↓

Missing Value Handling

↓

Numerical Feature Scaling

↓

Categorical Feature Encoding

↓

Random Forest Training

↓

Model Evaluation

↓

Save Pipeline

↓

New Customer Prediction



## Features Used

Numerical Features:

- SeniorCitizen
- Tenure
- MonthlyCharges
- TotalCharges


Categorical Features:

- Gender
- Contract
- PaymentMethod
- InternetService
- OnlineSecurity
- TechSupport
- Streaming Services
- Other customer service features


## Output Files
