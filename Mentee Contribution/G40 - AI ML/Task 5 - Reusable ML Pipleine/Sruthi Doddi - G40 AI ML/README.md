# Reusable Customer Churn Prediction Pipeline using scikit-learn

## Project Overview

Customer churn prediction is an important business problem in subscription-based industries. Churn occurs when customers discontinue using a company's services.

This project develops a reusable machine learning pipeline using scikit-learn to predict whether a customer is likely to churn.

The entire workflow integrates data preprocessing, model training, evaluation, and prediction into a single reusable pipeline.

---

## Project Objective

The main objectives of this project are:

* Build an end-to-end machine learning pipeline.
* Handle missing values automatically.
* Encode categorical variables using OneHotEncoder.
* Scale numerical features.
* Train a Random Forest classification model.
* Evaluate model performance.
* Save and reuse the complete pipeline for future predictions.

---

## Dataset Description

The dataset contains customer-related information such as:

| Column Name     | Description                                             |
| --------------- | ------------------------------------------------------- |
| CustomerID      | Unique customer identifier                              |
| Gender          | Customer gender                                         |
| Age             | Customer age                                            |
| Tenure          | Number of months the customer stayed                    |
| MonthlyCharges  | Monthly subscription charges                            |
| TotalCharges    | Total amount paid by the customer                       |
| ContractType    | Type of subscription contract                           |
| PaymentMethod   | Payment method used                                     |
| InternetService | Type of internet service                                |
| SupportTickets  | Number of support issues raised                         |
| Churn           | Target variable indicating whether the customer churned |

---

## Technologies Used

* Python
* Pandas
* scikit-learn
* Joblib
* Jupyter Notebook

---

## Project Workflow

```text
Raw Data
   ↓
Data Exploration
   ↓
Train-Test Split
   ↓
Missing Value Handling
   ↓
Feature Scaling
   ↓
Categorical Encoding
   ↓
Random Forest Model Training
   ↓
Model Evaluation
   ↓
Save Pipeline
   ↓
Predict New Customer Churn
```

---

## Machine Learning Pipeline Components

### Numerical Pipeline

* Missing value imputation using median.
* Feature scaling using StandardScaler.

### Categorical Pipeline

* Missing value imputation using most frequent category.
* Encoding using OneHotEncoder.

### Model

* RandomForestClassifier

---

## Evaluation Metrics

The model was evaluated using:

* Accuracy Score
* Confusion Matrix
* Classification Report

---

## Reusability

The complete machine learning pipeline was saved using Joblib.

```python
joblib.dump(model_pipeline, "customer_churn_pipeline.pkl")
```

The saved pipeline can later be loaded and reused for predictions on new customer data.

---

## Project Structure

```text
Mini_Project_2_Customer_Churn_Pipeline/
│
├── customer_churn_pipeline.ipynb
├── customer_churn_pipeline.pkl
├── decision_log.md
├── model_evaluation_report.md
└── README.md
```

---

## Business Impact

The developed churn prediction system can help organizations:

* Reduce customer attrition.
* Improve customer retention.
* Increase revenue.
* Provide targeted retention strategies.
* Enhance customer satisfaction.

---

## Conclusion

A reusable customer churn prediction pipeline was successfully developed using scikit-learn. The pipeline automates preprocessing, model training, and prediction tasks, making it suitable for future deployment and real-world business applications.
