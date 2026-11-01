import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.cluster import KMeans

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    silhouette_score
)

warnings.filterwarnings("ignore")

DATA_PATH = "data/ecommerce_recommendation_data.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("TASK 7 - MULTI-ALGORITHM RECOMMENDATION SYSTEM COMPARISON")
print("=" * 70)

# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("\n1. DATASET INFORMATION")
print("-" * 70)

print("Dataset Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

# Remove duplicates
df = df.drop_duplicates()

# ============================================================
# 2. REGRESSION - RIDGE REGRESSION
# ============================================================

print("\n" + "=" * 70)
print("2. RIDGE REGRESSION - RATING PREDICTION")
print("=" * 70)

reg_features = [
    "Price",
    "ProductCategory",
    "NumberOfViews",
    "CartStatus",
    "TimeSpent",
    "PreviousPurchases"
]

X_reg = df[reg_features]
y_reg = df["Rating"]

categorical_features = ["ProductCategory"]

numerical_features = [
    "Price",
    "NumberOfViews",
    "CartStatus",
    "TimeSpent",
    "PreviousPurchases"
]

reg_preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)

X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_reg,
    y_reg,
    test_size=0.20,
    random_state=42
)

ridge_pipeline = Pipeline(
    steps=[
        ("preprocessor", reg_preprocessor),
        ("model", Ridge())
    ]
)

# Baseline Ridge Regression
ridge_pipeline.fit(X_reg_train, y_reg_train)

reg_predictions = ridge_pipeline.predict(X_reg_test)

baseline_mae = mean_absolute_error(
    y_reg_test,
    reg_predictions
)

baseline_rmse = np.sqrt(
    mean_squared_error(
        y_reg_test,
        reg_predictions
    )
)

baseline_r2 = r2_score(
    y_reg_test,
    reg_predictions
)

print("\nBaseline Ridge Regression Results:")
print(f"MAE  : {baseline_mae:.4f}")
print(f"RMSE : {baseline_rmse:.4f}")
print(f"R2   : {baseline_r2:.4f}")

# GridSearchCV
ridge_params = {
    "model__alpha": [
        0.01,
        0.1,
        1,
        10,
        100
    ]
}

ridge_grid = GridSearchCV(
    ridge_pipeline,
    ridge_params,
    cv=5,
    scoring="neg_mean_squared_error"
)

ridge_grid.fit(
    X_reg_train,
    y_reg_train
)

best_ridge = ridge_grid.best_estimator_

tuned_reg_predictions = best_ridge.predict(
    X_reg_test
)

tuned_mae = mean_absolute_error(
    y_reg_test,
    tuned_reg_predictions
)

tuned_rmse = np.sqrt(
    mean_squared_error(
        y_reg_test,
        tuned_reg_predictions
    )
)

tuned_r2 = r2_score(
    y_reg_test,
    tuned_reg_predictions
)

print("\nBest Ridge Parameters:")
print(ridge_grid.best_params_)

print("\nTuned Ridge Regression Results:")
print(f"MAE  : {tuned_mae:.4f}")
print(f"RMSE : {tuned_rmse:.4f}")
print(f"R2   : {tuned_r2:.4f}")

# ============================================================
# 3. CLASSIFICATION - LOGISTIC REGRESSION
# ============================================================

print("\n" + "=" * 70)
print("3. LOGISTIC REGRESSION - PURCHASE PREDICTION")
print("=" * 70)

classification_features = [
    "Price",
    "ProductCategory",
    "NumberOfViews",
    "CartStatus",
    "TimeSpent",
    "PreviousPurchases",
    "Rating"
]

X_cls = df[classification_features]
y_cls = df["PurchaseStatus"]

cls_numerical_features = [
    "Price",
    "NumberOfViews",
    "CartStatus",
    "TimeSpent",
    "PreviousPurchases",
    "Rating"
]

cls_preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            cls_numerical_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            ["ProductCategory"]
        )
    ]
)

X_cls_train, X_cls_test, y_cls_train, y_cls_test = train_test_split(
    X_cls,
    y_cls,
    test_size=0.20,
    random_state=42,
    stratify=y_cls
)

logistic_pipeline = Pipeline(
    steps=[
        ("preprocessor", cls_preprocessor),
        (
            "model",
            LogisticRegression(
                max_iter=500
            )
        )
    ]
)

# Baseline Logistic Regression
logistic_pipeline.fit(
    X_cls_train,
    y_cls_train
)

cls_predictions = logistic_pipeline.predict(
    X_cls_test
)

baseline_accuracy = accuracy_score(
    y_cls_test,
    cls_predictions
)

baseline_precision = precision_score(
    y_cls_test,
    cls_predictions
)

baseline_recall = recall_score(
    y_cls_test,
    cls_predictions
)

baseline_f1 = f1_score(
    y_cls_test,
    cls_predictions
)

print("\nBaseline Logistic Regression Results:")
print(f"Accuracy  : {baseline_accuracy:.4f}")
print(f"Precision : {baseline_precision:.4f}")
print(f"Recall    : {baseline_recall:.4f}")
print(f"F1 Score  : {baseline_f1:.4f}")

# Hyperparameter tuning
logistic_params = [
    {
        "model__C": [0.01, 0.1, 1, 10],
        "model__solver": ["liblinear"],
        "model__max_iter": [100, 200, 500]
    },
    {
        "model__C": [0.01, 0.1, 1, 10],
        "model__solver": ["lbfgs"],
        "model__max_iter": [100, 200, 500]
    }
]

logistic_grid = GridSearchCV(
    logistic_pipeline,
    logistic_params,
    cv=5,
    scoring="f1"
)

logistic_grid.fit(
    X_cls_train,
    y_cls_train
)

best_logistic = logistic_grid.best_estimator_

tuned_cls_predictions = best_logistic.predict(
    X_cls_test
)

tuned_accuracy = accuracy_score(
    y_cls_test,
    tuned_cls_predictions
)

tuned_precision = precision_score(
    y_cls_test,
    tuned_cls_predictions
)

tuned_recall = recall_score(
    y_cls_test,
    tuned_cls_predictions
)

tuned_f1 = f1_score(
    y_cls_test,
    tuned_cls_predictions
)

print("\nBest Logistic Regression Parameters:")
print(logistic_grid.best_params_)

print("\nTuned Logistic Regression Results:")
print(f"Accuracy  : {tuned_accuracy:.4f}")
print(f"Precision : {tuned_precision:.4f}")
print(f"Recall    : {tuned_recall:.4f}")
print(f"F1 Score  : {tuned_f1:.4f}")

# Confusion Matrix
cm = confusion_matrix(
    y_cls_test,
    tuned_cls_predictions
)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

display.plot()
plt.title("Logistic Regression Confusion Matrix")
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "confusion_matrix.png"
    )
)

plt.close()

# ============================================================
# 4. K-MEANS CLUSTERING
# ============================================================

print("\n" + "=" * 70)
print("4. K-MEANS CUSTOMER SEGMENTATION")
print("=" * 70)

customer_data = df.groupby(
    "UserID"
).agg(
    NumberOfProductsViewed=(
        "NumberOfViews",
        "sum"
    ),
    NumberOfPurchases=(
        "PurchaseStatus",
        "sum"
    ),
    AverageRating=(
        "Rating",
        "mean"
    ),
    AverageTimeSpent=(
        "TimeSpent",
        "mean"
    ),
    TotalAmountSpent=(
        "TotalAmountSpent",
        "sum"
    ),
    ProductsAddedToCart=(
        "CartStatus",
        "sum"
    )
).reset_index()

cluster_features = [
    "NumberOfProductsViewed",
    "NumberOfPurchases",
    "AverageRating",
    "AverageTimeSpent",
    "TotalAmountSpent",
    "ProductsAddedToCart"
]

X_cluster = customer_data[
    cluster_features
]

scaler = StandardScaler()

X_cluster_scaled = scaler.fit_transform(
    X_cluster
)

inertias = []
silhouette_scores = []

cluster_range = range(2, 7)

for k in cluster_range:

    kmeans_test = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans_test.fit_predict(
        X_cluster_scaled
    )

    inertias.append(
        kmeans_test.inertia_
    )

    silhouette_scores.append(
        silhouette_score(
            X_cluster_scaled,
            labels
        )
    )

    print(
        f"K={k} | "
        f"Inertia={kmeans_test.inertia_:.4f} | "
        f"Silhouette={silhouette_scores[-1]:.4f}"
    )

# Best K using silhouette score
best_k = list(cluster_range)[
    np.argmax(silhouette_scores)
]

print(
    f"\nBest number of clusters "
    f"based on Silhouette Score: {best_k}"
)

# Elbow Method Graph
plt.figure()

plt.plot(
    list(cluster_range),
    inertias,
    marker="o"
)

plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "elbow_method.png"
    )
)

plt.close()

# Final K-Means
final_kmeans = KMeans(
    n_clusters=best_k,
    random_state=42,
    n_init=10
)

customer_data["Cluster"] = final_kmeans.fit_predict(
    X_cluster_scaled
)

final_silhouette = silhouette_score(
    X_cluster_scaled,
    customer_data["Cluster"]
)

print(
    f"Final K-Means Inertia: "
    f"{final_kmeans.inertia_:.4f}"
)

print(
    f"Final Silhouette Score: "
    f"{final_silhouette:.4f}"
)

print("\nCustomer Cluster Distribution:")
print(
    customer_data["Cluster"]
    .value_counts()
    .sort_index()
)

# Save customer segmentation
customer_data.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "customer_segments.csv"
    ),
    index=False
)

# ============================================================
# 5. MODEL COMPARISON
# ============================================================

print("\n" + "=" * 70)
print("5. MODEL COMPARISON")
print("=" * 70)

comparison = pd.DataFrame({
    "ML Task": [
        "Regression",
        "Classification",
        "Clustering"
    ],
    "Algorithm": [
        "Ridge Regression",
        "Logistic Regression",
        "K-Means"
    ],
    "Goal": [
        "Predict Product Rating",
        "Predict Purchase Likelihood",
        "Segment Customers"
    ],
    "Best Result": [
        f"RMSE={tuned_rmse:.4f}, R2={tuned_r2:.4f}",
        f"Accuracy={tuned_accuracy:.4f}, F1={tuned_f1:.4f}",
        f"Silhouette={final_silhouette:.4f}"
    ],
    "Business Use": [
        "Recommend products customers may like",
        "Identify customers likely to purchase",
        "Create targeted customer segments"
    ]
})

print("\n")
print(
    comparison.to_string(
        index=False
    )
)

comparison.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "model_comparison.csv"
    ),
    index=False
)

# ============================================================
# 6. BUSINESS INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("6. BUSINESS INTERPRETATION")
print("=" * 70)

print(
    """
Ridge Regression:
Helps estimate the rating a customer may give to a product.
Products with higher predicted ratings can be prioritized
in personalized recommendations.

Logistic Regression:
Helps identify customers who are more likely to purchase.
The business can target these customers with personalized
offers, discounts, and recommendations.

K-Means Clustering:
Groups customers with similar shopping behaviour.
These groups can be used for customer-specific marketing
and recommendation strategies.
"""
)

print("=" * 70)
print("TASK 7 COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nOutput files created:")
print("1. outputs/confusion_matrix.png")
print("2. outputs/elbow_method.png")
print("3. outputs/customer_segments.csv")
print("4. outputs/model_comparison.csv")