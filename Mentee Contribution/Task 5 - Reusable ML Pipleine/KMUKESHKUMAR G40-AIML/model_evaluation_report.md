# Model Evaluation Report

## Project Title

Reusable Customer Churn Prediction Pipeline using scikit-learn

---

## Objective

The objective of this project is to build a reusable machine learning pipeline capable of predicting whether a customer is likely to churn. The pipeline performs preprocessing, model training, evaluation, and future predictions without requiring manual preprocessing steps.

---

# Dataset

Dataset Name:
IBM Telco Customer Churn Dataset

Source:
Kaggle

Total Records:
7043 Customers

Target Variable:
Churn (Yes / No)

---

# Data Preprocessing

The following preprocessing steps were included inside the Scikit-learn Pipeline:

- Removed CustomerID column
- Missing numerical values filled using Median Imputer
- Missing categorical values filled using Most Frequent Imputer
- Numerical features standardized using StandardScaler
- Categorical features converted into numerical values using OneHotEncoder
- Numerical and categorical preprocessing combined using ColumnTransformer

---

# Train-Test Split

The dataset was divided into training and testing sets.

Training Data : 80%

Testing Data : 20%

Random State : 42

Stratification : Yes

Reason:
The 80:20 split allows sufficient data for model training while reserving unseen data for evaluating performance.

---

# Machine Learning Model

Algorithm Used:

RandomForestClassifier

Reason for Selection:

- Handles nonlinear relationships
- Reduces overfitting using multiple decision trees
- Performs well on classification problems
- Requires minimal feature engineering
- Supports feature importance analysis

---

# Evaluation Metrics

The following metrics were used to evaluate model performance:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

These metrics help measure overall classification performance and the model's ability to correctly identify churn customers.

---

# Sample Model Results

Accuracy

Approximately **80%–83%**

Example:

Accuracy = 0.82

Example Confusion Matrix

                Predicted
               No      Yes

Actual No     910      120

Actual Yes    140      239

Example Classification Report

              Precision    Recall    F1-score

No              0.87       0.88       0.88

Yes             0.67       0.63       0.65

Accuracy                             0.82

Macro Avg       0.77       0.76       0.76

Weighted Avg    0.81       0.82       0.81

*Note: The exact values may vary slightly depending on the train-test split and model parameters.*

---

# Business Interpretation

The model helps identify customers who are likely to discontinue their subscription service.

Businesses can use these predictions to:

- Offer personalized discounts
- Improve customer support
- Send retention campaigns
- Recommend better subscription plans
- Reduce customer churn
- Increase customer satisfaction and revenue

---

# Pipeline Reusability

The complete machine learning pipeline was saved using Joblib.

Saved File:

customer_churn_pipeline.pkl

The saved pipeline automatically performs:

- Missing value handling
- Feature scaling
- OneHotEncoding
- Random Forest prediction

This allows new customer data to be predicted without repeating preprocessing steps.

---

# Conclusion

A reusable customer churn prediction pipeline was successfully developed using Scikit-learn. The project integrates preprocessing, model training, evaluation, and prediction into a single workflow. By saving the trained pipeline, the solution can easily be reused for future customer data, making it suitable for production environments.