# Reusable ML Pipeline with scikit-learn — Customer Churn Prediction

## Overview
This project builds a reusable, end-to-end machine learning pipeline using
scikit-learn to predict customer churn. The pipeline combines data
preprocessing and model training into a single object that can be saved,
reloaded, and reused on new customer data without rewriting any logic.

## Dataset
- Dataset: Telco Customer Churn dataset
- Target column: `Churn` (1 = customer churned, 0 = customer stayed)
- Features: mix of numeric (e.g. tenure, monthly charges) and
  categorical (e.g. contract type, gender) columns

## Pipeline Structure
1. **Train-test split** — 80% train / 20% test, stratified on the target
2. **Numeric preprocessing** — `SimpleImputer` (median) + `StandardScaler`
3. **Categorical preprocessing** — `SimpleImputer` (most frequent) +
   `OneHotEncoder` (with `handle_unknown='ignore'`)
4. **ColumnTransformer** — routes numeric and categorical columns to
   their respective preprocessing pipelines
5. **Model** — `RandomForestClassifier` (100 trees)
6. All steps are wrapped in a single `Pipeline` object, so calling
   `.fit()` and `.predict()` runs the full workflow consistently.

## How to Run
1. Open `churn_pipeline.ipynb` in Google Colab or Jupyter
2. Upload the dataset when prompted (or load it from a URL)
3. Run all cells top to bottom
4. The trained pipeline is saved as `churn_pipeline.pkl`

## Evaluation
Model performance is measured using:
- Accuracy
- Precision / Recall / F1-score (`classification_report`)
- Confusion matrix (see `confusion_matrix.png`)

Recall is especially important here — missing an actual churn customer
is more costly to the business than a false alarm.

## Reusing the Saved Pipeline
```python
import joblib

loaded_pipeline = joblib.load('churn_pipeline.pkl')
predictions = loaded_pipeline.predict(new_customer_data)
```

Because preprocessing is built into the pipeline, new/unseen data is
automatically imputed, encoded, and scaled the same way as the training
data — no manual preprocessing needed.

## Files in this Repo
| File | Description |
|---|---|
| `churn_pipeline.ipynb` | Full notebook: data prep, training, evaluation |
| `churn_pipeline.pkl` | Saved trained pipeline (preprocessing + model) |
| `confusion_matrix.png` | Visual evaluation of model performance |
| `requirements.txt` | Python dependencies |

## Requirements
See `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```
