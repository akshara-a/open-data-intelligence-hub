# Mini Project 2: Production-Ready ML Pipeline with documented decisions.

## 1. Project Overview
This project implements a reproducible, end-to-end Machine Learning pipeline to predict customer churn using the Telco Customer Churn dataset.

## 2. Engineering Decisions & Architecture
* **Data Leakage Prevention:** Built using `scikit-learn.pipeline.Pipeline` and `ColumnTransformer`. Preprocessing steps (scaling and imputation) are chained directly with the estimator, ensuring no test data statistics leak into the training process.
* **Handling Missing Values:** Missing numerical values (specifically in `TotalCharges`) are handled using `SimpleImputer` with a `median` strategy to avoid outlier distortion. Categorical missing values use the `most_frequent` (mode) strategy.
* **Feature Encoding & Scaling:** Categorical variables are transformed via `OneHotEncoder(handle_unknown='ignore')` to safely manage unseen categories in production. Continuous numerical features are standardized using `StandardScaler`.
* **Class Imbalance Management:** Since customer churn datasets are inherently imbalanced, a `RandomForestClassifier` with the parameter `class_weight='balanced'` was selected to penalize misclassifications of the minority (churned) class.

## 3. Evaluation Strategy
Instead of relying on basic accuracy, the model is evaluated using **Precision, Recall, F1-Score**, and **ROC-AUC** to ensure it effectively identifies actual churning customers without generating excessive false positives.