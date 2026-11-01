# Reusable Customer Churn Prediction Pipeline using scikit-learn

## Overview

This project implements a **production-ready Customer Churn Prediction Pipeline** using **scikit-learn**. The pipeline automates data preprocessing, model training, evaluation, and prediction in a reusable workflow.

The solution is designed to prevent data leakage by integrating all preprocessing steps inside a single sklearn `Pipeline`. The trained pipeline is saved using `joblib` and can be reused to predict churn for new customer data without manually repeating preprocessing steps.

---

## Project Objectives

* Build a reusable machine learning pipeline.
* Predict customer churn using historical customer data.
* Handle numerical and categorical features separately.
* Prevent data leakage using sklearn Pipeline.
* Save and reload the trained pipeline.
* Demonstrate prediction on unseen customer data.

---

## Technologies Used

* Python 3
* pandas
* scikit-learn
* joblib

---

## Machine Learning Workflow

```text
Customer Dataset
        │
        ▼
Data Validation
        │
        ▼
Feature & Target Separation
        │
        ▼
Train-Test Split
        │
        ▼
Numerical Pipeline
        │
        ├── Median Imputation
        └── StandardScaler
        │
        ▼
Categorical Pipeline
        │
        ├── Most Frequent Imputation
        └── OneHotEncoder
        │
        ▼
ColumnTransformer
        │
        ▼
Machine Learning Pipeline
        │
        ▼
Logistic Regression
        │
        ▼
Model Evaluation
        │
        ▼
Save Pipeline (.pkl)
        │
        ▼
Load Pipeline
        │
        ▼
Predict New Customer
```

---

## Project Structure

```text
Mini_Project_2/
│
├── Customer_Churn_Pipeline.ipynb
├── Customer_Churn_Dataset_GKeerthana.csv
├── customer_churn_pipeline.pkl
├── Decision_Log.docx
├── Project_Report.docx
└── README.md
```

---

## Features

* Automatic data validation
* Missing value handling
* Numerical feature scaling
* Categorical feature encoding
* Logistic Regression classification
* Model evaluation
* Pipeline saving and loading
* Prediction for new customer data
* Reusable production-ready workflow

---

## Libraries Required

Install the required packages before running the project.

```bash
pip install pandas scikit-learn joblib
```

---

## How to Run

1. Open the notebook (`Customer_Churn_Pipeline.ipynb`) or Python script.
2. Place the dataset (`Customer_Churn_Dataset_GKeerthana.csv`) in the project folder.
3. Run all notebook cells in sequence.
4. Train the machine learning pipeline.
5. Evaluate the model.
6. Save the trained pipeline.
7. Load the saved pipeline.
8. Predict churn for new customer data.

---

## Output

The project produces:

* Trained Machine Learning Pipeline
* Accuracy Score
* Confusion Matrix
* Classification Report
* Saved Pipeline (`customer_churn_pipeline.pkl`)
* Prediction for New Customer Data

---

## Business Benefits

The developed solution helps businesses identify customers who are likely to churn before they discontinue the service. Organizations can use these predictions to:

* Improve customer retention.
* Offer personalized discounts.
* Enhance customer support.
* Reduce customer churn.
* Increase long-term business revenue.

---

## Learning Outcomes

This project demonstrates:

* Building reusable sklearn Pipelines.
* Using ColumnTransformer for feature preprocessing.
* Handling numerical and categorical data.
* Preventing data leakage.
* Training classification models.
* Evaluating machine learning performance.
* Saving and reusing trained pipelines.
* Applying machine learning to solve real-world business problems.

---

## Author

**Gundreddy Keerthana Reddy**

Mini Project 2 – Production-Ready Customer Churn Prediction Pipeline using scikit-learn
