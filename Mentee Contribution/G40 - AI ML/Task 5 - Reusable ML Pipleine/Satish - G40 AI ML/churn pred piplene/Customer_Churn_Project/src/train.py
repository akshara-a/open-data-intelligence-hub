"""
Train a reusable machine learning pipeline for customer churn prediction.

This script:
1. Loads and validates the customer churn dataset.
2. Builds a Scikit-Learn preprocessing and classification pipeline.
3. Trains and evaluates a Logistic Regression model.
4. Saves the complete trained pipeline with Joblib.
5. Writes evaluation and decision log reports.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "customer_churn.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "customer_churn_pipeline.pkl"
REPORTS_DIR = PROJECT_ROOT / "reports"
EVALUATION_REPORT_PATH = REPORTS_DIR / "evaluation_report.txt"
DECISION_LOG_PATH = REPORTS_DIR / "decision_log.md"
BUSINESS_INTERPRETATION_PATH = REPORTS_DIR / "business_interpretation.md"

TARGET_COLUMN = "Churn"
ID_COLUMN = "CustomerID"

REQUIRED_COLUMNS = [
    "CustomerID",
    "Gender",
    "Age",
    "Tenure",
    "MonthlyCharges",
    "TotalCharges",
    "ContractType",
    "PaymentMethod",
    "InternetService",
    "SupportTickets",
    "Churn",
]

NUMERICAL_COLUMNS = ["Age", "Tenure", "MonthlyCharges", "TotalCharges", "SupportTickets"]
CATEGORICAL_COLUMNS = ["Gender", "ContractType", "PaymentMethod", "InternetService"]


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the churn dataset from a CSV file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {file_path}")
    return pd.read_csv(file_path)


def validate_data(df: pd.DataFrame) -> None:
    """Validate required columns and print basic data quality checks."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    print("\n========== Data Validation ==========")
    print(f"Dataset shape: {df.shape}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nData types:")
    print(df.dtypes)

    print("\nChurn distribution:")
    print(df[TARGET_COLUMN].value_counts())
    print("\nChurn distribution (%):")
    print((df[TARGET_COLUMN].value_counts(normalize=True) * 100).round(2))


def build_pipeline() -> Pipeline:
    """Create the full preprocessing and model pipeline."""
    numerical_pipeline = Pipeline(
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
            ("num", numerical_pipeline, NUMERICAL_COLUMNS),
            ("cat", categorical_pipeline, CATEGORICAL_COLUMNS),
        ]
    )

    model = LogisticRegression(max_iter=1000)

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model),
        ]
    )


def train_model(df: pd.DataFrame) -> tuple[Pipeline, dict[str, object]]:
    """Train the model and return the fitted pipeline plus evaluation results."""
    X = df.drop(columns=[TARGET_COLUMN, ID_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, pos_label="Yes"),
        "recall": recall_score(y_test, y_pred, pos_label="Yes"),
        "f1_score": f1_score(y_test, y_pred, pos_label="Yes"),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=["No", "Yes"]),
        "classification_report": classification_report(y_test, y_pred),
        "test_records": len(X_test),
    }

    return pipeline, metrics


def save_pipeline(pipeline: Pipeline, model_path: Path) -> None:
    """Save the complete trained pipeline."""
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)


def write_reports(metrics: dict[str, object]) -> None:
    """Write evaluation, decision log, and business interpretation reports."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    evaluation_text = f"""Customer Churn Model Evaluation
================================

Test records: {metrics["test_records"]}

Accuracy : {metrics["accuracy"]:.4f}
Precision: {metrics["precision"]:.4f}
Recall   : {metrics["recall"]:.4f}
F1-score : {metrics["f1_score"]:.4f}

Confusion Matrix
Rows: Actual [No, Yes]
Columns: Predicted [No, Yes]
{metrics["confusion_matrix"]}

Classification Report
{metrics["classification_report"]}
"""
    EVALUATION_REPORT_PATH.write_text(evaluation_text, encoding="utf-8")

    decision_log = """# Decision Log

## Dataset
- Created a synthetic customer churn dataset with 1000 records to support a complete college mini-project workflow.
- Included customer profile, account, billing, service, and support-ticket fields that commonly influence churn.
- Kept `CustomerID` only as an identifier and removed it before training to avoid learning from non-predictive IDs.

## Preprocessing
- Used median imputation for numerical columns because it is robust to outliers.
- Used most frequent imputation for categorical columns because it preserves common category patterns.
- Used `StandardScaler` for numerical columns because Logistic Regression performs better when numeric features are scaled.
- Used `OneHotEncoder(handle_unknown="ignore")` so the pipeline can safely handle unseen categories during prediction.

## Model
- Selected `LogisticRegression(max_iter=1000)` because it is interpretable, fast, and suitable for a baseline churn classifier.
- Used a single Scikit-Learn `Pipeline` so preprocessing and model inference are reusable and saved together.

## Evaluation
- Used stratified train-test split to preserve the original churn ratio in both training and test sets.
- Reported accuracy, precision, recall, F1-score, confusion matrix, and classification report for a balanced evaluation view.
"""
    DECISION_LOG_PATH.write_text(decision_log, encoding="utf-8")

    business_interpretation = """# Business Interpretation

Customer churn prediction helps a company identify customers who may leave soon. The model can support retention teams by ranking customers according to churn risk and enabling timely offers, service follow-ups, or contract upgrades.

In this project, churn risk is estimated using customer demographics, tenure, charges, contract type, payment method, internet service, and support ticket history. Customers with short tenure, month-to-month contracts, higher charges, electronic check payments, and more support tickets are often more likely to churn in the generated dataset.

The model should be used as a decision-support tool, not as the only decision maker. A high-risk prediction can trigger a customer care review, while final actions should consider business rules, customer value, and fairness checks.
"""
    BUSINESS_INTERPRETATION_PATH.write_text(business_interpretation, encoding="utf-8")


def print_metrics(metrics: dict[str, object]) -> None:
    """Print model evaluation results to the console."""
    print("\n========== Model Evaluation ==========")
    print(f"Accuracy : {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall   : {metrics['recall']:.4f}")
    print(f"F1-score : {metrics['f1_score']:.4f}")
    print("\nConfusion Matrix")
    print(metrics["confusion_matrix"])
    print("\nClassification Report")
    print(metrics["classification_report"])


def main() -> None:
    """Run the training workflow."""
    df = load_data(DATA_PATH)
    validate_data(df)

    pipeline, metrics = train_model(df)
    print_metrics(metrics)

    save_pipeline(pipeline, MODEL_PATH)
    write_reports(metrics)

    print(f"\nSaved trained pipeline to: {MODEL_PATH}")
    print(f"Saved reports to: {REPORTS_DIR}")


if __name__ == "__main__":
    main()
