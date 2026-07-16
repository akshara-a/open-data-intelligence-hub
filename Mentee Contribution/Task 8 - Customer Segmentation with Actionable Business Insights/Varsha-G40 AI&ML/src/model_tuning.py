# ==========================================
# Hyperparameter Tuning
# ==========================================

import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.cluster import KMeans
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.metrics import (
    silhouette_score,
    accuracy_score,
    r2_score
)

# ------------------------------------------
# Load Dataset
# ------------------------------------------

df = pd.read_csv("reports/customer_segments.csv")

print("=" * 60)
print("HYPERPARAMETER TUNING")
print("=" * 60)

# ==========================================
# K-Means Hyperparameter Tuning
# ==========================================

print("\nK-Means Hyperparameter Tuning")

cluster_features = df[
    [
        "R",
        "F",
        "M",
        "Income",
        "Age"
    ]
]

best_score = -1
best_model = None
best_k = None

for k in range(2,11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(cluster_features)

    score = silhouette_score(cluster_features, labels)

    print(f"k={k} --> Silhouette Score={score:.4f}")

    if score > best_score:
        best_score = score
        best_model = model
        best_k = k

print("\nBest Number of Clusters:", best_k)
print("Best Silhouette Score:", round(best_score,4))

# ==========================================
# Ridge Regression Hyperparameter Tuning
# ==========================================

print("\nRidge Regression Hyperparameter Tuning")

X = df[
    [
        "Income",
        "Age",
        "R",
        "F",
        "Children",
        "CampaignsAccepted",
        "WebActivity"
    ]
]

y = df["M"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

ridge = Ridge()

parameters = {
    "alpha":[0.01,0.1,1,10,100]
}

grid = GridSearchCV(
    ridge,
    parameters,
    cv=5,
    scoring="r2"
)

grid.fit(X_train,y_train)

best_ridge = grid.best_estimator_

prediction = best_ridge.predict(X_test)

print("\nBest Alpha:",grid.best_params_)

print("Best CV Score:",round(grid.best_score_,4))

print("Test R2 Score:",round(r2_score(y_test,prediction),4))

# ==========================================
# Logistic Regression Hyperparameter Tuning
# ==========================================

print("\nLogistic Regression Hyperparameter Tuning")

df["PurchaseLikelihood"] = (
    df["F"] >= df["F"].median()
).astype(int)

X = df[
    [
        "Income",
        "Age",
        "R",
        "M",
        "Children",
        "CampaignsAccepted",
        "WebActivity"
    ]
]

y = df["PurchaseLikelihood"]

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

logistic = LogisticRegression()

parameters = {

    "C":[0.01,0.1,1,10],

    "solver":[
        "liblinear",
        "lbfgs"
    ],

    "max_iter":[100,500,1000]

}

grid = GridSearchCV(
    logistic,
    parameters,
    cv=5,
    scoring="accuracy"
)

grid.fit(X_train,y_train)

best_logistic = grid.best_estimator_

prediction = best_logistic.predict(X_test)

print("\nBest Parameters")

print(grid.best_params_)

print("\nBest CV Accuracy")

print(round(grid.best_score_,4))

print("\nTest Accuracy")

print(round(
    accuracy_score(
        y_test,
        prediction
    ),
4))

# ==========================================
# Save Results
# ==========================================

results = pd.DataFrame({

    "Model":[
        "KMeans",
        "Ridge Regression",
        "Logistic Regression"
    ],

    "Best Parameter":[
        f"Clusters={best_k}",
        str(grid.best_params_) if False else str({"alpha": grid.best_params_.get("alpha", "N/A")}),
        str(best_logistic.get_params())
    ]

})

results.to_csv(
    "reports/tuned_models.csv",
    index=False
)

print("\nHyperparameter Tuning Completed Successfully!")