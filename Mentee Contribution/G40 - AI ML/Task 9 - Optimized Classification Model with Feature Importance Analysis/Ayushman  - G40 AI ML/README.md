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
# Customer Churn Prediction using Machine Learning

## Project Overview
This project predicts whether a telecom customer is likely to churn using machine learning classification models. Multiple models were evaluated, and a Random Forest classifier was optimized using GridSearchCV.

## Dataset
- Telco Customer Churn Dataset

## Technologies
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Joblib
- ReportLab

## Workflow
1. Data Loading
2. Data Cleaning
3. Exploratory Data Analysis
4. Data Preprocessing
5. Train-Test Split
6. Baseline Model Training
7. Hyperparameter Optimization
8. Hyperparameter Sensitivity Analysis
9. Optimized Model Evaluation
10. Feature Importance Analysis
11. Business Recommendations

## Models Used
- Logistic Regression
- Decision Tree
- Random Forest

## Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

## Generated Files
- optimized_model.pkl
- customer_churn_predictions.csv
- feature_importance.csv
- confusion_matrix.png
- roc_curve.png
- feature_importance.png
- hyperparameter_sensitivity.png
- correlation_heatmap.png
- churn_distribution.png
- business_recommendations.pdf
- feature_importance_report.pdf

## Conclusion
The optimized Random Forest model achieved the best overall performance for customer churn prediction. Feature importance analysis highlighted the key factors influencing churn, helping businesses design effective customer retention strategies.
