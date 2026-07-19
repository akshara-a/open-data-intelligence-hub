# Decision Log

## Dataset
- Created a synthetic customer churn dataset with 1000 records to support a complete college mini-project workflow.
- Included customer profile, account, billing, service, and support-ticket fields that commonly influence churn.
- Kept `CustomerID` only as an identifier and removed it before training to avoid learning from non-predictive IDs.

## Preprocessing
- Used median imputation for numerical columns because it is robust to outliers.
- Used most frequent imputation for categorical columns because it preserves common category patterns.
- Used `StandardScaler` for numerical columns because Logistic Regression performs better when numeric features are scaled.
- Used `OneHotEncoder(handle_unknown="ignore")` so the pipeline can safely handle unseen categories during prediction.

## Model
- Selected `LogisticRegression(max_iter=1000)` because it is interpretable, fast, and suitable for a baseline churn classifier.
- Used a single Scikit-Learn `Pipeline` so preprocessing and model inference are reusable and saved together.

## Evaluation
- Used stratified train-test split to preserve the original churn ratio in both training and test sets.
- Reported accuracy, precision, recall, F1-score, confusion matrix, and classification report for a balanced evaluation view.
