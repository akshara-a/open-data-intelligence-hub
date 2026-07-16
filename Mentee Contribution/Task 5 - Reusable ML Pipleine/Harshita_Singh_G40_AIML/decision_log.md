Decision Log
Mini Project 2 - Customer Churn Prediction Pipeline


1. Dataset
   Decision: Used Kaggle Telco Customer Churn dataset (7043 records, 21 columns)
   Reason: Real world dataset with genuine missing values and class imbalance. More reliable than synthetic data.

2. Removed Column
   Decision: customerID column was not present in this dataset version
   Reason: The dataset downloaded from Kaggle did not include customerID so the drop step was skipped.

3. TotalCharges Fix
   Decision: Used pd.to_numeric with errors set to coerce
   Reason: TotalCharges was stored as a string column. New customers with zero tenure had blank values which caused errors. Converting to numeric and filling blanks with median fixed this.

4. Train Test Split
   Decision: 80 percent train, 20 percent test with stratify=y
   Reason: Stratification ensures both train and test sets maintain the same 73/27 churn ratio. Without it the split could be skewed.

5. Missing Value Handling for Numbers
   Decision: Used median imputation
   Reason: Median is not affected by outliers. TotalCharges has high variance so median is safer than mean.

6. Missing Value Handling for Categories
   Decision: Used most frequent value imputation
   Reason: Filling with the most common category preserves the existing distribution.

7. Encoding
   Decision: Used OneHotEncoder with handle_unknown set to ignore
   Reason: Machine learning models cannot read text. OneHotEncoder converts categories to 0 and 1 columns. Setting handle_unknown to ignore prevents crashes when new categories appear at prediction time.

8. Scaling
   Decision: Used StandardScaler on numerical columns
   Reason: tenure ranges from 0 to 72 while TotalCharges ranges from 0 to 8000. Scaling brings all numerical columns to the same range.

9. Feature Engineering
   Decision: Added AvgMonthlySpend, IsNewCustomer, NumServices, NoProtection, ChargesTier
   Reason: These features capture patterns not visible in raw columns. For example IsNewCustomer flags customers in their first 6 months who have the highest churn risk.

10. Model
    Decision: Used RandomForestClassifier as required by the assignment
    Reason: Random Forest builds many decision trees and takes a majority vote. It handles nonlinear patterns and works well for classification problems.

11. class_weight Parameter
    Decision: Set class_weight to balanced
    Reason: Only 27 percent of customers churned. Without balancing the model ignores the minority churn class and predicts No for almost everyone.

12. Accuracy Result
    Decision: Final accuracy is 77 percent
    Reason: This is consistent with published benchmarks for Random Forest on the Telco churn dataset. The realistic ceiling for RF on this data is around 80 percent due to class imbalance and noise in real world data.

13. Pipeline Reusability
    Decision: Saved the full pipeline using joblib
    Reason: joblib saves the entire pipeline including the imputer, scaler, encoder, and model. Loading the file allows prediction on new customers without repeating any preprocessing steps.
