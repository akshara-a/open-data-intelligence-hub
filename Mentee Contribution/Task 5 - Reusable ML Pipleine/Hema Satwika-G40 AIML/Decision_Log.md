# Decision Log - Customer Churn Prediction Pipeline

## Project

Reusable Machine Learning Pipeline for Customer Churn Prediction

## Technical Decisions

| Decision Area              | Decision Taken                                    | Reason                                                           |
| -------------------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| Dataset                    | Telco Customer Churn Dataset                      | Contains customer information and churn status                   |
| Removed Column             | customerID                                        | Unique identifier, not useful for prediction                     |
| Target Variable            | Churn                                             | Represents whether the customer leaves the service               |
| Train-Test Split           | 80% Training, 20% Testing                         | Standard machine learning practice                               |
| Missing Numerical Values   | Median Imputation                                 | Handles missing values effectively                               |
| Missing Categorical Values | Most Frequent Imputation                          | Replaces missing values with the most common category            |
| Feature Scaling            | StandardScaler                                    | Scales numerical features                                        |
| Encoding                   | OneHotEncoder                                     | Converts categorical features into numerical format              |
| Preprocessing              | ColumnTransformer                                 | Applies different preprocessing steps to different feature types |
| Model                      | Logistic Regression                               | Suitable for binary classification problems                      |
| Pipeline                   | Scikit-learn Pipeline                             | Combines preprocessing and model training                        |
| Evaluation                 | Accuracy, Confusion Matrix, Classification Report | Measures model performance                                       |
| Model Saving               | Joblib                                            | Saves the trained pipeline for future predictions                |

## Final Decision

A reusable machine learning pipeline was developed that automatically performs data preprocessing, feature scaling, categorical encoding, model training, prediction, and evaluation. The trained pipeline was saved using Joblib for future reuse.
