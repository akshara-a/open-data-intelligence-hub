# Optimized Classification Model with Feature Importance Analysis

A Google Colab–ready machine learning project that trains a hyperparameter-tuned
Random Forest classifier and analyzes which features drive its predictions.

## 📂 Files
- `classification_model_feature_importance.ipynb` — main Colab notebook (EDA → training → tuning → evaluation → feature importance)
- `README.md` — this file

## 📊 Dataset
**Breast Cancer Wisconsin (Diagnostic) Dataset**

Dataset URL (loaded directly in the notebook via `pandas.read_csv`, no manual download needed):

```
https://raw.githubusercontent.com/plotly/datasets/master/breast-cancer-wisconsin-data.csv
```

Original source (UCI Machine Learning Repository):
```
https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
```

> To use your own dataset instead, just replace the `DATA_URL` variable in the notebook's
> "Load Dataset" cell with a link to your CSV file.

## 🚀 How to Run
1. Open `classification_model_feature_importance.ipynb` in [Google Colab](https://colab.research.google.com/).
2. Run all cells (`Runtime → Run all`). No file upload is required — data loads directly from the URL above.
3. Review the metrics, plots, and feature importance charts produced at each step.

## 🧠 What's Inside
- **EDA**: class balance plot, correlation heatmap
- **Preprocessing**: cleaning, encoding, train/test split, feature scaling
- **Model optimization**: `RandomForestClassifier` tuned with `GridSearchCV` (5-fold stratified cross-validation, ROC-AUC scoring)
- **Evaluation**: accuracy, classification report, confusion matrix, ROC curve
- **Feature importance analysis**:
  - Built-in Random Forest importance (mean decrease in impurity)
  - Permutation importance (model-agnostic, more robust)
- **Model export**: saves the trained model and scaler as `.pkl` files

## 🛠 Requirements
Installed automatically in the first notebook cell:
- pandas, numpy, matplotlib, seaborn
- scikit-learn
- joblib

## 📈 Results
Exact metrics depend on the tuned hyperparameters found by `GridSearchCV`, printed at
the end of the notebook run (accuracy, ROC-AUC, top predictive features).
