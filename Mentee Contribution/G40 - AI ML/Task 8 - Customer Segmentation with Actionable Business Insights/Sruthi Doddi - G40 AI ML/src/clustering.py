"""
Clustering Module
Handles K-Means clustering and segment analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
import warnings
warnings.filterwarnings('ignore')


class CustomerSegmenter:
    """Class to handle customer segmentation using K-Means"""
    
    def __init__(self, customer_data, feature_cols=None):
        """
        Initialize with customer data
        
        Parameters:
        -----------
        customer_data : DataFrame
            Aggregated customer data
        feature_cols : list
            List of features to use for clustering
        """
        self.customer_data = customer_data
        self.feature_cols = feature_cols or ['total_revenue', 'total_purchases', 'avg_rating', 
                                            'total_pages_viewed', 'total_time_on_site', 
                                            'total_cart_abandoned', 'total_sessions']
        self.X = None
        self.X_scaled = None
        self.scaler = None
        self.kmeans = None
        self.optimal_k = None
        self.labels = None
        
    def prepare_features(self):
        """Prepare and scale features for clustering"""
        print("Preparing features for clustering...")
        self.X = self.customer_data[self.feature_cols]
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_scaled = self.scaler.fit_transform(self.X)
        
        print(f"Features prepared: {self.X_scaled.shape[1]} features")
        print(f"Features: {self.feature_cols}")
        
        return self.X_scaled
    
    def find_optimal_k(self, k_range=range(1, 11)):
        """Find optimal number of clusters using Elbow Method and Silhouette Score"""
        print("\n" + "="*50)
        print("FINDING OPTIMAL K")
        print("="*50)
        
        # Elbow Method
        wcss = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
            kmeans.fit(self.X_scaled)
            wcss.append(kmeans.inertia_)
            print(f"K={k}: WCSS = {kmeans.inertia_:,.2f}")
        
        # Find elbow point
        kl = KneeLocator(k_range, wcss, curve='convex', direction='decreasing')
        elbow_k = kl.elbow
        
        # Silhouette Scores
        silhouette_scores = []
        for k in range(2, len(k_range) + 1):
            kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
            labels = kmeans.fit_predict(self.X_scaled)
            score = silhouette_score(self.X_scaled, labels)
            silhouette_scores.append(score)
            print(f"K={k}: Silhouette Score = {score:.4f}")
        
        # Select optimal K
        silhouette_k = range(2, len(k_range) + 1)[silhouette_scores.index(max(silhouette_scores))]
        
        # Determine final K
        if elbow_k is not None and 3 <= elbow_k <= 7:
            self.optimal_k = elbow_k
        elif silhouette_k is not None and 3 <= silhouette_k <= 7:
            self.optimal_k = silhouette_k
        else:
            self.optimal_k = 5
        
        print(f"\nElbow Method suggests: K={elbow_k}")
        print(f"Silhouette Score suggests: K={silhouette_k}")
        print(f"FINAL SELECTED K: {self.optimal_k}")
        
        return self.optimal_k
    
    def fit_clusters(self, k=None):
        """Fit K-Means clustering model"""
        if k is None:
            k = self.optimal_k
        
        print(f"\nFitting K-Means with K={k}...")
        self.kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
        self.labels = self.kmeans.fit_predict(self.X_scaled)
        
        # Add cluster labels to data
        self.customer_data['cluster'] = self.labels
        
        print(f"✓ K-Means fitted with {k} clusters")
        
        return self.customer_data
    
    def analyze_segments(self):
        """Analyze and profile each customer segment"""
        print("\n" + "="*50)
        print("SEGMENT ANALYSIS")
        print("="*50)
        
        cluster_summary = self.customer_data.groupby('cluster').agg({
            'total_revenue': ['mean', 'median', 'sum'],
            'total_purchases': ['mean', 'median'],
            'avg_rating': ['mean', 'median'],
            'total_sessions': ['mean', 'median'],
            'total_pages_viewed': ['mean', 'median'],
            'total_cart_abandoned': ['mean', 'median']
        }).round(2)
        
        print("Cluster Summary Statistics:")
        print(cluster_summary)
        
        # Detailed profile per segment
        print("\n" + "="*50)
        print("DETAILED SEGMENT PROFILES")
        print("="*50)
        
        for cluster in range(self.optimal_k):
            cluster_data = self.customer_data[self.customer_data['cluster'] == cluster]
            print(f"\n🔹 CLUSTER {cluster}:")
            print("-" * 40)
            print(f"  Size: {len(cluster_data)} customers ({len(cluster_data)/len(self.customer_data)*100:.1f}%)")
            print(f"  Total Revenue: ${cluster_data['total_revenue'].sum():,.2f}")
            print(f"  Avg Revenue per Customer: ${cluster_data['total_revenue'].mean():.2f}")
            print(f"  Avg Purchases: {cluster_data['total_purchases'].mean():.2f}")
            print(f"  Avg Rating: {cluster_data['avg_rating'].mean():.2f}")
            print(f"  Avg Sessions: {cluster_data['total_sessions'].mean():.2f}")
        
        return cluster_summary
    
    def visualize_segments(self, save_path="../reports/visualizations/"):
        """Create visualizations for segments"""
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # PCA Visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.X_scaled)
        
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], 
                             c=self.customer_data['cluster'], 
                             cmap='viridis', alpha=0.6, s=50)
        plt.title('Customer Segments Visualization (PCA)', fontsize=16)
        plt.xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=14)
        plt.ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=14)
        plt.colorbar(scatter, label='Cluster')
        plt.tight_layout()
        plt.savefig(f"{save_path}pca_clusters.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Segment visualizations saved")
    
    def save_results(self, save_path="../data/customer_segments.csv"):
        """Save clustering results"""
        self.customer_data.to_csv(save_path, index=False)
        print(f"✓ Customer segments saved to '{save_path}'")
        
        return self.customer_data
    
    def run_pipeline(self, k=None):
        """Run the complete clustering pipeline"""
        self.prepare_features()
        self.find_optimal_k()
        self.fit_clusters(k)
        self.analyze_segments()
        self.visualize_segments()
        self.save_results()
        
        print("\n" + "="*50)
        print("CLUSTERING PIPELINE COMPLETE!")
        print("="*50)
        
        return self.customer_data


# Example usage
if __name__ == "__main__":
    # Load customer data
    customer_data = pd.read_csv("../data/customer_features.csv")
    
    # Run segmentation
    segmenter = CustomerSegmenter(customer_data)
    segmented_customers = segmenter.run_pipeline()