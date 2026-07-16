from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.utils.class_weight import compute_sample_weight


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "ecommerce_historical_features.csv"
)

RESULT_PATH = PROJECT_ROOT / "outputs" / "results"

FIGURE_PATH = PROJECT_ROOT / "outputs" / "figures"

MODEL_PATH = PROJECT_ROOT / "models"


# ---------------------------------------------------------
# CREATE OUTPUT DIRECTORIES
# ---------------------------------------------------------

def create_output_directories():
    """Create directories used for models and outputs."""

    RESULT_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    FIGURE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    MODEL_PATH.mkdir(
        parents=True,
        exist_ok=True
    )


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_data(file_path):
    """Load historical feature dataset."""

    print("Loading historical feature dataset...")

    df = pd.read_csv(
        file_path,
        parse_dates=["visit_date"]
    )

    print("Dataset loaded successfully.")
    print("Dataset shape:", df.shape)

    return df


# ---------------------------------------------------------
# PREPARE FEATURES
# ---------------------------------------------------------

def prepare_features(df):
    """Prepare leakage-safe current and historical features."""

    current_session_features = [
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

    historical_features = [
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

    feature_columns = (
        current_session_features
        + historical_features
    )

    X = df[feature_columns].copy()

    y = df["purchased"].copy()

    print("\n--- FEATURE CONFIGURATION ---")

    print(
        "Current session features:",
        len(current_session_features)
    )

    print(
        "Historical customer features:",
        len(historical_features)
    )

    print(
        "Total features:",
        len(feature_columns)
    )

    print("\nHistorical features:")

    for feature in historical_features:
        print("-", feature)

    return X, y, feature_columns


# ---------------------------------------------------------
# TEMPORAL TRAIN-TEST SPLIT
# ---------------------------------------------------------

def temporal_train_test_split(
    df,
    X,
    y,
    train_fraction=0.80
):
    """Split earlier sessions for training and later sessions for testing."""

    print("\nCreating temporal train-test split...")

    temporal_order = df.sort_values(
        by=[
            "visit_date",
            "session_id"
        ]
    ).index

    split_position = int(
        len(temporal_order)
        * train_fraction
    )

    train_indices = temporal_order[
        :split_position
    ]

    test_indices = temporal_order[
        split_position:
    ]

    X_train = X.loc[train_indices].copy()
    X_test = X.loc[test_indices].copy()

    y_train = y.loc[train_indices].copy()
    y_test = y.loc[test_indices].copy()

    train_dates = df.loc[
        train_indices,
        "visit_date"
    ]

    test_dates = df.loc[
        test_indices,
        "visit_date"
    ]

    print(
        "Training date range:",
        train_dates.min(),
        "to",
        train_dates.max()
    )

    print(
        "Testing date range:",
        test_dates.min(),
        "to",
        test_dates.max()
    )

    print(
        "Training shape:",
        X_train.shape
    )

    print(
        "Testing shape:",
        X_test.shape
    )

    print(
        "\n--- TRAIN TARGET DISTRIBUTION ---"
    )

    print(
        y_train
        .value_counts()
        .sort_index()
    )

    print("\nPercentage:")

    print(
        y_train
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    print(
        "\n--- TEST TARGET DISTRIBUTION ---"
    )

    print(
        y_test
        .value_counts()
        .sort_index()
    )

    print("\nPercentage:")

    print(
        y_test
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


# ---------------------------------------------------------
# MODEL CONFIGURATION
# ---------------------------------------------------------

def create_models():
    """Create models for temporal purchase prediction."""

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=400,
            max_depth=8,
            min_samples_split=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),

        "HistGradientBoosting": (
            HistGradientBoostingClassifier(
                learning_rate=0.05,
                max_iter=300,
                max_leaf_nodes=15,
                l2_regularization=1.0,
                random_state=42,
            )
        ),
    }

    return models


# ---------------------------------------------------------
# MODEL EVALUATION
# ---------------------------------------------------------

def evaluate_model(
    model_name,
    model,
    X_train,
    X_test,
    y_train,
    y_test,
):
    """Train and evaluate a purchase prediction model."""

    print(
        f"\n{'=' * 60}"
    )

    print(
        f"TRAINING: {model_name}"
    )

    print(
        f"{'=' * 60}"
    )

    if model_name == "HistGradientBoosting":

        sample_weights = compute_sample_weight(
            class_weight="balanced",
            y=y_train
        )

        model.fit(
            X_train,
            y_train,
            sample_weight=sample_weights
        )

    else:

        model.fit(
            X_train,
            y_train
        )

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    print("\n--- MODEL PERFORMANCE ---")

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

    print("\n--- CONFUSION MATRIX ---")

    print(matrix)

    print(
        "\n--- CLASSIFICATION REPORT ---"
    )

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    metrics = {
        "Algorithm": model_name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
    }

    return (
        metrics,
        model,
        probabilities,
    )


# ---------------------------------------------------------
# SAVE COMPARISON FIGURE
# ---------------------------------------------------------

def save_comparison_figure(results_df):
    """Create model comparison figure."""

    metric_columns = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC",
    ]

    plot_df = (
        results_df
        .set_index("Algorithm")[
            metric_columns
        ]
        .T
    )

    plt.figure(
        figsize=(10, 6)
    )

    plot_df.plot(
        kind="bar",
        ax=plt.gca()
    )

    plt.title(
        "Temporal Purchase Prediction Model Comparison"
    )

    plt.xlabel(
        "Evaluation Metric"
    )

    plt.ylabel(
        "Score"
    )

    plt.ylim(
        0,
        1
    )

    plt.xticks(
        rotation=0
    )

    plt.legend(
        title="Algorithm"
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH
        / "temporal_model_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "\nComparison figure saved:",
        output_path
    )


# ---------------------------------------------------------
# SAVE RESULTS
# ---------------------------------------------------------

def save_results(
    results_df,
    best_model,
    best_model_name,
):
    """Save model comparison and best model."""

    result_file = (
        RESULT_PATH
        / "temporal_purchase_model_comparison.csv"
    )

    results_df.to_csv(
        result_file,
        index=False
    )

    model_file = (
        MODEL_PATH
        / "temporal_purchase_model.pkl"
    )

    with open(
        model_file,
        "wb"
    ) as file:

        pickle.dump(
            best_model,
            file
        )

    print(
        "\nModel comparison saved:",
        result_file
    )

    print(
        "Best model saved:",
        model_file
    )

    print(
        "Saved model algorithm:",
        best_model_name
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    create_output_directories()

    df = load_data(
        DATA_PATH
    )

    X, y, feature_columns = prepare_features(
        df
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = temporal_train_test_split(
        df,
        X,
        y
    )

    models = create_models()

    results = []

    trained_models = {}

    model_probabilities = {}

    for model_name, model in models.items():

        (
            metrics,
            trained_model,
            probabilities,
        ) = evaluate_model(
            model_name,
            model,
            X_train,
            X_test,
            y_train,
            y_test,
        )

        results.append(
            metrics
        )

        trained_models[
            model_name
        ] = trained_model

        model_probabilities[
            model_name
        ] = probabilities

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        by="ROC-AUC",
        ascending=False
    ).reset_index(
        drop=True
    )

    print(
        "\n"
        + "=" * 60
    )

    print(
        "TEMPORAL MODEL COMPARISON"
    )

    print(
        "=" * 60
    )

    print(
        results_df.to_string(
            index=False
        )
    )

    best_model_name = results_df.loc[
        0,
        "Algorithm"
    ]

    best_model = trained_models[
        best_model_name
    ]

    best_probabilities = model_probabilities[
        best_model_name
    ]

    print(
        "\n--- BEST TEMPORAL MODEL ---"
    )

    print(
        "Algorithm:",
        best_model_name
    )

    print(
        "ROC-AUC:",
        round(
            results_df.loc[
                0,
                "ROC-AUC"
            ],
            4
        )
    )

    save_comparison_figure(
        results_df
    )

    save_results(
        results_df,
        best_model,
        best_model_name,
    )

    prediction_output = df.loc[
        X_test.index,
        [
            "customer_id",
            "session_id",
            "visit_date",
            "purchased",
        ]
    ].copy()

    prediction_output[
        "purchase_probability"
    ] = best_probabilities

    prediction_output[
        "predicted_purchase"
    ] = (
        best_probabilities >= 0.5
    ).astype(int)

    prediction_output = (
        prediction_output
        .sort_values(
            by=[
                "visit_date",
                "session_id",
            ]
        )
    )

    probability_file = (
        RESULT_PATH
        / "temporal_purchase_predictions.csv"
    )

    prediction_output.to_csv(
        probability_file,
        index=False
    )

    print(
        "Purchase probabilities saved:",
        probability_file
    )

    print(
        "\nTemporal purchase prediction completed successfully."
    )


if __name__ == "__main__":
    main()