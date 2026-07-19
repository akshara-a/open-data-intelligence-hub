# Optimized Classification Model with Feature Importance Analysis

## Overview
Predicts e-commerce purchase likelihood by training and comparing three 
classification models (Logistic Regression, Decision Tree, Random Forest), 
tuning with GridSearchCV, and analyzing feature importance to generate 
actionable business recommendations.

## Dataset
Synthetic e-commerce dataset (3000 rows), ~25% purchase rate (class imbalance).

## Model Comparison

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (Baseline) | 0.823 | 0.677 | 0.560 | 0.613 | 0.864 |
| Decision Tree (Baseline) | 0.755 | 0.510 | 0.493 | 0.502 | 0.668 |
| Random Forest (Baseline) | 0.815 | 0.767 | 0.373 | 0.502 | 0.845 |
| Random Forest (Optimized) | 0.780 | 0.545 | 0.720 | 0.621 | 0.852 |
| **Logistic Regression (Optimized) - SELECTED** | 0.765 | 0.520 | 0.793 | **0.628** | **0.864** |

Logistic Regression (Optimized) was selected as the final model: it achieved 
the best F1-Score and ROC-AUC on the held-out test set, despite Random Forest 
scoring similarly during cross-validation - illustrating why final model 
selection should rely on test-set performance, not CV scores alone.

## Top Features Influencing Purchase
1. DaysSinceLastVisit (decreases likelihood)
2. CartItems (increases likelihood)
3. PagesViewed (increases likelihood)
4. PreviousPurchases (increases likelihood)
5. DiscountUsed (increases likelihood)

## Files
- `purchase_prediction_analysis.ipynb` — full notebook
- `ecommerce_purchase_data.csv` — dataset
- `eda_charts_task9.png` — exploratory data analysis
- `hyperparam_sensitivity_task9.png` — max_depth sensitivity analysis
- `feature_importance_task9.png` / `.csv` — feature importance analysis
- `model_comparison_task9.csv` — full model comparison table
- `customer_risk_categories_task9.csv` — Low/Medium/High purchase-likelihood segments
- `purchase_prediction_model.pkl` — saved final pipeline (preprocessing + model)
- `business_report_task9.md` — full report with business recommendations

## Business Value
Purchase-likelihood segments allow targeted marketing: personalized offers 
for High-likelihood customers, incentive nudges for Medium, and low-cost 
awareness campaigns for Low - reducing wasted marketing spend while 
improving conversion.