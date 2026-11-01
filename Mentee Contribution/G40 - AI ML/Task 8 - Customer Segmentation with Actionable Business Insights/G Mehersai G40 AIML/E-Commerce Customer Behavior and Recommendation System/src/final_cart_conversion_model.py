from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
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


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "ecommerce_historical_features.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_cart_conversion_model.pkl"
)

RESULT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "results"
)

FIGURE_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "figures"
)


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


FEATURES = CURRENT_SESSION_FEATURES + HISTORICAL_FEATURES

TARGET = "purchased"


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

def create_directories():
    """Create model and output directories."""

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULT_PATH.mkdir(
        parents=True,
        exist_ok=True,
    )

    FIGURE_PATH.mkdir(
        parents=True,
        exist_ok=True,
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
# PREPARE CART CONVERSION DATA
# ============================================================

def prepare_cart_conversion_data(df):
    """
    Filter sessions where the customer added a product to cart.

    The prediction task is:

    Will a cart-engaged customer complete the purchase?
    """

    print("\nPreparing cart conversion dataset...")

    cart_df = (
        df[df["added_to_cart"] == 1]
        .copy()
    )

    print(
        "Cart-engaged sessions:",
        len(cart_df),
    )

    print(
        "\n--- CART CONVERSION TARGET DISTRIBUTION ---"
    )

    print(
        cart_df[TARGET]
        .value_counts()
        .sort_index()
    )

    print("\nPercentage:")

    print(
        cart_df[TARGET]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    missing_features = [
        column
        for column in FEATURES
        if column not in cart_df.columns
    ]

    if missing_features:
        raise ValueError(
            "Missing model features: "
            + ", ".join(missing_features)
        )

    return cart_df


# ============================================================
# TEMPORAL TRAIN VALIDATION TEST SPLIT
# ============================================================

def create_temporal_split(df):
    """
    Create a chronological split.

    First 70%  -> Training
    Next 10%   -> Validation
    Final 20%  -> Future Test
    """

    print(
        "\nCreating temporal train-validation-test split..."
    )

    df = df.copy()

    df["visit_date"] = pd.to_datetime(
        df["visit_date"],
        errors="coerce",
    )

    invalid_dates = (
        df["visit_date"]
        .isna()
        .sum()
    )

    if invalid_dates > 0:
        raise ValueError(
            f"Invalid visit dates found: {invalid_dates}"
        )

    df = df.sort_values(
        [
            "visit_date",
            "session_id",
        ]
    ).reset_index(drop=True)

    train_end = int(
        len(df) * 0.70
    )

    validation_end = int(
        len(df) * 0.80
    )

    train_df = (
        df.iloc[:train_end]
        .copy()
    )

    validation_df = (
        df.iloc[
            train_end:validation_end
        ]
        .copy()
    )

    test_df = (
        df.iloc[validation_end:]
        .copy()
    )

    print("\n--- TEMPORAL SPLIT ---")

    print(
        "Training date range:",
        train_df["visit_date"].min(),
        "to",
        train_df["visit_date"].max(),
    )

    print(
        "Validation date range:",
        validation_df["visit_date"].min(),
        "to",
        validation_df["visit_date"].max(),
    )

    print(
        "Testing date range:",
        test_df["visit_date"].min(),
        "to",
        test_df["visit_date"].max(),
    )

    print(
        "\nTraining shape:",
        (
            len(train_df),
            len(FEATURES),
        ),
    )

    print(
        "Validation shape:",
        (
            len(validation_df),
            len(FEATURES),
        ),
    )

    print(
        "Testing shape:",
        (
            len(test_df),
            len(FEATURES),
        ),
    )

    return (
        train_df,
        validation_df,
        test_df,
    )


# ============================================================
# PRINT TARGET DISTRIBUTION
# ============================================================

def print_target_distribution(
    y,
    name,
):
    """Print target class distribution."""

    print(
        f"\n--- {name.upper()} TARGET DISTRIBUTION ---"
    )

    print(
        y.value_counts()
        .sort_index()
    )

    print("\nPercentage:")

    print(
        y.value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )


# ============================================================
# RANDOM UNDER-SAMPLING
# ============================================================

def random_under_sample(
    X,
    y,
    random_state=42,
):
    """
    Randomly under-sample the majority class.

    Only training data is balanced.
    """

    training_data = X.copy()

    training_data[TARGET] = (
        y.values
    )

    majority = (
        training_data[
            training_data[TARGET] == 0
        ]
    )

    minority = (
        training_data[
            training_data[TARGET] == 1
        ]
    )

    majority_sample = majority.sample(
        n=len(minority),
        random_state=random_state,
    )

    balanced_data = pd.concat(
        [
            majority_sample,
            minority,
        ],
        ignore_index=True,
    )

    balanced_data = (
        balanced_data
        .sample(
            frac=1,
            random_state=random_state,
        )
        .reset_index(drop=True)
    )

    X_balanced = (
        balanced_data[FEATURES]
    )

    y_balanced = (
        balanced_data[TARGET]
    )

    return (
        X_balanced,
        y_balanced,
    )


# ============================================================
# CREATE MODEL
# ============================================================

def create_random_forest(
    class_weight=None,
):
    """Create Random Forest classifier."""

    return RandomForestClassifier(
        n_estimators=500,
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=5,
        max_features="sqrt",
        class_weight=class_weight,
        random_state=42,
        n_jobs=-1,
    )


# ============================================================
# THRESHOLD OPTIMIZATION
# ============================================================

def optimize_threshold(
    y_true,
    probabilities,
):
    """
    Select probability threshold using validation F1 score.
    """

    threshold_results = []

    thresholds = np.arange(
        0.20,
        0.81,
        0.01,
    )

    for threshold in thresholds:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            y_true,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            y_true,
            predictions,
            zero_division=0,
        )

        balanced_accuracy = (
            balanced_accuracy_score(
                y_true,
                predictions,
            )
        )

        threshold_results.append(
            {
                "Threshold": threshold,
                "Precision": precision,
                "Recall": recall,
                "F1 Score": f1,
                "Balanced Accuracy": (
                    balanced_accuracy
                ),
            }
        )

    threshold_df = pd.DataFrame(
        threshold_results
    )

    best_row = (
        threshold_df
        .sort_values(
            [
                "F1 Score",
                "Balanced Accuracy",
                "Recall",
            ],
            ascending=False,
        )
        .iloc[0]
    )

    return (
        float(best_row["Threshold"]),
        threshold_df,
    )


# ============================================================
# MODEL EVALUATION
# ============================================================

def evaluate_model(
    model_name,
    y_true,
    probabilities,
    threshold,
):
    """Evaluate model using locked threshold."""

    predictions = (
        probabilities >= threshold
    ).astype(int)

    accuracy = accuracy_score(
        y_true,
        predictions,
    )

    balanced_accuracy = (
        balanced_accuracy_score(
            y_true,
            predictions,
        )
    )

    precision = precision_score(
        y_true,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        predictions,
        zero_division=0,
    )

    f1 = f1_score(
        y_true,
        predictions,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_true,
        probabilities,
    )

    pr_auc = average_precision_score(
        y_true,
        probabilities,
    )

    matrix = confusion_matrix(
        y_true,
        predictions,
    )

    print(
        f"\n--- {model_name} TEST PERFORMANCE ---"
    )

    print(
        f"Threshold         : {threshold:.2f}"
    )

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

    print("\nConfusion Matrix:")

    print(matrix)

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_true,
            predictions,
            zero_division=0,
        )
    )

    result = {
        "Strategy": model_name,
        "Threshold": threshold,
        "Accuracy": accuracy,
        "Balanced Accuracy": (
            balanced_accuracy
        ),
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc,
    }

    return (
        result,
        predictions,
    )


# ============================================================
# TRAIN CLASS-WEIGHTED MODEL
# ============================================================

def train_class_weight_model(
    X_train,
    y_train,
):
    """Train class-weighted Random Forest."""

    print(
        "\n"
        + "=" * 60
    )

    print(
        "TRAINING: CLASS-WEIGHTED RANDOM FOREST"
    )

    print(
        "=" * 60
    )

    model = create_random_forest(
        class_weight="balanced",
    )

    model.fit(
        X_train,
        y_train,
    )

    print(
        "Class-weighted model trained successfully."
    )

    return model


# ============================================================
# TRAIN UNDER-SAMPLED MODEL
# ============================================================

def train_under_sample_model(
    X_train,
    y_train,
):
    """Train Random Forest using under-sampled data."""

    print(
        "\n"
        + "=" * 60
    )

    print(
        "TRAINING: RANDOM UNDER-SAMPLED RANDOM FOREST"
    )

    print(
        "=" * 60
    )

    (
        X_balanced,
        y_balanced,
    ) = random_under_sample(
        X_train,
        y_train,
    )

    print(
        "\nUnder-sampled training distribution:"
    )

    print(
        y_balanced
        .value_counts()
        .sort_index()
    )

    print(
        "Balanced training shape:",
        X_balanced.shape,
    )

    model = create_random_forest()

    model.fit(
        X_balanced,
        y_balanced,
    )

    print(
        "Under-sampled model trained successfully."
    )

    return model


# ============================================================
# PLOT MODEL COMPARISON
# ============================================================

def plot_model_comparison(
    comparison_df,
):
    """Create final model comparison figure."""

    metrics = [
        "Balanced Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC",
        "PR-AUC",
    ]

    plot_df = (
        comparison_df
        .set_index("Strategy")[metrics]
        .T
    )

    plt.figure(
        figsize=(11, 7)
    )

    plot_df.plot(
        kind="bar",
    )

    plt.title(
        "Final Cart Conversion Model Comparison"
    )

    plt.xlabel(
        "Evaluation Metric"
    )

    plt.ylabel(
        "Score"
    )

    plt.xticks(
        rotation=45,
        ha="right",
    )

    plt.ylim(
        0,
        1,
    )

    plt.tight_layout()

    output_path = (
        FIGURE_PATH
        / "final_cart_conversion_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        "\nComparison figure saved:",
        output_path,
    )


# ============================================================
# MAIN
# ============================================================

def main():

    create_directories()

    df = load_data()

    cart_df = (
        prepare_cart_conversion_data(
            df
        )
    )

    (
        train_df,
        validation_df,
        test_df,
    ) = create_temporal_split(
        cart_df
    )

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_validation = (
        validation_df[FEATURES]
    )

    y_validation = (
        validation_df[TARGET]
    )

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    print_target_distribution(
        y_train,
        "Training",
    )

    print_target_distribution(
        y_validation,
        "Validation",
    )

    print_target_distribution(
        y_test,
        "Testing",
    )

    models = {}

    # --------------------------------------------------------
    # CLASS-WEIGHTED RANDOM FOREST
    # --------------------------------------------------------

    class_weight_model = (
        train_class_weight_model(
            X_train,
            y_train,
        )
    )

    models[
        "Class-Weighted Random Forest"
    ] = class_weight_model

    # --------------------------------------------------------
    # RANDOM UNDER-SAMPLED RANDOM FOREST
    # --------------------------------------------------------

    under_sample_model = (
        train_under_sample_model(
            X_train,
            y_train,
        )
    )

    models[
        "Under-Sampled Random Forest"
    ] = under_sample_model

    # --------------------------------------------------------
    # VALIDATION THRESHOLD SELECTION
    # --------------------------------------------------------

    model_thresholds = {}

    threshold_frames = []

    print(
        "\n"
        + "=" * 60
    )

    print(
        "VALIDATION THRESHOLD OPTIMIZATION"
    )

    print(
        "=" * 60
    )

    for (
        model_name,
        model,
    ) in models.items():

        validation_probabilities = (
            model.predict_proba(
                X_validation
            )[:, 1]
        )

        (
            best_threshold,
            threshold_df,
        ) = optimize_threshold(
            y_validation,
            validation_probabilities,
        )

        model_thresholds[
            model_name
        ] = best_threshold

        threshold_df[
            "Strategy"
        ] = model_name

        threshold_frames.append(
            threshold_df
        )

        best_validation_row = (
            threshold_df.loc[
                threshold_df[
                    "Threshold"
                ].sub(
                    best_threshold
                ).abs().idxmin()
            ]
        )

        print(
            f"\n{model_name}"
        )

        print(
            f"Best Validation Threshold: "
            f"{best_threshold:.2f}"
        )

        print(
            f"Validation Precision: "
            f"{best_validation_row['Precision']:.4f}"
        )

        print(
            f"Validation Recall: "
            f"{best_validation_row['Recall']:.4f}"
        )

        print(
            f"Validation F1: "
            f"{best_validation_row['F1 Score']:.4f}"
        )

        print(
            f"Validation Balanced Accuracy: "
            f"{best_validation_row['Balanced Accuracy']:.4f}"
        )

    # --------------------------------------------------------
    # FUTURE TEST EVALUATION
    # --------------------------------------------------------

    print(
        "\n"
        + "=" * 60
    )

    print(
        "LOCKED FUTURE TEST EVALUATION"
    )

    print(
        "=" * 60
    )

    results = []

    prediction_output = (
        test_df[
            [
                "customer_id",
                "session_id",
                "visit_date",
                TARGET,
            ]
        ]
        .copy()
    )

    for (
        model_name,
        model,
    ) in models.items():

        threshold = (
            model_thresholds[
                model_name
            ]
        )

        test_probabilities = (
            model.predict_proba(
                X_test
            )[:, 1]
        )

        (
            result,
            predictions,
        ) = evaluate_model(
            model_name,
            y_test,
            test_probabilities,
            threshold,
        )

        results.append(
            result
        )

        safe_name = (
            model_name
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        prediction_output[
            f"{safe_name}_probability"
        ] = test_probabilities

        prediction_output[
            f"{safe_name}_prediction"
        ] = predictions

    # --------------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------------

    comparison_df = pd.DataFrame(
        results
    )

    comparison_df = (
        comparison_df
        .sort_values(
            [
                "PR-AUC",
                "ROC-AUC",
                "F1 Score",
            ],
            ascending=False,
        )
        .reset_index(drop=True)
    )

    print(
        "\n"
        + "=" * 60
    )

    print(
        "FINAL CART CONVERSION MODEL COMPARISON"
    )

    print(
        "=" * 60
    )

    print(
        comparison_df.to_string(
            index=False
        )
    )

    best_strategy = (
        comparison_df.iloc[0][
            "Strategy"
        ]
    )

    best_threshold = (
        model_thresholds[
            best_strategy
        ]
    )

    best_model = models[
        best_strategy
    ]

    print(
        "\n--- FINAL SELECTED MODEL ---"
    )

    print(
        "Strategy:",
        best_strategy,
    )

    print(
        "Locked Threshold:",
        f"{best_threshold:.2f}",
    )

    print(
        "ROC-AUC:",
        f"{comparison_df.iloc[0]['ROC-AUC']:.4f}",
    )

    print(
        "PR-AUC:",
        f"{comparison_df.iloc[0]['PR-AUC']:.4f}",
    )

    print(
        "F1 Score:",
        f"{comparison_df.iloc[0]['F1 Score']:.4f}",
    )

    print(
        "Recall:",
        f"{comparison_df.iloc[0]['Recall']:.4f}",
    )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    comparison_output = (
        RESULT_PATH
        / "final_cart_conversion_comparison.csv"
    )

    comparison_df.to_csv(
        comparison_output,
        index=False,
    )

    threshold_output = (
        RESULT_PATH
        / "final_cart_conversion_thresholds.csv"
    )

    pd.concat(
        threshold_frames,
        ignore_index=True,
    ).to_csv(
        threshold_output,
        index=False,
    )

    prediction_output_path = (
        RESULT_PATH
        / "final_cart_conversion_predictions.csv"
    )

    prediction_output.to_csv(
        prediction_output_path,
        index=False,
    )

    model_artifact = {
        "model": best_model,
        "strategy": best_strategy,
        "threshold": best_threshold,
        "features": FEATURES,
        "target": TARGET,
        "task": "cart_conversion_prediction",
        "split_strategy": (
            "70% temporal training, "
            "10% temporal validation, "
            "20% future testing"
        ),
    }

    joblib.dump(
        model_artifact,
        MODEL_PATH,
    )

    plot_model_comparison(
        comparison_df
    )

    print(
        "\nModel comparison saved:",
        comparison_output,
    )

    print(
        "Threshold results saved:",
        threshold_output,
    )

    print(
        "Future test predictions saved:",
        prediction_output_path,
    )

    print(
        "Final model artifact saved:",
        MODEL_PATH,
    )

    print(
        "\nFinal cart conversion modeling "
        "completed successfully."
    )


if __name__ == "__main__":
    main()