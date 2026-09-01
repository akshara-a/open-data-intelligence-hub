# Task 9 - Optimized Classification Model with Feature Importance Analysis

## Project Overview

This project builds an optimized machine learning classification model to predict whether an e-commerce customer will make a purchase.

The project includes data quality checks, exploratory data analysis, baseline model comparison, Random Forest hyperparameter optimization, feature importance analysis, threshold analysis, and final model saving.

## Dataset

The dataset contains **2,000 customer records** and **19 columns**.

Target variable:

- `Purchase = 0` → Customer did not purchase
- `Purchase = 1` → Customer purchased

The dataset contains numerical and categorical customer behavior features such as:

- Age
- Gender
- Location
- DeviceType
- TrafficSource
- PagesViewed
- TimeOnSite
- ProductsViewed
- CartItems
- PreviousPurchases
- AverageOrderValue
- DiscountUsed
- EmailClicked
- AdClicked
- ReviewScoreViewed
- DaysSinceLastVisit
- SessionCount

## Models

The project evaluates:

1. Logistic Regression - Baseline
2. Decision Tree - Baseline
3. Random Forest - Baseline
4. Optimized Random Forest

### Model Results

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression - Baseline | 0.6250 | 0.1634 | 0.5319 | 0.2500 | 0.5841 |
| Decision Tree - Baseline | 0.7925 | 0.1250 | 0.1277 | 0.1263 | 0.5043 |
| Random Forest - Baseline | 0.8825 | 0.0000 | 0.0000 | 0.0000 | 0.5939 |
| Optimized Random Forest | 0.8575 | 0.0000 | 0.0000 | 0.0000 | 0.5798 |

## Random Forest Optimization

Random Forest hyperparameter optimization was performed using cross-validation.

Best parameters:

- `max_depth = 8`
- `max_features = log2`
- `min_samples_leaf = 1`
- `min_samples_split = 2`
- `n_estimators = 100`

Best cross-validation F1-score:

**0.0755**

## Feature Importance

The most important features identified by the optimized Random Forest include:

1. TimeOnSite
2. DaysSinceLastVisit
3. ReviewScoreViewed
4. AverageOrderValue
5. Age
6. SessionCount
7. PagesViewed
8. ProductsViewed
9. PreviousPurchases
10. CartItems

## Threshold Analysis

Different classification thresholds were evaluated to improve purchase detection.

At a threshold of **0.3**:

- Precision: 0.1374
- Recall: 0.5319
- F1-Score: 0.2183

## Project Structure

```text
P.Shadik Khan - G40 AI ML/
│
├── data/
│   └── ecommerce_customer_data.csv
│
├── notebooks/
│   ├── optimized_classification.ipynb
│   └── purchase_prediction_analysis.ipynb
│
├── models/
│   └── purchase_prediction_model.pkl
│
├── reports/
│   ├── baseline_roc_curve.png
│   ├── cart_items_purchase.png
│   ├── correlation_heatmap.png
│   ├── confusion_matrix.png
│   ├── customer_purchase_predictions.csv
│   ├── decision_tree_confusion_matrix.png
│   ├── feature_importance.csv
│   ├── feature_importance.png
│   ├── logistic_regression_confusion_matrix.png
│   ├── model_comparison.csv
│   ├── optimization_summary.csv
│   ├── purchase_distribution.png
│   ├── purchase_rate_by_device.png
│   ├── purchase_rate_by_traffic_source.png
│   ├── random_forest_confusion_matrix.png
│   ├── roc_curve.png
│   ├── threshold_analysis.csv
│   └── time_on_site_purchase.png
│
├── presentation/
│
├── generate_dataset.py
├── purchase_prediction_analysis.py
├── requirements.txt
└── README.md