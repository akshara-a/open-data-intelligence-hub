# Decision Log

## Project

**Customer Churn Prediction using Random Forest Pipeline**

---

## Decision 1: Selected Random Forest Classifier

**Reason:**

Random Forest was selected because it provides good accuracy, reduces overfitting by combining multiple decision trees, and performs well on classification problems with mixed feature types.

---

## Decision 2: Removed customerID Column

**Reason:**

The `customerID` column is a unique identifier and does not contain meaningful information for predicting customer churn. Therefore, it was removed before training the model.

---

## Decision 3: Converted TotalCharges to Numeric

**Reason:**

The `TotalCharges` column contained blank spaces that prevented numerical preprocessing. Blank values were replaced with `NaN`, and the column was converted to numeric format.

---

## Decision 4: Used Median Imputation

**Reason:**

Missing values in numerical features were filled using the median because the median is less sensitive to outliers than the mean.

---

## Decision 5: Used Most Frequent Imputation

**Reason:**

Missing values in categorical features were filled using the most frequent category to preserve the existing data distribution.

---

## Decision 6: Applied One-Hot Encoding

**Reason:**

Machine Learning algorithms cannot directly process categorical text values. One-Hot Encoding converts categorical features into numerical format suitable for model training.

---

## Decision 7: Applied Standard Scaling

**Reason:**

StandardScaler was included in the numerical preprocessing pipeline to standardize numerical features and create a reusable preprocessing workflow.

---

## Decision 8: Used Train-Test Split

**Reason:**

The dataset was divided into 80% training data and 20% testing data to evaluate the model on unseen data and reduce the risk of data leakage.

---

## Decision 9: Used Stratified Sampling

**Reason:**

`stratify=y` was used during train-test splitting to maintain the same class distribution of the target variable in both training and testing datasets.

---

## Decision 10: Built a Reusable Pipeline

**Reason:**

A Scikit-learn Pipeline was used to combine preprocessing and model training into a single reusable workflow. This ensures that the same preprocessing steps are automatically applied during both training and prediction.

---

## Decision 11: Saved the Trained Model

**Reason:**

The trained model was saved using Joblib (`customer_churn_random_forest.pkl`) so that it can be loaded later for prediction without retraining.
