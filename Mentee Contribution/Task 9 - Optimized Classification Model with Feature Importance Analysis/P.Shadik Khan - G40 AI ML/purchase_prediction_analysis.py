import os
import warnings

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = (
    "Mentee Contribution/"
    "Task 9 - Optimized Classification Model with Feature Importance Analysis/"
    "P.Shadik Khan - G40 AI ML"
)

DATA_PATH = f"{BASE_DIR}/data/ecommerce_customer_data.csv"

REPORTS_DIR = f"{BASE_DIR}/reports"
MODELS_DIR = f"{BASE_DIR}/models"

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("TASK 9 - OPTIMIZED CLASSIFICATION MODEL")
print("=" * 70)

print("\nDataset shape:", df.shape)

print("\nFirst five rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nPurchase distribution:")
print(df["Purchase"].value_counts())

print("\nPurchase percentage:")
print(df["Purchase"].value_counts(normalize=True).round(4))


# ============================================================
# 3. DATA QUALITY CHECKS
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY CHECKS")
print("=" * 70)

print("\nUnique Customer IDs:", df["CustomerID"].nunique())

print("\nNumerical columns:")
print(df.select_dtypes(include=np.number).columns.tolist())

print("\nCategorical columns:")
print(df.select_dtypes(include="object").columns.tolist())


# ============================================================
# 4. EXPLORATORY DATA ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)


# Target distribution

plt.figure(figsize=(7, 5))

df["Purchase"].value_counts().sort_index().plot(
    kind="bar"
)

plt.title("Purchase Distribution")
plt.xlabel("Purchase")
plt.ylabel("Number of Customers")
plt.xticks(
    [0, 1],
    ["Did Not Purchase", "Purchased"],
    rotation=0
)

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/purchase_distribution.png",
    dpi=150
)

plt.close()


# Purchase rate by device

device_purchase = (
    df.groupby("DeviceType", dropna=False)["Purchase"]
    .mean()
    .sort_values(ascending=False)
)

print("\nPurchase rate by device:")
print(device_purchase)

plt.figure(figsize=(8, 5))

device_purchase.plot(kind="bar")

plt.title("Purchase Rate by Device Type")
plt.xlabel("Device Type")
plt.ylabel("Purchase Rate")

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/purchase_rate_by_device.png",
    dpi=150
)

plt.close()


# Purchase rate by traffic source

traffic_purchase = (
    df.groupby("TrafficSource", dropna=False)["Purchase"]
    .mean()
    .sort_values(ascending=False)
)

print("\nPurchase rate by traffic source:")
print(traffic_purchase)

plt.figure(figsize=(9, 5))

traffic_purchase.plot(kind="bar")

plt.title("Purchase Rate by Traffic Source")
plt.xlabel("Traffic Source")
plt.ylabel("Purchase Rate")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/purchase_rate_by_traffic_source.png",
    dpi=150
)

plt.close()


# Time on site vs purchase

plt.figure(figsize=(8, 5))

df.boxplot(
    column="TimeOnSite",
    by="Purchase"
)

plt.title("Time on Site by Purchase Status")
plt.suptitle("")
plt.xlabel("Purchase")
plt.ylabel("Time on Site")

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/time_on_site_purchase.png",
    dpi=150
)

plt.close()


# Cart items vs purchase

plt.figure(figsize=(8, 5))

df.boxplot(
    column="CartItems",
    by="Purchase"
)

plt.title("Cart Items by Purchase Status")
plt.suptitle("")
plt.xlabel("Purchase")
plt.ylabel("Cart Items")

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/cart_items_purchase.png",
    dpi=150
)

plt.close()


# Correlation heatmap

numeric_df = df.select_dtypes(include=np.number)

correlation = numeric_df.corr()

plt.figure(figsize=(13, 10))

plt.imshow(
    correlation,
    aspect="auto"
)

plt.colorbar()

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=90
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

plt.title("Numerical Feature Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/correlation_heatmap.png",
    dpi=150
)

plt.close()


# ============================================================
# 5. PREPARE FEATURES AND TARGET
# ============================================================

X = df.drop(
    columns=["Purchase", "CustomerID"]
)

y = df["Purchase"]


numerical_columns = X.select_dtypes(
    include=np.number
).columns.tolist()

categorical_columns = X.select_dtypes(
    include="object"
).columns.tolist()

print("\nNumerical features:")
print(numerical_columns)

print("\nCategorical features:")
print(categorical_columns)


# ============================================================
# 6. TRAIN-TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))

print("\nTraining target distribution:")
print(y_train.value_counts(normalize=True).round(4))

print("\nTesting target distribution:")
print(y_test.value_counts(normalize=True).round(4))


# ============================================================
# 7. PREPROCESSING PIPELINE
# ============================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numerical_columns
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_columns
        )
    ]
)


# ============================================================
# 8. MODEL EVALUATION FUNCTION
# ============================================================

def evaluate_model(name, model, X_test, y_test):
    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(
            y_test,
            predictions
        ),
        "Precision": precision_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "Recall": recall_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "F1-Score": f1_score(
            y_test,
            predictions,
            zero_division=0
        ),
        "ROC-AUC": roc_auc_score(
            y_test,
            probabilities
        )
    }

    print("\n" + "-" * 70)
    print(name)
    print("-" * 70)

    for metric, value in metrics.items():
        if metric != "Model":
            print(
                f"{metric}: {value:.4f}"
            )

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    return metrics, predictions, probabilities


# ============================================================
# 9. BASELINE MODELS
# ============================================================

logistic_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)

tree_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            DecisionTreeClassifier(
                random_state=42,
                class_weight="balanced"
            )
        )
    ]
)

forest_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            RandomForestClassifier(
                random_state=42,
                class_weight="balanced",
                n_jobs=-1
            )
        )
    ]
)


print("\n" + "=" * 70)
print("TRAINING BASELINE MODELS")
print("=" * 70)


logistic_pipeline.fit(
    X_train,
    y_train
)

tree_pipeline.fit(
    X_train,
    y_train
)

forest_pipeline.fit(
    X_train,
    y_train
)


baseline_results = []


result, _, _ = evaluate_model(
    "Logistic Regression - Baseline",
    logistic_pipeline,
    X_test,
    y_test
)

baseline_results.append(result)


result, _, _ = evaluate_model(
    "Decision Tree - Baseline",
    tree_pipeline,
    X_test,
    y_test
)

baseline_results.append(result)


result, _, _ = evaluate_model(
    "Random Forest - Baseline",
    forest_pipeline,
    X_test,
    y_test
)

baseline_results.append(result)


# ============================================================
# 10. HYPERPARAMETER OPTIMIZATION
# ============================================================

print("\n" + "=" * 70)
print("RANDOM FOREST HYPERPARAMETER OPTIMIZATION")
print("=" * 70)


parameter_grid = {
    "classifier__n_estimators": [
        100,
        200
    ],
    "classifier__max_depth": [
        None,
        8,
        12
    ],
    "classifier__min_samples_split": [
        2,
        5
    ],
    "classifier__min_samples_leaf": [
        1,
        2
    ],
    "classifier__max_features": [
        "sqrt",
        "log2"
    ]
}


grid_search = GridSearchCV(
    estimator=forest_pipeline,
    param_grid=parameter_grid,
    scoring="f1",
    cv=5,
    n_jobs=-1,
    verbose=1
)

grid_search.fit(
    X_train,
    y_train
)


print("\nBest parameters:")
print(grid_search.best_params_)

print(
    "\nBest cross-validation F1:",
    round(grid_search.best_score_, 4)
)


best_model = grid_search.best_estimator_


# ============================================================
# 11. OPTIMIZED MODEL EVALUATION
# ============================================================

optimized_result, optimized_predictions, optimized_probabilities = (
    evaluate_model(
        "Optimized Random Forest",
        best_model,
        X_test,
        y_test
    )
)


# ============================================================
# 12. MODEL COMPARISON
# ============================================================

comparison_results = baseline_results + [
    optimized_result
]

comparison_df = pd.DataFrame(
    comparison_results
)

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(comparison_df.to_string(index=False))

comparison_df.to_csv(
    f"{REPORTS_DIR}/model_comparison.csv",
    index=False
)


# ============================================================
# 13. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    optimized_predictions
)

print("\nOptimized model confusion matrix:")
print(cm)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[
        "No Purchase",
        "Purchase"
    ]
)

disp.plot()

plt.title(
    "Optimized Random Forest - Confusion Matrix"
)

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/confusion_matrix.png",
    dpi=150
)

plt.close()


# ============================================================
# 14. ROC CURVE
# ============================================================

fpr, tpr, _ = roc_curve(
    y_test,
    optimized_probabilities
)

roc_auc = roc_auc_score(
    y_test,
    optimized_probabilities
)

plt.figure(figsize=(8, 6))

plt.plot(
    fpr,
    tpr,
    label=f"Random Forest AUC = {roc_auc:.3f}"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title(
    "ROC Curve - Optimized Random Forest"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/roc_curve.png",
    dpi=150
)

plt.close()


# ============================================================
# 15. FEATURE IMPORTANCE
# ============================================================

feature_names = (
    best_model
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

importance_values = (
    best_model
    .named_steps["classifier"]
    .feature_importances_
)

feature_importance = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": importance_values
    }
).sort_values(
    by="Importance",
    ascending=False
)

print("\n" + "=" * 70)
print("TOP 15 FEATURE IMPORTANCES")
print("=" * 70)

print(
    feature_importance.head(15).to_string(
        index=False
    )
)

feature_importance.to_csv(
    f"{REPORTS_DIR}/feature_importance.csv",
    index=False
)


# ============================================================
# 16. FEATURE IMPORTANCE VISUALIZATION
# ============================================================

top_features = (
    feature_importance
    .head(10)
    .sort_values("Importance")
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"],
    top_features["Importance"]
)

plt.xlabel("Feature Importance")
plt.ylabel("Feature")

plt.title(
    "Top 10 Features Influencing Purchase Prediction"
)

plt.tight_layout()

plt.savefig(
    f"{REPORTS_DIR}/feature_importance.png",
    dpi=150
)

plt.close()


# ============================================================
# 17. THRESHOLD ANALYSIS
# ============================================================

thresholds = [
    0.30,
    0.40,
    0.50,
    0.60,
    0.70
]

threshold_results = []

for threshold in thresholds:

    custom_predictions = (
        optimized_probabilities >= threshold
    ).astype(int)

    threshold_results.append(
        {
            "Threshold": threshold,
            "Precision": precision_score(
                y_test,
                custom_predictions,
                zero_division=0
            ),
            "Recall": recall_score(
                y_test,
                custom_predictions,
                zero_division=0
            ),
            "F1-Score": f1_score(
                y_test,
                custom_predictions,
                zero_division=0
            )
        }
    )


threshold_df = pd.DataFrame(
    threshold_results
)

print("\n" + "=" * 70)
print("THRESHOLD ANALYSIS")
print("=" * 70)

print(
    threshold_df.to_string(index=False)
)

threshold_df.to_csv(
    f"{REPORTS_DIR}/threshold_analysis.csv",
    index=False
)


# ============================================================
# 18. CUSTOMER PURCHASE-LIKELIHOOD CATEGORIES
# ============================================================

customer_results = X_test.copy()

customer_results["ActualPurchase"] = (
    y_test.values
)

customer_results["PurchaseProbability"] = (
    optimized_probabilities
)

customer_results["PurchaseLikelihood"] = pd.cut(
    customer_results["PurchaseProbability"],
    bins=[
        0.0,
        0.30,
        0.60,
        1.0
    ],
    labels=[
        "Low",
        "Medium",
        "High"
    ],
    include_lowest=True
)


customer_results.to_csv(
    f"{REPORTS_DIR}/customer_purchase_predictions.csv",
    index=False
)

print("\nPurchase likelihood categories:")
print(
    customer_results[
        "PurchaseLikelihood"
    ].value_counts()
)


# ============================================================
# 19. SAVE FINAL MODEL
# ============================================================

model_path = (
    f"{MODELS_DIR}/purchase_prediction_model.pkl"
)

joblib.dump(
    best_model,
    model_path
)

print(
    f"\nSaved model to: {model_path}"
)


# ============================================================
# 20. SAVE OPTIMIZATION SUMMARY
# ============================================================

optimization_summary = pd.DataFrame(
    {
        "Item": [
            "Model",
            "Search Method",
            "Cross Validation",
            "Optimization Metric",
            "Best CV F1 Score",
            "Best Parameters"
        ],
        "Value": [
            "Random Forest",
            "GridSearchCV",
            "5-fold",
            "F1-Score",
            grid_search.best_score_,
            str(grid_search.best_params_)
        ]
    }
)

optimization_summary.to_csv(
    f"{REPORTS_DIR}/optimization_summary.csv",
    index=False
)


# ============================================================
# 21. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated reports:")

for filename in sorted(
    os.listdir(REPORTS_DIR)
):
    print(" -", filename)

print("\nFinal model:")
print(model_path)

print("\nTask 9 analysis finished.")