"""
Streamlit app for the Customer Churn Prediction mini project.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "customer_churn.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "customer_churn_pipeline.pkl"
EVALUATION_REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_report.txt"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load customer churn data."""
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def load_pipeline():
    """Load the saved machine learning pipeline."""
    return joblib.load(MODEL_PATH)


def show_project_overview(df: pd.DataFrame) -> None:
    """Display dataset and validation summary."""
    churn_counts = df["Churn"].value_counts()
    churn_rate = (df["Churn"].eq("Yes").mean() * 100).round(2)

    st.subheader("Project Overview")
    st.write(
        "This app demonstrates a reusable machine learning pipeline for customer "
        "churn prediction using Pandas, Scikit-Learn, Logistic Regression, and Joblib."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Records", f"{len(df):,}")
    col2.metric("Features", df.shape[1] - 2)
    col3.metric("Churn Rate", f"{churn_rate}%")
    col4.metric("Duplicates", int(df.duplicated().sum()))

    st.subheader("Data Validation")
    left, right = st.columns(2)

    with left:
        st.write("Missing Values")
        st.dataframe(df.isnull().sum().rename("Missing Count"), use_container_width=True)

    with right:
        st.write("Churn Distribution")
        st.bar_chart(churn_counts)

    with st.expander("Show Data Types"):
        st.dataframe(df.dtypes.astype(str).rename("Data Type"), use_container_width=True)

    with st.expander("Preview Dataset"):
        st.dataframe(df.head(20), use_container_width=True)


def show_pipeline_details() -> None:
    """Display preprocessing and model pipeline details."""
    st.subheader("Reusable ML Pipeline")

    st.markdown(
        """
        1. Remove `CustomerID`
        2. Numerical preprocessing:
           - Median imputation
           - StandardScaler
        3. Categorical preprocessing:
           - Most frequent imputation
           - OneHotEncoder(handle_unknown="ignore")
        4. Combine preprocessing with ColumnTransformer
        5. Train LogisticRegression(max_iter=1000)
        6. Save the complete pipeline as `customer_churn_pipeline.pkl`
        """
    )

    st.info(
        "Because preprocessing and the model are saved together, the same pipeline "
        "can be reused for future predictions without repeating manual preparation."
    )


def show_model_evaluation() -> None:
    """Display saved model evaluation report."""
    st.subheader("Model Evaluation")

    metric_cols = st.columns(4)
    metric_cols[0].metric("Accuracy", "73.00%")
    metric_cols[1].metric("Precision", "62.16%")
    metric_cols[2].metric("Recall", "36.51%")
    metric_cols[3].metric("F1-score", "46.00%")

    st.write("Confusion Matrix")
    confusion_df = pd.DataFrame(
        [[123, 14], [40, 23]],
        index=["Actual No", "Actual Yes"],
        columns=["Predicted No", "Predicted Yes"],
    )
    st.dataframe(confusion_df, use_container_width=True)

    if EVALUATION_REPORT_PATH.exists():
        with st.expander("Full Evaluation Report"):
            st.code(EVALUATION_REPORT_PATH.read_text(encoding="utf-8"))


def show_prediction_form() -> None:
    """Collect customer details and predict churn."""
    st.subheader("Predict Churn for a New Customer")

    pipeline = load_pipeline()

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox("Gender", ["Female", "Male"])
            age = st.slider("Age", 18, 75, 34)
            tenure = st.slider("Tenure", 1, 72, 8)

        with col2:
            monthly_charges = st.number_input(
                "Monthly Charges", min_value=18.0, max_value=120.0, value=89.50, step=1.0
            )
            total_charges = st.number_input(
                "Total Charges", min_value=18.0, max_value=9000.0, value=716.00, step=50.0
            )
            support_tickets = st.slider("Support Tickets", 0, 8, 4)

        with col3:
            contract_type = st.selectbox(
                "Contract Type", ["Month-to-month", "One year", "Two year"]
            )
            payment_method = st.selectbox(
                "Payment Method",
                ["Electronic check", "Mailed check", "Bank transfer", "Credit card"],
            )
            internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])

        submitted = st.form_submit_button("Predict Churn")

    if submitted:
        customer = pd.DataFrame(
            [
                {
                    "Gender": gender,
                    "Age": age,
                    "Tenure": tenure,
                    "MonthlyCharges": monthly_charges,
                    "TotalCharges": total_charges,
                    "ContractType": contract_type,
                    "PaymentMethod": payment_method,
                    "InternetService": internet_service,
                    "SupportTickets": support_tickets,
                }
            ]
        )

        prediction = pipeline.predict(customer)[0]
        probabilities = pipeline.predict_proba(customer)[0]
        probability_map = dict(zip(pipeline.named_steps["classifier"].classes_, probabilities))
        churn_probability = probability_map.get("Yes", 0.0)

        if prediction == "Yes":
            st.error(f"Predicted Churn: Yes | Churn Probability: {churn_probability:.2%}")
        else:
            st.success(f"Predicted Churn: No | Churn Probability: {churn_probability:.2%}")

        st.write("Customer Input")
        st.dataframe(customer, use_container_width=True)


def show_business_interpretation() -> None:
    """Display business interpretation."""
    st.subheader("Business Interpretation")
    st.write(
        "Customer churn prediction helps a business identify customers who may leave. "
        "High-risk customers can be prioritized for retention offers, service follow-ups, "
        "or contract upgrade discussions. The model should be used as a decision-support "
        "tool along with business judgement."
    )


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(
        page_title="Customer Churn Prediction",
        page_icon="📊",
        layout="wide",
    )

    st.title("Reusable Machine Learning Pipeline for Customer Churn Prediction")
    st.caption("Python | Pandas | Scikit-Learn | Joblib | Streamlit")

    if not DATA_PATH.exists():
        st.error("Dataset not found. Please make sure data/customer_churn.csv exists.")
        st.stop()

    if not MODEL_PATH.exists():
        st.error("Saved model not found. Run `python src/train.py` before opening the app.")
        st.stop()

    df = load_data()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Overview", "Pipeline", "Prediction", "Business Interpretation"]
    )

    with tab1:
        show_project_overview(df)
        show_model_evaluation()

    with tab2:
        show_pipeline_details()

    with tab3:
        show_prediction_form()

    with tab4:
        show_business_interpretation()


if __name__ == "__main__":
    main()
