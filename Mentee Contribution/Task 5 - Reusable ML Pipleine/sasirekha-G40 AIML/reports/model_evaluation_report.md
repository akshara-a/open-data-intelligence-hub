# Model Evaluation Report

## Mini Project 2: Reusable Customer Churn Prediction Pipeline using scikit-learn

### Student Name

**Sasi Rekha**

---

# 1. Project Objective

The objective of this project is to build a reusable machine learning pipeline using **scikit-learn** to predict whether a customer is likely to churn. The pipeline performs preprocessing, model training, evaluation, and prediction in a single reusable workflow.

---

# 2. Model Used

**RandomForestClassifier**

Random Forest is an ensemble learning algorithm that builds multiple decision trees and combines their predictions using majority voting. It is well suited for classification problems such as customer churn prediction because it can capture complex patterns while reducing overfitting.

---

# 3. Evaluation Metrics

The trained model was evaluated using the testing dataset (20% of the total data).

| Metric                |      Value |
| --------------------- | ---------: |
| **Accuracy**          | **97.60%** |
| **Precision (Churn)** |   **100%** |
| **Recall (Churn)**    |    **86%** |
| **F1-Score (Churn)**  |    **92%** |

---

# 4. Classification Report

```text
              precision    recall  f1-score   support

           0       0.97      1.00      0.99       936
           1       1.00      0.86      0.92       190

    accuracy                           0.98      1126
   macro avg       0.99      0.93      0.95      1126
weighted avg       0.98      0.98      0.98      1126
```

---

# 5. Interpretation of Results

### Accuracy

The model achieved an overall **accuracy of 97.60%**, indicating that it correctly classified the vast majority of customers in the test dataset.

---

### Precision

The model achieved **100% precision** for predicting churned customers.

This means that whenever the model predicted a customer would churn, the prediction was correct. There were virtually no false positive predictions for the churn class.

---

### Recall

The recall for churn prediction is **86%**.

This indicates that the model successfully identified **86% of the customers who actually churned**. A small percentage of churning customers were missed.

---

### F1-Score

The **F1-score of 92%** demonstrates an excellent balance between precision and recall, indicating that the model performs reliably for churn prediction.

---

# 6. Business Interpretation

The developed machine learning pipeline can help businesses:

* Identify customers who are at high risk of leaving.
* Launch targeted retention campaigns before customers churn.
* Improve customer support for dissatisfied customers.
* Offer personalized discounts and loyalty rewards.
* Reduce customer attrition and increase long-term revenue.
* Enable proactive decision-making based on predictive analytics.

Because the model has **100% precision**, businesses can confidently focus retention efforts on customers predicted to churn. The **86% recall** also means that most at-risk customers are successfully detected.

---

# 7. Strengths of the Model

* High prediction accuracy (**97.60%**).
* Excellent precision for churn prediction.
* Strong F1-score indicating balanced performance.
* Handles both numerical and categorical features automatically.
* Uses a reusable Scikit-learn Pipeline.
* Prevents data leakage by performing preprocessing only on training data.
* Can be saved and reused for future customer predictions using Joblib.

---

# 8. Limitations

* Approximately **14%** of actual churning customers were not identified (false negatives).
* Model performance may improve further through hyperparameter tuning or additional feature engineering.
* Future versions could compare Random Forest with other algorithms such as XGBoost, LightGBM, or Gradient Boosting.

---

# 9. Conclusion

The reusable machine learning pipeline successfully preprocesses customer data, trains a RandomForestClassifier, and predicts customer churn with high accuracy.

The model achieved an overall **accuracy of 97.60%**, **100% precision**, **86% recall**, and an **F1-score of 92%** for the churn class. These results demonstrate that the pipeline is effective in identifying customers who are likely to leave the service.

The trained pipeline has been saved using **Joblib**, making it reusable for future customer data without requiring manual preprocessing. This project demonstrates a production-ready machine learning workflow suitable for real-world customer churn prediction.
