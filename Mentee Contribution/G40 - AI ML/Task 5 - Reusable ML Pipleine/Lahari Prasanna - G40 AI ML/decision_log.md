# Decision Log — Mini Project 2: Customer Churn Prediction Pipeline

**Student:** Lahari Prasanna Desetty
**Dataset:** Telco Customer Churn (adapted)
**Model:** RandomForestClassifier via scikit-learn Pipeline

---

## Dataset Preparation Decisions

### 1. Dataset Selection
**Decision:** Used the Telco Customer Churn dataset from Kaggle (blastchar/telco-customer-churn)

**Reason:** The dataset closely matches all assignment-required columns. It contains real-world customer subscription data with a mix of numerical and categorical features, making it ideal for demonstrating a reusable ML pipeline.

### 2. Column Renaming
**Decision:** Renamed `customerID` → `CustomerID`, `gender` → `Gender`, `tenure` → `Tenure`, `Contract` → `ContractType`

**Reason:** To match the exact column names specified in the assignment requirements for consistency and clarity.

### 3. Adding Missing Columns
**Decision:** Added `Age` (random integers 18–70) and `SupportTickets` (random integers 0–10) using `np.random.seed(42)`

**Reason:** The assignment requires these columns. `random_state=42` ensures reproducibility — the same values are generated every time the notebook runs.

### 4. Dropping Extra Columns
**Decision:** Kept only the 11 assignment-required columns and dropped all other Telco columns (`SeniorCitizen`, `Partner`, `Dependents`, `PhoneService`, etc.)

**Reason:** The extra columns are not part of the assignment specification. Keeping them would add noise and make the pipeline harder to interpret and explain.

---

## Pipeline Design Decisions

| Decision Area | Decision Taken | Reason |
|---|---|---|
| Removed column | Removed `CustomerID` | It is only a unique identifier and does not help the model learn churn behaviour. Including it would add noise with no predictive value. |
| Train-test split | Used 80:20 split (`test_size=0.2`) | 80% of data (5,634 rows) is used for training and 20% (1,409 rows) for testing. This gives the model enough data to learn while keeping a meaningful held-out set for evaluation. |
| Stratification | Used `stratify=y` | The dataset is imbalanced — 73.46% No and 26.54% Yes. Without stratification, the random split might put most churn cases in one set. `stratify=y` ensures both train and test sets maintain the same 73/27 ratio. |
| Missing numeric values | Used `SimpleImputer(strategy="median")` | `TotalCharges` had 11 hidden missing values (blank spaces converted to NaN). Median imputation is preferred over mean because it is not affected by outliers — `TotalCharges` ranges from 18.80 to 8,684.80, making the median a more stable fill value. |
| Missing categorical values | Used `SimpleImputer(strategy="most_frequent")` | Fills any missing categorical values with the most commonly occurring category. This preserves the natural distribution of the data without introducing an arbitrary value. |
| Encoding | Used `OneHotEncoder(handle_unknown="ignore")` | Machine learning models cannot process text values like "Month-to-month" or "Electronic check" directly. OneHotEncoder converts each unique category into a separate 0/1 binary column. `handle_unknown="ignore"` prevents errors when new unseen categories appear in future prediction data. |
| Scaling | Used `StandardScaler()` | Numerical columns like `Age` (18–70), `Tenure` (0–72), `MonthlyCharges` (18–118), and `TotalCharges` (18–8684) are on very different scales. StandardScaler brings all of them to mean=0 and std=1 so no single column dominates the model. |
| Preprocessing architecture | Used `ColumnTransformer` | Numerical and categorical columns require completely different preprocessing steps. `ColumnTransformer` applies the correct pipeline to each column type automatically, cleanly, and without manual separation. |
| Model | Used `RandomForestClassifier(random_state=42)` | Random Forest is an ensemble model made of many decision trees. It handles non-linear relationships, is robust to outliers, and works well for classification problems like churn prediction. `random_state=42` ensures reproducible results. |
| Data leakage prevention | Fitted pipeline only on `X_train` | All preprocessing steps (imputer medians, scaler means, encoder categories) are learned exclusively from training data. Applying them to test data without re-fitting prevents data leakage — the model never "sees" test data during training. |
| Evaluation metrics | Used accuracy, confusion matrix, classification report | Churn is a classification problem. These metrics together give a complete picture — accuracy for overall correctness, precision and recall for class-specific performance, and the confusion matrix for detailed breakdown of correct and incorrect predictions. |
| Reusability | Saved complete pipeline using `joblib` | The `.pkl` file contains the entire pipeline — preprocessing rules, learned parameters, and the trained model — in one file. It can be loaded and used for prediction on any new customer data without repeating any preprocessing steps. |

---

## Key Finding During Exploration

**TotalCharges Hidden Missing Values:**
During data exploration, `TotalCharges` was found to have dtype `object` instead of `float64`. This was caused by blank spaces `" "` in the original Telco dataset that pandas could not convert to numbers. After applying `pd.to_numeric(errors="coerce")`, these blank spaces became 11 real `NaN` values — which were then correctly handled by the `SimpleImputer` inside the pipeline.

This demonstrates a real-world data quality issue and shows why missing value handling inside the pipeline is important.
