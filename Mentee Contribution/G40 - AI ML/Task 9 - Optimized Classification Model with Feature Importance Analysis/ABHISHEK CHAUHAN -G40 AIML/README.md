# Purchase Prediction — Online Shoppers Purchasing Intention

Predicts whether an online shopping session will end in a purchase, using session-level
behavioral data (page views, durations, bounce/exit rates, visitor type, month, etc.).
Built and evaluated three models (Logistic Regression, Decision Tree, Random Forest),
tuned the two tree-based models with grid search, and selected a final model with a
business-driven decision threshold.

## Folder Structure

```
purchase-prediction-project/
│
├── README.md
├── BUSINESS_REPORT.md
├── requirements.txt
│
├── notebooks/
│   └── purchase_prediction_analysis.ipynb
│
├── data/
│   └── online_shoppers_intention.csv
│
├── models/
│   └── purchase_prediction_model.pkl
│
└── reports/
    ├── tables/
    │   ├── model_comparison_table.csv
    │   ├── hyperparameter_optimization_summary.csv
    │   └── feature_importance_report.csv
    │
    └── figures/
        ├── roc_curve.png
        ├── final_model_confusion_matrix.png
        ├── feature_importance.png
        └── threshold_analysis.png
```

## Files in this submission

| File | Location | What it is |
|---|---|---|
| `purchase_prediction_analysis.ipynb` | `notebooks/` | Full analysis notebook — EDA, preprocessing, baseline models, hyperparameter tuning, sensitivity analysis, final model selection, threshold analysis, customer segmentation, and business recommendations |
| `BUSINESS_REPORT.md` | root | Non-technical write-up of findings and recommendations |
| `purchase_prediction_model.pkl` | `models/` | Saved final model (full pipeline: preprocessing + classifier) |
| `model_comparison_table.csv` | `reports/tables/` | All 5 models (3 baseline + 2 optimized) with Accuracy/Precision/Recall/F1/ROC-AUC |
| `hyperparameter_optimization_summary.csv` | `reports/tables/` | Grid search setup and results for the Decision Tree and Random Forest |
| `feature_importance_report.csv` | `reports/tables/` | Top 10 features with business interpretation for each |
| `roc_curve.png` | `reports/figures/` | ROC curves — baseline vs. optimized models |
| `final_model_confusion_matrix.png` | `reports/figures/` | Confusion matrix for the selected final model |
| `feature_importance.png` | `reports/figures/` | Bar chart of the top 10 features |
| `threshold_analysis.png` | `reports/figures/` | Precision/Recall/F1 vs. classification threshold |

## Dataset

UCI "Online Shoppers Purchasing Intention" dataset — 12,330 sessions, 17 raw features
(page counts/durations, bounce/exit rates, `PageValues`, `Month`, `VisitorType`,
`TrafficType`, `Region`, `Weekend`, etc.), target `Revenue` (purchase / no purchase).
Purchases are the minority class at 15.47% of sessions.

Place the CSV at `data/online_shoppers_intention.csv` (this is what the local file path in
the notebook expects — see below).

## How to run

1. Put `online_shoppers_intention.csv` in `data/`.
2. Open `notebooks/purchase_prediction_analysis.ipynb`.
3. The notebook was originally written for Google Colab with Drive mounted in the first
   cell (`drive.mount(...)` + a `/content/drive/...` path). To run it against this folder
   structure instead, replace those two cells with:
   ```python
   df = pd.read_csv('../data/online_shoppers_intention.csv')
   ```
   (adjust the relative path if you launch Jupyter from a different working directory).
4. Run all cells top to bottom. Grid search cells (Decision Tree and Random Forest tuning)
   are the slowest part — expect several minutes total.
5. Update the `plt.savefig(...)`, `joblib.dump(...)`, and `.to_csv(...)` paths inside the
   notebook to point at `reports/figures/`, `models/`, and `reports/tables/` respectively
   if you want re-runs to land directly in this folder structure instead of the original
   output directory.

## Result summary

- **Final model:** Optimized Random Forest (`class_weight='balanced'`, `min_samples_split=10`,
  `n_estimators=100`) — best cross-validated F1 (0.686), test F1 0.668, ROC-AUC 0.925.
- **Recommended decision threshold: 0.45** (not the default 0.5) — see
  `reports/figures/threshold_analysis.png` and the notebook's Task 14 section for the reasoning.
- **Top predictive signal:** `PageValues`, alone responsible for 38% of the model's importance.

See `BUSINESS_REPORT.md` for the full write-up in plain-language, business-facing terms.

## Requirements

See `requirements.txt`:

```
pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
```

Install with:
```bash
pip install -r requirements.txt
```

## Using the saved model

```python
import joblib

model = joblib.load('models/purchase_prediction_model.pkl')  # full pipeline: preprocessing + classifier
probabilities = model.predict_proba(new_sessions_df)[:, 1]
predictions = (probabilities >= 0.45).astype(int)  # use 0.45, not the sklearn default of 0.5
```

`new_sessions_df` needs the same 17 raw columns as the training data — the pipeline handles
encoding and scaling internally.
