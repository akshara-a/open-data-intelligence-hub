import os
import pandas as pd
from src.data_loader import load_data
from src.preprocess import preprocess_pipeline
from src.clustering import perform_kmeans
from src.visualization import plot_elbow, plot_clusters_2d_pca, plot_clusters_3d, plot_cluster_profiles
from src.evaluation import evaluate_clustering_performance
from src.hyperparameter_tuning import tune_classifier_hyperparameters
from src.classification import train_segment_classifier
from src.regression import train_spend_regressor
from src.business_insights import analyze_segments

def main():
    print("==========================================================")
    print("      CUSTOMER SEGMENTATION END-TO-END PIPELINE           ")
    print("==========================================================")
    
    # Establish project directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'customer_data.csv')
    output_dir = os.path.join(base_dir, 'outputs')
    
    # 1. Load data
    print("\n--- STEP 1: LOADING DATA ---")
    raw_df = load_data(data_path)
    
    # 2. Preprocess data and construct RFM metrics
    print("\n--- STEP 2: PREPROCESSING & RFM GENERATION ---")
    processed_df, scaler = preprocess_pipeline(raw_df)
    
    # Define scaled feature set
    scaled_cols = [col for col in processed_df.columns if col.endswith('_scaled')]
    scaled_df = processed_df[scaled_cols]
    
    # 3. Plot Elbow Method to find optimal K
    print("\n--- STEP 3: ELBOW METHOD VISUALIZATION ---")
    plot_elbow(scaled_df, output_dir, max_k=5)
    
    # 4. Perform K-Means clustering (using K=3 for this setup)
    print("\n--- STEP 4: K-MEANS CLUSTERING ---")
    k = 3
    kmeans_model, labels = perform_kmeans(scaled_df, n_clusters=k)
    processed_df['Cluster'] = labels
    
    # 5. Evaluate clustering performance
    print("\n--- STEP 5: CLUSTERING PERFORMANCE EVALUATION ---")
    _ = evaluate_clustering_performance(scaled_df, labels)
    
    # 6. Generate visualizations
    print("\n--- STEP 6: GENERATING CLUSTER VISUALIZATIONS ---")
    plots_subdir = os.path.join(output_dir, 'plots')
    os.makedirs(plots_subdir, exist_ok=True)
    
    # Save to outputs/
    plot_clusters_2d_pca(scaled_df, labels, output_dir)
    plot_clusters_3d(processed_df, 'Cluster', output_dir)
    plot_cluster_profiles(processed_df, 'Cluster', output_dir)
    
    # Save copies to outputs/plots/
    plot_clusters_2d_pca(scaled_df, labels, plots_subdir)
    plot_clusters_3d(processed_df, 'Cluster', plots_subdir)
    plot_cluster_profiles(processed_df, 'Cluster', plots_subdir)
    plot_elbow(scaled_df, plots_subdir, max_k=5)
    
    # 7. Classification: Tune and train segment classifier
    print("\n--- STEP 7: SEGMENT CLASSIFICATION ---")
    # Features are scaled RFM
    # Split into train/test manually to feed GridSearchCV
    from sklearn.model_selection import train_test_split
    X = processed_df[scaled_cols]
    y = processed_df['Cluster']
    
    # Standard split without stratification due to potentially small class/sample size
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    print("Tuning classifier hyperparameters...")
    best_estimator, best_params = tune_classifier_hyperparameters(X_train, y_train)
    
    print("Training final segment classifier...")
    clf, clf_report, conf_matrix = train_segment_classifier(
        processed_df, scaled_cols, target_col='Cluster', test_size=0.3, random_state=42
    )
    
    # Write classification results to file
    import numpy as np
    classification_txt_path = os.path.join(output_dir, 'classification_results.txt')
    with open(classification_txt_path, 'w') as f:
        f.write("==========================================================\n")
        f.write("              CLASSIFICATION RESULTS                     \n")
        f.write("==========================================================\n\n")
        f.write(f"Classifier Model: Random Forest Classifier\n")
        f.write(f"Accuracy: {clf_report['accuracy']:.4f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(np.array2string(conf_matrix) + "\n\n")
        f.write("Classification Report:\n")
        for label, metrics in clf_report.items():
            if isinstance(metrics, dict):
                f.write(f"Class '{label}':\n")
                f.write(f"  Precision: {metrics['precision']:.4f}\n")
                f.write(f"  Recall:    {metrics['recall']:.4f}\n")
                f.write(f"  F1-Score:  {metrics['f1-score']:.4f}\n")
                f.write(f"  Support:   {metrics['support']}\n")
            else:
                f.write(f"{label.capitalize()}: {metrics:.4f}\n")
    print(f"Classification results written to {classification_txt_path}")
    
    # 8. Regression: Predict customer monetary spend
    print("\n--- STEP 8: CUSTOMER SPEND REGRESSION ---")
    reg_features = ['Recency_scaled', 'Frequency_scaled']
    reg_model, reg_metrics = train_spend_regressor(
        processed_df, reg_features, target_col='Monetary_scaled', test_size=0.3, random_state=42
    )
    
    # Write regression results to file
    regression_txt_path = os.path.join(output_dir, 'regression_results.txt')
    with open(regression_txt_path, 'w') as f:
        f.write("==========================================================\n")
        f.write("                REGRESSION RESULTS                        \n")
        f.write("==========================================================\n\n")
        f.write(f"Regression Model: Random Forest Regressor\n")
        f.write(f"Target Variable: Monetary Spend (Scaled)\n\n")
        for metric_name, val in reg_metrics.items():
            f.write(f"{metric_name}: {val:.4f}\n")
    print(f"Regression results written to {regression_txt_path}")
    
    # 9. Profile segments and generate business insights
    print("\n--- STEP 9: BUSINESS INSIGHTS REPORT ---")
    summary = analyze_segments(processed_df, cluster_col='Cluster', output_dir=output_dir)
    
    # Save additional structured CSV outputs
    summary.to_csv(os.path.join(output_dir, 'cluster_summary.csv'))
    print(f"Cluster summary CSV written to {os.path.join(output_dir, 'cluster_summary.csv')}")
    
    clustered_csv_path = os.path.join(plots_subdir, 'clustered_data.csv')
    processed_df.to_csv(clustered_csv_path, index=False)
    print(f"Clustered data CSV written to {clustered_csv_path}")
    
    print("\n==========================================================")
    print("    PIPELINE EXECUTION COMPLETED SUCCESSFULLY!             ")
    print("    Review outputs and visual plots in './outputs/'       ")
    print("==========================================================")

if __name__ == "__main__":
    main()
