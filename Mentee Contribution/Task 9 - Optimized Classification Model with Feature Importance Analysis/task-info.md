# Optimized Classification Model with Feature Importance Analysis

## 1. Project Title

**Predicting E-Commerce Purchase Likelihood Using an Optimized Classification Model**

---

## 2. Project Overview

An e-commerce company wants to identify customers who are most likely to purchase a product based on their browsing behavior, transaction history, engagement level, and demographic information.

Students must build a machine learning classification model that predicts whether a customer will make a purchase.

The project must go beyond training a basic model. Students are expected to:

* Perform exploratory data analysis.
* Prepare the dataset for classification.
* Train multiple classification algorithms.
* Optimize model hyperparameters.
* Compare model performance.
* Select the most appropriate model.
* Analyze the importance of input features.
* Translate model findings into actionable business recommendations.

---

## 3. Business Problem

E-commerce platforms often attract a large number of visitors, but only a small percentage complete a purchase.

The company wants to answer the following question:

> Based on customer behavior and profile information, can we predict whether a customer is likely to make a purchase?

Accurate purchase prediction can help the business:

* Target customers with a high likelihood of purchasing.
* Reduce unnecessary marketing expenditure.
* Personalize discounts and product recommendations.
* Improve conversion rates.
* Identify factors that influence purchase decisions.
* Prioritize customers for remarketing campaigns.

---

## 4. Project Objective

Build and optimize a classification model that predicts whether an e-commerce customer will complete a purchase.

The final model should provide:

1. A purchase prediction for each customer.
2. A probability representing the likelihood of purchase.
3. An explanation of the most influential features.
4. Business recommendations based on the analysis.

---

## 5. Target Variable

The target variable should represent whether the customer completed a purchase.

Example:

| Purchase | Meaning                       |
| -------: | ----------------------------- |
|        0 | Customer did not purchase     |
|        1 | Customer completed a purchase |

This is a **binary classification problem**.

---

## 6. Suggested Dataset Features

Students may use an existing e-commerce dataset or create a structured sample dataset.

Possible input features include:

| Feature              | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| `CustomerID`         | Unique identifier for the customer                                 |
| `Age`                | Age of the customer                                                |
| `Gender`             | Customer gender                                                    |
| `Location`           | Customer location or region                                        |
| `DeviceType`         | Mobile, desktop, or tablet                                         |
| `TrafficSource`      | Search engine, social media, email, direct visit, or advertisement |
| `PagesViewed`        | Number of product or website pages viewed                          |
| `TimeOnSite`         | Total time spent on the website                                    |
| `ProductsViewed`     | Number of products viewed                                          |
| `CartItems`          | Number of products added to the cart                               |
| `PreviousPurchases`  | Number of earlier purchases                                        |
| `AverageOrderValue`  | Average amount spent in previous purchases                         |
| `DiscountUsed`       | Whether the customer used or received a discount                   |
| `EmailClicked`       | Whether the customer clicked a promotional email                   |
| `AdClicked`          | Whether the customer clicked an advertisement                      |
| `ReviewScoreViewed`  | Average review score of products viewed                            |
| `DaysSinceLastVisit` | Number of days since the customer's previous visit                 |
| `SessionCount`       | Total number of website sessions                                   |
| `Purchase`           | Target variable indicating whether the customer purchased          |

Identifiers such as `CustomerID` should normally be removed before model training because they usually do not contain meaningful predictive information.

---

## 7. Recommended Classification Algorithms

Students must implement and compare at least three classification algorithms.

### 7.1 Logistic Regression

Use Logistic Regression as the baseline classification model.

It is useful because:

* It is easy to implement.
* It provides interpretable coefficients.
* It generates purchase probabilities.
* It works well when the relationship between features and the target is approximately linear.

### 7.2 Decision Tree Classifier

A Decision Tree can capture nonlinear relationships and interactions between variables.

It is useful because:

* Its predictions are easier to explain.
* It handles numerical and categorical patterns.
* It can identify meaningful decision rules.
* It provides built-in feature importance.

### 7.3 Random Forest Classifier

Random Forest combines multiple decision trees to improve generalization.

It is useful because:

* It handles nonlinear relationships.
* It is less likely to overfit than a single decision tree.
* It works well with mixed feature types.
* It provides feature importance values.

### Optional Algorithms

Students may also experiment with:

* K-Nearest Neighbors
* Support Vector Machine
* Gradient Boosting Classifier
* XGBoost
* AdaBoost
* Naive Bayes

The final comparison should focus on models appropriate for the selected dataset.

---

## 8. Project Tasks

## Task 1: Understand the Dataset

Students must inspect the dataset and document:

* Number of rows and columns.
* Feature names and data types.
* Target variable distribution.
* Missing values.
* Duplicate records.
* Numerical variables.
* Categorical variables.
* Potential data quality issues.
* Possible class imbalance.

Questions to investigate include:

* What percentage of customers completed a purchase?
* Are there more non-purchasers than purchasers?
* Which customer activities appear to be associated with purchases?
* Are there unusual or unrealistic values?
* Are any columns identifiers rather than predictive features?

---

## Task 2: Perform Exploratory Data Analysis

Perform exploratory data analysis to understand customer purchase behavior.

Recommended analysis includes:

* Distribution of the target variable.
* Purchase rate by device type.
* Purchase rate by traffic source.
* Purchase rate for customers who used discounts.
* Relationship between time on site and purchase.
* Relationship between cart items and purchase.
* Relationship between previous purchases and current purchase.
* Correlation between numerical features.
* Detection of outliers.
* Comparison of purchasers and non-purchasers.

Recommended visualizations include:

* Count plots.
* Histograms.
* Box plots.
* Bar charts.
* Correlation heatmaps.
* Scatter plots.
* Conversion-rate charts.

Students must explain the business meaning of each important visualization instead of only displaying charts.

---

## Task 3: Prepare the Data

The dataset must be cleaned and transformed before model training.

### Data-preparation activities

* Remove duplicate rows.
* Handle missing values.
* Correct invalid values.
* Remove unnecessary identifier columns.
* Separate features from the target variable.
* Encode categorical variables.
* Scale numerical features where required.
* Split the data into training and testing sets.

### Example split

* 80% training data.
* 20% testing data.

Use stratified splitting when the purchase classes are imbalanced.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
```

Stratification helps maintain a similar purchase and non-purchase distribution in both datasets.

---

## Task 4: Build a Preprocessing Pipeline

Students should use a preprocessing pipeline to prevent inconsistencies between training and testing data.

Typical preprocessing may include:

* Median imputation for missing numerical values.
* Most-frequent imputation for missing categorical values.
* Standardization of numerical variables.
* One-hot encoding of categorical variables.

Example:

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numerical_columns),
        ("categorical", categorical_pipeline, categorical_columns)
    ]
)
```

Using a pipeline reduces the risk of data leakage and ensures that the same transformations are applied during training and prediction.

---

## Task 5: Train Baseline Models

Train at least three classification models using default or basic parameters.

Suggested models:

1. Logistic Regression.
2. Decision Tree Classifier.
3. Random Forest Classifier.

Example:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

logistic_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)

tree_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(random_state=42))
    ]
)

forest_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                random_state=42
            )
        )
    ]
)
```

Students must record the baseline performance of each model before optimization.

---

## Task 6: Evaluate Baseline Performance

Each model must be evaluated using multiple classification metrics.

### Accuracy

Accuracy measures the overall percentage of correct predictions.

[
Accuracy = \frac{Correct\ Predictions}{Total\ Predictions}
]

Accuracy may be misleading when the dataset contains significantly more non-purchasers than purchasers.

### Precision

Precision measures how many customers predicted as purchasers actually purchased.

[
Precision = \frac{True\ Positives}{True\ Positives + False\ Positives}
]

High precision is important when marketing offers are expensive and the business wants to avoid targeting unlikely buyers.

### Recall

Recall measures how many actual purchasers were correctly identified.

[
Recall = \frac{True\ Positives}{True\ Positives + False\ Negatives}
]

High recall is important when the business does not want to miss potential buyers.

### F1-Score

The F1-score balances precision and recall.

[
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
]

### ROC-AUC

ROC-AUC measures the model's ability to rank purchasers above non-purchasers across different classification thresholds.

### Confusion Matrix

The confusion matrix must be used to analyze:

* True positives.
* True negatives.
* False positives.
* False negatives.

Example:

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

predictions = logistic_pipeline.predict(X_test)
probabilities = logistic_pipeline.predict_proba(X_test)[:, 1]

print("Accuracy:", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions))
print("Recall:", recall_score(y_test, predictions))
print("F1-Score:", f1_score(y_test, predictions))
print("ROC-AUC:", roc_auc_score(y_test, probabilities))
print(classification_report(y_test, predictions))
print(confusion_matrix(y_test, predictions))
```

---

## Task 7: Select the Optimization Metric

Before tuning the models, students must select the most appropriate optimization metric.

The selected metric must be connected to the business objective.

Examples:

| Business Objective                            | Recommended Metric   |
| --------------------------------------------- | -------------------- |
| Minimize money spent on unlikely buyers       | Precision            |
| Identify as many potential buyers as possible | Recall               |
| Balance missed buyers and incorrect targeting | F1-score             |
| Rank customers by purchase likelihood         | ROC-AUC              |
| Overall performance with balanced classes     | Accuracy or F1-score |

Students must justify why the chosen metric is appropriate.

---

## Task 8: Perform Hyperparameter Optimization

Optimize at least two classification models using one of the following:

* `GridSearchCV`
* `RandomizedSearchCV`

### Suggested Decision Tree parameters

* `max_depth`
* `min_samples_split`
* `min_samples_leaf`
* `criterion`
* `class_weight`

### Suggested Random Forest parameters

* `n_estimators`
* `max_depth`
* `min_samples_split`
* `min_samples_leaf`
* `max_features`
* `class_weight`

### Suggested Logistic Regression parameters

* `C`
* `penalty`
* `solver`
* `class_weight`

Example:

```python
from sklearn.model_selection import GridSearchCV

parameter_grid = {
    "classifier__n_estimators": [100, 200, 300],
    "classifier__max_depth": [None, 5, 10, 20],
    "classifier__min_samples_split": [2, 5, 10],
    "classifier__min_samples_leaf": [1, 2, 4],
    "classifier__class_weight": [None, "balanced"]
}

grid_search = GridSearchCV(
    estimator=forest_pipeline,
    param_grid=parameter_grid,
    scoring="f1",
    cv=5,
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

print("Best parameters:", grid_search.best_params_)
print("Best cross-validation score:", grid_search.best_score_)
```

Students should avoid selecting a very large parameter grid without considering computation time.

---

## Task 9: Analyze Hyperparameter Sensitivity

Students must examine how important hyperparameters influence model performance.

Examples include:

* How does increasing tree depth affect training and testing performance?
* Does increasing the number of trees improve Random Forest performance?
* Does a smaller or larger Logistic Regression `C` value improve generalization?
* Does using `class_weight="balanced"` improve recall?
* At what point do additional estimators provide little improvement?
* Which parameter combinations lead to overfitting?

Students should present the sensitivity analysis using:

* Tables.
* Line charts.
* Validation curves.
* Cross-validation scores.
* Training-versus-testing comparisons.

The analysis must explain why model performance changed.

---

## Task 10: Evaluate the Optimized Model

Evaluate the best estimator on the untouched test dataset.

Example:

```python
best_model = grid_search.best_estimator_

optimized_predictions = best_model.predict(X_test)
optimized_probabilities = best_model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, optimized_predictions))
print("ROC-AUC:", roc_auc_score(y_test, optimized_probabilities))
```

Compare baseline and optimized performance.

Example comparison:

| Model                        | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| ---------------------------- | -------: | --------: | -----: | -------: | ------: |
| Baseline Logistic Regression |     0.82 |      0.71 |   0.64 |     0.67 |    0.84 |
| Baseline Decision Tree       |     0.78 |      0.61 |   0.70 |     0.65 |    0.74 |
| Baseline Random Forest       |     0.85 |      0.76 |   0.69 |     0.72 |    0.88 |
| Optimized Random Forest      |     0.87 |      0.79 |   0.75 |     0.77 |    0.91 |

The values above are examples only. Students must report results generated from their own dataset.

---

## Task 11: Address Class Imbalance

Students must check whether the target classes are imbalanced.

For example:

* 90% non-purchasers.
* 10% purchasers.

When imbalance exists, students may experiment with:

* `class_weight="balanced"`
* Oversampling.
* Undersampling.
* SMOTE.
* Threshold adjustment.
* Evaluation metrics such as precision, recall, F1-score, and ROC-AUC.

Students must compare performance before and after handling imbalance.

Accuracy alone must not be used as the primary evaluation metric for a heavily imbalanced dataset.

---

## Task 12: Perform Feature Importance Analysis

The selected model must be interpreted to identify the variables that most strongly influence purchase predictions.

### For Logistic Regression

Analyze the model coefficients.

* Positive coefficients increase predicted purchase likelihood.
* Negative coefficients decrease predicted purchase likelihood.
* Coefficient magnitude indicates the strength of the relationship.

### For Tree-Based Models

Use built-in feature importance.

```python
import pandas as pd

feature_names = best_model.named_steps[
    "preprocessor"
].get_feature_names_out()

importance_values = best_model.named_steps[
    "classifier"
].feature_importances_

feature_importance = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": importance_values
    }
).sort_values(
    by="Importance",
    ascending=False
)

print(feature_importance.head(10))
```

### Optional Advanced Interpretation

Students may use:

* Permutation importance.
* SHAP values.
* Partial dependence plots.

Built-in feature importance should be interpreted carefully because it does not always indicate a causal relationship.

---

## Task 13: Visualize Feature Importance

Create a chart showing the most influential features.

Example:

```python
import matplotlib.pyplot as plt

top_features = feature_importance.head(10).sort_values(
    by="Importance"
)

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.xlabel("Feature Importance")
plt.ylabel("Feature")
plt.title("Top Features Influencing Purchase Prediction")
plt.tight_layout()
plt.show()
```

Students must explain each important feature in business terms.

Example interpretation:

* Customers with more cart items may have a higher probability of purchasing.
* Customers who previously purchased may be more likely to purchase again.
* Longer time on site may indicate stronger buying intent.
* Discount usage may influence price-sensitive customers.
* A high number of days since the last visit may reduce purchase probability.

---

## Task 14: Analyze the Classification Threshold

The default classification threshold is commonly `0.50`.

However, the business may benefit from using a different threshold.

For example:

```python
purchase_probabilities = best_model.predict_proba(X_test)[:, 1]

custom_predictions = (
    purchase_probabilities >= 0.40
).astype(int)
```

A lower threshold may:

* Identify more potential buyers.
* Increase recall.
* Increase false positives.
* Reduce precision.

A higher threshold may:

* Improve precision.
* Reduce unnecessary targeting.
* Miss some potential buyers.
* Reduce recall.

Students must recommend a threshold based on business priorities.

---

## Task 15: Create Customer Purchase-Risk Categories

Use purchase probabilities to group customers into meaningful segments.

Example:

| Predicted Probability | Customer Category          |
| --------------------: | -------------------------- |
|             0.00–0.29 | Low purchase likelihood    |
|             0.30–0.59 | Medium purchase likelihood |
|             0.60–1.00 | High purchase likelihood   |

Example:

```python
import pandas as pd

results = X_test.copy()

results["ActualPurchase"] = y_test.values
results["PurchaseProbability"] = optimized_probabilities

results["PurchaseLikelihood"] = pd.cut(
    results["PurchaseProbability"],
    bins=[0.0, 0.30, 0.60, 1.0],
    labels=[
        "Low",
        "Medium",
        "High"
    ],
    include_lowest=True
)
```

These categories can support targeted marketing decisions.

---

## Task 16: Generate Actionable Business Recommendations

Students must translate the model findings into specific business actions.

Possible recommendations include:

### High-Likelihood Customers

* Display personalized product recommendations.
* Offer limited-time discounts.
* Send cart reminders.
* Promote complementary products.
* Prioritize these customers in paid remarketing campaigns.

### Medium-Likelihood Customers

* Provide customer reviews and product comparisons.
* Offer small incentives.
* Send educational or promotional content.
* Use personalized email campaigns.
* Highlight free shipping or return policies.

### Low-Likelihood Customers

* Avoid expensive promotional campaigns.
* Use low-cost awareness campaigns.
* Collect feedback on why customers did not purchase.
* Improve product discovery and website usability.
* Retarget only when stronger engagement signals appear.

Recommendations must be supported by the model results and feature-importance analysis.

---

## 9. AI-Augmented Activities

Students are expected to use AI as an assistant while maintaining responsibility for the final implementation and interpretation.

### 9.1 Algorithm Selection

Use AI to explore questions such as:

* Which classification algorithms are appropriate for this dataset?
* Why should Logistic Regression be used as a baseline?
* When is Random Forest preferable to a Decision Tree?
* Which models are easier to interpret?
* Which models are suitable for class imbalance?

Students must verify AI suggestions through experimentation.

### 9.2 Debugging Model Performance

Use AI to investigate:

* Why training performance is high but testing performance is low.
* Why the model predicts only the majority class.
* Why precision is high but recall is low.
* Why GridSearchCV takes too long.
* Why categorical encoding causes errors.
* Why feature names do not match feature importance values.
* Why ROC-AUC cannot be calculated from class predictions.

Students must document at least one issue investigated with AI and explain the final correction.

### 9.3 Hyperparameter Analysis

Use AI to understand:

* The effect of tree depth.
* The effect of regularization strength.
* The effect of the number of estimators.
* The role of minimum samples per split.
* The effect of class weighting.
* The difference between GridSearchCV and RandomizedSearchCV.

### 9.4 Feature-Importance Interpretation

Use AI to help translate model output into business language.

Students must avoid presenting AI-generated explanations without validating them against:

* Dataset definitions.
* Model results.
* Visualizations.
* Domain logic.

---

## 10. Mandatory Deliverables

## Deliverable 1: Jupyter Notebook

The notebook must contain:

1. Project objective.
2. Dataset description.
3. Data-quality checks.
4. Exploratory data analysis.
5. Data preprocessing.
6. Baseline model training.
7. Baseline model evaluation.
8. Hyperparameter optimization.
9. Optimized model evaluation.
10. Baseline-versus-optimized comparison.
11. Confusion matrix.
12. ROC curve.
13. Feature-importance analysis.
14. Threshold analysis.
15. Business recommendations.
16. Final conclusion.

---

## Deliverable 2: Model Comparison Table

Include a table similar to:

| Model               | Optimization Status | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| ------------------- | ------------------- | -------: | --------: | -----: | -------: | ------: |
| Logistic Regression | Baseline            |          |           |        |          |         |
| Decision Tree       | Baseline            |          |           |        |          |         |
| Random Forest       | Baseline            |          |           |        |          |         |
| Selected Model      | Optimized           |          |           |        |          |         |

---

## Deliverable 3: Hyperparameter Optimization Summary

Include:

* Model optimized.
* Search method used.
* Parameters tested.
* Cross-validation strategy.
* Optimization metric.
* Best parameter combination.
* Best cross-validation score.
* Test-set score.
* Evidence of whether optimization improved performance.

---

## Deliverable 4: Feature-Importance Report

The report must include:

* Top 10 influential features.
* Importance score or coefficient.
* Direction of influence where available.
* Business interpretation.
* Recommended business action.

Example:

| Feature            | Importance | Interpretation                                             | Recommended Action               |
| ------------------ | ---------: | ---------------------------------------------------------- | -------------------------------- |
| Cart items         |       0.24 | Customers with more cart items show stronger buying intent | Send timely cart reminders       |
| Previous purchases |       0.18 | Existing customers are more likely to purchase again       | Run loyalty campaigns            |
| Time on site       |       0.14 | Longer engagement may indicate product interest            | Personalize product suggestions  |
| Discount used      |       0.10 | Discounts influence purchase decisions                     | Target price-sensitive customers |

---

## Deliverable 5: Business Recommendation Summary

Provide at least five recommendations supported by model evidence.

Each recommendation must include:

1. The model finding.
2. The business interpretation.
3. The recommended action.
4. The expected business benefit.
5. A possible risk or limitation.

---

## Deliverable 6: Saved Model

Save the final preprocessing and classification pipeline.

```python
import joblib

joblib.dump(
    best_model,
    "purchase_prediction_model.pkl"
)
```

The saved pipeline should include both preprocessing and the classification model.

---

## Deliverable 7: Presentation

Prepare a presentation of approximately 8–10 slides covering:

1. Business problem.
2. Dataset overview.
3. Exploratory findings.
4. Preprocessing approach.
5. Models compared.
6. Hyperparameter optimization.
7. Final model performance.
8. Feature importance.
9. Business recommendations.
10. Limitations and next steps.

---

## 11. Mentor Validation Checklist

The mentor should validate whether the student has:

* Clearly defined the target variable.
* Identified the project as a binary classification problem.
* Checked target-class distribution.
* Performed meaningful exploratory analysis.
* Prevented data leakage.
* Used appropriate encoding and scaling.
* Trained at least three classification models.
* Recorded baseline model performance.
* Used cross-validation during optimization.
* Justified the selected optimization metric.
* Reported the best hyperparameters.
* Evaluated the final model on unseen test data.
* Used more than accuracy for evaluation.
* Presented a confusion matrix.
* Analyzed false positives and false negatives.
* Compared baseline and optimized performance.
* Presented feature importance.
* Connected important features to business actions.
* Considered classification-threshold adjustment.
* Provided realistic limitations.
* Documented how AI assistance was used and validated.

---

## 12. Suggested Evaluation Rubric

| Evaluation Area                              |   Weight |
| -------------------------------------------- | -------: |
| Problem understanding and business objective |      10% |
| Data cleaning and exploratory analysis       |      15% |
| Data preprocessing and leakage prevention    |      15% |
| Baseline model implementation                |      10% |
| Hyperparameter optimization                  |      15% |
| Model evaluation and comparison              |      15% |
| Feature-importance analysis                  |      10% |
| Business recommendations                     |       5% |
| Code quality and documentation               |       5% |
| **Total**                                    | **100%** |

---

## 13. Expected Learning Outcomes

After completing this project, students should be able to:

* Frame an e-commerce problem as a classification task.
* Prepare numerical and categorical data for machine learning.
* Build preprocessing and classification pipelines.
* Compare multiple classification algorithms.
* Evaluate models using business-relevant metrics.
* Optimize models using cross-validation.
* Identify and address class imbalance.
* Interpret feature importance and model coefficients.
* Adjust classification thresholds.
* Convert predictions into customer-prioritization strategies.
* Translate machine learning results into business recommendations.
* Use AI assistance responsibly for analysis and debugging.

---

## 14. Suggested Technology Stack

* Python
* Jupyter Notebook or Google Colab
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Joblib
* SHAP, optional
* Imbalanced-learn, optional

---

## 15. Constraints

Students must follow these constraints:

* Do not use the test dataset during hyperparameter selection.
* Do not apply preprocessing to the complete dataset before splitting.
* Do not use accuracy as the only evaluation metric.
* Do not select the final model solely because it has the highest training score.
* Do not include customer identifiers as predictive features without justification.
* Do not claim that feature importance proves causation.
* Do not present AI-generated explanations without validating them.
* Use a fixed random state where possible for reproducibility.
* Document all important assumptions.

---

## 16. Final Submission Structure

The final submission folder may follow this structure:

```text
mini-project-5/
│
├── data/
│   └── ecommerce_customer_data.csv
│
├── notebooks/
│   └── purchase_prediction_analysis.ipynb
│
├── models/
│   └── purchase_prediction_model.pkl
│
├── reports/
│   ├── feature_importance_report.pdf
│   └── business_recommendations.pdf
│
├── presentation/
│   └── mini_project_5_presentation.pptx
│
├── requirements.txt
└── README.md
```

---

## 17. Final Project Question

At the end of the project, students must answer:

> Which classification model should the e-commerce company use to identify customers who are likely to purchase, how much did hyperparameter optimization improve its performance, which features influenced the predictions, and how can the company use these findings to improve conversion rates?

The answer must be supported by:

* Evaluation metrics.
* Cross-validation results.
* Confusion-matrix analysis.
* Feature-importance results.
* Threshold analysis.
* Business reasoning.
