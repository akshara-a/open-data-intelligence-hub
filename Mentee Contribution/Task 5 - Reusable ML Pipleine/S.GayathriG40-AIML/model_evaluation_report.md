# Model Evaluation Report

## Project Title

Customer Churn Prediction using Reusable Machine Learning Pipeline


## Model Used

RandomForestClassifier


## Dataset

Telco Customer Churn Dataset


## Data Processing Steps

The pipeline performs:

1. Missing value handling
2. Numerical feature scaling
3. Categorical feature encoding using OneHotEncoder
4. Random Forest model training


## Train-Test Split

The dataset was divided into:

- Training Data: 80%
- Testing Data: 20%


## Evaluation Metrics


### Accuracy

Accuracy represents the percentage of correct predictions made by the model.

Accuracy:

(Add your notebook output here)



### Confusion Matrix

The confusion matrix shows:

- Correct churn predictions
- Incorrect churn predictions
- Correct non-churn predictions
- Missed churn cases


Confusion Matrix:

(Add your notebook output here)



### Classification Report

The report contains:

- Precision
- Recall
- F1-score


Classification Report:

(Add your notebook output here)



## Business Interpretation

The churn prediction model helps a subscription business identify customers who may leave the service.

By predicting possible churn customers early, the company can:

- Provide retention offers
- Improve customer support
- Create personalized plans
- Reduce customer loss


## Conclusion

The RandomForest based reusable pipeline successfully performs customer churn prediction.

The complete pipeline including preprocessing and model is saved using joblib and can be reused for future customer predictions.