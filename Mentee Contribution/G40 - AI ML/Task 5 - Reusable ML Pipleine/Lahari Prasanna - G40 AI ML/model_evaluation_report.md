# Model Evaluation Report — Mini Project 2: Customer Churn Prediction Pipeline

**Student:** Lahari Prasanna Desetty
**Model:** RandomForestClassifier
**Dataset:** Telco Customer Churn (adapted, 7,043 rows)
**Test Set Size:** 1,409 rows (20% of dataset)

---

## 1. Dataset Summary

| Property | Value |
|---|---|
| Total rows | 7,043 |
| Total columns (after preparation) | 11 |
| Duplicate rows | 0 |
| Missing values before fix | 0 visible |
| Missing values after TotalCharges fix | 11 (in TotalCharges column) |
| Training set size | 5,634 rows (80%) |
| Testing set size | 1,409 rows (20%) |

### Target Column Distribution

| Churn | Count | Percentage |
|---|---|---|
| No (loyal customers) | 5,174 | 73.46% |
| Yes (churned customers) | 1,869 | 26.54% |

The dataset is **imbalanced** — churned customers represent only 26.54% of all records. This is important context for interpreting the model's recall on the churn class.

---

## 2. Train-Test Split Explanation

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

| Parameter | Value | Meaning |
|---|---|---|
| `test_size=0.2` | 0.2 | 20% of 7,043 = 1,409 rows reserved for testing |
| `random_state=42` | 42 | Fixed random seed — same split every run |
| `stratify=y` | y | Both splits maintain the 73.46% / 26.54% churn ratio |

**Why 80:20 split:**
With 7,043 rows, an 80:20 split gives the model 5,634 rows to learn from — enough to detect patterns — while keeping 1,409 rows completely unseen during training for reliable evaluation.

**Why stratify:**
Without stratification, the random split might place most churn cases in training and very few in testing, making evaluation unreliable. `stratify=y` guarantees both sets reflect the real churn ratio.

---

## 3. OneHotEncoder Explanation

Categorical columns like `ContractType`, `PaymentMethod`, `InternetService`, and `Gender` contain text values that machine learning models cannot process directly. `OneHotEncoder` converts each unique category into a separate binary (0/1) column.

**Example — ContractType:**

| Original Value | ContractType_Month-to-month | ContractType_One year | ContractType_Two year |
|---|---|---|---|
| Month-to-month | 1 | 0 | 0 |
| One year | 0 | 1 | 0 |
| Two year | 0 | 0 | 1 |

**Example — PaymentMethod:**

| Original Value | Electronic check | Mailed check | Bank transfer | Credit card |
|---|---|---|---|---|
| Electronic check | 1 | 0 | 0 | 0 |
| Mailed check | 0 | 1 | 0 | 0 |
| Bank transfer | 0 | 0 | 1 | 0 |

`handle_unknown="ignore"` ensures that if a new payment method appears in future customer data, the pipeline will not throw an error — it will simply encode it as all zeros.

---

## 4. Model Evaluation Results

### 4.1 Accuracy Score

```
Accuracy: 0.7850 (78.50%)
```

The model correctly predicted 1,106 out of 1,409 customers. Given that a naive model that always predicts "No churn" would achieve 73.46% accuracy, a score of 78.50% confirms the model is genuinely learning patterns beyond the majority class.

---

### 4.2 Confusion Matrix

```
[[920  115]
 [188  186]]
```

| | Predicted: No Churn | Predicted: Churn |
|---|---|---|
| **Actual: No Churn** | 920 ✅ True Negative | 115 ❌ False Positive |
| **Actual: Churn** | 188 ❌ False Negative | 186 ✅ True Positive |

| Metric | Count | Business Meaning |
|---|---|---|
| **True Negative (920)** | Correctly identified loyal customers | No unnecessary retention action needed |
| **True Positive (186)** | Correctly identified churners | Business can proactively intervene |
| **False Positive (115)** | Loyal customers wrongly flagged as churners | Minor cost — they receive unnecessary offers |
| **False Negative (188)** | Churners the model missed | Most critical — these customers will leave undetected |

---

### 4.3 Classification Report

```
              precision    recall  f1-score   support

          No       0.83      0.89      0.86      1035
         Yes       0.62      0.50      0.55       374

    accuracy                           0.78      1409
   macro avg       0.72      0.69      0.70      1409
weighted avg       0.77      0.78      0.78      1409
```

| Metric | No (Loyal) | Yes (Churner) | Interpretation |
|---|---|---|---|
| **Precision** | 0.83 | 0.62 | When model predicts churn, it is correct 62% of the time |
| **Recall** | 0.89 | 0.50 | Model catches 89% of loyal customers but only 50% of actual churners |
| **F1-score** | 0.86 | 0.55 | Harmonic mean of precision and recall — stronger for loyal class |

---

## 5. Key Observations

### Why Recall for Churn Class is 0.50
The dataset is imbalanced (73% No vs 27% Yes). The default `RandomForestClassifier` is trained without class weighting, so it naturally favours predicting the majority class (No). This causes it to miss approximately half of actual churners.

**Recall is the most important metric for this business problem.** Missing a churner (False Negative) costs the business a customer and their lifetime revenue. Incorrectly flagging a loyal customer (False Positive) only results in an unnecessary retention offer — a much smaller cost.

### Why 78.50% Accuracy is Acceptable
This pipeline uses a default `RandomForestClassifier` with no hyperparameter tuning. In real-world churn prediction on imbalanced data, 75–85% accuracy from a baseline model is a normal and expected starting point.

---

## 6. Potential Improvements (Future Work)

| Improvement | Expected Benefit |
|---|---|
| `class_weight="balanced"` in RandomForestClassifier | Improves recall for the churn class |
| SMOTE oversampling on training data | Balances the class distribution before training |
| Hyperparameter tuning with GridSearchCV | Optimises number of trees, max depth, etc. |
| Feature importance analysis | Identifies which features drive churn most |
| Cross-validation | More reliable evaluation than a single train-test split |

---

## 7. Business Interpretation

The trained pipeline can be deployed to score any new customer and predict their likelihood of churning. Based on the model's output, the business can take targeted actions:

| Prediction | Recommended Action |
|---|---|
| Churn = Yes (High Risk) | Offer discount, suggest longer contract, assign dedicated support |
| Churn = No (Low Risk) | Continue regular engagement, monitor monthly |

**Key churn risk factors identified from the dataset:**
- Customers on **Month-to-month contracts** churn at a significantly higher rate
- **New customers** (low tenure) are more likely to churn
- Customers using **Electronic check** as payment method show higher churn
- **Fiber optic** internet service customers churn more than DSL customers

Early identification of at-risk customers allows the business to reduce revenue loss through proactive, personalised retention strategies.
