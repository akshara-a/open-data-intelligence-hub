# Mini Project 2: Production-Ready Customer Churn Prediction Pipeline using scikit-learn

## 1. Project Title

**Reusable Machine Learning Pipeline for Customer Churn Prediction**

---

## 2. Project Objective

The goal of this mini project is to build a **reusable machine learning pipeline** using `scikit-learn` to predict customer churn for a subscription business.

Students should not write one-time scattered code. Instead, they should build a structured ML pipeline that can be reused for:

* Training the model
* Testing the model
* Predicting churn for new customers
* Running the workflow again when new data is received

The final output should be a **clean, reusable, explainable, and production-ready ML pipeline**.

---

## 3. Business Problem

A subscription-based business wants to identify customers who are likely to stop using the service.

This is called **customer churn prediction**.

The business wants to answer:

> Which customers are likely to leave the service?

If the business can identify high-risk customers early, it can take action such as:

* Offering discounts
* Improving customer support
* Sending retention offers
* Providing personalized plans
* Reducing customer loss

---

## 4. Dataset Example

Students can use a customer churn dataset with columns like:

| Column Name     | Description                           |
| --------------- | ------------------------------------- |
| CustomerID      | Unique customer identifier            |
| Gender          | Customer gender                       |
| Age             | Customer age                          |
| Tenure          | Number of months the customer stayed  |
| MonthlyCharges  | Monthly subscription fee              |
| TotalCharges    | Total amount paid by customer         |
| ContractType    | Monthly, yearly, or two-year contract |
| PaymentMethod   | Payment mode used by customer         |
| InternetService | Type of internet service              |
| SupportTickets  | Number of support issues raised       |
| Churn           | Target column: Yes or No              |

The target column is:

```text
Churn
```

---

## 5. Main Requirement

This project must be implemented as a **reusable sklearn pipeline**.

The pipeline should combine:

```text
Missing value handling
        ↓
Feature scaling
        ↓
Categorical encoding
        ↓
Model training
        ↓
Prediction
```

Students should avoid manually preprocessing train and test data separately because that can cause mistakes and data leakage.

---

## 6. Expected Pipeline Flow

```text
Raw Customer Data
        ↓
Data Validation
        ↓
Feature and Target Separation
        ↓
Train-Test Split
        ↓
Numerical Preprocessing Pipeline
        ↓
Categorical Preprocessing Pipeline
        ↓
ColumnTransformer
        ↓
Final sklearn Pipeline
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Reusable Prediction on New Data
```

---

## 7. Tools and Libraries

| Tool / Library                                  | Purpose                                                 |
| ----------------------------------------------- | ------------------------------------------------------- |
| `pandas`                                        | Load and inspect dataset                                |
| `train_test_split`                              | Split data into train and test sets                     |
| `Pipeline`                                      | Connect preprocessing and model steps                   |
| `ColumnTransformer`                             | Apply different preprocessing to different column types |
| `SimpleImputer`                                 | Handle missing values                                   |
| `StandardScaler`                                | Scale numerical columns                                 |
| `OneHotEncoder`                                 | Convert categorical columns into numerical format       |
| `LogisticRegression` / `RandomForestClassifier` | Train churn prediction model                            |
| `classification_report`                         | Evaluate model performance                              |
| `joblib`                                        | Save and load reusable pipeline                         |

---

## 8. Step-by-Step Implementation

## Step 1: Import Required Libraries

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import joblib
```

---

## Step 2: Load the Dataset

```python
df = pd.read_csv("customer_churn.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())
```

### What students should check

* Are all required columns present?
* Are there missing values?
* Are there duplicate rows?
* Are numeric columns stored correctly?
* Is the target column available?
* Is the churn distribution balanced or imbalanced?

---

## Step 3: Remove Unnecessary Columns

`CustomerID` is only an identifier. It does not help the model learn churn behavior.

```python
df = df.drop("CustomerID", axis=1)
```

### Decision

| Column Removed | Reason                                       |
| -------------- | -------------------------------------------- |
| `CustomerID`   | Unique identifier, not useful for prediction |

---

## Step 4: Separate Features and Target

```python
X = df.drop("Churn", axis=1)
y = df["Churn"]
```

| Variable | Meaning        |
| -------- | -------------- |
| `X`      | Input features |
| `y`      | Target output  |

Example:

```text
X = Age, Tenure, MonthlyCharges, ContractType, PaymentMethod
y = Churn
```

---

## Step 5: Identify Numerical and Categorical Columns

```python
numeric_features = [
    "Age",
    "Tenure",
    "MonthlyCharges",
    "TotalCharges",
    "SupportTickets"
]

categorical_features = [
    "Gender",
    "ContractType",
    "PaymentMethod",
    "InternetService"
]
```

### Why this is important

Different column types need different preprocessing.

| Column Type         | Required Processing                 |
| ------------------- | ----------------------------------- |
| Numerical columns   | Missing value handling and scaling  |
| Categorical columns | Missing value handling and encoding |

---

## Step 6: Split the Dataset

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

### Explanation

| Parameter         | Meaning                                          |
| ----------------- | ------------------------------------------------ |
| `test_size=0.2`   | 20% data for testing, 80% for training           |
| `random_state=42` | Gives consistent results every time              |
| `stratify=y`      | Keeps churn ratio similar in train and test data |

`stratify=y` is useful because churn datasets are often imbalanced.

---

## Step 7: Create Numerical Preprocessing Pipeline

```python
numeric_pipeline = Pipeline(steps=[
    ("missing_value_handler", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
```

### Explanation

| Step                               | Purpose                                       |
| ---------------------------------- | --------------------------------------------- |
| `SimpleImputer(strategy="median")` | Fills missing numeric values using the median |
| `StandardScaler()`                 | Scales numerical values to a common scale     |

This pipeline will be applied only to numerical columns.

---

## Step 8: Create Categorical Preprocessing Pipeline

```python
categorical_pipeline = Pipeline(steps=[
    ("missing_value_handler", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])
```

### Explanation

| Step                                      | Purpose                                                      |
| ----------------------------------------- | ------------------------------------------------------------ |
| `SimpleImputer(strategy="most_frequent")` | Fills missing categorical values using the most common value |
| `OneHotEncoder(handle_unknown="ignore")`  | Converts text categories into numeric format                 |

`handle_unknown="ignore"` is important because future data may contain new categories not seen during training.

---

## Step 9: Combine Preprocessing using ColumnTransformer

```python
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])
```

### Explanation

`ColumnTransformer` applies the correct preprocessing to the correct columns.

| Transformer | Applied To          |
| ----------- | ------------------- |
| `num`       | Numerical columns   |
| `cat`       | Categorical columns |

This keeps the pipeline reusable and clean.

---

## Step 10: Create the Final Reusable ML Pipeline

```python
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000))
])
```

### What this pipeline does

When the pipeline runs, it automatically:

```text
1. Fills missing numeric values
2. Scales numeric columns
3. Fills missing categorical values
4. Encodes categorical columns
5. Trains the machine learning model
```

This is the most important part of the project.

The final output should not be only a model. It should be a **complete reusable ML pipeline**.

---

## Step 11: Train the Pipeline

```python
model_pipeline.fit(X_train, y_train)
```

### Explanation

This single line runs the full workflow.

It trains the preprocessing steps and the model together.

The pipeline learns only from the training data, which helps avoid data leakage.

---

## Step 12: Make Predictions

```python
y_pred = model_pipeline.predict(X_test)
```

### Explanation

The same pipeline is reused for prediction.

Before predicting, it automatically applies the same preprocessing steps to the test data.

Students do not need to manually clean, encode, or scale the test data.

---

## Step 13: Evaluate the Model

```python
print("Accuracy:", accuracy_score(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report(y_test, y_pred))
```

### Important Metrics

| Metric           | Meaning                                                           |
| ---------------- | ----------------------------------------------------------------- |
| Accuracy         | Overall correct predictions                                       |
| Precision        | Out of predicted churn customers, how many actually churned       |
| Recall           | Out of actual churn customers, how many were correctly identified |
| F1-score         | Balance between precision and recall                              |
| Confusion Matrix | Shows correct and incorrect predictions                           |

For churn prediction, **recall is very important** because the business does not want to miss customers who are likely to leave.

---

## Step 14: Save the Reusable Pipeline

```python
joblib.dump(model_pipeline, "customer_churn_pipeline.pkl")
```

### Explanation

This saves the complete pipeline, including:

* Missing value handling
* Scaling
* Encoding
* Trained model

This makes the pipeline reusable in the future.

---

## Step 15: Load and Reuse the Pipeline

```python
loaded_pipeline = joblib.load("customer_churn_pipeline.pkl")
```

Now the saved pipeline can be reused for new customer data.

---

## Step 16: Predict for New Customer Data

```python
new_customer = pd.DataFrame({
    "Gender": ["Female"],
    "Age": [32],
    "Tenure": [5],
    "MonthlyCharges": [850],
    "TotalCharges": [4250],
    "ContractType": ["Monthly"],
    "PaymentMethod": ["Credit Card"],
    "InternetService": ["Fiber"],
    "SupportTickets": [3]
})

prediction = loaded_pipeline.predict(new_customer)

print("Churn Prediction:", prediction)
```

### Why this is reusable

The student does not need to manually preprocess the new customer data.

The saved pipeline automatically:

```text
Handles missing values
        ↓
Scales numerical values
        ↓
Encodes categorical values
        ↓
Predicts churn
```

---

## 9. Full Code Example

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import joblib


# 1. Load dataset
df = pd.read_csv("customer_churn.csv")


# 2. Remove unnecessary identifier column
df = df.drop("CustomerID", axis=1)


# 3. Separate features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]


# 4. Define numerical and categorical columns
numeric_features = [
    "Age",
    "Tenure",
    "MonthlyCharges",
    "TotalCharges",
    "SupportTickets"
]

categorical_features = [
    "Gender",
    "ContractType",
    "PaymentMethod",
    "InternetService"
]


# 5. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 6. Numerical preprocessing pipeline
numeric_pipeline = Pipeline(steps=[
    ("missing_value_handler", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# 7. Categorical preprocessing pipeline
categorical_pipeline = Pipeline(steps=[
    ("missing_value_handler", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


# 8. Combine preprocessing pipelines
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])


# 9. Final reusable ML pipeline
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000))
])


# 10. Train the reusable pipeline
model_pipeline.fit(X_train, y_train)


# 11. Predict on test data
y_pred = model_pipeline.predict(X_test)


# 12. Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report(y_test, y_pred))


# 13. Save the reusable pipeline
joblib.dump(model_pipeline, "customer_churn_pipeline.pkl")


# 14. Load the pipeline for future use
loaded_pipeline = joblib.load("customer_churn_pipeline.pkl")


# 15. Predict for a new customer
new_customer = pd.DataFrame({
    "Gender": ["Female"],
    "Age": [32],
    "Tenure": [5],
    "MonthlyCharges": [850],
    "TotalCharges": [4250],
    "ContractType": ["Monthly"],
    "PaymentMethod": ["Credit Card"],
    "InternetService": ["Fiber"],
    "SupportTickets": [3]
})

new_prediction = loaded_pipeline.predict(new_customer)

print("New Customer Churn Prediction:", new_prediction)
```

---

## 10. Decision Log Template

Students must submit a decision log.

| Decision Area              | Decision Taken                 | Reason                                                |
| -------------------------- | ------------------------------ | ----------------------------------------------------- |
| Removed column             | Removed `CustomerID`           | It is only an identifier and does not help prediction |
| Missing numeric values     | Used median imputation         | Median is less affected by outliers                   |
| Missing categorical values | Used most frequent value       | Keeps the most common category pattern                |
| Encoding                   | Used OneHotEncoder             | ML models need numerical input                        |
| Unknown categories         | Used `handle_unknown="ignore"` | Prevents errors when new categories appear            |
| Scaling                    | Used StandardScaler            | Brings numeric values to a common scale               |
| Model                      | Used Logistic Regression       | Simple, explainable baseline model                    |
| Split                      | Used 80:20 train-test split    | Common approach for model validation                  |
| Stratification             | Used `stratify=y`              | Keeps churn distribution balanced                     |
| Reusability                | Saved pipeline using joblib    | Allows future reuse without rewriting code            |

---

## 11. Expected Final Deliverables

| Deliverable                     | Description                                                   |
| ------------------------------- | ------------------------------------------------------------- |
| Python Notebook or Script       | Complete reusable sklearn pipeline code                       |
| Data Validation Summary         | Missing values, duplicates, column types, target distribution |
| Reusable ML Pipeline            | Pipeline combining preprocessing and model training           |
| Model Evaluation Report         | Accuracy, precision, recall, F1-score, confusion matrix       |
| Saved Pipeline File             | `.pkl` file saved using joblib                                |
| New Customer Prediction Example | Example showing pipeline reuse                                |
| Decision Log                    | Explanation of all technical decisions                        |
| Business Interpretation         | Explanation of how churn prediction helps the business        |

---

## 12. Mentor Evaluation Checklist

| Criteria                | Expected Standard                                        |
| ----------------------- | -------------------------------------------------------- |
| Reusable Pipeline       | Student uses sklearn `Pipeline` correctly                |
| ColumnTransformer Usage | Numerical and categorical columns are handled separately |
| Missing Value Handling  | Missing values are handled inside the pipeline           |
| Encoding                | Categorical columns are encoded inside the pipeline      |
| Scaling                 | Numerical columns are scaled inside the pipeline         |
| Model Training          | Model is trained through the pipeline                    |
| Data Leakage Prevention | Preprocessing is fitted only on training data            |
| Evaluation              | Student uses proper classification metrics               |
| Pipeline Saving         | Student saves the trained pipeline                       |
| Pipeline Reuse          | Student demonstrates prediction on new data              |
| Documentation           | Student explains all major decisions                     |
| Business Understanding  | Student connects prediction results to churn reduction   |

---

## 13. Important Notes for Students

* Do not manually preprocess `X_train` and `X_test` separately.
* Put preprocessing steps inside the sklearn pipeline.
* Use `ColumnTransformer` when the dataset has both numerical and categorical columns.
* Use `fit()` only on training data.
* Use `predict()` on test data and new data.
* Save the full pipeline, not just the model.
* Explain every major decision in the decision log.

---

## 14. Final Student Explanation

At the end of the project, students should be able to explain:

> I built a reusable customer churn prediction pipeline using scikit-learn. The pipeline handles missing values, scales numerical columns, encodes categorical columns, trains a Logistic Regression model, evaluates the model, and saves the complete workflow for future use. The same pipeline can be reused to predict churn for new customer data without manually repeating preprocessing steps.

---

## 15. Learning Outcome

After completing this mini project, students will understand how to move from basic ML code to a reusable ML engineering workflow.

They will learn how to:

* Build a reusable sklearn pipeline
* Handle numerical and categorical columns properly
* Avoid data leakage
* Train and evaluate a churn prediction model
* Save and reuse a trained pipeline
* Document technical decisions clearly
* Connect model output with business action
