# Customer Churn Prediction using Machine Learning Pipeline

## Project Overview

This project predicts whether a telecom customer is likely to churn (leave the service) using a **Random Forest Classifier**. A reusable Machine Learning Pipeline was developed using Scikit-learn to automate data preprocessing and model training.

The pipeline handles missing values, feature encoding, feature scaling, model training, prediction, and evaluation in a single workflow.

---

## Dataset

**Dataset Name:** Telco Customer Churn Dataset

* Total Records: **7043**
* Total Features: **21**
* Target Variable: **Churn**

---

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Google Colab

---

## Machine Learning Workflow

1. Import Required Libraries
2. Load Dataset
3. Data Cleaning
4. Handle Missing Values
5. Remove Unnecessary Columns
6. Split Features and Target
7. Train-Test Split
8. Create Numerical Pipeline
9. Create Categorical Pipeline
10. Combine Pipelines using ColumnTransformer
11. Train Random Forest Classifier
12. Make Predictions
13. Evaluate Model
14. Save Trained Model

---

## Data Preprocessing

The following preprocessing steps were performed:

* Removed **customerID** column.
* Converted **TotalCharges** to numeric format.
* Replaced blank values with **NaN**.
* Filled numerical missing values using **Median Imputer**.
* Filled categorical missing values using **Most Frequent Imputer**.
* Applied **One-Hot Encoding** to categorical features.
* Applied **Standard Scaling** to numerical features.
* Combined preprocessing using **ColumnTransformer**.

---

## Machine Learning Model

**Algorithm Used:** Random Forest Classifier

### Parameters

* Number of Trees (`n_estimators`) = 100
* Random State = 42

---

## Model Performance

| Metric   | Value      |
| -------- | ---------- |
| Accuracy | **77.79%** |

---

## Project Structure

```text
Mini_Project_2_Customer_Churn_Pipeline/
│
├── customer_churn_pipeline.ipynb
├── decision_log.md
├── model_evaluation_report.md
└── README.md
```

---

## Author

**Japneet Kaur**
