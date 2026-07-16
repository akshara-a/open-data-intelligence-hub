import os

import pandas as pd


RESULTS_DIRECTORY = "outputs/results"


def create_model_comparison(
    regression_results,
    classification_results,
    tuned_ridge_results,
    tuned_logistic_results
):
    """
    Create a final comparison of all machine learning models.
    """

    print("\n" + "=" * 60)
    print("FINAL MODEL COMPARISON")
    print("=" * 60)


    linear_result = regression_results[
        regression_results["Model"]
        == "Linear Regression"
    ].iloc[0]


    ridge_result = regression_results[
        regression_results["Model"]
        == "Ridge Regression"
    ].iloc[0]


    tuned_ridge_result = (
        tuned_ridge_results.iloc[0]
    )


    logistic_result = (
        classification_results.iloc[0]
    )


    tuned_logistic_result = (
        tuned_logistic_results.iloc[0]
    )


    model_comparison = pd.DataFrame(
        [
            {
                "Model": "Linear Regression",
                "ML_Task": "Rating Prediction",
                "Primary_Metric": "RMSE",
                "Metric_Value": linear_result["RMSE"],
                "Business_Value": (
                    "Predicts product ratings"
                )
            },
            {
                "Model": "Ridge Regression",
                "ML_Task": "Rating Prediction",
                "Primary_Metric": "RMSE",
                "Metric_Value": ridge_result["RMSE"],
                "Business_Value": (
                    "Predicts ratings with "
                    "regularization"
                )
            },
            {
                "Model": "Tuned Ridge Regression",
                "ML_Task": "Rating Prediction",
                "Primary_Metric": "RMSE",
                "Metric_Value": (
                    tuned_ridge_result["RMSE"]
                ),
                "Business_Value": (
                    "Estimates customer product "
                    "preference"
                )
            },
            {
                "Model": "Logistic Regression",
                "ML_Task": "Purchase Prediction",
                "Primary_Metric": "ROC-AUC",
                "Metric_Value": (
                    logistic_result["ROC_AUC"]
                ),
                "Business_Value": (
                    "Identifies customers likely "
                    "to purchase"
                )
            },
            {
                "Model": (
                    "Tuned Logistic Regression"
                ),
                "ML_Task": "Purchase Prediction",
                "Primary_Metric": "ROC-AUC",
                "Metric_Value": (
                    tuned_logistic_result[
                        "ROC_AUC"
                    ]
                ),
                "Business_Value": (
                    "Optimized purchase likelihood "
                    "prediction"
                )
            },
            {
                "Model": "K-Means Clustering",
                "ML_Task": "Customer Segmentation",
                "Primary_Metric": (
                    "Silhouette Score"
                ),
                "Metric_Value": 0.1959,
                "Business_Value": (
                    "Groups customers by shopping "
                    "behavior"
                )
            }
        ]
    )


    model_comparison["Metric_Value"] = (
        model_comparison["Metric_Value"]
        .round(6)
    )


    print("\nMODEL PERFORMANCE SUMMARY")
    print("-" * 60)


    print(
        model_comparison.to_string(
            index=False
        )
    )


    os.makedirs(
        RESULTS_DIRECTORY,
        exist_ok=True
    )


    comparison_file = os.path.join(
        RESULTS_DIRECTORY,
        "final_model_comparison.csv"
    )


    model_comparison.to_csv(
        comparison_file,
        index=False
    )


    print(
        f"\nModel comparison saved to: "
        f"{comparison_file}"
    )


    return model_comparison


def display_business_interpretation():
    """
    Display business interpretation of
    machine learning results.
    """

    print("\n" + "=" * 60)
    print("BUSINESS INTERPRETATION")
    print("=" * 60)


    print("\n1. RATING PREDICTION")
    print("-" * 60)

    print(
        "Tuned Ridge Regression was selected for "
        "rating prediction. The model achieved a low "
        "MAE, but the low R2 score indicates limited "
        "rating variation in the dataset."
    )


    print("\n2. PURCHASE LIKELIHOOD PREDICTION")
    print("-" * 60)

    print(
        "The original Logistic Regression model "
        "achieved a slightly higher ROC-AUC than the "
        "tuned model. It was therefore selected for "
        "purchase probability estimation."
    )


    print("\n3. CUSTOMER SEGMENTATION")
    print("-" * 60)

    print(
        "K-Means identified two customer segments: "
        "Low-Conversion Browsers and Active "
        "High-Value Buyers."
    )


    print("\n4. RECOMMENDATION STRATEGY")
    print("-" * 60)

    print(
        "Low-Conversion Browsers are ranked using "
        "70% purchase probability and 30% predicted "
        "rating to focus on sales conversion."
    )

    print(
        "Active High-Value Buyers are ranked using "
        "40% purchase probability and 60% predicted "
        "rating to prioritize product preference."
    )


    print("\n5. BUSINESS VALUE")
    print("-" * 60)

    print(
        "The system can support personalized product "
        "recommendations, targeted marketing, cart "
        "recovery campaigns, customer loyalty "
        "strategies, and product ranking."
    )


def display_final_conclusion():
    """
    Display the final project conclusion.
    """

    print("\n" + "=" * 60)
    print("FINAL CONCLUSION")
    print("=" * 60)


    print(
        "\nShop Sense AI combines regression, "
        "classification, and clustering to solve "
        "multiple e-commerce recommendation problems."
    )


    print(
        "\nTuned Ridge Regression estimates customer "
        "ratings, Logistic Regression predicts "
        "purchase likelihood, and K-Means identifies "
        "customer behavioral segments."
    )


    print(
        "\nThe segment-aware recommendation engine "
        "combines predicted rating and purchase "
        "probability using different weights for each "
        "customer segment."
    )


    print(
        "\nThis approach allows the e-commerce platform "
        "to rank products according to customer "
        "behavior and business objectives."
    )


    print(
        "\nThe system can help improve recommendation "
        "personalization, identify potential buyers, "
        "target customer segments, and support sales "
        "conversion strategies."
    )


def perform_final_evaluation(
    regression_results,
    classification_results,
    tuned_ridge_results,
    tuned_logistic_results
):
    """
    Perform final model evaluation and
    business interpretation.
    """

    print("\n" + "=" * 60)
    print(
        "FINAL MODEL EVALUATION AND "
        "BUSINESS ALIGNMENT"
    )
    print("=" * 60)


    model_comparison = create_model_comparison(
        regression_results,
        classification_results,
        tuned_ridge_results,
        tuned_logistic_results
    )


    display_business_interpretation()


    display_final_conclusion()


    print("\n" + "=" * 60)
    print("SHOP SENSE AI COMPLETED SUCCESSFULLY")
    print("=" * 60)


    return model_comparison