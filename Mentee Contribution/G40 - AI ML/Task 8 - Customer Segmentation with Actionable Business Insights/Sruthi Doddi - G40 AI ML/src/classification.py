"""
Classification Module
Handles Logistic Regression for predicting purchase likelihood
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve
)
import warnings
warnings.filterwarnings('ignore')


class PurchasePredictor:
    """Class to handle classification for predicting purchase likelihood"""
    
    def __init__(self, data, target_col='purchase_likelihood', feature_cols=None):
        """
        Initialize with data
        
        Parameters:
        -----------
        data : DataFrame
            Customer data with features and target
        target_col : str
            Column name for target variable (0=No purchase, 1=Purchase)
        feature_cols : list
            List of feature columns
        """
        self.data = data
        self.target_col = target_col
        self.feature_cols = feature_cols or [
            'total_purchases', 'avg_rating', 'total_pages_viewed', 
            'total_time_on_site', 'total_cart_abandoned', 'total_sessions',
            'avg_order_value', 'avg_session_value', 'pages_per_session',
            'time_per_session_min', 'purchase_rate', 'abandon_rate'
        ]
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.log_reg = None
        self.best_log_reg = None
        self.results = {}
        
    def prepare_data(self):
        """Prepare data for classification"""
        print("Preparing data for classification...")
        
        # Create target variable if it doesn't exist
        if self.target_col not in self.data.columns:
            self.data['purchase_likelihood'] = (self.data['total_purchases'] > 0).astype(int)
        
        # Create derived features if they don't exist
        if 'avg_order_value' not in self.data.columns:
            self.data['avg_order_value'] = self.data['total_revenue'] / self.data['total_purchases'].replace(0, 1)
            self.data['avg_order_value'] = self.data['avg_order_value'].replace([np.inf, -np.inf], 0)
        
        if 'avg_session_value' not in self.data.columns:
            self.data['avg_session_value'] = self.data['total_revenue'] / self.data['total_sessions'].replace(0, 1)
            self.data['avg_session_value'] = self.data['avg_session_value'].replace([np.inf, -np.inf], 0)
        
        if 'pages_per_session' not in self.data.columns:
            self.data['pages_per_session'] = self.data['total_pages_viewed'] / self.data['total_sessions'].replace(0, 1)
            self.data['pages_per_session'] = self.data['pages_per_session'].replace([np.inf, -np.inf], 0)
        
        if 'time_per_session_min' not in self.data.columns:
            self.data['time_per_session_min'] = self.data['total_time_on_site'] / self.data['total_sessions'].replace(0, 1) / 60
            self.data['time_per_session_min'] = self.data['time_per_session_min'].replace([np.inf, -np.inf], 0)
        
        if 'purchase_rate' not in self.data.columns:
            self.data['purchase_rate'] = self.data['total_purchases'] / self.data['total_sessions'].replace(0, 1)
            self.data['purchase_rate'] = self.data['purchase_rate'].replace([np.inf, -np.inf], 0)
        
        if 'abandon_rate' not in self.data.columns:
            self.data['abandon_rate'] = self.data['total_cart_abandoned'] / self.data['total_sessions'].replace(0, 1)
            self.data['abandon_rate'] = self.data['abandon_rate'].replace([np.inf, -np.inf], 0)
        
        # Split features and target
        self.X = self.data[self.feature_cols]
        self.y = self.data[self.target_col]
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(self.X)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, self.y, test_size=0.2, random_state=42
        )
        
        print(f"Training set: {self.X_train.shape[0]} samples")
        print(f"Test set: {self.X_test.shape[0]} samples")
        
        print("\nTarget Distribution:")
        print(f"  Purchasers: {sum(self.y_train)} ({sum(self.y_train)/len(self.y_train)*100:.1f}%)")
        print(f"  Non-Purchasers: {len(self.y_train)-sum(self.y_train)} ({(len(self.y_train)-sum(self.y_train))/len(self.y_train)*100:.1f}%)")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def fit_logistic_regression(self):
        """Fit base Logistic Regression model"""
        print("\n" + "="*50)
        print("LOGISTIC REGRESSION")
        print("="*50)
        
        self.log_reg = LogisticRegression(random_state=42, max_iter=1000)
        self.log_reg.fit(self.X_train, self.y_train)
        
        # Make predictions
        y_pred = self.log_reg.predict(self.X_test)
        y_pred_proba = self.log_reg.predict_proba(self.X_test)[:, 1]
        
        # Evaluate
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)
        roc_auc = roc_auc_score(self.y_test, y_pred_proba)
        
        self.results['base'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': confusion_matrix(self.y_test, y_pred)
        }
        
        print(f"Logistic Regression Performance:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  ROC-AUC: {roc_auc:.4f}")
        
        return self.log_reg
    
    def tune_logistic_regression(self):
        """Tune Logistic Regression using RandomizedSearchCV"""
        print("\n" + "="*50)
        print("TUNING LOGISTIC REGRESSION")
        print("="*50)
        
        # Parameter grid
        param_grid = {
            'C': [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0],
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear', 'saga']
        }
        
        # Randomized search
        log_reg = LogisticRegression(random_state=42, max_iter=1000)
        random_search = RandomizedSearchCV(
            estimator=log_reg,
            param_distributions=param_grid,
            n_iter=15,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1,
            random_state=42,
            verbose=1
        )
        
        print("Running RandomizedSearchCV for Logistic Regression...")
        random_search.fit(self.X_train, self.y_train)
        
        self.best_log_reg = random_search.best_estimator_
        best_params = random_search.best_params_
        
        print(f"\nBest Parameters:")
        for param, value in best_params.items():
            print(f"  {param}: {value}")
        print(f"Best CV ROC-AUC: {random_search.best_score_:.4f}")
        
        # Evaluate on test set
        y_pred = self.best_log_reg.predict(self.X_test)
        y_pred_proba = self.best_log_reg.predict_proba(self.X_test)[:, 1]
        
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred)
        roc_auc = roc_auc_score(self.y_test, y_pred_proba)
        
        self.results['tuned'] = {
            'best_params': best_params,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': confusion_matrix(self.y_test, y_pred)
        }
        
        print(f"\nTuned Logistic Regression Performance:")
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  ROC-AUC: {roc_auc:.4f}")
        
        return self.best_log_reg
    
    def compare_results(self):
        """Compare base vs tuned results"""
        print("\n" + "="*50)
        print("MODEL COMPARISON: BEFORE VS AFTER TUNING")
        print("="*50)
        
        print("\n🔹 LOGISTIC REGRESSION:")
        print(f"  Before Tuning: Accuracy={self.results['base']['accuracy']:.4f}, "
              f"ROC-AUC={self.results['base']['roc_auc']:.4f}, "
              f"F1={self.results['base']['f1_score']:.4f}")
        print(f"  After Tuning:  Accuracy={self.results['tuned']['accuracy']:.4f}, "
              f"ROC-AUC={self.results['tuned']['roc_auc']:.4f}, "
              f"F1={self.results['tuned']['f1_score']:.4f}")
        
        return self.results
    
    def visualize_results(self, save_path="../reports/visualizations/"):
        """Create classification visualizations"""
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # Get confusion matrix from tuned model
        cm = self.results['tuned']['confusion_matrix']
        y_pred_proba = self.best_log_reg.predict_proba(self.X_test)[:, 1]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Confusion Matrix
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Not Purchase', 'Purchase'],
                    yticklabels=['Not Purchase', 'Purchase'], 
                    ax=axes[0])
        axes[0].set_title('Confusion Matrix - Tuned Logistic Regression')
        axes[0].set_xlabel('Predicted')
        axes[0].set_ylabel('Actual')
        
        # ROC Curve
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        axes[1].plot(fpr, tpr, color='darkorange', lw=2, 
                    label=f'ROC (AUC = {self.results["tuned"]["roc_auc"]:.4f})')
        axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random (AUC = 0.5)')
        axes[1].set_xlim([0.0, 1.0])
        axes[1].set_ylim([0.0, 1.05])
        axes[1].set_xlabel('False Positive Rate')
        axes[1].set_ylabel('True Positive Rate')
        axes[1].set_title('ROC Curve')
        axes[1].legend(loc="lower right")
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{save_path}classification_results.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Classification visualizations saved")
    
    def save_results(self, save_path="../reports/classification_results.json"):
        """Save classification results"""
        import json
        
        results = {
            'base_model': self.results['base'],
            'tuned_model': self.results['tuned'],
            'feature_importance': dict(zip(self.feature_cols, self.log_reg.coef_[0]))
        }
        
        with open(save_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Classification results saved to '{save_path}'")
    
    def run_pipeline(self):
        """Run the complete classification pipeline"""
        self.prepare_data()
        self.fit_logistic_regression()
        self.tune_logistic_regression()
        self.compare_results()
        self.visualize_results()
        self.save_results()
        
        print("\n" + "="*50)
        print("CLASSIFICATION PIPELINE COMPLETE!")
        print("="*50)
        
        return self.best_log_reg, self.results


# Example usage
if __name__ == "__main__":
    # Load customer data
    customer_data = pd.read_csv("../data/customer_features.csv")
    
    # Run classification
    predictor = PurchasePredictor(customer_data)
    best_model, results = predictor.run_pipeline()