import os
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import joblib

from src.preprocessing import (
    load_data, 
    preprocess_regression_data, 
    preprocess_classification_data, 
    preprocess_clustering_data
)
from src.regression import train_ridge_regression
from src.classification import train_logistic_regression
from src.clustering import perform_kmeans_clustering
from src.utils import (
    plot_regression_results, 
    plot_classification_results, 
    plot_elbow_curve, 
    plot_silhouette_scores, 
    plot_cluster_characteristics
)
from src.report_generator import generate_pdf_report

def main():
    print("=" * 60)
    print("Multi-Algorithm Recommendation System Comparison Pipeline")
    print("=" * 60)
    
    # Paths
    dataset_path = 'data/ecommerce_data.csv'
    output_dir = 'outputs'
    images_dir = 'images'
    pdf_report_path = 'report.pdf'
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # Step 1: Load dataset
    df = load_data(dataset_path)
    
    # Step 2: Build Regression Model (Ridge Regression)
    print("\n--- 1. Regression Model (Ridge Regression) ---")
    reg_X_train, reg_X_test, reg_y_train, reg_y_test, reg_scaler, reg_feat_names = preprocess_regression_data(df)
    reg_model, reg_results = train_ridge_regression(reg_X_train, reg_y_train, reg_X_test, reg_y_test)
    
    # Generate regression plot
    plot_regression_results(
        reg_y_test, 
        reg_results['predictions'], 
        os.path.join(images_dir, 'regression_results.png')
    )
    
    # Step 3: Build Classification Model (Logistic Regression)
    print("\n--- 2. Classification Model (Logistic Regression) ---")
    clf_X_train, clf_X_test, clf_y_train, clf_y_test, clf_scaler, clf_feat_names = preprocess_classification_data(df)
    clf_model, clf_results = train_logistic_regression(clf_X_train, clf_y_train, clf_X_test, clf_y_test)
    
    # Generate classification plot
    plot_classification_results(
        clf_results['tuned']['confusion_matrix'], 
        os.path.join(images_dir, 'classification_confusion_matrix.png')
    )
    
    # Step 4: Build Clustering Model (K-Means)
    print("\n--- 3. Clustering Model (K-Means) ---")
    cust_df, cust_X_scaled, cust_scaler = preprocess_clustering_data(df)
    kmeans_model, clustering_results = perform_kmeans_clustering(cust_df, cust_X_scaled)
    
    # Generate clustering plots
    plot_elbow_curve(
        clustering_results['k_range'], 
        clustering_results['inertias'], 
        os.path.join(images_dir, 'kmeans_elbow_curve.png')
    )
    plot_silhouette_scores(
        clustering_results['k_range'], 
        clustering_results['silhouette_scores'], 
        os.path.join(images_dir, 'kmeans_silhouette_scores.png')
    )
    plot_cluster_characteristics(
        clustering_results['profiles'], 
        os.path.join(images_dir, 'cluster_characteristics.png')
    )
    
    # Step 5: Save evaluation results to CSV
    print("\nSaving evaluation metrics...")
    metrics_data = [
        # Regression
        {"ML Task": "Regression", "Algorithm": "Ridge Regression", "Metric": "MAE", "Value": f"{reg_results['tuned']['mae']:.4f}"},
        {"ML Task": "Regression", "Algorithm": "Ridge Regression", "Metric": "RMSE", "Value": f"{reg_results['tuned']['rmse']:.4f}"},
        {"ML Task": "Regression", "Algorithm": "Ridge Regression", "Metric": "R2 Score", "Value": f"{reg_results['tuned']['r2']:.4f}"},
        {"ML Task": "Regression", "Algorithm": "Ridge Regression", "Metric": "Best Alpha", "Value": f"{reg_results['best_params']['alpha']}"},
        
        # Classification
        {"ML Task": "Classification", "Algorithm": "Logistic Regression", "Metric": "Accuracy", "Value": f"{clf_results['tuned']['accuracy']:.4f}"},
        {"ML Task": "Classification", "Algorithm": "Logistic Regression", "Metric": "Precision", "Value": f"{clf_results['tuned']['precision']:.4f}"},
        {"ML Task": "Classification", "Algorithm": "Logistic Regression", "Metric": "Recall", "Value": f"{clf_results['tuned']['recall']:.4f}"},
        {"ML Task": "Classification", "Algorithm": "Logistic Regression", "Metric": "F1 Score", "Value": f"{clf_results['tuned']['f1']:.4f}"},
        {"ML Task": "Classification", "Algorithm": "Logistic Regression", "Metric": "Best C", "Value": f"{clf_results['best_params']['C']}"},
        {"ML Task": "Classification", "Algorithm": "Logistic Regression", "Metric": "Best Solver", "Value": f"{clf_results['best_params']['solver']}"},
        {"ML Task": "Classification", "Algorithm": "Logistic Regression", "Metric": "Best Max Iter", "Value": f"{clf_results['best_params']['max_iter']}"},
        
        # Clustering
        {"ML Task": "Clustering", "Algorithm": "K-Means", "Metric": "Optimal Clusters (K)", "Value": f"{clustering_results['best_k']}"},
        {"ML Task": "Clustering", "Algorithm": "K-Means", "Metric": "Best Inertia", "Value": f"{clustering_results['best_inertia']:.4f}"},
        {"ML Task": "Clustering", "Algorithm": "K-Means", "Metric": "Best Silhouette Score", "Value": f"{clustering_results['best_silhouette']:.4f}"}
    ]
    
    metrics_df = pd.DataFrame(metrics_data)
    metrics_df.to_csv(os.path.join(output_dir, 'evaluation_results.csv'), index=False)
    print(f"Metrics saved to '{os.path.join(output_dir, 'evaluation_results.csv')}'")
    
    # Step 6: Generate final report PDF
    print("\nGenerating PDF Report...")
    generate_pdf_report(reg_results, clf_results, clustering_results, pdf_report_path)
    
    print("\n" + "=" * 60)
    print("Pipeline Execution Completed Successfully!")
    print("=" * 60)

if __name__ == '__main__':
    main()
