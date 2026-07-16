from src.data_preprocessing import (
    load_data,
    preprocess_data,
    save_processed_data
)
from src.hyperparameter_tuning import (
    perform_hyperparameter_tuning
)
from src.eda import perform_eda
from src.classification import (
    train_classification_model
)
from src.regression import (
    train_regression_models
)
from src.clustering import (
    perform_customer_clustering
)
from src.recommendation import (
    run_recommendation_engine
)
from src.evaluation import (
    perform_final_evaluation
)

def main():

    print("=" * 60)
    print(
        "SHOP SENSE AI - "
        "E-COMMERCE RECOMMENDATION SYSTEM"
    )
    print("=" * 60)


    input_file = "data/Ecommerce.csv"

    output_file = (
        "data/processed_ecommerce_data.csv"
    )


    # Load dataset
    ecommerce_df = load_data(
        input_file
    )


    # Preprocess dataset
    processed_df = preprocess_data(
        ecommerce_df
    )


    # Save processed dataset
    save_processed_data(
        processed_df,
        output_file
    )


    # Perform Exploratory Data Analysis
    perform_eda(
        processed_df
    )


    # Train Regression Models
    regression_model, regression_results = (
        train_regression_models(
            processed_df
        )
    )
        # Train Classification Model
    classification_model, classification_results = (
        train_classification_model(
            processed_df
        )
    )
        # Perform Customer Segmentation
    (
        clustering_model,
        clustering_scaler,
        customer_segments,
        cluster_summary
    ) = perform_customer_clustering(
        processed_df
    )
    
        # Perform Hyperparameter Optimization
    (
        tuned_ridge_model,
        tuned_logistic_model,
        tuned_ridge_results,
        tuned_logistic_results
    ) = perform_hyperparameter_tuning(
        processed_df
    )
    
        # Run Shop Sense AI Recommendation Engine

    recommendations = run_recommendation_engine(
        df=processed_df,
        rating_model=tuned_ridge_model,
        purchase_model=classification_model,
        customer_segments=customer_segments,
        top_n=5
    )
        # Final Model Evaluation and Business Alignment

    final_model_comparison = perform_final_evaluation(
        regression_results=regression_results,
        classification_results=classification_results,
        tuned_ridge_results=tuned_ridge_results,
        tuned_logistic_results=tuned_logistic_results
    )


    print("\n" + "=" * 60)
    print("PHASE 10 COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()