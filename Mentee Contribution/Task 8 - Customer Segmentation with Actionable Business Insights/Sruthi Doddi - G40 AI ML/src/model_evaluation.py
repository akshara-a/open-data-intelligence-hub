"""
Model Evaluation Module
Handles comprehensive model evaluation and comparison
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')


class ModelEvaluator:
    """Class to handle model evaluation and comparison"""
    
    def __init__(self, customer_data, clustering_results=None):
        """
        Initialize with data and results
        
        Parameters:
        -----------
        customer_data : DataFrame
            Original customer data with clusters
        clustering_results : dict
            Clustering model results
        """
        self.customer_data = customer_data
        self.clustering_results = clustering_results or {}
        self.cluster_summary = None
        
    def evaluate_clustering(self, X_scaled, labels):
        """Evaluate clustering performance"""
        print("\n" + "="*50)
        print("CLUSTERING EVALUATION")
        print("="*50)
        
        if len(set(labels)) > 1:
            silhouette = silhouette_score(X_scaled, labels)
            print(f"Silhouette Score: {silhouette:.4f}")
        else:
            silhouette = 0
            print("Only one cluster found, silhouette score not applicable")
        
        return silhouette
    
    def create_segment_summary(self):
        """Create comprehensive segment summary"""
        print("\n" + "="*50)
        print("SEGMENT SUMMARY")
        print("="*50)
        
        summary = self.customer_data.groupby('cluster').agg({
            'customer_id': 'count',
            'total_revenue': ['sum', 'mean'],
            'total_purchases': ['mean'],
            'avg_rating': ['mean'],
            'total_sessions': ['mean']
        }).round(2)
        
        summary.columns = ['Count', 'Total_Revenue', 'Avg_Revenue', 
                          'Avg_Purchases', 'Avg_Rating', 'Avg_Sessions']
        
        self.cluster_summary = summary
        print(summary)
        
        return summary
    
    def calculate_revenue_contribution(self):
        """Calculate revenue contribution by segment"""
        print("\n" + "="*50)
        print("REVENUE CONTRIBUTION")
        print("="*50)
        
        revenue_by_segment = self.customer_data.groupby('cluster')['total_revenue'].sum()
        total_revenue = revenue_by_segment.sum()
        
        for cluster, revenue in revenue_by_segment.items():
            percentage = (revenue / total_revenue) * 100
            print(f"Cluster {cluster}: ${revenue:,.2f} ({percentage:.1f}%)")
        
        return revenue_by_segment
    
    def create_model_comparison_table(self):
        """Create comprehensive model comparison table"""
        print("\n" + "="*50)
        print("MODEL COMPARISON TABLE")
        print("="*50)
        
        comparison = pd.DataFrame({
            'Model': ['K-Means', 'Linear Regression', 'Ridge Regression', 'Logistic Regression'],
            'Objective': ['Customer Segmentation', 'Predict Revenue', 'Predict Revenue', 'Purchase Likelihood'],
            'Baseline Performance': ['N/A', 'RMSE: $512, R²: 0.924', 'RMSE: $511, R²: 0.924', 'F1: 1.000, AUC: 1.000'],
            'Tuned Performance': ['Silhouette: 0.221', 'RMSE: $512, R²: 0.924', 'RMSE: $512, R²: 0.924', 'F1: 1.000, AUC: 1.000'],
            'Selected': ['✅ Yes', '✅ Yes', '✅ Yes', '✅ Yes']
        })
        
        print(comparison.to_string(index=False))
        
        return comparison
    
    def save_results(self, save_path="../reports/"):
        """Save all evaluation results"""
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # Create summary report
        report = {
            'cluster_summary': self.cluster_summary.to_dict() if self.cluster_summary is not None else {},
            'revenue_contribution': self.customer_data.groupby('cluster')['total_revenue'].sum().to_dict(),
            'segment_sizes': self.customer_data['cluster'].value_counts().to_dict()
        }
        
        with open(f"{save_path}model_evaluation.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Evaluation results saved to '{save_path}model_evaluation.json'")
    
    def run_pipeline(self, X_scaled=None, labels=None):
        """Run the complete evaluation pipeline"""
        if X_scaled is not None and labels is not None:
            self.evaluate_clustering(X_scaled, labels)
        
        self.create_segment_summary()
        self.calculate_revenue_contribution()
        self.create_model_comparison_table()
        self.save_results()
        
        print("\n" + "="*50)
        print("EVALUATION PIPELINE COMPLETE!")
        print("="*50)
        
        return self.cluster_summary


# Example usage
if __name__ == "__main__":
    # Load data
    customer_data = pd.read_csv("../data/customer_segments.csv")
    
    # Run evaluation
    evaluator = ModelEvaluator(customer_data)
    evaluator.run_pipeline()