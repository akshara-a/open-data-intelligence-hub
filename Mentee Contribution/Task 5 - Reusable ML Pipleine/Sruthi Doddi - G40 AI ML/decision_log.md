# Decision Log

## Project: Reusable Customer Churn Prediction Pipeline using scikit-learn

This document explains the important technical decisions taken during the development of the customer churn prediction pipeline.

| Decision Area                 | Decision Taken                                                                         | Reason                                                                                                               |
| ----------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Dataset Selection             | Used a customer churn dataset containing customer demographic and subscription details | The dataset contains relevant information required to predict customer churn                                         |
| Removed Column                | Removed `customerID` column                                                            | `customerID` is only an identifier and does not contribute to churn prediction                                       |
| Feature and Target Separation | Selected all columns except `Churn` as features and `Churn` as target                  | Machine learning models require independent variables (`X`) and dependent variable (`y`)                             |
| Train-Test Split              | Used `train_test_split()` with `test_size=0.2`                                         | An 80:20 split helps evaluate model performance on unseen data                                                       |
| Random State                  | Used `random_state=42`                                                                 | Ensures reproducibility by generating the same train-test split every time                                           |
| Stratification                | Used `stratify=y`                                                                      | Maintains the same proportion of churn and non-churn records in both train and test datasets                         |
| Numerical Missing Values      | Used `SimpleImputer(strategy='median')`                                                | Median is robust to outliers and is suitable for numerical features                                                  |
| Categorical Missing Values    | Used `SimpleImputer(strategy='most_frequent')`                                         | Replaces missing categorical values with the most common category                                                    |
| Numerical Feature Scaling     | Used `StandardScaler()`                                                                | Standardization brings all numerical features to a similar scale                                                     |
| Categorical Encoding          | Used `OneHotEncoder(handle_unknown='ignore')`                                          | Machine learning algorithms cannot process text directly, so categorical variables are converted to numerical format |
| Preprocessing Framework       | Used `ColumnTransformer`                                                               | Allows different preprocessing techniques for numerical and categorical columns                                      |
| Pipeline Construction         | Used `Pipeline`                                                                        | Combines preprocessing and model training into a single reusable workflow                                            |
| Machine Learning Model        | Used `RandomForestClassifier`                                                          | Random Forest handles nonlinear relationships, reduces overfitting, and performs well on classification tasks        |
| Evaluation Metrics            | Used Accuracy, Confusion Matrix, and Classification Report                             | These metrics provide a comprehensive evaluation of classification performance                                       |
| Pipeline Persistence          | Saved the complete pipeline using `joblib`                                             | Enables future reuse without repeating preprocessing and training steps                                              |
| New Data Prediction           | Used the saved pipeline to predict churn for new customer records                      | Demonstrates the reusability of the machine learning pipeline                                                        |

## Summary

The project was designed to create a reusable, production-ready machine learning workflow. All preprocessing steps, model training, evaluation, and prediction processes were integrated into a single scikit-learn pipeline to avoid data leakage and improve maintainability.
