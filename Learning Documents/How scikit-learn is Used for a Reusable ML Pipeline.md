# Learning Material 2: How scikit-learn is Used for a Reusable ML Pipeline

## 1. What is scikit-learn?

`scikit-learn`, also written as `sklearn`, is a popular Python library used for machine learning.

It provides ready-made tools for:

```text
- Data preprocessing
- Feature transformation
- Model training
- Model evaluation
- Building reusable ML pipelines
```

For Mini Project 2, we use `sklearn` because it helps us organize the complete ML workflow in a clean and reusable way.

---

## 2. Why Use scikit-learn for ML Pipelines?

Without `sklearn`, students may write separate code for each step:

```text
Clean missing values separately
Encode categorical data separately
Scale numerical data separately
Train the model separately
Evaluate separately
```

This becomes messy and difficult to reuse.

With `sklearn`, we can combine all these steps into one pipeline.

```text
Raw Data → Preprocessing → Model Training → Prediction
```

This makes the ML workflow:

| Benefit             | Explanation                                           |
| ------------------- | ----------------------------------------------------- |
| Reusable            | Same pipeline can be used for training and prediction |
| Clean               | Steps are organized in one structure                  |
| Consistent          | Same preprocessing is applied every time              |
| Less Error-Prone    | Reduces manual mistakes                               |
| Production-Friendly | Easier to save, load, and reuse later                 |

---

## 3. Important scikit-learn Tools Used in Pipelines

| sklearn Tool        | Purpose                                                              |
| ------------------- | -------------------------------------------------------------------- |
| `Pipeline`          | Connects multiple ML steps in order                                  |
| `ColumnTransformer` | Applies different preprocessing to different column types            |
| `SimpleImputer`     | Handles missing values                                               |
| `OneHotEncoder`     | Converts categorical columns into numeric format                     |
| `StandardScaler`    | Scales numerical columns                                             |
| ML Models           | Trains models like Logistic Regression, Decision Tree, Random Forest |

---

## 4. What is `Pipeline` in sklearn?

`Pipeline` is used to connect multiple steps together.

Example:

```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

numeric_pipeline = Pipeline(steps=[
    ("missing_value_handler", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])
```

This pipeline runs the steps in order:

```text
Step 1: Fill missing values
Step 2: Scale the data
Step 3: Train the model
```

So instead of calling each step manually, we can simply call:

```python
numeric_pipeline.fit(X_train, y_train)
```

---

## 5. Why Do We Need `ColumnTransformer`?

In real datasets, we usually have different types of columns.

For example, in a customer churn dataset:

| Column         | Type        |
| -------------- | ----------- |
| Age            | Numerical   |
| Tenure         | Numerical   |
| MonthlyCharges | Numerical   |
| Gender         | Categorical |
| ContractType   | Categorical |
| PaymentMethod  | Categorical |

Numerical columns and categorical columns need different preprocessing.

Numerical columns may need:

```text
- Missing value handling
- Scaling
```

Categorical columns may need:

```text
- Missing value handling
- Encoding
```

`ColumnTransformer` helps us apply different transformations to different columns.

---

## 6. Example: Customer Churn Pipeline Using sklearn

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
```

### Step 1: Define Numerical and Categorical Columns

```python
numeric_features = ["Age", "Tenure", "MonthlyCharges", "TotalCharges"]

categorical_features = [
    "Gender",
    "ContractType",
    "PaymentMethod",
    "InternetService"
]
```

---

### Step 2: Create Pipeline for Numerical Columns

```python
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])
```

Explanation:

| Step                               | Meaning                                   |
| ---------------------------------- | ----------------------------------------- |
| `SimpleImputer(strategy="median")` | Fills missing numeric values using median |
| `StandardScaler()`                 | Scales numerical values to a common range |

---

### Step 3: Create Pipeline for Categorical Columns

```python
categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])
```

Explanation:

| Step                                      | Meaning                                                   |
| ----------------------------------------- | --------------------------------------------------------- |
| `SimpleImputer(strategy="most_frequent")` | Fills missing category values using the most common value |
| `OneHotEncoder(handle_unknown="ignore")`  | Converts text categories into numeric columns             |

`handle_unknown="ignore"` is important because new unseen categories may appear during prediction.

---

### Step 4: Combine Both Pipelines Using ColumnTransformer

```python
preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features)
])
```

This tells sklearn:

```text
Apply numeric_pipeline to numeric_features
Apply categorical_pipeline to categorical_features
```

---

### Step 5: Add the ML Model

```python
model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(random_state=42))
])
```

Now the full pipeline contains:

```text
Preprocessing + Model Training
```

This is the reusable ML pipeline.

---

## 7. Training the Pipeline

Once the pipeline is ready, training becomes simple.

```python
model_pipeline.fit(X_train, y_train)
```

When we call `fit`, sklearn automatically does this:

```text
1. Fill missing values
2. Scale numerical columns
3. Encode categorical columns
4. Train the model
```

Students do not need to manually run each step separately.

---

## 8. Making Predictions

After training, we can use the same pipeline for prediction.

```python
y_pred = model_pipeline.predict(X_test)
```

When we call `predict`, sklearn automatically applies the same preprocessing steps before prediction.

This is very important because the test data or new data must be processed in the same way as the training data.

---

## 9. Why This Makes the Pipeline Reusable

The same pipeline can be reused for:

```text
- Training data
- Testing data
- New customer data
- Future monthly customer data
```

Example:

```python
new_predictions = model_pipeline.predict(new_customer_data)
```

The pipeline will automatically:

```text
Clean the new data
Encode categories
Scale numbers
Predict churn
```

This is why it is called a reusable ML pipeline.

---

## 10. Important Concept: Avoiding Data Leakage

Data leakage happens when information from the test data is accidentally used during training.

This can make the model look better than it actually is.

Using sklearn pipelines helps avoid data leakage because preprocessing is learned only from the training data.

Correct approach:

```python
model_pipeline.fit(X_train, y_train)
y_pred = model_pipeline.predict(X_test)
```

Here:

```text
- The pipeline learns preprocessing rules from X_train only
- The same rules are applied to X_test
- The test data remains unseen during training
```

This gives a more honest evaluation.

---

## 11. Evaluating the Pipeline

After prediction, students can evaluate the model.

```python
from sklearn.metrics import classification_report, confusion_matrix

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

For churn prediction, useful metrics are:

| Metric    | Why It Matters                                             |
| --------- | ---------------------------------------------------------- |
| Accuracy  | Shows overall correct predictions                          |
| Precision | Shows how many predicted churn customers actually churned  |
| Recall    | Shows how many actual churn customers were correctly found |
| F1-score  | Balances precision and recall                              |

For a churn project, recall is especially important because we do not want to miss customers who are likely to leave.

---

## 12. Full Example Code

```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Separate input features and target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Define column types
numeric_features = ["Age", "Tenure", "MonthlyCharges", "TotalCharges"]

categorical_features = [
    "Gender",
    "ContractType",
    "PaymentMethod",
    "InternetService"
]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Numerical preprocessing
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Categorical preprocessing
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

# Train the pipeline
model_pipeline.fit(X_train, y_train)

# Predict
y_pred = model_pipeline.predict(X_test)

# Evaluate
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

---

## 13. Simple Explanation of the Code

| Code Part                | Meaning                                          |
| ------------------------ | ------------------------------------------------ |
| `train_test_split`       | Splits data into training and testing sets       |
| `Pipeline`               | Connects multiple steps together                 |
| `SimpleImputer`          | Handles missing values                           |
| `StandardScaler`         | Scales numeric data                              |
| `OneHotEncoder`          | Converts categories into numbers                 |
| `ColumnTransformer`      | Applies correct preprocessing to correct columns |
| `RandomForestClassifier` | ML model used for prediction                     |
| `fit()`                  | Trains the full pipeline                         |
| `predict()`              | Makes predictions using the trained pipeline     |

---

## 14. Student Takeaway

`scikit-learn` helps us build a reusable ML pipeline by combining preprocessing and model training into one structured workflow.

Instead of manually cleaning, encoding, scaling, and training separately, students can create one pipeline that can be reused for training, testing, and future predictions.

For the customer churn project, sklearn pipelines help students build a workflow that is:

```text
- Clean
- Reusable
- Consistent
- Less error-prone
- Easier to explain
- More suitable for real-world ML engineering
```
