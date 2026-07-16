# Model Evaluation Report

## Project Title

Reusable Machine Learning Pipeline for Customer Churn Prediction

## Model Used

Logistic Regression

## Dataset

Telco Customer Churn Dataset

## Data Processing

* Missing value handling
* Numerical feature scaling using StandardScaler
* Categorical feature encoding using OneHotEncoder
* Data preprocessing using ColumnTransformer
* Model training using Logistic Regression

## Train-Test Split

* Training Data: 80%
* Testing Data: 20%

## Evaluation Results

### Accuracy

**80.55%**

### Confusion Matrix

```
[[926 109]
 [165 209]]
```

### Classification Report

```
              precision    recall    f1-score   support

No              0.85      0.89      0.87      1035
Yes             0.66      0.56      0.60       374

Accuracy                             0.81      1409
Macro Avg       0.75      0.73      0.74      1409
Weighted Avg    0.80      0.81      0.80      1409
```

## Business Interpretation

The model predicts whether a customer is likely to leave the service. This helps businesses identify at-risk customers, improve retention strategies, provide personalized offers, and reduce customer churn.

## Conclusion

The Logistic Regression pipeline achieved an accuracy of **80.55%**. The complete preprocessing pipeline and trained model were saved using Joblib, allowing the model to be reused for future customer churn predictions.
