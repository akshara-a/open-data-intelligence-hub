"""
Regression Module
Handles Linear and Ridge Regression for predicting customer revenue
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class RevenuePredictor:
    """Class to handle regression models for predicting customer revenue"""
    
    def __init__(self, data, target_col='total_revenue', feature_cols=None):
        """
        Initialize with data
        
        Parameters:
        -----------
        data : DataFrame
            Customer data with features and target
        target_col : str
            Column name for target variable
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
        self.lin_reg = None
        self.ridge = None
        self.best_ridge = None
        self.linear_results = {}
        self.ridge_results = {}
        self.best_model = None
        
    def prepare_data(self):
        """Prepare data for modeling"""
        print("Preparing data for regression...")
        
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
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def fit_linear_regression(self):
        """Fit Linear Regression model"""
        print("\n" + "="*50)
        print("LINEAR REGRESSION")
        print("="*50)
        
        self.lin_reg = LinearRegression()
        self.lin_reg.fit(self.X_train, self.y_train)
        
        # Make predictions
        y_pred = self.lin_reg.predict(self.X_test)
        
        # Evaluate
        mae = mean_absolute_error(self.y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        r2 = r2_score(self.y_test, y_pred)
        
        self.linear_results = {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'coefficients': dict(zip(self.feature_cols, self.lin_reg.coef_))
        }
        
        print(f"Linear Regression Performance:")
        print(f"  MAE: ${mae:,.2f}")
        print(f"  RMSE: ${rmse:,.2f}")
        print(f"  R²: {r2:.4f}")
        
        return self.lin_reg
    
    def tune_ridge_regression(self):
        """Tune and fit Ridge Regression model using RandomizedSearchCV"""
        print("\n" + "="*50)
        print("RIDGE REGRESSION TUNING")
        print("="*50)
        
        # Parameter grid
        param_grid = {
            'alpha': [0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0],
            'solver': ['auto', 'svd', 'cholesky', 'lsqr', 'sag']
        }
        
        # Randomized search
        ridge = Ridge(random_state=42)
        random_search = RandomizedSearchCV(
            estimator=ridge,
            param_distributions=param_grid,
            n_iter=15,
            cv=5,
            scoring='r2',
            n_jobs=-1,
            random_state=42,
            verbose=1
        )
        
        print("Running RandomizedSearchCV for Ridge Regression...")
        random_search.fit(self.X_train, self.y_train)
        
        self.best_ridge = random_search.best_estimator_
        best_params = random_search.best_params_
        
        print(f"\nBest Parameters:")
        for param, value in best_params.items():
            print(f"  {param}: {value}")
        print(f"Best CV R²: {random_search.best_score_:.4f}")
        
        # Evaluate on test set
        y_pred = self.best_ridge.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        r2 = r2_score(self.y_test, y_pred)
        
        self.ridge_results = {
            'best_params': best_params,
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }
        
        print(f"\nTuned Ridge Regression Performance:")
        print(f"  MAE: ${mae:,.2f}")
        print(f"  RMSE: ${rmse:,.2f}")
        print(f"  R²: {r2:.4f}")
        
        return self.best_ridge
    
    def compare_models(self):
        """Compare Linear and Ridge Regression results"""
        print("\n" + "="*50)
        print("MODEL COMPARISON")
        print("="*50)
        
        comparison = pd.DataFrame({
            'Model': ['Linear Regression', 'Ridge Regression'],
            'MAE': [self.linear_results['mae'], self.ridge_results['mae']],
            'RMSE': [self.linear_results['rmse'], self.ridge_results['rmse']],
            'R²': [self.linear_results['r2'], self.ridge_results['r2']]
        })
        
        print(comparison.to_string(index=False))
        
        # Determine best model
        if self.linear_results['r2'] > self.ridge_results['r2']:
            self.best_model = 'Linear Regression'
        else:
            self.best_model = 'Ridge Regression'
        
        print(f"\n✓ Best Model: {self.best_model}")
        
        return comparison
    
    def visualize_results(self, save_path="../reports/visualizations/"):
        """Create regression visualizations"""
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # Predictions
        y_pred_lin = self.lin_reg.predict(self.X_test)
        y_pred_ridge = self.best_ridge.predict(self.X_test)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Linear Regression
        axes[0].scatter(self.y_test, y_pred_lin, alpha=0.5, color='blue')
        axes[0].plot([self.y_test.min(), self.y_test.max()], 
                    [self.y_test.min(), self.y_test.max()], 'r--', lw=2)
        axes[0].set_title(f'Linear Regression\nR² = {self.linear_results["r2"]:.4f}')
        axes[0].set_xlabel('Actual Revenue')
        axes[0].set_ylabel('Predicted Revenue')
        
        # Ridge Regression
        axes[1].scatter(self.y_test, y_pred_ridge, alpha=0.5, color='green')
        axes[1].plot([self.y_test.min(), self.y_test.max()], 
                    [self.y_test.min(), self.y_test.max()], 'r--', lw=2)
        axes[1].set_title(f'Ridge Regression\nR² = {self.ridge_results["r2"]:.4f}')
        axes[1].set_xlabel('Actual Revenue')
        axes[1].set_ylabel('Predicted Revenue')
        
        plt.tight_layout()
        plt.savefig(f"{save_path}regression_comparison.png", dpi=150, bbox_inches='tight')
        plt.close()
        
        print("✓ Regression visualizations saved")
    
    def save_results(self, save_path="../reports/regression_results.json"):
        """Save regression results"""
        import json
        
        results = {
            'linear_regression': self.linear_results,
            'ridge_regression': self.ridge_results,
            'best_model': self.best_model,
            'feature_importance': dict(zip(self.feature_cols, self.lin_reg.coef_))
        }
        
        with open(save_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Regression results saved to '{save_path}'")
    
    def run_pipeline(self):
        """Run the complete regression pipeline"""
        self.prepare_data()
        self.fit_linear_regression()
        self.tune_ridge_regression()
        self.compare_models()
        self.visualize_results()
        self.save_results()
        
        print("\n" + "="*50)
        print("REGRESSION PIPELINE COMPLETE!")
        print("="*50)
        
        return self.best_model, self.ridge_results


# Example usage
if __name__ == "__main__":
    # Load customer data
    customer_data = pd.read_csv("../data/customer_features.csv")
    
    # Run regression
    predictor = RevenuePredictor(customer_data)
    best_model, results = predictor.run_pipeline()