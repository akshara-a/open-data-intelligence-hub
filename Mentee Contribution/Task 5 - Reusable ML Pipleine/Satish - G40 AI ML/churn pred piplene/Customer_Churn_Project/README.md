# Reusable Machine Learning Pipeline for Customer Churn Prediction

This mini project builds a reusable customer churn prediction workflow using Python, Pandas, Scikit-Learn, and Joblib.

## Project Structure

```text
Customer_Churn_Project/
|-- data/customer_churn.csv
|-- models/customer_churn_pipeline.pkl
|-- src/train.py
|-- src/predict.py
|-- reports/
|-- app.py
|-- README.md
`-- requirements.txt
```

## Features

The dataset contains 1000 customer records with these columns:

- `CustomerID`
- `Gender`
- `Age`
- `Tenure`
- `MonthlyCharges`
- `TotalCharges`
- `ContractType`
- `PaymentMethod`
- `InternetService`
- `SupportTickets`
- `Churn`

## Methodology

The training workflow includes:

- Data loading and validation
- Missing value checks
- Duplicate row checks
- Data type display
- Churn distribution analysis
- Removal of `CustomerID` before training
- Numerical preprocessing with median imputation and `StandardScaler`
- Categorical preprocessing with most frequent imputation and `OneHotEncoder(handle_unknown="ignore")`
- Combined preprocessing using `ColumnTransformer`
- Reusable Scikit-Learn `Pipeline`
- Logistic Regression model with `max_iter=1000`
- Stratified train-test split using `test_size=0.2` and `random_state=42`
- Evaluation using accuracy, precision, recall, F1-score, confusion matrix, and classification report
- Complete pipeline saving with Joblib

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python src/train.py
```

Run a prediction example:

```bash
python src/predict.py
```

Open the Streamlit web app:

```bash
streamlit run app.py
```

## Output Files

After training, the project creates:

- `models/customer_churn_pipeline.pkl`
- `reports/evaluation_report.txt`
- `reports/decision_log.md`
- `reports/business_interpretation.md`
- `app.py`

## Decision Log

See `reports/decision_log.md`.

## Business Interpretation

See `reports/business_interpretation.md`.
