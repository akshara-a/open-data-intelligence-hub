"""
Classification Module
======================
Predicts customer Purchase Likelihood using Logistic Regression.
"""

import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib
matplotlib.use('Agg')
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
# pyrefly: ignore [missing-import]
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, roc_auc_score
import os

from . import model_evaluation


def prepare_classification_data(df):
    """
    Prepare features and target for classification.
    Target: PurchaseLikelihood (0/1)
    """
    # Define feature columns (exclude identifiers and target)
    exclude_cols = ['CustomerID', 'PurchaseLikelihood', 'Gender', 'ProductCategory']
    # Also exclude cluster if present
    if 'Cluster' in df.columns:
        exclude_cols.append('Cluster')

    feature_cols = [c for c in df.columns if c not in exclude_cols]

    # Encode Gender if not already encoded
    df_prep = df.copy()
    if 'Gender' in df_prep.columns and 'Gender_Encoded' not in df_prep.columns:
        le = LabelEncoder()
        df_prep['Gender_Encoded'] = le.fit_transform(df_prep['Gender'])
        feature_cols.append('Gender_Encoded')

    # One-hot encode ProductCategory if not already done
    if 'ProductCategory' in df_prep.columns:
        cat_cols = [c for c in df_prep.columns if c.startswith('Category_')]
        if not cat_cols:
            dummies = pd.get_dummies(df_prep['ProductCategory'], prefix='Category', dtype=int)
            df_prep = pd.concat([df_prep, dummies], axis=1)
            feature_cols.extend(dummies.columns.tolist())

    # Include any existing encoded columns
    for c in df_prep.columns:
        if c.startswith('Category_') and c not in feature_cols:
            feature_cols.append(c)
    if 'Gender_Encoded' in df_prep.columns and 'Gender_Encoded' not in feature_cols:
        feature_cols.append('Gender_Encoded')

    # Include Cluster as feature if available
    if 'Cluster' in df.columns:
        feature_cols.append('Cluster')
        df_prep['Cluster'] = df['Cluster']

    # Remove any remaining non-numeric or problematic columns
    feature_cols = [c for c in feature_cols if c in df_prep.columns
                    and df_prep[c].dtype in [np.float64, np.int64, np.float32, np.int32, np.uint8]]

    X = df_prep[feature_cols]
    y = df_prep['PurchaseLikelihood']

    print(f"Classification features ({len(feature_cols)}): {feature_cols}")
    print(f"Target distribution:\n{y.value_counts()}")

    return X, y, feature_cols


def train_classification(X, y, test_size=0.2, random_state=42):
    """
    Train a Logistic Regression model for purchase likelihood prediction.
    Returns the model, predictions, and train/test splits.
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set : {X_test.shape[0]} samples")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Logistic Regression
    model = LogisticRegression(max_iter=1000, random_state=random_state)
    model.fit(X_train_scaled, y_train)

    # Predict
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    return model, scaler, X_train, X_test, y_train, y_test, y_pred, y_prob


def plot_confusion_matrix(y_true, y_pred, save_path=None):
    """Plot and save the confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['Not Likely (0)', 'Likely (1)'],
                yticklabels=['Not Likely (0)', 'Likely (1)'],
                linewidths=1, linecolor='white',
                annot_kws={'size': 16, 'fontweight': 'bold'})
    ax.set_title('Confusion Matrix - Purchase Likelihood', fontweight='bold')
    ax.set_xlabel('Predicted', fontsize=12)
    ax.set_ylabel('Actual', fontsize=12)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {save_path}")
    plt.close(fig)


def run_classification(df, images_dir, outputs_dir):
    """
    Run the full classification pipeline.
    Returns the model, metrics, and predictions.
    """
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("CLASSIFICATION - PURCHASE LIKELIHOOD PREDICTION")
    print("=" * 60)

    # Prepare data
    X, y, feature_cols = prepare_classification_data(df)

    # Train model
    model, scaler, X_train, X_test, y_train, y_test, y_pred, y_prob = train_classification(X, y)

    # Evaluate
    metrics = model_evaluation.evaluate_classification(
        y_test, y_pred, y_prob, model_name="Logistic Regression"
    )

    # Plot confusion matrix
    plot_confusion_matrix(y_test, y_pred,
                          save_path=os.path.join(images_dir, 'confusion_matrix.png'))

    # Save predictions
    pred_df = pd.DataFrame({
        'Actual': y_test.values,
        'Predicted': y_pred,
        'Probability': y_prob.round(4)
    })
    pred_df.to_csv(os.path.join(outputs_dir, 'classification_predictions.csv'), index=False)
    print(f"Saved: {os.path.join(outputs_dir, 'classification_predictions.csv')}")

    print("\nClassification complete!")
    return model, metrics, pred_df


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "customer_data.csv")
    images_dir = os.path.join(base_dir, "images")
    outputs_dir = os.path.join(base_dir, "outputs")
    df = pd.read_csv(data_path)
    run_classification(df, images_dir, outputs_dir)
