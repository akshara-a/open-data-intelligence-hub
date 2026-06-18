import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
    classification_report,
)
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'Churn_Modelling.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_model.joblib')


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def preprocess_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, ColumnTransformer]:
    # Drop unnecessary identifiers
    df = df.drop(columns=['RowNumber', 'CustomerId', 'Surname'], errors='ignore')

    # Handle duplicates and missing values
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.dropna()

    X = df.drop(columns=['Exited'])
    y = df['Exited']

    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = ['Geography', 'Gender']

    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ])

    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first')),
    ])

    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
    ])

    return X, y, preprocessor


def evaluate_model(name: str, model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else model.decision_function(X_test)

    metrics = {
        'model': name,
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba),
        'confusion_matrix': confusion_matrix(y_test, y_pred),
    }
    return metrics, y_pred_proba


def plot_roc_curve(y_test: np.ndarray, y_pred_proba: np.ndarray, model_name: str) -> None:
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC Curve ({model_name})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {model_name}')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.savefig(os.path.join(os.path.dirname(__file__), f'{model_name}_roc_curve.png'))
    plt.close()


def plot_feature_importance(model, feature_names: list[str]):
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_[0])
    else:
        return

    feature_importances = pd.Series(importances, index=feature_names).sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importances.values, y=feature_importances.index)
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), 'feature_importance.png'))
    plt.close()


def main():
    df = load_data(DATA_PATH)
    X, y, preprocessor = preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    models = {
        'LogisticRegression': LogisticRegression(max_iter=500, random_state=42),
        'DecisionTree': DecisionTreeClassifier(random_state=42),
        'RandomForest': RandomForestClassifier(random_state=42),
        'KNN': KNeighborsClassifier(),
        'SVM': SVC(probability=True, random_state=42),
    }

    param_grids = {
        'LogisticRegression': {
            'model__C': [0.01, 0.1, 1, 10],
            'model__penalty': ['l2'],
        },
        'DecisionTree': {
            'model__max_depth': [3, 5, 7, 9],
            'model__min_samples_split': [2, 5, 10],
        },
        'RandomForest': {
            'model__n_estimators': [100, 200],
            'model__max_depth': [None, 10, 20],
            'model__min_samples_split': [2, 5],
        },
        'KNN': {
            'model__n_neighbors': [3, 5, 7],
            'model__weights': ['uniform', 'distance'],
        },
        'SVM': {
            'model__C': [0.1, 1, 10],
            'model__kernel': ['rbf', 'linear'],
        },
    }

    evaluation_results = []
    best_model = None
    best_score = 0.0

    for name, estimator in models.items():
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('model', estimator),
        ])

        grid_search = GridSearchCV(pipeline, param_grids[name], cv=5, scoring='roc_auc', n_jobs=-1)
        grid_search.fit(X_train, y_train)

        print(f"Best parameters for {name}: {grid_search.best_params_}")

        test_metrics, y_pred_proba = evaluate_model(name, grid_search.best_estimator_, X_test, y_test)
        evaluation_results.append(test_metrics)
        plot_roc_curve(y_test, y_pred_proba, name)

        if test_metrics['roc_auc'] > best_score:
            best_score = test_metrics['roc_auc']
            best_model = grid_search.best_estimator_

    results_df = pd.DataFrame(evaluation_results)
    results_df.to_csv(os.path.join(os.path.dirname(__file__), 'model_evaluation_results.csv'), index=False)
    print(results_df)

    transformer = best_model.named_steps['preprocessor']
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = ['Geography', 'Gender']

    encoded_cat_features = transformer.transformers_[1][1].named_steps['onehot'].get_feature_names_out(categorical_features)
    feature_names = numeric_features + encoded_cat_features.tolist()

    plot_feature_importance(best_model.named_steps['model'], feature_names)

    joblib.dump(best_model, MODEL_PATH)
    print(f"Saved best model to {MODEL_PATH}")


if __name__ == '__main__':
    main()
