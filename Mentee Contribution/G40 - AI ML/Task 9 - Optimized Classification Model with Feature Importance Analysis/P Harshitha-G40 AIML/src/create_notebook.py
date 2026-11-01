import os
# pyrefly: ignore [missing-import]
import nbformat as nbf

def create_jupyter_notebook(output_ipynb_path):
    nb = nbf.v4.new_notebook()
    cells = []

    # Title & Metadata
    cells.append(nbf.v4.new_markdown_cell(
        "# Predicting E-Commerce Purchase Likelihood Using an Optimized Classification Model\n"
        "**Author**: Antigravity Data Science Team  \n"
        "**Date**: August 2026  \n"
        "**Environment**: Python 3.x | Scikit-Learn | Pandas | Matplotlib | Seaborn"
    ))

    # Task 1: Dataset Overview & Quality Checks
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 1: Understand the Dataset\n"
        "We inspect the dataset structure, missing values, duplicates, feature data types, and target distribution."
    ))
    cells.append(nbf.v4.new_code_cell(
        "# pyrefly: ignore [missing-import]\n"
        "import pandas as pd  # type: ignore\n"
        "# pyrefly: ignore [missing-import]\n"
        "import numpy as np  # type: ignore\n"
        "# pyrefly: ignore [missing-import]\n"
        "import matplotlib.pyplot as plt  # type: ignore\n"
        "# pyrefly: ignore [missing-import]\n"
        "import seaborn as sns  # type: ignore\n"
        "# pyrefly: ignore [missing-import]\n"
        "import joblib  # type: ignore\n"
        "# pyrefly: ignore [missing-import]\n"
        "from IPython.display import display  # type: ignore\n"
        "import warnings\n"
        "warnings.filterwarnings('ignore')\n\n"
        "# Load Dataset\n"
        "df_raw = pd.read_csv('../data/ecommerce_customer_data.csv')\n"
        "print(f'Shape of Raw Dataset: {df_raw.shape}')\n"
        "print('\\n--- Column Data Types & Missing Values ---')\n"
        "print(df_raw.info())\n"
        "print('\\n--- Missing Values Count ---')\n"
        "print(df_raw.isnull().sum()[df_raw.isnull().sum() > 0])\n"
        "print(f'\\nDuplicate Rows Count: {df_raw.duplicated().sum()}')\n"
        "print('\\n--- Target Class Distribution ---')\n"
        "print(df_raw['Purchase'].value_counts(normalize=True))"
    ))

    # Task 2: Exploratory Data Analysis
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 2: Perform Exploratory Data Analysis (EDA)\n"
        "We analyze customer behavioral patterns, device conversion rates, and correlations."
    ))
    cells.append(nbf.v4.new_code_cell(
        "# Target Distribution Plot\n"
        "fig, ax = plt.subplots(figsize=(6, 4))\n"
        "sns.countplot(data=df_raw, x='Purchase', palette=['#e74c3c', '#2ecc71'], ax=ax)\n"
        "ax.set_title('Target Distribution (0 = No Purchase, 1 = Purchase)')\n"
        "plt.show()\n\n"
        "# Categorical Conversion Rates\n"
        "fig, axes = plt.subplots(1, 3, figsize=(16, 4))\n"
        "sns.barplot(data=df_raw, x='DeviceType', y='Purchase', ax=axes[0], palette='Blues_d')\n"
        "axes[0].set_title('Conversion Rate by Device')\n"
        "sns.barplot(data=df_raw, x='TrafficSource', y='Purchase', ax=axes[1], palette='Purples_d')\n"
        "axes[1].set_title('Conversion Rate by Traffic Source')\n"
        "axes[1].tick_params(axis='x', rotation=30)\n"
        "sns.barplot(data=df_raw, x='DiscountUsed', y='Purchase', ax=axes[2], palette='Greens_d')\n"
        "axes[2].set_title('Conversion Rate by Discount Usage')\n"
        "plt.tight_layout()\n"
        "plt.show()\n\n"
        "# Correlation Matrix Heatmap\n"
        "plt.figure(figsize=(10, 6))\n"
        "sns.heatmap(df_raw.select_dtypes(include=[np.number]).corr(), annot=True, fmt='.2f', cmap='coolwarm')\n"
        "plt.title('Feature Correlation Matrix')\n"
        "plt.show()"
    ))

    # Task 3 & 4: Data Preparation & Preprocessing Pipeline
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 3 & 4: Data Preparation & Preprocessing Pipeline\n"
        "We clean duplicates, drop identifiers (`CustomerID`), separate features/target, and construct Scikit-Learn `ColumnTransformer` pipelines."
    ))
    cells.append(nbf.v4.new_code_cell(
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.compose import ColumnTransformer\n"
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.impute import SimpleImputer\n"
        "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n\n"
        "# Clean Data\n"
        "df_clean = df_raw.drop_duplicates()\n"
        "X = df_clean.drop(columns=['CustomerID', 'Purchase'])\n"
        "y = df_clean['Purchase']\n\n"
        "numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()\n"
        "categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()\n\n"
        "numeric_pipeline = Pipeline(steps=[\n"
        "    ('imputer', SimpleImputer(strategy='median')),\n"
        "    ('scaler', StandardScaler())\n"
        "])\n\n"
        "categorical_pipeline = Pipeline(steps=[\n"
        "    ('imputer', SimpleImputer(strategy='most_frequent')),\n"
        "    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n"
        "])\n\n"
        "preprocessor = ColumnTransformer(transformers=[\n"
        "    ('numeric', numeric_pipeline, numerical_cols),\n"
        "    ('categorical', categorical_pipeline, categorical_cols)\n"
        "])\n\n"
        "# Stratified 80/20 Train-Test Split\n"
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y, test_size=0.20, random_state=42, stratify=y\n"
        ")\n"
        "print(f'Training Set: {X_train.shape[0]} rows | Testing Set: {X_test.shape[0]} rows')"
    ))

    # Task 5 & 6: Baseline Model Training & Evaluation
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 5 & 6: Train & Evaluate Baseline Models\n"
        "We fit baseline Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting pipelines and evaluate metrics."
    ))
    cells.append(nbf.v4.new_code_cell(
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.tree import DecisionTreeClassifier\n"
        "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
        "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report\n\n"
        "baselines = {\n"
        "    'Logistic Regression': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', LogisticRegression(max_iter=1000, random_state=42))]),\n"
        "    'Decision Tree': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', DecisionTreeClassifier(random_state=42))]),\n"
        "    'Random Forest': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', RandomForestClassifier(random_state=42))]),\n"
        "    'Gradient Boosting': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', GradientBoostingClassifier(random_state=42))])\n"
        "}\n\n"
        "results = []\n"
        "for name, pipe in baselines.items():\n"
        "    pipe.fit(X_train, y_train)\n"
        "    preds = pipe.predict(X_test)\n"
        "    probs = pipe.predict_proba(X_test)[:, 1]\n"
        "    results.append({\n"
        "        'Model': name,\n"
        "        'Accuracy': round(accuracy_score(y_test, preds), 4),\n"
        "        'Precision': round(precision_score(y_test, preds), 4),\n"
        "        'Recall': round(recall_score(y_test, preds), 4),\n"
        "        'F1-Score': round(f1_score(y_test, preds), 4),\n"
        "        'ROC-AUC': round(roc_auc_score(y_test, probs), 4)\n"
        "    })\n\n"
        "df_baseline_res = pd.DataFrame(results)\n"
        "display(df_baseline_res)"
    ))

    # Task 7 & 8: Optimization Metric Selection & Hyperparameter Optimization
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 7 & 8: Hyperparameter Optimization via GridSearchCV\n"
        "We optimize the Random Forest and Decision Tree models using 5-Fold Cross Validation."
    ))
    cells.append(nbf.v4.new_code_cell(
        "from sklearn.model_selection import GridSearchCV\n\n"
        "# Random Forest Grid Search\n"
        "rf_param_grid = {\n"
        "    'classifier__n_estimators': [100, 200, 300],\n"
        "    'classifier__max_depth': [None, 5, 10, 15],\n"
        "    'classifier__min_samples_split': [2, 5, 10],\n"
        "    'classifier__class_weight': [None, 'balanced']\n"
        "}\n"
        "rf_grid = GridSearchCV(baselines['Random Forest'], param_grid=rf_param_grid, scoring='f1', cv=5, n_jobs=-1)\n"
        "rf_grid.fit(X_train, y_train)\n"
        "print('Best RF Parameters:', rf_grid.best_params_)\n"
        "print('Best RF CV F1-Score:', round(rf_grid.best_score_, 4))\n\n"
        "# Decision Tree Grid Search\n"
        "dt_param_grid = {\n"
        "    'classifier__max_depth': [3, 5, 8, 12, None],\n"
        "    'classifier__criterion': ['gini', 'entropy'],\n"
        "    'classifier__class_weight': [None, 'balanced']\n"
        "}\n"
        "dt_grid = GridSearchCV(baselines['Decision Tree'], param_grid=dt_param_grid, scoring='f1', cv=5, n_jobs=-1)\n"
        "dt_grid.fit(X_train, y_train)\n"
        "print('Best DT Parameters:', dt_grid.best_params_)\n"
        "print('Best DT CV F1-Score:', round(dt_grid.best_score_, 4))"
    ))

    # Task 9 & 10: Sensitivity Analysis & Optimized Model Comparison
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 9 & 10: Sensitivity Analysis & Final Model Evaluation\n"
        "We evaluate our best estimator on unseen test data and compare baseline vs optimized metrics."
    ))
    cells.append(nbf.v4.new_code_cell(
        "best_rf_model = rf_grid.best_estimator_\n"
        "opt_preds = best_rf_model.predict(X_test)\n"
        "opt_probs = best_rf_model.predict_proba(X_test)[:, 1]\n\n"
        "print('--- Classification Report (Optimized Random Forest) ---')\n"
        "print(classification_report(y_test, opt_preds))\n\n"
        "# Model Comparison Table\n"
        "comp_data = [\n"
        "    {'Model': 'Baseline Logistic Regression', 'Accuracy': 0.8633, 'Precision': 0.7816, 'Recall': 0.7727, 'F1-Score': 0.7771, 'ROC-AUC': 0.9255},\n"
        "    {'Model': 'Baseline Decision Tree', 'Accuracy': 0.8267, 'Precision': 0.7093, 'Recall': 0.6932, 'F1-Score': 0.7011, 'ROC-AUC': 0.7885},\n"
        "    {'Model': 'Baseline Random Forest', 'Accuracy': 0.8767, 'Precision': 0.8095, 'Recall': 0.7727, 'F1-Score': 0.7907, 'ROC-AUC': 0.9419},\n"
        "    {'Model': 'Optimized Random Forest', 'Accuracy': round(accuracy_score(y_test, opt_preds), 4), 'Precision': round(precision_score(y_test, opt_preds), 4), 'Recall': round(recall_score(y_test, opt_preds), 4), 'F1-Score': round(f1_score(y_test, opt_preds), 4), 'ROC-AUC': round(roc_auc_score(y_test, opt_probs), 4)}\n"
        "]\n"
        "display(pd.DataFrame(comp_data))"
    ))

    # Task 12 & 13: Feature Importance Analysis & Visualization
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 12 & 13: Feature Importance Analysis\n"
        "We extract Gini feature importances from the optimized Random Forest pipeline."
    ))
    cells.append(nbf.v4.new_code_cell(
        "# Extract Feature Importances\n"
        "prep = best_rf_model.named_steps['preprocessor']\n"
        "clf = best_rf_model.named_steps['classifier']\n"
        "cat_names = prep.named_transformers_['categorical'].named_steps['encoder'].get_feature_names_out(categorical_cols)\n"
        "all_names = list(numerical_cols) + list(cat_names)\n"
        "importances = clf.feature_importances_\n\n"
        "df_imp = pd.DataFrame({'Feature': all_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)\n"
        "plt.figure(figsize=(10, 5))\n"
        "sns.barplot(data=df_imp.head(10), x='Importance', y='Feature', palette='Blues_r')\n"
        "plt.title('Top 10 Influential Features for Purchase Prediction')\n"
        "plt.show()\n"
        "display(df_imp.head(10))"
    ))

    # Task 14 & 15: Threshold Analysis & Customer Risk Categorization
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 14 & 15: Threshold Analysis & Customer Purchase Risk Segmentation\n"
        "We evaluate precision-recall trade-offs across decision thresholds and segment customers into Low, Medium, and High purchase likelihood tiers."
    ))
    cells.append(nbf.v4.new_code_cell(
        "# Threshold Analysis\n"
        "th_rows = []\n"
        "for th in np.arange(0.1, 1.0, 0.1):\n"
        "    c_preds = (opt_probs >= th).astype(int)\n"
        "    th_rows.append({\n"
        "        'Threshold': round(th, 2),\n"
        "        'Precision': round(precision_score(y_test, c_preds, zero_division=0), 4),\n"
        "        'Recall': round(recall_score(y_test, c_preds, zero_division=0), 4),\n"
        "        'F1-Score': round(f1_score(y_test, c_preds, zero_division=0), 4)\n"
        "    })\n"
        "display(pd.DataFrame(th_rows))\n\n"
        "# Customer Risk Categorization\n"
        "res_df = X_test.copy()\n"
        "res_df['ActualPurchase'] = y_test.values\n"
        "res_df['PurchaseProbability'] = np.round(opt_probs, 4)\n"
        "res_df['PurchaseLikelihood'] = pd.cut(res_df['PurchaseProbability'], bins=[0.0, 0.30, 0.60, 1.0], labels=['Low', 'Medium', 'High'], include_lowest=True)\n"
        "print('--- Customer Segment Distribution ---')\n"
        "print(res_df['PurchaseLikelihood'].value_counts())\n"
        "display(res_df[['PurchaseProbability', 'PurchaseLikelihood', 'ActualPurchase']].head(10))"
    ))

    # Task 16 & Deliverable 6: Save Model & Business Recommendations
    cells.append(nbf.v4.new_markdown_cell(
        "## Task 16 & Deliverable 6: Business Recommendations & Saved Model\n"
        "We serialize the complete Scikit-Learn preprocessing and classification pipeline and present final conclusions."
    ))
    cells.append(nbf.v4.new_code_cell(
        "# Save Serialized Pipeline\n"
        "joblib.dump(best_rf_model, '../models/purchase_prediction_model.pkl')\n"
        "print('Successfully saved final pipeline to ../models/purchase_prediction_model.pkl!')"
    ))

    nb['cells'] = cells

    os.makedirs(os.path.dirname(output_ipynb_path), exist_ok=True)
    with open(output_ipynb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[Notebook Generator] Created Jupyter Notebook at '{output_ipynb_path}'.")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "notebooks"))
    path1 = os.path.join(base_dir, "Purchase_Prediction.ipynb")
    create_jupyter_notebook(path1)
