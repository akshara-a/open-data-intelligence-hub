# Mini Project 2: Reusable ML Pipeline for Customer Churn Prediction

## Phase

**Phase 1: ML Engineering Fundamentals**

## Case Study

**Predicting Customer Churn for a Subscription Business**

---

## Project Title

**Reusable Customer Churn Prediction Pipeline using scikit-learn**

---

## Project Objective

The objective of this mini project is to build a **reusable machine learning pipeline** using `scikit-learn`.

Students will create an end-to-end ML workflow that can:

* Load customer churn data
* Split data into training and testing sets
* Handle missing values
* Encode categorical features using `OneHotEncoder`
* Scale numerical features
* Train a `RandomForestClassifier`
* Evaluate model performance
* Reuse the same pipeline for future customer data

The main focus is not only model training, but building a **clean, reusable, and production-ready ML pipeline**.

---

## Business Problem

A subscription-based business wants to identify customers who are likely to leave the service.

This is called **customer churn prediction**.

The business wants to answer:

> Which customers are likely to churn?

If churn can be predicted early, the business can take actions such as:

* Offering discounts
* Improving customer support
* Sending retention offers
* Creating personalized plans
* Reducing customer loss

---

## Learning Outcomes

By completing this mini project, students will understand:

* What a reusable ML pipeline is
* How `scikit-learn` helps build ML pipelines
* Why train-test split is required
* How `test_size=0.2` creates an 80:20 split
* How numerical and categorical columns are handled differently
* Why `OneHotEncoder` is used for categorical data
* How `RandomForestClassifier` works at a beginner level
* How to evaluate a classification model
* How to save and reuse a trained pipeline

---

## Dataset Requirement

Students can use a customer churn dataset with columns similar to the following:

| Column Name     | Description                           |
| --------------- | ------------------------------------- |
| CustomerID      | Unique customer identifier            |
| Gender          | Customer gender                       |
| Age             | Customer age                          |
| Tenure          | Number of months the customer stayed  |
| MonthlyCharges  | Monthly subscription amount           |
| TotalCharges    | Total amount paid by the customer     |
| ContractType    | Monthly, yearly, or two-year contract |
| PaymentMethod   | Payment method used                   |
| InternetService | Type of internet service              |
| SupportTickets  | Number of support issues raised       |
| Churn           | Target column: Yes or No              |

---

## Target Column

The target column is:

```text
Churn
```

This column tells whether the customer left the service or not.

Example:

| CustomerID | Tenure | MonthlyCharges | ContractType | Churn |
| ---------- | -----: | -------------: | ------------ | ----- |
| C001       |      5 |            850 | Monthly      | Yes   |
| C002       |     24 |            600 | Yearly       | No    |
| C003       |      3 |            950 | Monthly      | Yes   |

---

## Main Requirement

Students must build the project using a **reusable sklearn pipeline**.

They should not manually preprocess training and testing data separately.

The pipeline should include:

```text
Raw Data
   ↓
Train-Test Split
   ↓
Missing Value Handling
   ↓
Scaling Numerical Columns
   ↓
OneHotEncoding Categorical Columns
   ↓
RandomForestClassifier
   ↓
Evaluation
   ↓
Reusable Prediction
```

---

## Step-by-Step Task Instructions

## Step 1: Import Required Libraries

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.ensemble import RandomForestClassifier
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

Students should check:

* Number of rows and columns
* Missing values
* Duplicate records
* Data types
* Target column availability
* Churn and non-churn count

---

## Step 3: Remove Unnecessary Columns

If the dataset has a unique identifier like `CustomerID`, remove it before training.

```python
df = df.drop("CustomerID", axis=1)
```

Reason:

| Column     | Reason for Removal                                                        |
| ---------- | ------------------------------------------------------------------------- |
| CustomerID | It is only an identifier and does not help the model learn churn behavior |

---

## Step 4: Separate Features and Target

```python
X = df.drop("Churn", axis=1)
y = df["Churn"]
```

Explanation:

| Variable | Meaning                                     |
| -------- | ------------------------------------------- |
| `X`      | Input features used for prediction          |
| `y`      | Target output that the model should predict |

Example:

```text
X = Age, Tenure, MonthlyCharges, ContractType, PaymentMethod
y = Churn
```

---

## Step 5: Split Train and Test Data

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

| Parameter         | Meaning                                                        |
| ----------------- | -------------------------------------------------------------- |
| `test_size=0.2`   | 20% of the data is used for testing                            |
| `random_state=42` | Gives the same split every time the code runs                  |
| `stratify=y`      | Keeps churn and non-churn ratio similar in train and test data |

### Why `test_size=0.2` means 80:20

If the dataset has 100 records:

| Split         |    Records |
| ------------- | ---------: |
| Training Data | 80 records |
| Testing Data  | 20 records |

So:

```text
test_size = 0.2 means 20% test data
remaining 80% becomes training data
```

---

## Step 6: Identify Numerical and Categorical Columns

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

Explanation:

| Column Type | Example                             | Required Processing                 |
| ----------- | ----------------------------------- | ----------------------------------- |
| Numerical   | Age, Tenure, MonthlyCharges         | Missing value handling and scaling  |
| Categorical | Gender, ContractType, PaymentMethod | Missing value handling and encoding |

---

## Step 7: Create Numerical Pipeline

```python
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
```

Explanation:

| Step                               | Purpose                                       |
| ---------------------------------- | --------------------------------------------- |
| `SimpleImputer(strategy="median")` | Fills missing numeric values using the median |
| `StandardScaler()`                 | Scales numerical columns to a common range    |

---

## Step 8: Create Categorical Pipeline using OneHotEncoder

```python
categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])
```

Explanation:

| Step                                      | Purpose                                                   |
| ----------------------------------------- | --------------------------------------------------------- |
| `SimpleImputer(strategy="most_frequent")` | Fills missing category values using the most common value |
| `OneHotEncoder(handle_unknown="ignore")`  | Converts text categories into 0/1 numeric columns         |

### OneHotEncoder Example

Before encoding:

| ContractType |
| ------------ |
| Monthly      |
| Yearly       |
| Two-Year     |

After encoding:

| ContractType_Monthly | ContractType_Yearly | ContractType_Two-Year |
| -------------------: | ------------------: | --------------------: |
|                    1 |                   0 |                     0 |
|                    0 |                   1 |                     0 |
|                    0 |                   0 |                     1 |

Reason:

Machine learning models cannot directly understand text values like:

```text
Monthly, Yearly, Two-Year
```

So `OneHotEncoder` converts them into numeric 0/1 columns.

---

## Step 9: Combine Pipelines using ColumnTransformer

```python
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])
```

Explanation:

| Transformer | Applied To          |
| ----------- | ------------------- |
| `num`       | Numerical columns   |
| `cat`       | Categorical columns |

`ColumnTransformer` ensures that the correct preprocessing is applied to the correct columns.

---

## Step 10: Create Final Reusable ML Pipeline

```python
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(random_state=42))
])
```

This final pipeline includes:

```text
Preprocessing + Model Training
```

When `fit()` is called, the pipeline automatically:

* Fills missing numerical values
* Scales numerical columns
* Fills missing categorical values
* One-hot encodes categorical columns
* Trains the Random Forest model

---

## Step 11: Train the Pipeline

```python
model_pipeline.fit(X_train, y_train)
```

Important:

The pipeline should be trained only on training data.

Correct:

```python
model_pipeline.fit(X_train, y_train)
```

Wrong:

```python
model_pipeline.fit(X, y)
```

Reason:

Training on the full dataset before testing can cause **data leakage**.

---

## Step 12: Make Predictions

```python
y_pred = model_pipeline.predict(X_test)
```

The pipeline automatically applies the same preprocessing to `X_test` before prediction.

Students do not need to manually clean, scale, or encode the test data.

---

## Step 13: Evaluate the Model

```python
print("Accuracy:", accuracy_score(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report(y_test, y_pred))
```

Important metrics:

| Metric           | Meaning                                                           |
| ---------------- | ----------------------------------------------------------------- |
| Accuracy         | Overall correct predictions                                       |
| Precision        | Out of predicted churn customers, how many actually churned       |
| Recall           | Out of actual churn customers, how many were correctly identified |
| F1-score         | Balance between precision and recall                              |
| Confusion Matrix | Shows correct and incorrect predictions                           |

For churn prediction, **recall** is very important because the business does not want to miss customers who are likely to leave.

---

## Step 14: Save the Reusable Pipeline

```python
joblib.dump(model_pipeline, "customer_churn_pipeline.pkl")
```

This saves the complete pipeline, including:

* Missing value handling
* Scaling
* One-hot encoding
* Random Forest model

---

## Step 15: Load and Reuse the Pipeline

```python
loaded_pipeline = joblib.load("customer_churn_pipeline.pkl")
```

---

## Step 16: Predict for a New Customer

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

## RandomForestClassifier Explanation

`RandomForestClassifier` is a machine learning model used for classification problems.

It is made of many decision trees.

Each tree gives a prediction, and the final output is decided by majority voting.

Example:

```text
Tree 1 → Churn
Tree 2 → No Churn
Tree 3 → Churn
Tree 4 → Churn
Tree 5 → No Churn

Final Prediction → Churn
```

Why?

Because most trees predicted `Churn`.

### Why Random Forest is useful

| Benefit                       | Explanation                              |
| ----------------------------- | ---------------------------------------- |
| Handles complex patterns      | Can learn nonlinear relationships        |
| Reduces overfitting           | Uses many trees instead of one tree      |
| Works well for classification | Useful for churn prediction              |
| Supports feature importance   | Helps understand important churn factors |

---

## Full Code

```python
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import joblib


# Load dataset
df = pd.read_csv("customer_churn.csv")


# Remove unnecessary ID column
df = df.drop("CustomerID", axis=1)


# Separate features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Define column types
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


# Numerical preprocessing pipeline
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# Categorical preprocessing pipeline
categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


# Combine preprocessing
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])


# Final reusable ML pipeline
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(random_state=42))
])


# Train pipeline
model_pipeline.fit(X_train, y_train)


# Predict on test data
y_pred = model_pipeline.predict(X_test)


# Evaluate model
print("Accuracy:", accuracy_score(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report(y_test, y_pred))


# Save reusable pipeline
joblib.dump(model_pipeline, "customer_churn_pipeline.pkl")


# Load reusable pipeline
loaded_pipeline = joblib.load("customer_churn_pipeline.pkl")


# Predict for new customer
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

print("New Customer Churn Prediction:", prediction)
```

---

## Expected Deliverables

Students should submit:

| Deliverable                     | Description                                             |
| ------------------------------- | ------------------------------------------------------- |
| Python Notebook or Script       | Complete reusable sklearn pipeline code                 |
| Dataset Summary                 | Basic data understanding and validation                 |
| Train-Test Split Explanation    | Explanation of `test_size=0.2` and 80:20 split          |
| Reusable Pipeline               | Pipeline with preprocessing and model training          |
| OneHotEncoder Explanation       | Example of categorical encoding                         |
| Model Evaluation Report         | Accuracy, precision, recall, F1-score, confusion matrix |
| Saved Pipeline File             | `.pkl` file saved using `joblib`                        |
| New Customer Prediction Example | Demonstration of pipeline reuse                         |
| Decision Log                    | Explanation of important technical decisions            |
| Business Interpretation         | How the model can help reduce churn                     |

---

## Decision Log Template

| Decision Area              | Decision Taken              | Reason                                         |
| -------------------------- | --------------------------- | ---------------------------------------------- |
| Removed column             | Removed `CustomerID`        | It is only an identifier                       |
| Train-test split           | Used 80:20 split            | To test the model on unseen data               |
| Stratification             | Used `stratify=y`           | To maintain churn ratio                        |
| Missing numeric values     | Used median imputation      | Median handles outliers better                 |
| Missing categorical values | Used most frequent value    | Preserves common category pattern              |
| Encoding                   | Used OneHotEncoder          | Converts text categories into numeric format   |
| Scaling                    | Used StandardScaler         | Brings numerical values to similar scale       |
| Model                      | Used RandomForestClassifier | Good for classification and nonlinear patterns |
| Evaluation                 | Used classification metrics | Churn is a classification problem              |
| Reusability                | Saved pipeline using joblib | Allows future reuse                            |

---

## Mentor Evaluation Checklist

| Criteria                 | Expected Standard                                        |
| ------------------------ | -------------------------------------------------------- |
| Correct train-test split | Student uses `train_test_split` properly                 |
| Reusable pipeline        | Student uses sklearn `Pipeline`                          |
| ColumnTransformer usage  | Numerical and categorical columns are handled separately |
| Missing value handling   | Done inside the pipeline                                 |
| OneHotEncoder usage      | Categorical values are encoded inside the pipeline       |
| Model training           | RandomForestClassifier is trained through the pipeline   |
| Evaluation               | Student uses suitable classification metrics             |
| Data leakage prevention  | Pipeline is fitted only on training data                 |
| Saving pipeline          | Complete pipeline is saved using joblib                  |
| Reuse demonstration      | Student predicts for new customer data                   |
| Documentation            | Student explains all major decisions                     |

---

## Important Notes for Students

* Do not preprocess train and test data manually in separate steps.
* Put preprocessing inside the sklearn pipeline.
* Use `ColumnTransformer` for numerical and categorical columns.
* Use `OneHotEncoder` for categorical/text columns.
* Use `fit()` only on training data.
* Use `predict()` on test or new data.
* Save the full pipeline, not just the model.
* Explain each decision clearly.

---

## Final Student Explanation

At the end of the project, students should be able to explain:

> I built a reusable customer churn prediction pipeline using scikit-learn. The pipeline handles missing values, scales numerical columns, encodes categorical columns using OneHotEncoder, trains a RandomForestClassifier, evaluates the model, and saves the complete workflow for future use. The same pipeline can be reused to predict churn for new customer data without manually repeating preprocessing steps.

---

## Submission Format

Students should submit:

```text
Mini_Project_2_Customer_Churn_Pipeline/
│
├── customer_churn_pipeline.ipynb
├── decision_log.md
├── model_evaluation_report.md
└── README.md
```
