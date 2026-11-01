from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from imblearn.over_sampling import SMOTENC
from imblearn.under_sampling import RandomUnderSampler

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)
from sklearn.utils.class_weight import compute_sample_weight


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "ecommerce_historical_features.csv"
)

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


FEATURE_COLUMNS = (
    CURRENT_SESSION_FEATURES
    + HISTORICAL_FEATURES
)


CATEGORICAL_FEATURES = [
    "device_type",
    "user_type",
    "marketing_channel",
    "product_category",
    "visit_month",
    "visit_weekday",
    "visit_season",
    "location",
]


TARGET_COLUMN = "purchased"


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    """Load the historical feature dataset."""

    print("Loading historical feature dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully.")
    print("Dataset shape:", df.shape)

    return df


# ============================================================
# PREPARE CART CONVERSION DATA
# ============================================================

def prepare_cart_conversion_data(df):
    """Keep only cart-engaged sessions."""

    print("\nPreparing cart conversion dataset...")

    cart_df = df[
        df["added_to_cart"] == 1
    ].copy()

    print(
        "Cart-engaged sessions:",
        len(cart_df)
    )

    print(
        "\n--- TARGET DISTRIBUTION ---"
    )

    print(
        cart_df[TARGET_COLUMN]
        .value_counts()
        .sort_index()
    )

    print("\nPercentage:")

    print(
        cart_df[TARGET_COLUMN]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    return cart_df


# ============================================================
# TEMPORAL SPLIT
# ============================================================

def create_temporal_split(df):
    """Create chronological train-test split."""

    print("\nCreating temporal train-test split...")

    df["visit_date"] = pd.to_datetime(
        df["visit_date"],
        errors="coerce"
    )

    df = df.sort_values(
        ["visit_date", "session_id"]
    ).reset_index(drop=True)

    split_index = int(
        len(df) * 0.80
    )

    train_df = df.iloc[
        :split_index
    ].copy()

    test_df = df.iloc[
        split_index:
    ].copy()

    X_train = train_df[
        FEATURE_COLUMNS
    ].copy()

    y_train = train_df[
        TARGET_COLUMN
    ].copy()

    X_test = test_df[
        FEATURE_COLUMNS
    ].copy()

    y_test = test_df[
        TARGET_COLUMN
    ].copy()

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

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


# ============================================================
# MODEL
# ============================================================

def create_random_forest(
    class_weight=None
):
    """Create Random Forest classifier."""

    return RandomForestClassifier(
        n_estimators=400,
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight=class_weight,
        random_state=42,
        n_jobs=-1,
    )


# ============================================================
# EVALUATION
# ============================================================

def evaluate_model(
    model,
    X_test,
    y_test,
    algorithm,
):
    """Evaluate trained model."""

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    predictions = (
        probabilities >= 0.50
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

    pr_auc = average_precision_score(
        y_test,
        probabilities
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    print(
        f"\n--- {algorithm} PERFORMANCE ---"
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

    print(
        "\nConfusion Matrix:"
    )

    print(matrix)

    return {
        "Strategy": algorithm,
        "Accuracy": accuracy,
        "Balanced Accuracy": balanced_accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    RESULT_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    FIGURE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    df = load_data()

    cart_df = (
        prepare_cart_conversion_data(df)
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = create_temporal_split(
        cart_df
    )

    results = []


    # ========================================================
    # BASELINE
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "EXPERIMENT 1: BASELINE RANDOM FOREST"
    )

    print(
        "=" * 60
    )

    baseline_model = (
        create_random_forest()
    )

    baseline_model.fit(
        X_train,
        y_train
    )

    results.append(
        evaluate_model(
            baseline_model,
            X_test,
            y_test,
            "Baseline"
        )
    )


    # ========================================================
    # CLASS WEIGHT
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "EXPERIMENT 2: CLASS-WEIGHTED RANDOM FOREST"
    )

    print(
        "=" * 60
    )

    weighted_model = (
        create_random_forest(
            class_weight="balanced"
        )
    )

    weighted_model.fit(
        X_train,
        y_train
    )

    results.append(
        evaluate_model(
            weighted_model,
            X_test,
            y_test,
            "Class Weight"
        )
    )


    # ========================================================
    # RANDOM UNDER-SAMPLING
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "EXPERIMENT 3: RANDOM UNDER-SAMPLING"
    )

    print(
        "=" * 60
    )

    under_sampler = RandomUnderSampler(
        random_state=42
    )

    (
        X_train_under,
        y_train_under,
    ) = under_sampler.fit_resample(
        X_train,
        y_train
    )

    print(
        "\nUnder-sampled distribution:"
    )

    print(
        y_train_under.value_counts()
    )

    under_model = (
        create_random_forest()
    )

    under_model.fit(
        X_train_under,
        y_train_under
    )

    results.append(
        evaluate_model(
            under_model,
            X_test,
            y_test,
            "Random Under-Sampling"
        )
    )


    # ========================================================
    # SMOTENC
    # ========================================================

    print(
        "\n"
        + "=" * 60
    )

    print(
        "EXPERIMENT 4: SMOTENC"
    )

    print(
        "=" * 60
    )

    categorical_indices = [
        FEATURE_COLUMNS.index(column)
        for column
        in CATEGORICAL_FEATURES
    ]

    print(
        "Categorical feature indices:"
    )

    print(
        categorical_indices
    )

    print(
        "\nCategorical features:"
    )

    for column in CATEGORICAL_FEATURES:
        print(
            "-",
            column
        )

    smotenc = SMOTENC(
        categorical_features=(
            categorical_indices
        ),
        random_state=42,
        k_neighbors=5,
    )

    (
        X_train_smote,
        y_train_smote,
    ) = smotenc.fit_resample(
        X_train,
        y_train
    )

    print(
        "\nSMOTENC balanced distribution:"
    )

    print(
        y_train_smote.value_counts()
    )

    print(
        "SMOTENC training shape:",
        X_train_smote.shape
    )

    smote_model = (
        create_random_forest()
    )

    smote_model.fit(
        X_train_smote,
        y_train_smote
    )

    results.append(
        evaluate_model(
            smote_model,
            X_test,
            y_test,
            "SMOTENC"
        )
    )


    # ========================================================
    # COMPARISON
    # ========================================================

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        by=[
            "ROC-AUC",
            "PR-AUC",
        ],
        ascending=False
    )

    print(
        "\n"
        + "=" * 60
    )

    print(
        "BALANCING STRATEGY COMPARISON"
    )

    print(
        "=" * 60
    )

    print(
        results_df.to_string(
            index=False
        )
    )


    # ========================================================
    # BEST STRATEGY
    # ========================================================

    best_result = (
        results_df.iloc[0]
    )

    print(
        "\n--- BEST BALANCING STRATEGY ---"
    )

    print(
        "Strategy:",
        best_result["Strategy"]
    )

    print(
        "ROC-AUC:",
        f"{best_result['ROC-AUC']:.4f}"
    )

    print(
        "PR-AUC:",
        f"{best_result['PR-AUC']:.4f}"
    )

    print(
        "F1 Score:",
        f"{best_result['F1 Score']:.4f}"
    )


    # ========================================================
    # SAVE RESULTS
    # ========================================================

    result_file = (
        RESULT_PATH
        / "balancing_strategy_comparison.csv"
    )

    results_df.to_csv(
        result_file,
        index=False
    )

    print(
        "\nResults saved:",
        result_file
    )


    # ========================================================
    # VISUALIZATION
    # ========================================================

    plot_df = (
        results_df
        .set_index("Strategy")[
            [
                "Balanced Accuracy",
                "F1 Score",
                "ROC-AUC",
                "PR-AUC",
            ]
        ]
    )

    plt.figure(
        figsize=(11, 6)
    )

    plot_df.plot(
        kind="bar"
    )

    plt.title(
        "Comparison of Data Balancing Strategies"
    )

    plt.ylabel(
        "Metric Score"
    )

    plt.xlabel(
        "Balancing Strategy"
    )

    plt.xticks(
        rotation=20
    )

    plt.tight_layout()

    figure_file = (
        FIGURE_PATH
        / "balancing_strategy_comparison.png"
    )

    plt.savefig(
        figure_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "Comparison figure saved:",
        figure_file
    )

    print(
        "\nBalancing experiment completed successfully."
    )


if __name__ == "__main__":
    main()