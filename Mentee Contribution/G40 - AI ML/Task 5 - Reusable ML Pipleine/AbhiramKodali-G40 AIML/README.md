# Mini Project 2: Reusable Customer Churn Prediction Pipeline

## Project Objective

This project builds a reusable machine learning pipeline using `scikit-learn` to predict customer churn for a subscription business.

The pipeline performs the full workflow:

1. Loads customer churn data.
2. Removes the identifier column.
3. Splits data into training and testing sets.
4. Handles missing values.
5. Scales numerical features.
6. One-hot encodes categorical features.
7. Trains a `RandomForestClassifier`.
8. Evaluates model performance.
9. Saves the complete trained pipeline.
10. Reuses the saved pipeline for a new customer prediction.

## Files Included

| File | Purpose |
| --- | --- |
| `customer_churn.csv` | Sample churn dataset used for training and testing. |
| `customer_churn_pipeline.py` | Complete reusable sklearn pipeline code. |
| `customer_churn_pipeline.ipynb` | Notebook version of the project. |
| `customer_churn_pipeline.pkl` | Saved reusable pipeline generated after running the script. |
| `model_evaluation_report.md` | Dataset summary and model evaluation report. |
| `decision_log.md` | Explanation of important technical decisions. |

## Train-Test Split Explanation

The project uses:

```python
test_size=0.2
```

This means 20% of the dataset is used for testing. The remaining 80% is used for training.

For example, with 100 records:

| Split | Records |
| --- | ---: |
| Training Data | 80 |
| Testing Data | 20 |

The code also uses `stratify=y`, which keeps the churn and non-churn ratio similar in both training and testing data.

## Reusable Pipeline

The final sklearn pipeline combines preprocessing and model training:

```text
Raw Data
   -> Missing Value Handling
   -> Numerical Scaling
   -> OneHotEncoding
   -> RandomForestClassifier
   -> Prediction
```

Because preprocessing is inside the pipeline, the training data, test data, and future customer data all receive the same transformations.

## How to Run

Run the project from this folder:

```powershell
python customer_churn_pipeline.py
```

After running, the script creates:

- `customer_churn_pipeline.pkl`
- `model_evaluation_report.md`

## Final Student Explanation

I built a reusable customer churn prediction pipeline using scikit-learn. The pipeline handles missing values, scales numerical columns, encodes categorical columns using OneHotEncoder, trains a RandomForestClassifier, evaluates the model, and saves the complete workflow for future use. The same pipeline can be reused to predict churn for new customer data without manually repeating preprocessing steps.
