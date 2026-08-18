import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

def train_ridge_regression(X_train, y_train, X_test, y_test):
    """
    Train a Ridge Regression model, perform GridSearchCV for alpha, and evaluate.
    """
    # 1. Base model (untuned)
    base_model = Ridge(random_state=42)
    base_model.fit(X_train, y_train)
    
    y_pred_base = base_model.predict(X_test)
    mae_base = mean_absolute_error(y_test, y_pred_base)
    rmse_base = np.sqrt(mean_squared_error(y_test, y_pred_base))
    r2_base = r2_score(y_test, y_pred_base)
    
    print("Base Ridge Regression Metrics:")
    print(f"  MAE: {mae_base:.4f}")
    print(f"  RMSE: {rmse_base:.4f}")
    print(f"  R2: {r2_base:.4f}")
    
    # 2. Hyperparameter tuning using GridSearchCV
    param_grid = {'alpha': [0.01, 0.1, 1.0, 10.0, 100.0]}
    grid_search = GridSearchCV(
        estimator=Ridge(random_state=42),
        param_grid=param_grid,
        scoring='neg_mean_squared_error',
        cv=5
    )
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    best_alpha = grid_search.best_params_['alpha']
    print(f"Best alpha found by GridSearchCV: {best_alpha}")
    
    # Evaluate best model
    y_pred_best = best_model.predict(X_test)
    mae_best = mean_absolute_error(y_test, y_pred_best)
    rmse_best = np.sqrt(mean_squared_error(y_test, y_pred_best))
    r2_best = r2_score(y_test, y_pred_best)
    
    print("Tuned Ridge Regression Metrics:")
    print(f"  MAE: {mae_best:.4f}")
    print(f"  RMSE: {rmse_best:.4f}")
    print(f"  R2: {r2_best:.4f}")
    
    # Save the model
    os.makedirs('outputs', exist_ok=True)
    joblib.dump(best_model, 'outputs/ridge_model.pkl')
    print("Model saved to 'outputs/ridge_model.pkl'")
    
    results = {
        'base': {'mae': mae_base, 'rmse': rmse_base, 'r2': r2_base},
        'tuned': {'mae': mae_best, 'rmse': rmse_best, 'r2': r2_best},
        'best_params': grid_search.best_params_,
        'predictions': y_pred_best
    }
    
    return best_model, results
