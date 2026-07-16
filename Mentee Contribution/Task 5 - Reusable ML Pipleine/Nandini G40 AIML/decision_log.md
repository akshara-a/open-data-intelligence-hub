# Decision Log

## Customer Churn Prediction Pipeline

This document explains the important decisions made while building the customer churn prediction pipeline.

### 1. Removing CustomerID
The **CustomerID** column was removed because it is only used to identify customers. It does not help the model in predicting whether a customer will churn.

### 2. Splitting the Dataset
The dataset was divided into **80% training data** and **20% testing data** using `test_size=0.2`. This allows the model to learn from most of the data while keeping some data for testing its performance.

### 3. Handling Missing Values
Missing values in numerical columns were filled using the **median**, and missing values in categorical columns were filled using the **most frequent value**. This helps prevent errors during model training.

### 4. Encoding Categorical Data
Categorical columns such as Gender, Contract Type, Payment Method, and Internet Service were converted into numerical values using **OneHotEncoder** because machine learning models cannot work directly with text data.

### 5. Scaling Numerical Features
Numerical features were standardized using **StandardScaler** so that all values are on a similar scale. This helps improve the preprocessing process and keeps the pipeline consistent.

### 6. Choosing the Model
A **Random Forest Classifier** was selected because it is a reliable algorithm for classification problems. It can handle different types of data and usually provides good prediction accuracy.

### 7. Creating a Reusable Pipeline
A Scikit-learn **Pipeline** was created to combine preprocessing and model training into one workflow. This makes the code cleaner and allows the same steps to be reused for new customer data.

### 8. Saving the Pipeline
The trained pipeline was saved as a **.pkl** file using Joblib. This makes it possible to load the model later and make predictions without training it again.

## Conclusion

These decisions were made to build a simple, organized, and reusable machine learning pipeline. The final pipeline can preprocess new customer data and predict customer churn efficiently.