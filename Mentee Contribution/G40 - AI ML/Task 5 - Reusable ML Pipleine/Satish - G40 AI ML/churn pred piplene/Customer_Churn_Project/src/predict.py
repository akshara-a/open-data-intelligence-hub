"""
Make a prediction for a new customer using the saved churn pipeline.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "customer_churn_pipeline.pkl"


def load_pipeline(model_path: Path):
    """Load the saved Joblib pipeline."""
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run `python src/train.py` first."
        )
    return joblib.load(model_path)


def create_new_customer() -> pd.DataFrame:
    """Create a sample customer record for prediction."""
    return pd.DataFrame(
        [
            {
                "Gender": "Female",
                "Age": 34,
                "Tenure": 8,
                "MonthlyCharges": 89.50,
                "TotalCharges": 716.00,
                "ContractType": "Month-to-month",
                "PaymentMethod": "Electronic check",
                "InternetService": "Fiber optic",
                "SupportTickets": 4,
            }
        ]
    )


def predict_churn(customer_data: pd.DataFrame) -> None:
    """Predict churn and print the predicted class and probabilities."""
    pipeline = load_pipeline(MODEL_PATH)

    prediction = pipeline.predict(customer_data)[0]
    probabilities = pipeline.predict_proba(customer_data)[0]
    class_labels = pipeline.named_steps["classifier"].classes_
    probability_map = dict(zip(class_labels, probabilities))

    print("========== New Customer ==========")
    print(customer_data)

    print("\n========== Prediction ==========")
    print(f"Predicted churn: {prediction}")
    print(f"Probability of No churn : {probability_map.get('No', 0):.4f}")
    print(f"Probability of Churn    : {probability_map.get('Yes', 0):.4f}")


def main() -> None:
    """Run a sample churn prediction."""
    new_customer = create_new_customer()
    predict_churn(new_customer)


if __name__ == "__main__":
    main()
