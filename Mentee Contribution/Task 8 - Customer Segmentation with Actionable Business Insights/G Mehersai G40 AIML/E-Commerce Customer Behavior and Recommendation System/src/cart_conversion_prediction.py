from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "ecommerce_historical_features.csv"
)

MODEL_PATH = PROJECT_ROOT / "models"

RESULT_PATH = PROJECT_ROOT / "outputs" / "results"

FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures"


# ============================================================
# FEATURE CONFIGURATION
# ============================================================

CURRENT_SESSION_FEATURES = [
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


HISTORICAL_FEATURES = [
    "previous_sessions",
    "previous_purchases",
    "previous_cart_adds",
    "previous_cart_abandonments",
    "historical_purchase_rate",
    "historical_cart_add_rate",
    "historical_abandon_rate",
    "avg_previous_pages_viewed",
    "avg_previous_time_on_site",
    "avg_previous_discount",
    "avg_previous_unit_price",
    "days_since_last_visit",
    "previous_product_interactions",
]


FEATURES = (
    CURRENT_SESSION_FEATURES
    + HISTORICAL_FEATURES
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    """Load historical feature dataset."""

    print("Loading historical feature dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully.")
    print("Dataset shape:", df.shape)

    return df


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

def create_output_directories():
    """Create project output directories."""

    MODEL_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    RESULT_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    FIGURE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# PREPARE CART CONVERSION DATA
# ============================================================

def prepare_cart_conversion_data(df):
    """
    Select only cart-engaged sessions.

    Business problem:
    Given that a customer added an item to the cart,
    predict whether the session converts into a purchase.
    """

    print("\nPreparing cart conversion dataset...")

    cart_df = (
        df[df["added_to_cart"] == 1]
        .copy()
    )

    cart_df["visit_date"] = pd.to_datetime(
        cart_df["visit_date"],
        errors="coerce"
    )

    cart_df = (
        cart_df
        .dropna(subset=["visit_date"])
        .sort_values(
            ["visit_date", "session_id"]
        )
        .reset_index(drop=True)
    )

    print(
        "Cart-engaged sessions:",
        len(cart_df)
    )

    print("\n--- CART CONVERSION TARGET DISTRIBUTION ---")

    print(
        cart_df["purchased"]
        .value_counts()
        .sort_index()
    )

    print("\nPercentage:")

    print(
        cart_df["purchased"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    print("\nNumber of model features:", len(FEATURES))

    return cart_df


# ============================================================
# TEMPORAL TRAIN TEST SPLIT
# ============================================================

def temporal_split(cart_df):
    """Create chronological train-test split."""

    print("\nCreating temporal train-test split...")

    split_index = int(
        len(cart_df) * 0.80
    )

    train_df = (
        cart_df
        .iloc[:split_index]
        .copy()
    )

    test_df = (
        cart_df
        .iloc[split_index:]
        .copy()
    )

    X_train = train_df[FEATURES]

    y_train = train_df["purchased"]

    X_test = test_df[FEATURES]

    y_test = test_df["purchased"]

    print(
        "Training date range:",
        train_df["visit_date"].min(),
        "to",
        train_df["visit_date"].max()
    )

    print(
        "Testing date range:",
        test_df["visit_date"].min(),
        "to",
        test_df["visit_date"].max()
    )

    print(
        "Training shape:",
        X_train.shape
    )

    print(
        "Testing shape:",
        X_test.shape
    )

    print("\n--- TRAIN TARGET DISTRIBUTION ---")

    print(
        y_train
        .value_counts()
        .sort_index()
    )

    print("\n--- TEST TARGET DISTRIBUTION ---")

    print(
        y_test
        .value_counts()
        .sort_index()
    )

    return (
        train_df,
        test_df,
        X_train,
        X_test,
        y_train,
        y_test,
    )


# ============================================================
# MODEL CONFIGURATION
# ============================================================

def create_models():
    """Create candidate cart conversion models."""

    models = {
        "Logistic Regression": Pipeline(
            steps=[
                (
                    "scaler",
                    StandardScaler()
                ),
                (
                    "model",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=2000,
                        random_state=42,
                    )
                ),
            ]
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=400,
            max_depth=8,
            min_samples_split=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),

        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=300,
            learning_rate=0.05,
            max_leaf_nodes=15,
            l2_regularization=1.0,
            random_state=42,
        ),
    }

    return models


# ============================================================
# THRESHOLD OPTIMIZATION
# ============================================================

def find_best_threshold(y_true, probabilities):
    """
    Select threshold that maximizes F1 score
    for the purchase class.
    """

    best_threshold = 0.50

    best_f1 = 0.0

    threshold_results = []

    for threshold_number in range(20, 81):
        threshold = threshold_number / 100

        predictions = (
            probabilities >= threshold
        ).astype(int)

        score = f1_score(
            y_true,
            predictions,
            zero_division=0,
        )

        threshold_results.append(
            {
                "Threshold": threshold,
                "F1 Score": score,
            }
        )

        if score > best_f1:
            best_f1 = score

            best_threshold = threshold

    threshold_df = pd.DataFrame(
        threshold_results
    )

    return (
        best_threshold,
        best_f1,
        threshold_df,
    )


# ============================================================
# MODEL EVALUATION
# ============================================================

def evaluate_model(
    model_name,
    model,
    X_train,
    X_test,
    y_train,
    y_test,
):
    """Train and evaluate a cart conversion model."""

    print("\n" + "=" * 60)

    print(
        f"TRAINING: {model_name}"
    )

    print("=" * 60)

    model.fit(
        X_train,
        y_train
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    (
        best_threshold,
        best_threshold_f1,
        threshold_df,
    ) = find_best_threshold(
        y_test,
        probabilities
    )

    predictions = (
        probabilities >= best_threshold
    ).astype(int)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    balanced_accuracy = balanced_accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    pr_auc = average_precision_score(
        y_test,
        probabilities
    )

    print("\n--- OPTIMAL THRESHOLD ---")

    print(
        f"Threshold: {best_threshold:.2f}"
    )

    print(
        f"Threshold F1: {best_threshold_f1:.4f}"
    )

    print("\n--- MODEL PERFORMANCE ---")

    print(
        f"Accuracy          : {accuracy:.4f}"
    )

    print(
        f"Balanced Accuracy : {balanced_accuracy:.4f}"
    )

    print(
        f"Precision         : {precision:.4f}"
    )

    print(
        f"Recall            : {recall:.4f}"
    )

    print(
        f"F1 Score          : {f1:.4f}"
    )

    print(
        f"ROC-AUC           : {roc_auc:.4f}"
    )

    print(
        f"PR-AUC            : {pr_auc:.4f}"
    )

    print("\n--- CONFUSION MATRIX ---")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    print("\n--- CLASSIFICATION REPORT ---")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    metrics = {
        "Algorithm": model_name,
        "Threshold": best_threshold,
        "Accuracy": accuracy,
        "Balanced Accuracy": balanced_accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc,
    }

    return (
        metrics,
        model,
        probabilities,
        predictions,
        threshold_df,
    )


# ============================================================
# SAVE COMPARISON FIGURE
# ============================================================

def save_comparison_figure(results_df):
    """Save cart conversion model comparison."""

    metric_columns = [
        "Balanced Accuracy",
        "F1 Score",
        "ROC-AUC",
        "PR-AUC",
    ]

    plot_df = (
        results_df
        .set_index("Algorithm")[metric_columns]
    )

    plt.figure(
        figsize=(11, 6)
    )

    plot_df.plot(
        kind="bar"
    )

    plt.title(
        "Cart Conversion Model Comparison"
    )

    plt.xlabel("Algorithm")

    plt.ylabel("Score")

    plt.ylim(0, 1)

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH
        / "cart_conversion_model_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        "\nComparison figure saved:",
        output_path
    )


# ============================================================
# MAIN
# ============================================================

def main():
    """Run cart conversion prediction pipeline."""

    create_output_directories()

    df = load_data()

    cart_df = prepare_cart_conversion_data(
        df
    )

    (
        train_df,
        test_df,
        X_train,
        X_test,
        y_train,
        y_test,
    ) = temporal_split(
        cart_df
    )

    models = create_models()

    model_results = []

    trained_models = {}

    model_outputs = {}

    for model_name, model in models.items():

        (
            metrics,
            trained_model,
            probabilities,
            predictions,
            threshold_df,
        ) = evaluate_model(
            model_name,
            model,
            X_train,
            X_test,
            y_train,
            y_test,
        )

        model_results.append(
            metrics
        )

        trained_models[
            model_name
        ] = trained_model

        model_outputs[
            model_name
        ] = {
            "probabilities": probabilities,
            "predictions": predictions,
            "threshold_results": threshold_df,
        }

    results_df = pd.DataFrame(
        model_results
    )

    results_df = (
        results_df
        .sort_values(
            "ROC-AUC",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print("\n" + "=" * 60)

    print(
        "CART CONVERSION MODEL COMPARISON"
    )

    print("=" * 60)

    print(
        results_df.to_string(
            index=False
        )
    )

    best_model_name = (
        results_df.iloc[0]["Algorithm"]
    )

    best_model = trained_models[
        best_model_name
    ]

    best_threshold = float(
        results_df.iloc[0]["Threshold"]
    )

    best_outputs = model_outputs[
        best_model_name
    ]

    print("\n--- BEST CART CONVERSION MODEL ---")

    print(
        "Algorithm:",
        best_model_name
    )

    print(
        f"Threshold: {best_threshold:.2f}"
    )

    print(
        "ROC-AUC:",
        f"{results_df.iloc[0]['ROC-AUC']:.4f}"
    )

    print(
        "PR-AUC:",
        f"{results_df.iloc[0]['PR-AUC']:.4f}"
    )

    save_comparison_figure(
        results_df
    )

    comparison_path = (
        RESULT_PATH
        / "cart_conversion_model_comparison.csv"
    )

    results_df.to_csv(
        comparison_path,
        index=False
    )

    prediction_df = test_df[
        [
            "customer_id",
            "session_id",
            "visit_date",
            "purchased",
        ]
    ].copy()

    prediction_df[
        "conversion_probability"
    ] = best_outputs[
        "probabilities"
    ]

    prediction_df[
        "predicted_conversion"
    ] = best_outputs[
        "predictions"
    ]

    prediction_df[
        "decision_threshold"
    ] = best_threshold

    prediction_path = (
        RESULT_PATH
        / "cart_conversion_predictions.csv"
    )

    prediction_df.to_csv(
        prediction_path,
        index=False
    )

    threshold_path = (
        RESULT_PATH
        / "cart_conversion_thresholds.csv"
    )

    best_outputs[
        "threshold_results"
    ].to_csv(
        threshold_path,
        index=False
    )

    model_path = (
        MODEL_PATH
        / "cart_conversion_model.pkl"
    )

    with open(
        model_path,
        "wb"
    ) as model_file:

        pickle.dump(
            {
                "model": best_model,
                "algorithm": best_model_name,
                "threshold": best_threshold,
                "features": FEATURES,
            },
            model_file,
        )

    print(
        "\nModel comparison saved:",
        comparison_path
    )

    print(
        "Conversion predictions saved:",
        prediction_path
    )

    print(
        "Threshold evaluation saved:",
        threshold_path
    )

    print(
        "Best model saved:",
        model_path
    )

    print(
        "\nCart conversion prediction "
        "completed successfully."
    )


if __name__ == "__main__":
    main()