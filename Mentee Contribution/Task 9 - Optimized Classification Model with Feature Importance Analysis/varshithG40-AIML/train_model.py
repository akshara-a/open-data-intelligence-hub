"""
Standalone model training script.
Run this if the saved model can't be loaded (e.g., sklearn version mismatch).
"""
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data" / "ecommerce_customer_data.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "purchase_prediction_model.pkl"

def train_model():
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # Drop CustomerID
    df_model = df.drop('CustomerID', axis=1)
    X = df_model.drop('Purchase', axis=1)
    y = df_model['Purchase']
    
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    
    # Preprocessing
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Grid search
    print("Training model...")
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42, max_iter=1000))
    ])
    
    param_grid = {
        'classifier__C': [0.1, 1.0, 10.0],
        'classifier__class_weight': [None, 'balanced'],
        'classifier__solver': ['lbfgs', 'saga']
    }
    
    grid = GridSearchCV(pipeline, param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    best = grid.best_estimator_
    
    # Save
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Best params: {grid.best_params_}")
    print(f"Best CV F1: {grid.best_score_:.4f}")
    
    # Save metadata
    import json
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    
    y_pred = best.predict(X_test)
    y_prob = best.predict_proba(X_test)[:, 1]
    
    metadata = {
        'model_name': 'Logistic Regression (Optimized)',
        'model_type': 'LogisticRegression',
        'hyperparameters': best.named_steps['classifier'].get_params(),
        'metrics': {
            'Accuracy': float(accuracy_score(y_test, y_pred)),
            'Precision': float(precision_score(y_test, y_pred)),
            'Recall': float(recall_score(y_test, y_pred)),
            'F1': float(f1_score(y_test, y_pred)),
            'ROC-AUC': float(roc_auc_score(y_test, y_prob))
        },
        'features': {
            'numeric': numeric_features,
            'categorical': categorical_features,
            'total_after_encoding': len(numeric_features) + len(
                best.named_steps['preprocessor'].named_transformers_['cat']
                    .named_steps['onehot'].get_feature_names_out(categorical_features)
            )
        },
        'training_info': {
            'train_size': len(X_train),
            'test_size': len(X_test),
            'purchase_rate_train': float(y_train.mean()),
            'purchase_rate_test': float(y_test.mean())
        }
    }
    
    with open(MODEL_PATH.parent / 'model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved. F1={metadata['metrics']['F1']:.4f}, ROC-AUC={metadata['metrics']['ROC-AUC']:.4f}")
    return best

if __name__ == "__main__":
    train_model()
