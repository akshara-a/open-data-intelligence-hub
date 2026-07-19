decision\_log.md



\# Decision Log - Customer Churn Prediction Pipeline



**# Project Details**

Project:= Customer Churn Prediction using Reusable ML Pipeline

Dataset:= Kaggle dataset (Telco Customer Churn)

Model:= RandomForestClassifier



**## Technical Decisions Table**



| Decision Area  Decision Taken | Reason



* Dataset Selection:=  Used Kaggle Telco Churn Dataset , It is a standard industry dataset for churn prediction. manual upload needed.
* Column Removal:= Removed "customerID"  It is a unique identifier for each row. ML models cannot learn patterns from IDs, and it causes overfitting. 
* Target Encoding:= Mapped "Churn"(Yes/No) to (1/0), Scikit-learn requires numeric target variables for classification. 
* TotalCharges Cleaning:=| Used "pd.to\_numeric(errors='coerce')",Dataset had blank/empty values in TotalCharges. Converting to NaN is the first step before imputation.
* Train-Test Split:= Used 80:20 split with "stratify=y" 80% training, 20% testing is standard. Stratification ensures the churn ratio (Yes/No) remains the same in both sets, 



**preventing bias:**



Handling Missing Numeric Values:= "SimpleImputer(strategy='median')"  Median is robust to outliers. TotalCharges and MonthlyCharges can have extreme values (high spenders).

Handling Missing Categorical Values:= "SimpleImputer(strategy='most\_frequent') Mode (most frequent value) is the safest default for categorical data. It preserves the most common 



**pattern:**

Numerical Feature Scaling:= "StandardScaler() Standardizes features to mean=0 and std=1. This ensures the model treats all numeric features (tenure, charges) equally without bias toward             larger numbers. 

Categorical Feature Encoding:="OneHotEncoder(handle\_unknown='ignore')" Converts text categories (e.g., Contract: Monthly, Yearly) into numeric 0/1 columns. `ignore` prevents errors if new **categories appear in production data:**

Model Selection:= "RandomForestClassifier(class\_weight='balanced') Handles non-linear relationships well without manual feature engineering. "balanced" automatically handles class **imbalance (churners are fewer than non-churners)**

Handling Age Column (PDF vs Reality):=Used "SeniorCitizen" (0/1) instead of "Age" The Kaggle dataset does not have an exact "Age" column. "SeniorCitizen" serves as a valid proxy because age matters for churn. If "Age" comes in future data, I will add it to the numeric\_features list.



Handling SupportTickets (PDF vs Reality):= Used "TechSupport" (Yes/No) instead of "SupportTickets" The Kaggle dataset does not have ticket counts. "TechSupport" indicates if the customer has support issues, which is a strong churn indicator.

&#x20;

Evaluation Metric Focus:= Used Accuracy, ROC-AUC, Precision, Recall Accuracy gives overall performance. ROC-AUC measures how well the model separates churners/non-churners. Recall is critical because we don't want to miss customers who are likely to churn.



Pipeline Structure:=Used "Pipeline" + "ColumnTransformer" | Ensures preprocessing (imputing, scaling, encoding) happens inside the pipeline. This prevents data leakage and makes the workflow reusable. |



Model Saving:=Used "joblib.dump()" Saves the entire pipeline (preprocessing + model) into a ".pkl" file. This allows direct loading and prediction without re-running preprocessing steps.



Encoding Fix for Windows:= Added "sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')"  Windows CMD/PowerShell default encoding is CP1252.



**## Final Note**



This project follows a "production-ready ML pipeline" approach. All preprocessing and modeling steps are encapsulated in a single scikit-learn pipeline, making it "reusable", "scalable", and deployable" in real-world applications.



\## Developer Signature

Name:Suraj Singh

Class:= G40 AIML



