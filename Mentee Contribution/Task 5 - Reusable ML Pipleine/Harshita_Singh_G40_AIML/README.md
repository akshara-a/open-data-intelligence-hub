README
Mini Project 2 - Reusable Customer Churn Prediction Pipeline


Project Overview

This project builds a reusable machine learning pipeline using scikit-learn to predict customer churn for a subscription based business. The pipeline covers the full workflow from raw data to saved predictions without any manual preprocessing outside the pipeline.


Dataset

Name: Telco Customer Churn
Source: Kaggle (blastchar/telco-customer-churn)
Records: 7043 customers
Columns: 21 features
Target: Churn (Yes or No)


Files in This Project

1. customer_churn_pipeline.ipynb - Main notebook with the full pipeline
2. decision_log.md - All technical decisions with reasons
3. model_evaluation_report.md - Accuracy, confusion matrix, classification report
4. README.md - This file


How to Run

1. Open Kaggle and go to the dataset page: kaggle.com/datasets/blastchar/telco-customer-churn
2. Click New Notebook
3. The dataset will be available at: /kaggle/input/telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv
4. Run all cells in order


Pipeline Steps

1. Load dataset from Kaggle input folder
2. Fix TotalCharges column (stored as string in source data)
3. Feature engineering (AvgMonthlySpend, IsNewCustomer, NumServices, NoProtection, ChargesTier)
4. Separate features and target
5. Train test split 80/20 with stratification
6. Numerical pipeline: median imputation then StandardScaler
7. Categorical pipeline: mode imputation then OneHotEncoder
8. Combine with ColumnTransformer
9. Train RandomForestClassifier through the pipeline
10. Evaluate with accuracy, confusion matrix, classification report
11. Save pipeline with joblib
12. Load pipeline and predict for a new customer


Results

Accuracy: 77 percent
This is consistent with Random Forest benchmarks on the Telco churn dataset.
The class imbalance (73 percent No, 27 percent Churn) is handled using class_weight=balanced.


Business Value

1. Customers predicted to churn can be offered discounts or retention plans
2. The saved pipeline can score new customers every month without retraining
3. Feature importance from Random Forest shows which factors drive churn most
4. Contract type and tenure are the strongest predictors in this dataset
