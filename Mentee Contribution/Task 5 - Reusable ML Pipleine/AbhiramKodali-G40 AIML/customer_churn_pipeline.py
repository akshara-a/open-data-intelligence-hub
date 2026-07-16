import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import joblib


DATASET_PATH = "customer_churn.csv"
PIPELINE_PATH = "customer_churn_pipeline.pkl"
REPORT_PATH = "model_evaluation_report.md"


def load_data(path=DATASET_PATH):
    df = pd.read_csv(path)
    return df


def build_pipeline():
    numeric_features = [
        "Age",
        "Tenure",
        "MonthlyCharges",
        "TotalCharges",
        "SupportTickets",
    ]

    categorical_features = [
        "Gender",
        "ContractType",
        "PaymentMethod",
        "InternetService",
    ]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )

    model_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestClassifier(random_state=42)),
        ]
    )

    return model_pipeline


def write_evaluation_report(df, y_test, y_pred, accuracy):
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    content = f"""# Model Evaluation Report

## Dataset Summary

- Rows: {df.shape[0]}
- Columns: {df.shape[1]}
- Duplicate rows: {df.duplicated().sum()}
- Target column: `Churn`
- Churn distribution:

{df["Churn"].value_counts().to_markdown()}

## Missing Values

{df.isnull().sum().to_markdown()}

## Train-Test Split

The project uses an 80:20 split through `test_size=0.2`.
This means 80% of the rows are used to train the model and 20% are held back for testing.
`random_state=42` makes the split repeatable, and `stratify=y` keeps the churn and non-churn ratio similar in both sets.

## Evaluation Results

- Accuracy: {accuracy:.2f}

## Confusion Matrix

Rows represent actual labels and columns represent predicted labels.

```text
{matrix}
```

## Classification Report

```text
{report}
```

## Business Interpretation

For churn prediction, recall for the `Yes` class is especially important because the business wants to find as many likely-to-leave customers as possible. Customers predicted as likely to churn can be prioritized for retention actions such as support follow-up, discounts, personalized plans, or renewal offers.
"""

    with open(REPORT_PATH, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    df = load_data()

    print("Dataset Preview:")
    print(df.head())
    print("\nDataset Info:")
    print(df.info())
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nChurn Distribution:")
    print(df["Churn"].value_counts())

    df = df.drop("CustomerID", axis=1)

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model_pipeline = build_pipeline()
    model_pipeline.fit(X_train, y_train)

    y_pred = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("\nAccuracy:", accuracy)
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model_pipeline, PIPELINE_PATH)
    write_evaluation_report(load_data(), y_test, y_pred, accuracy)

    loaded_pipeline = joblib.load(PIPELINE_PATH)

    new_customer = pd.DataFrame(
        {
            "Gender": ["Female"],
            "Age": [32],
            "Tenure": [5],
            "MonthlyCharges": [850],
            "TotalCharges": [4250],
            "ContractType": ["Monthly"],
            "PaymentMethod": ["Credit Card"],
            "InternetService": ["Fiber"],
            "SupportTickets": [3],
        }
    )

    prediction = loaded_pipeline.predict(new_customer)
    probability = loaded_pipeline.predict_proba(new_customer)

    print("\nNew Customer Churn Prediction:", prediction[0])
    print("Prediction Probabilities:", probability[0])


if __name__ == "__main__":
    main()
