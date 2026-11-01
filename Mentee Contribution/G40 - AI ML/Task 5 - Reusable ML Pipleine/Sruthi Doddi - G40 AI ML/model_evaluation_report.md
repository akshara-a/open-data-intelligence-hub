# Model Evaluation Report

## Project: Reusable Customer Churn Prediction Pipeline using scikit-learn

## Introduction

After training the Random Forest classification model, the model was evaluated on unseen test data to measure its predictive performance. The evaluation helps determine how well the model can identify customers who are likely to churn.

## Evaluation Metrics Used

The following evaluation metrics were used:

1. Accuracy Score
2. Confusion Matrix
3. Classification Report

---

## 1. Accuracy Score

Accuracy represents the proportion of correctly classified instances among all predictions.

### Formula

Accuracy = (Number of Correct Predictions) / (Total Number of Predictions)

### Interpretation

A high accuracy score indicates that the model correctly classifies most customers.

Example:

If the model correctly predicts 180 customers out of 200 customers:

Accuracy = 180 / 200 = 0.90 (90%)

---

## 2. Confusion Matrix

A confusion matrix summarizes prediction results by comparing actual values with predicted values.

| Actual / Predicted | No Churn             | Churn                |
| ------------------ | -------------------- | -------------------- |
| No Churn           | True Negatives (TN)  | False Positives (FP) |
| Churn              | False Negatives (FN) | True Positives (TP)  |

### Interpretation

* **True Positive (TP):** Customer churned and the model predicted churn.
* **True Negative (TN):** Customer did not churn and the model predicted no churn.
* **False Positive (FP):** Customer did not churn but the model predicted churn.
* **False Negative (FN):** Customer churned but the model predicted no churn.

False negatives are especially important because missing a customer who is likely to churn may result in revenue loss.

---

## 3. Classification Report

The classification report provides the following metrics:

### Precision

Precision measures how many predicted churn customers actually churned.

Formula:

Precision = TP / (TP + FP)

High precision means fewer false alarms.

### Recall

Recall measures how many actual churn customers were correctly identified.

Formula:

Recall = TP / (TP + FN)

Recall is highly important in churn prediction because businesses do not want to miss customers who are likely to leave.

### F1-Score

F1-score is the harmonic mean of precision and recall.

Formula:

F1-score = 2 × (Precision × Recall) / (Precision + Recall)

A high F1-score indicates a good balance between precision and recall.

---

## Business Interpretation

The trained model can help businesses proactively identify customers who are likely to leave the service.

Possible business actions include:

* Providing personalized retention offers.
* Offering discounts to high-risk customers.
* Improving customer support quality.
* Designing loyalty programs.
* Creating targeted marketing campaigns.

Early identification of churn customers can significantly reduce customer loss and improve business profitability.

---

## Conclusion

The Random Forest-based reusable machine learning pipeline successfully predicts customer churn using customer demographic and subscription information. The evaluation metrics demonstrate the effectiveness of the model, while the reusable pipeline architecture allows future predictions without repeating preprocessing steps.
