# Model Evaluation Report

## Customer Churn Prediction Pipeline

After training the machine learning model, its performance was evaluated using the test dataset. Different evaluation metrics were used to understand how well the model predicts whether a customer will churn or not.

### Accuracy

Accuracy shows the overall percentage of correct predictions made by the model. A higher accuracy means the model correctly predicts most of the customer records.

### Precision

Precision measures how many customers predicted as likely to churn actually churned. High precision means the model makes fewer incorrect churn predictions.

### Recall

Recall measures how many actual churn customers were correctly identified by the model. This is important because it helps the business identify customers who may leave the service.

### F1-Score

The F1-score combines both precision and recall into a single value. It provides a balanced measure of the model's performance, especially when both false positive and false negative predictions are important.

### Confusion Matrix

The confusion matrix compares the predicted values with the actual values. It shows the number of correct and incorrect predictions, helping us understand where the model performs well and where it makes mistakes.

## Overall Performance

Based on the evaluation metrics, the model performs well in predicting customer churn. The results show that the pipeline can make reliable predictions on new customer data and can be reused without repeating the preprocessing steps.

## Business Importance

A well-performing churn prediction model helps businesses identify customers who are likely to leave. This allows the company to take preventive actions such as offering discounts, improving customer support, or providing personalized services. As a result, customer retention can improve, leading to increased customer satisfaction and business growth.