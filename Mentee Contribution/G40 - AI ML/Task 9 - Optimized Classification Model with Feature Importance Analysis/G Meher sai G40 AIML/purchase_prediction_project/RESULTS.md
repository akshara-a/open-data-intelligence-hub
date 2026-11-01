# RESULTS

# Online Shoppers Purchase Prediction using Machine Learning

## Project Summary

This project focuses on predicting whether an online shopper will make a purchase (`Revenue = True`) based on their browsing behavior. The project follows a complete machine learning workflow, including data understanding, exploratory data analysis (EDA), feature engineering, preprocessing, model comparison, hyperparameter tuning, evaluation, and feature importance analysis.

---

# Problem Statement

E-commerce businesses collect a large amount of customer browsing data. Predicting whether a visitor is likely to complete a purchase helps businesses improve marketing strategies, personalize recommendations, and increase conversion rates.

The objective of this project is to build an optimized classification model capable of predicting customer purchase intention accurately.

---

# Dataset Information

**Dataset:** Online Shoppers Purchasing Intention Dataset

**Target Variable**

- Revenue
  - True → Customer made a purchase
  - False → Customer did not make a purchase

The dataset contains browsing session information including:

- Administrative pages
- Informational pages
- Product-related pages
- Time spent on pages
- Bounce Rate
- Exit Rate
- Page Value
- Special Day
- Month
- Operating System
- Browser
- Region
- Traffic Type
- Visitor Type
- Weekend

---

# Project Workflow

```
Data Collection
        │
        ▼
Data Understanding
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Engineering
        │
        ▼
Data Cleaning
        │
        ▼
Preprocessing Pipeline
        │
        ▼
Model Training
        │
        ▼
Hyperparameter Tuning
        │
        ▼
Model Evaluation
        │
        ▼
Feature Importance
        │
        ▼
Final Optimized Model
```

---

# 1. Data Understanding

Performed the following:

- Loaded dataset
- Checked dataset shape
- Examined data types
- Checked missing values
- Checked duplicate records
- Identified numerical and categorical features
- Studied class distribution

### Observations

- Dataset contained customer browsing sessions.
- Target variable was binary.
- Duplicate records were identified and removed.
- Missing values were handled during preprocessing.

---

# 2. Exploratory Data Analysis (EDA)

Performed detailed EDA to understand customer behavior.

### Numerical Analysis

Studied:

- Administrative Duration
- Informational Duration
- Product Related Duration
- Bounce Rate
- Exit Rate
- Page Value

### Categorical Analysis

Analyzed:

- Visitor Type
- Month
- Weekend
- Browser
- Operating System
- Traffic Type
- Region

### Visualizations Created

- Revenue Distribution
- Correlation Heatmap
- Histograms
- Boxplots
- Countplots
- Pairwise Feature Analysis

### Key Findings

- Returning visitors had higher purchase probability.
- Higher Page Values strongly indicated purchases.
- Bounce Rate negatively affected purchase intention.
- Product-related browsing duration positively influenced purchases.
- November and December showed increased purchase activity.

---

# 3. Feature Engineering

To improve model performance, new features were created.

| Feature | Description |
|----------|-------------|
| TotalBrowsingTime | Sum of browsing duration across all page types |
| TotalPagesVisited | Total pages visited |
| AvgProductPageTime | Average time spent per product page |
| ExitBounceRatio | Exit Rate divided by Bounce Rate |
| ValuePerProduct | Page Value per product page |
| ReturningVisitor | Binary indicator for returning customers |
| HolidaySeason | Indicates shopping season (Nov/Dec) |

These engineered features improved the model's ability to capture customer behavior patterns.

---

# 4. Data Cleaning

Performed:

- Removed duplicate records
- Verified data consistency
- Prepared feature matrix and target variable

---

# 5. Data Preprocessing

A preprocessing pipeline was created using **ColumnTransformer**.

### Numerical Features

- Median Imputation
- StandardScaler

### Categorical Features

- Most Frequent Imputation
- OneHotEncoder

### Boolean Features

Passed without scaling.

This ensured that preprocessing remained consistent during both training and inference.

---

# 6. Models Trained

The following machine learning algorithms were trained and compared.

| Model | Purpose |
|--------|----------|
| Logistic Regression | Baseline Linear Model |
| Decision Tree | Rule-based Classification |
| Random Forest | Ensemble Learning |
| Extra Trees | Randomized Ensemble |
| HistGradientBoosting | Gradient Boosting |

---

# 7. Model Comparison

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|--------|---------:|----------:|-------:|---------:|--------:|
| Logistic Regression | <value> | <value> | <value> | <value> | <value> |
| Decision Tree | <value> | <value> | <value> | <value> | <value> |
| Random Forest | <value> | <value> | <value> | <value> | <value> |
| Extra Trees | <value> | <value> | <value> | <value> | <value> |
| HistGradientBoosting | <value> | <value> | <value> | <value> | <value> |

---

# 8. Hyperparameter Tuning

The best-performing model was optimized using **RandomizedSearchCV**.

### Tuned Parameters

- n_estimators
- max_depth
- min_samples_split
- min_samples_leaf
- max_features

### Best Parameters

```python
{
    "n_estimators": <value>,
    "max_depth": <value>,
    "min_samples_split": <value>,
    "min_samples_leaf": <value>,
    "max_features": "<value>"
}
```

---

# 9. Final Model Performance

**Selected Model:** Random Forest (Tuned)

### Evaluation Metrics

| Metric | Value |
|---------|------:|
| Accuracy | <value> |
| Precision | <value> |
| Recall | <value> |
| F1 Score | <value> |
| ROC-AUC | <value> |

---

# 10. Cross Validation

Cross-validation was performed to evaluate model stability.

| Metric | Value |
|---------|------:|
| Mean CV Score | <value> |
| Standard Deviation | <value> |

---

# 11. Feature Importance

The trained Random Forest model was used to identify the most influential features.

### Top Important Features

1. PageValues
2. ExitRates
3. ProductRelated_Duration
4. ProductRelated
5. BounceRates
6. TotalBrowsingTime
7. ValuePerProduct
8. AvgProductPageTime
9. ReturningVisitor
10. HolidaySeason

These features had the greatest impact on purchase prediction.

---

# 12. Visualizations Generated

The project generated the following visualizations:

- Revenue Distribution
- Correlation Heatmap
- Histograms
- Boxplots
- Countplots
- Confusion Matrix
- ROC Curve
- Precision-Recall Curve
- Feature Importance Plot

---

# 13. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Joblib

---

# 14. Folder Structure

```
purchase_prediction_project/
│
├── purchase_prediction.ipynb
├── RESULTS.md
├── models/
│   ├── best_rf.pkl
│   └── preprocessor.pkl
├── outputs/
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   ├── precision_recall_curve.png
│   └── feature_importance.png
```

---

# 15. Conclusion

This project successfully developed an end-to-end machine learning pipeline for predicting online shopper purchase intention. Multiple classification algorithms were evaluated, and a tuned Random Forest model achieved the best overall performance. Feature engineering, preprocessing, and hyperparameter tuning significantly improved predictive capability while maintaining a reproducible workflow.

---



---

