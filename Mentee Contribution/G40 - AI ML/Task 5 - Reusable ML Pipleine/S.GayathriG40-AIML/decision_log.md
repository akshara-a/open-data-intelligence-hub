# Decision Log - Customer Churn Prediction Pipeline


## Project

Reusable Customer Churn Prediction Pipeline using Scikit-learn


## Technical Decisions


| Decision Area | Decision Taken | Reason |
|---|---|---|
| Dataset | Used Telco Customer Churn Dataset | Contains customer details and churn information required for prediction |
| Removed Column | Removed customerID | It is only a unique identifier and does not provide useful learning information |
| Target Column | Used Churn as target variable | It represents whether the customer leaves the service or not |
| Train-Test Split | Used 80:20 split | 80% data is used for training and 20% for testing model performance |
| Stratification | Used stratify=y | Maintains the same churn/non-churn ratio in training and testing data |
| Missing Numerical Values | Used Median Imputation | Median is less affected by outliers compared to mean |
| Missing Categorical Values | Used Most Frequent Imputation | Replaces missing categories with the common value |
| Feature Scaling | Used StandardScaler | Brings numerical features into a common scale |
| Encoding Method | Used OneHotEncoder | Converts categorical text values into numerical format for ML model |
| Preprocessing | Used ColumnTransformer | Applies different preprocessing methods to different column types |
| Model Selection | Used RandomForestClassifier | Handles classification problems and learns complex patterns |
| Pipeline Creation | Used sklearn Pipeline | Combines preprocessing and model training into one reusable workflow |
| Evaluation | Used Accuracy, Confusion Matrix and Classification Report | Measures model performance |
| Model Saving | Used joblib | Saves the complete pipeline for future predictions |


## Final Decision

A reusable machine learning pipeline was created that automatically performs:

- Missing value handling
- Feature scaling
- Categorical encoding
- Model training
- Prediction

The saved pipeline can be reused for predicting churn of new customers without repeating preprocessing steps.