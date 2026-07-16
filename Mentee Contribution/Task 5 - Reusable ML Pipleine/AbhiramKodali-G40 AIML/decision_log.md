# Decision Log

| Decision Area | Decision Taken | Reason |
| --- | --- | --- |
| Removed column | Removed `CustomerID` | It is only an identifier and does not help the model learn churn behavior. |
| Train-test split | Used `test_size=0.2` | 20% of the data is used for testing and the remaining 80% is used for training. |
| Stratification | Used `stratify=y` | Keeps the churn and non-churn ratio similar in training and testing data. |
| Missing numeric values | Used median imputation | Median is stable and handles outliers better than the mean. |
| Missing categorical values | Used most frequent value | Replaces missing categories with the most common observed category. |
| Encoding | Used `OneHotEncoder(handle_unknown="ignore")` | Converts text categories into numeric columns and safely handles new categories during future prediction. |
| Scaling | Used `StandardScaler` | Brings numerical columns to a similar scale inside the pipeline. |
| Model | Used `RandomForestClassifier(random_state=42)` | Random Forest works well for classification and can learn nonlinear patterns. |
| Evaluation | Used accuracy, confusion matrix, precision, recall, and F1-score | Churn prediction is a classification problem, and recall helps identify customers likely to leave. |
| Reusability | Saved the complete pipeline using `joblib` | The same preprocessing and model steps can be reused for future customers. |

## OneHotEncoder Explanation

Machine learning models cannot directly understand text values such as `Monthly`, `Yearly`, or `Two-Year`. `OneHotEncoder` converts these categories into separate numeric columns.

Example:

| ContractType | ContractType_Monthly | ContractType_Yearly | ContractType_Two-Year |
| --- | ---: | ---: | ---: |
| Monthly | 1 | 0 | 0 |
| Yearly | 0 | 1 | 0 |
| Two-Year | 0 | 0 | 1 |

This encoding allows the model to use contract type as an input feature without treating the categories as ordered numbers.

## Random Forest Explanation

`RandomForestClassifier` is made of many decision trees. Each tree makes a classification, and the final prediction is selected by majority voting. This makes the model more stable than a single decision tree and useful for customer churn classification.
