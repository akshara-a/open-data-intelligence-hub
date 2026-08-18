"""
Multi-Algorithm Recommendation System Comparison
Full pipeline: preprocessing -> Ridge Regression -> Logistic Regression -> K-Means
-> hyperparameter tuning (GridSearchCV) -> evaluation -> comparison table.
"""

import json
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                              mean_absolute_error, precision_score,
                              r2_score, recall_score,
                              root_mean_squared_error, silhouette_score)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")
sns.set_style("whitegrid")
RESULTS = {}

# ---------------------------------------------------------------------------
# Step 1: Load dataset
# ---------------------------------------------------------------------------
df = pd.read_csv("/home/claude/project/ecommerce_dataset.csv")

RESULTS["raw_shape"] = df.shape
RESULTS["duplicates"] = int(df.duplicated().sum())
RESULTS["missing_before"] = df.isna().sum().to_dict()

# ---------------------------------------------------------------------------
# Step 2: Preprocessing
# ---------------------------------------------------------------------------
df = df.drop_duplicates().reset_index(drop=True)

# Handle missing values: numeric -> median, categorical -> mode
df["Time_Spent"] = df["Time_Spent"].fillna(df["Time_Spent"].median())
df["Rating"] = df["Rating"].fillna(df["Rating"].median())
df["Rating"] = df["Rating"].astype(int)

RESULTS["clean_shape"] = df.shape

# One-hot encode Product_Category
ohe = OneHotEncoder(sparse_output=False, drop="first")
cat_encoded = ohe.fit_transform(df[["Product_Category"]])
cat_cols = ohe.get_feature_names_out(["Product_Category"])
cat_df = pd.DataFrame(cat_encoded, columns=cat_cols, index=df.index)

df_model = pd.concat([df, cat_df], axis=1)

# ---------------------------------------------------------------------------
# Step 3: Regression Model -- Ridge Regression predicting Rating
# ---------------------------------------------------------------------------
reg_features = ["Price", "Number_of_Views", "Time_Spent",
                 "Previous_Purchases", "Cart_Status"] + list(cat_cols)
X_reg = df_model[reg_features]
y_reg = df_model["Rating"]

Xr_train, Xr_test, yr_train, yr_test = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42)

scaler_reg = StandardScaler()
Xr_train_s = scaler_reg.fit_transform(Xr_train)
Xr_test_s = scaler_reg.transform(Xr_test)

# Baseline Ridge (default alpha)
ridge_base = Ridge(alpha=1.0, random_state=42)
ridge_base.fit(Xr_train_s, yr_train)
pred_base = ridge_base.predict(Xr_test_s)

reg_baseline = {
    "MAE": mean_absolute_error(yr_test, pred_base),
    "RMSE": root_mean_squared_error(yr_test, pred_base),
    "R2": r2_score(yr_test, pred_base),
}

# GridSearchCV tuning alpha
ridge_grid = GridSearchCV(
    Ridge(random_state=42),
    param_grid={"alpha": [0.01, 0.1, 1, 10, 100]},
    scoring="neg_mean_absolute_error",
    cv=5,
)
ridge_grid.fit(Xr_train_s, yr_train)
best_ridge = ridge_grid.best_estimator_
pred_tuned = best_ridge.predict(Xr_test_s)

reg_tuned = {
    "MAE": mean_absolute_error(yr_test, pred_tuned),
    "RMSE": root_mean_squared_error(yr_test, pred_tuned),
    "R2": r2_score(yr_test, pred_tuned),
}

RESULTS["regression"] = {
    "best_alpha": ridge_grid.best_params_["alpha"],
    "baseline": reg_baseline,
    "tuned": reg_tuned,
    "features": reg_features,
}

# Plot: Actual vs Predicted ratings
plt.figure(figsize=(6, 5))
plt.scatter(yr_test, pred_tuned, alpha=0.3, color="#4C72B0")
plt.plot([1, 5], [1, 5], "r--", label="Perfect prediction")
plt.xlabel("Actual Rating")
plt.ylabel("Predicted Rating")
plt.title("Ridge Regression: Actual vs Predicted Rating (Tuned)")
plt.legend()
plt.tight_layout()
plt.savefig("/home/claude/project/plot_regression.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Step 4: Classification Model -- Logistic Regression predicting Purchase_Status
# ---------------------------------------------------------------------------
clf_features = ["Price", "Number_of_Views", "Cart_Status", "Time_Spent",
                 "Previous_Purchases", "Rating"] + list(cat_cols)
X_clf = df_model[clf_features]
y_clf = df_model["Purchase_Status"]

Xc_train, Xc_test, yc_train, yc_test = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf)

scaler_clf = StandardScaler()
Xc_train_s = scaler_clf.fit_transform(Xc_train)
Xc_test_s = scaler_clf.transform(Xc_test)

# Baseline Logistic Regression
logreg_base = LogisticRegression(max_iter=200, random_state=42)
logreg_base.fit(Xc_train_s, yc_train)
pred_base_c = logreg_base.predict(Xc_test_s)

clf_baseline = {
    "Accuracy": accuracy_score(yc_test, pred_base_c),
    "Precision": precision_score(yc_test, pred_base_c, zero_division=0),
    "Recall": recall_score(yc_test, pred_base_c, zero_division=0),
    "F1": f1_score(yc_test, pred_base_c, zero_division=0),
}

# GridSearchCV tuning
logreg_grid = GridSearchCV(
    LogisticRegression(random_state=42),
    param_grid={
        "C": [0.01, 0.1, 1, 10],
        "solver": ["liblinear", "lbfgs"],
        "max_iter": [100, 200, 500],
    },
    scoring="f1",
    cv=5,
    n_jobs=-1,
)
logreg_grid.fit(Xc_train_s, yc_train)
best_logreg = logreg_grid.best_estimator_
pred_tuned_c = best_logreg.predict(Xc_test_s)

clf_tuned = {
    "Accuracy": accuracy_score(yc_test, pred_tuned_c),
    "Precision": precision_score(yc_test, pred_tuned_c, zero_division=0),
    "Recall": recall_score(yc_test, pred_tuned_c, zero_division=0),
    "F1": f1_score(yc_test, pred_tuned_c, zero_division=0),
}
cm = confusion_matrix(yc_test, pred_tuned_c)

RESULTS["classification"] = {
    "best_params": logreg_grid.best_params_,
    "baseline": clf_baseline,
    "tuned": clf_tuned,
    "confusion_matrix": cm.tolist(),
    "features": clf_features,
}

# Plot: Confusion matrix
plt.figure(figsize=(5, 4.5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Not Purchased", "Purchased"],
            yticklabels=["Not Purchased", "Purchased"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Logistic Regression: Confusion Matrix (Tuned)")
plt.tight_layout()
plt.savefig("/home/claude/project/plot_confusion_matrix.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Step 5: Clustering Model -- K-Means customer segmentation
# ---------------------------------------------------------------------------
customer = df.groupby("User_ID").agg(
    Number_of_Views=("Number_of_Views", "sum"),
    Number_of_Purchases=("Purchase_Status", "sum"),
    Avg_Rating=("Rating", "mean"),
    Avg_Time_Spent=("Time_Spent", "mean"),
    Total_Amount_Spent=("Price", lambda x: (x * df.loc[x.index, "Purchase_Status"]).sum()),
    Num_Added_to_Cart=("Cart_Status", "sum"),
).reset_index()

cluster_features = ["Number_of_Views", "Number_of_Purchases", "Avg_Rating",
                     "Avg_Time_Spent", "Total_Amount_Spent", "Num_Added_to_Cart"]
X_cluster = customer[cluster_features]

scaler_cluster = StandardScaler()
X_cluster_s = scaler_cluster.fit_transform(X_cluster)

# Elbow method + silhouette across k = 2..6
elbow_inertia = {}
elbow_silhouette = {}
for k in range(2, 7):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_k = km.fit_predict(X_cluster_s)
    elbow_inertia[k] = km.inertia_
    elbow_silhouette[k] = silhouette_score(X_cluster_s, labels_k)

best_k = max(elbow_silhouette, key=elbow_silhouette.get)

final_km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
customer["Cluster"] = final_km.fit_predict(X_cluster_s)

cluster_profile = customer.groupby("Cluster")[cluster_features].mean().round(2)

RESULTS["clustering"] = {
    "best_k": int(best_k),
    "inertia_by_k": elbow_inertia,
    "silhouette_by_k": elbow_silhouette,
    "final_inertia": float(final_km.inertia_),
    "final_silhouette": float(elbow_silhouette[best_k]),
    "cluster_sizes": customer["Cluster"].value_counts().sort_index().to_dict(),
    "cluster_profile": cluster_profile.to_dict(orient="index"),
    "features": cluster_features,
}

# Plot: Elbow method
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].plot(list(elbow_inertia.keys()), list(elbow_inertia.values()), marker="o", color="#4C72B0")
axes[0].set_xlabel("Number of Clusters (k)")
axes[0].set_ylabel("Inertia")
axes[0].set_title("Elbow Method")

axes[1].plot(list(elbow_silhouette.keys()), list(elbow_silhouette.values()), marker="o", color="#DD8452")
axes[1].set_xlabel("Number of Clusters (k)")
axes[1].set_ylabel("Silhouette Score")
axes[1].set_title("Silhouette Score by k")
plt.tight_layout()
plt.savefig("/home/claude/project/plot_elbow_silhouette.png", dpi=150)
plt.close()

# Plot: Cluster scatter (2 most interpretable dims)
plt.figure(figsize=(6, 5))
sns.scatterplot(data=customer, x="Total_Amount_Spent", y="Number_of_Views",
                 hue="Cluster", palette="Set2", alpha=0.7)
plt.title(f"Customer Segments (k={best_k})")
plt.tight_layout()
plt.savefig("/home/claude/project/plot_clusters.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# Save all results to JSON for the report-writing step
# ---------------------------------------------------------------------------
with open("/home/claude/project/results.json", "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)

print("Pipeline complete.")
print(json.dumps(RESULTS["regression"], indent=2))
print(json.dumps(RESULTS["classification"], indent=2))
print("Best k:", best_k, "Silhouette:", elbow_silhouette[best_k])
