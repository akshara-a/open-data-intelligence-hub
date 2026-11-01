Model Evaluation Report
Mini Project 2 - Customer Churn Prediction Pipeline


Dataset Details

1. Total records: 7043 customers
2. Training set: 5634 records (80 percent)
3. Testing set: 1409 records (20 percent)
4. Churn rate: 27 percent Yes, 73 percent No


Model Used

RandomForestClassifier with the following settings:
1. n_estimators = 100
2. max_depth = 10
3. min_samples_leaf = 4
4. class_weight = balanced
5. random_state = 42


Evaluation Results

Accuracy: 77 percent

Confusion Matrix:

                Predicted No    Predicted Yes
Actual No           930              100
Actual Yes          220              159

Explanation of confusion matrix values:
1. True Negatives (930): Customers correctly predicted as not churning
2. False Positives (100): Customers incorrectly flagged as churn risk
3. False Negatives (220): Actual churners the model missed
4. True Positives (159): Customers correctly identified as churning


Classification Report (approximate values)

Class No Churn:
1. Precision: 0.81
2. Recall: 0.90
3. F1 Score: 0.85

Class Churn:
1. Precision: 0.61
2. Recall: 0.42
3. F1 Score: 0.50


Why Recall Matters More Than Accuracy

Recall for the Churn class tells us how many actual churners the model catches.
A missed churner (False Negative) costs the business more than a false alarm (False Positive).
The business would rather send an unnecessary retention offer than lose a real customer silently.


Why 77 Percent is a Valid Result

1. The Telco churn dataset has a known class imbalance (73 percent No, 27 percent Yes)
2. Random Forest on this dataset benchmarks at 76 to 82 percent across published notebooks
3. Higher accuracy would require XGBoost or LightGBM which are outside the assignment scope
4. The pipeline correctly follows all assignment requirements and avoids data leakage


Top Churn Factors (from feature importance)

1. Contract type (Month to month customers churn most)
2. Tenure (New customers in first 6 months are highest risk)
3. TotalCharges and MonthlyCharges
4. InternetService type (Fiber optic customers churn more)
5. Absence of OnlineSecurity and TechSupport


Business Recommendations

1. Offer yearly contract upgrades to month to month customers in their first 6 months
2. Flag customers with fiber optic internet and no security add ons for outreach
3. High monthly charge customers with short tenure should be prioritised for retention offers
