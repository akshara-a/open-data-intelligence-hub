import os
import warnings

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

DATA_PATH = "data/customer_purchase_data.csv"
OUTPUT_FOLDER = "outputs"


def calculate_metrics(model, x_test, y_test):
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]

    return {
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions, zero_division=0),
        "Recall": recall_score(y_test, predictions, zero_division=0),
        "F1-Score": f1_score(y_test, predictions, zero_division=0),
        "ROC-AUC": roc_auc_score(y_test, probabilities),
    }


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Load the dataset
    data = pd.read_csv(DATA_PATH)

    print("\nDataset shape:")
    print(data.shape)

    print("\nFirst five rows:")
    print(data.head())

    print("\nMissing values:")
    print(data.isnull().sum())

    print("\nDuplicate rows:")
    print(data.duplicated().sum())

    print("\nTarget distribution:")
    print(data["Purchase"].value_counts())

    # Remove duplicate rows
    data = data.drop_duplicates()

    # CustomerID is only an identifier, so it is removed
    features = data.drop(columns=["CustomerID", "Purchase"])
    target = data["Purchase"]

    numerical_columns = features.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_columns = features.select_dtypes(
        include=["object"]
    ).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numerical_columns),
            ("categorical", categorical_pipeline, categorical_columns),
        ]
    )

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=42,
        stratify=target,
    )

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=42,
        ),
        "Decision Tree": DecisionTreeClassifier(
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            random_state=42,
        ),
    }

    results = []

    print("\nBaseline model results:")

    for model_name, classifier in models.items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("classifier", classifier),
            ]
        )

        pipeline.fit(x_train, y_train)
        metrics = calculate_metrics(pipeline, x_test, y_test)
        metrics["Model"] = model_name
        results.append(metrics)

        print(f"\n{model_name}")
        for metric_name, metric_value in metrics.items():
            if metric_name != "Model":
                print(f"{metric_name}: {metric_value:.4f}")

    baseline_results = pd.DataFrame(results)
    baseline_results = baseline_results[
        [
            "Model",
            "Accuracy",
            "Precision",
            "Recall",
            "F1-Score",
            "ROC-AUC",
        ]
    ]

    baseline_results.to_csv(
        f"{OUTPUT_FOLDER}/baseline_model_results.csv",
        index=False,
    )

    # Optimize Random Forest
    forest_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(random_state=42),
            ),
        ]
    )

    parameter_grid = {
        "classifier__n_estimators": [100, 200],
        "classifier__max_depth": [None, 8, 15],
        "classifier__min_samples_split": [2, 5],
        "classifier__min_samples_leaf": [1, 2],
        "classifier__class_weight": [None, "balanced"],
    }

    print("\nOptimizing Random Forest...")

    grid_search = GridSearchCV(
        estimator=forest_pipeline,
        param_grid=parameter_grid,
        scoring="f1",
        cv=5,
        n_jobs=-1,
        verbose=1,
    )

    grid_search.fit(x_train, y_train)

    best_model = grid_search.best_estimator_
    optimized_metrics = calculate_metrics(
        best_model,
        x_test,
        y_test,
    )

    print("\nBest parameters:")
    print(grid_search.best_params_)

    print("\nOptimized Random Forest results:")
    for metric_name, metric_value in optimized_metrics.items():
        print(f"{metric_name}: {metric_value:.4f}")

    optimized_result = pd.DataFrame(
        [
            {
                "Model": "Optimized Random Forest",
                **optimized_metrics,
            }
        ]
    )

    final_results = pd.concat(
        [baseline_results, optimized_result],
        ignore_index=True,
    )

    final_results.to_csv(
        f"{OUTPUT_FOLDER}/model_comparison.csv",
        index=False,
    )

    # Confusion matrix
    predictions = best_model.predict(x_test)
    matrix = confusion_matrix(y_test, predictions)

    plt.figure(figsize=(6, 5))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["No Purchase", "Purchase"],
        yticklabels=["No Purchase", "Purchase"],
    )
    plt.title("Optimized Random Forest Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_FOLDER}/confusion_matrix.png")
    plt.close()

    # Feature importance
    feature_names = best_model.named_steps[
        "preprocessor"
    ].get_feature_names_out()

    importance_values = best_model.named_steps[
        "classifier"
    ].feature_importances_

    feature_importance = pd.DataFrame(
        {
            "Feature": feature_names,
            "Importance": importance_values,
        }
    ).sort_values(
        by="Importance",
        ascending=False,
    )

    feature_importance.to_csv(
        f"{OUTPUT_FOLDER}/feature_importance.csv",
        index=False,
    )

    top_features = feature_importance.head(10).sort_values(
        by="Importance"
    )

    plt.figure(figsize=(10, 6))
    plt.barh(
        top_features["Feature"],
        top_features["Importance"],
    )
    plt.title("Top 10 Features Influencing Purchase")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_FOLDER}/feature_importance.png")
    plt.close()

    joblib.dump(
        best_model,
        f"{OUTPUT_FOLDER}/best_purchase_model.pkl",
    )

    print("\nAll results saved inside the outputs folder.")
    print("\nTop ten important features:")
    print(feature_importance.head(10))


if __name__ == "__main__":
    main()