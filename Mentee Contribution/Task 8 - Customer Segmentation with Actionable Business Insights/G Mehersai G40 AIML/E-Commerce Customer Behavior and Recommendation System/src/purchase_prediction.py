from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import (
    RandomizedSearchCV,
    train_test_split,
)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "Ecommerce.csv"

MODEL_PATH = PROJECT_ROOT / "models"

FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures"

RESULT_PATH = PROJECT_ROOT / "outputs" / "results"


MODEL_PATH.mkdir(
    parents=True,
    exist_ok=True
)

FIGURE_PATH.mkdir(
    parents=True,
    exist_ok=True
)

RESULT_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# MODEL CONFIGURATION
# --------------------------------------------------

RANDOM_STATE = 42

TARGET = "purchased"


FEATURES = [
    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "unit_price",
    "quantity",
    "discount_percent",
    "discount_amount",
    "pages_viewed",
    "time_on_site_sec",
    "visit_day",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "location",
]


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

def load_data(file_path):
    """Load the e-commerce dataset."""

    return pd.read_csv(file_path)


# --------------------------------------------------
# FEATURE SELECTION
# --------------------------------------------------

def prepare_features(df):
    """Select leakage-safe features and target."""

    X = df[FEATURES].copy()

    y = df[TARGET].copy()

    return X, y


# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

def split_data(X, y):
    """Create a stratified train-test split."""

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


# --------------------------------------------------
# TRAINING DATA BALANCING
# --------------------------------------------------

def balance_training_data(X_train, y_train):
    """Balance only the training data using undersampling."""

    train_df = X_train.copy()

    train_df[TARGET] = y_train.values

    not_purchased = train_df[
        train_df[TARGET] == 0
    ]

    purchased = train_df[
        train_df[TARGET] == 1
    ]

    not_purchased_sample = not_purchased.sample(
        n=len(purchased),
        random_state=RANDOM_STATE,
    )

    balanced_train = pd.concat(
        [
            not_purchased_sample,
            purchased,
        ],
        ignore_index=True,
    )

    balanced_train = balanced_train.sample(
        frac=1,
        random_state=RANDOM_STATE,
    ).reset_index(
        drop=True
    )

    X_train_balanced = balanced_train[
        FEATURES
    ]

    y_train_balanced = balanced_train[
        TARGET
    ]

    return (
        X_train_balanced,
        y_train_balanced,
    )


# --------------------------------------------------
# CLASS DISTRIBUTION
# --------------------------------------------------

def display_class_distribution(y, title):
    """Display target class count and percentage."""

    print(
        f"\n--- {title} ---"
    )

    print(
        y.value_counts().sort_index()
    )

    print(
        "\nPercentage:"
    )

    print(
        y.value_counts(
            normalize=True
        )
        .sort_index()
        .mul(100)
        .round(2)
    )


# --------------------------------------------------
# HYPERPARAMETER TUNING
# --------------------------------------------------

def tune_random_forest(X_train, y_train):
    """Tune Random Forest using RandomizedSearchCV."""

    random_forest = RandomForestClassifier(
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    parameter_distribution = {
        "n_estimators": [
            100,
            200,
            300,
            400,
        ],
        "max_depth": [
            None,
            5,
            10,
            15,
            20,
        ],
        "min_samples_split": [
            2,
            5,
            10,
        ],
        "min_samples_leaf": [
            1,
            2,
            4,
        ],
        "max_features": [
            "sqrt",
            "log2",
        ],
    }

    random_search = RandomizedSearchCV(
        estimator=random_forest,
        param_distributions=parameter_distribution,
        n_iter=20,
        scoring="roc_auc",
        cv=5,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
    )

    random_search.fit(
        X_train,
        y_train,
    )

    return random_search


# --------------------------------------------------
# MODEL EVALUATION
# --------------------------------------------------

def evaluate_model(model, X_test, y_test):
    """Evaluate the model on the untouched test data."""

    y_pred = model.predict(
        X_test
    )

    y_probability = model.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        y_pred,
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability,
    )

    matrix = confusion_matrix(
        y_test,
        y_pred,
    )

    print(
        "\n--- MODEL PERFORMANCE ---"
    )

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1 Score : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )

    print(
        "\n--- CONFUSION MATRIX ---"
    )

    print(
        matrix
    )

    print(
        "\n--- CLASSIFICATION REPORT ---"
    )

    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0,
        )
    )

    metrics = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
    }

    return metrics, matrix


# --------------------------------------------------
# FEATURE IMPORTANCE
# --------------------------------------------------

def analyze_feature_importance(model):
    """Analyze and visualize Random Forest feature importance."""

    feature_importance = pd.DataFrame(
        {
            "Feature": FEATURES,
            "Importance": model.feature_importances_,
        }
    )

    feature_importance = feature_importance.sort_values(
        by="Importance",
        ascending=False,
    )

    print(
        "\n--- FEATURE IMPORTANCE ---"
    )

    print(
        feature_importance.to_string(
            index=False
        )
    )

    figure_data = feature_importance.sort_values(
        by="Importance"
    )

    plt.figure(
        figsize=(9, 7)
    )

    plt.barh(
        figure_data["Feature"],
        figure_data["Importance"],
    )

    plt.title(
        "Random Forest Feature Importance"
    )

    plt.xlabel(
        "Importance"
    )

    plt.ylabel(
        "Feature"
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH / "rf_importance.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"\nFeature importance figure saved: {output_path}"
    )

    return feature_importance


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

def save_results(metrics, feature_importance):
    """Save model metrics and feature importance."""

    metrics_df = pd.DataFrame(
        [metrics]
    )

    metrics_path = (
        RESULT_PATH / "rf_metrics.csv"
    )

    importance_path = (
        RESULT_PATH / "rf_importance.csv"
    )

    metrics_df.to_csv(
        metrics_path,
        index=False,
    )

    feature_importance.to_csv(
        importance_path,
        index=False,
    )

    print(
        f"Metrics saved: {metrics_path}"
    )

    print(
        f"Feature importance saved: {importance_path}"
    )


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

def save_model(model):
    """Save the trained Random Forest model."""

    model_file = (
        MODEL_PATH / "rf_model.pkl"
    )

    joblib.dump(
        model,
        model_file,
    )

    print(
        f"Model saved: {model_file}"
    )


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------

def main():
    print(
        "Loading dataset..."
    )

    df = load_data(
        DATA_PATH
    )

    print(
        "Dataset loaded successfully."
    )

    print(
        "Dataset shape:",
        df.shape
    )

    print(
        "\nPreparing leakage-safe features..."
    )

    X, y = prepare_features(
        df
    )

    print(
        "Number of features:",
        X.shape[1]
    )

    print(
        "Selected features:"
    )

    for feature in FEATURES:
        print(
            f"- {feature}"
        )

    display_class_distribution(
        y,
        "ORIGINAL TARGET DISTRIBUTION",
    )

    print(
        "\nCreating stratified train-test split..."
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = split_data(
        X,
        y,
    )

    print(
        "Training shape:",
        X_train.shape
    )

    print(
        "Testing shape:",
        X_test.shape
    )

    display_class_distribution(
        y_train,
        "TRAINING DISTRIBUTION BEFORE BALANCING",
    )

    display_class_distribution(
        y_test,
        "UNTOUCHED TEST DISTRIBUTION",
    )

    print(
        "\nBalancing training data..."
    )

    (
        X_train_balanced,
        y_train_balanced,
    ) = balance_training_data(
        X_train,
        y_train,
    )

    print(
        "Balanced training shape:",
        X_train_balanced.shape
    )

    display_class_distribution(
        y_train_balanced,
        "TRAINING DISTRIBUTION AFTER BALANCING",
    )

    print(
        "\nStarting RandomizedSearchCV..."
    )

    random_search = tune_random_forest(
        X_train_balanced,
        y_train_balanced,
    )

    print(
        "\nHyperparameter tuning completed."
    )

    print(
        "\nBest Parameters:"
    )

    print(
        random_search.best_params_
    )

    print(
        f"\nBest Cross-Validation ROC-AUC: "
        f"{random_search.best_score_:.4f}"
    )

    best_model = (
        random_search.best_estimator_
    )

    print(
        "\nEvaluating model on untouched test data..."
    )

    metrics, _ = evaluate_model(
        best_model,
        X_test,
        y_test,
    )

    feature_importance = (
        analyze_feature_importance(
            best_model
        )
    )

    save_results(
        metrics,
        feature_importance,
    )

    save_model(
        best_model
    )

    print(
        "\nPurchase prediction completed successfully."
    )


# --------------------------------------------------
# SCRIPT ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()