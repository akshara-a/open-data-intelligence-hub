import os
# pyrefly: ignore [missing-import]
import joblib
import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# pyrefly: ignore [missing-import]
from generate_dataset import generate_ecommerce_dataset
# pyrefly: ignore [missing-import]
from data_preprocessing import load_and_clean_data, get_feature_types, build_preprocessor, split_data
# pyrefly: ignore [missing-import]
from exploratory_analysis import generate_eda_reports
# pyrefly: ignore [missing-import]
from model_training import get_baseline_pipelines, train_models
# pyrefly: ignore [missing-import]
from model_evaluation import evaluate_all_models, evaluate_single_model, plot_confusion_matrix, plot_roc_curves, threshold_analysis, categorize_purchase_risk
# pyrefly: ignore [missing-import]
from hyperparameter_tuning import optimize_random_forest, optimize_decision_tree, analyze_sensitivity
# pyrefly: ignore [missing-import]
from feature_importance import extract_feature_importance, generate_feature_business_table

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    models_dir = os.path.join(base_dir, "models")
    figures_dir = os.path.join(base_dir, "reports", "figures")
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, "ecommerce_customer_data.csv")
    
    # 1. Generate / Load Dataset
    print("\n=================== STEP 1: DATASET GENERATION & LOADING ===================")
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        print("[Runner] Generating synthetic dataset...")
        df_raw = generate_ecommerce_dataset()
        df_raw.to_csv(csv_path, index=False)
    
    df, X, y = load_and_clean_data(csv_path)
    
    # 2. EDA
    print("\n=================== STEP 2: EXPLORATORY DATA ANALYSIS ===================")
    generate_eda_reports(df, output_dir=figures_dir)
    
    # 3. Data Preprocessing & Splitting
    print("\n=================== STEP 3: PREPROCESSING & DATA SPLITTING ===================")
    num_cols, cat_cols = get_feature_types(X)
    preprocessor = build_preprocessor(num_cols, cat_cols)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.20, random_state=42)
    
    # 4. Baseline Models Training
    print("\n=================== STEP 4: BASELINE MODEL TRAINING ===================")
    baseline_pipelines = get_baseline_pipelines(preprocessor, random_state=42)
    trained_baselines = train_models(baseline_pipelines, X_train, y_train)
    
    # 5. Baseline Models Evaluation
    print("\n=================== STEP 5: BASELINE MODEL EVALUATION ===================")
    baseline_comparison = evaluate_all_models(trained_baselines, X_test, y_test)
    print("\n--- BASELINE MODEL COMPARISON ---")
    print(baseline_comparison.to_string(index=False))
    
    # Plot baseline confusion matrices & ROC curves
    for name, model in trained_baselines.items():
        _, preds, _ = evaluate_single_model(model, X_test, y_test, model_name=name)
        cm_path = os.path.join(figures_dir, f"cm_baseline_{name.replace(' ', '_').lower()}.png")
        plot_confusion_matrix(y_test, preds, model_name=f"Baseline {name}", output_path=cm_path)
        
    roc_path = os.path.join(figures_dir, "baseline_roc_curves.png")
    plot_roc_curves(trained_baselines, X_test, y_test, output_path=roc_path)

    # 6. Hyperparameter Optimization
    print("\n=================== STEP 6: HYPERPARAMETER OPTIMIZATION ===================")
    best_rf_grid = optimize_random_forest(baseline_pipelines["Random Forest"], X_train, y_train, scoring="f1", cv=5)
    best_rf_model = best_rf_grid.best_estimator_
    
    best_dt_grid = optimize_decision_tree(baseline_pipelines["Decision Tree"], X_train, y_train, scoring="f1", cv=5)
    best_dt_model = best_dt_grid.best_estimator_

    # Hyperparameter Sensitivity Analysis
    sens_path = os.path.join(figures_dir, "hyperparameter_sensitivity_rf_depth.png")
    analyze_sensitivity(best_rf_grid, param_name="classifier__max_depth", output_path=sens_path)

    # 7. Evaluate Optimized Model & Comparison Table
    print("\n=================== STEP 7: OPTIMIZED MODEL EVALUATION ===================")
    opt_models = {
        "Baseline Logistic Regression": trained_baselines["Logistic Regression"],
        "Baseline Decision Tree": trained_baselines["Decision Tree"],
        "Baseline Random Forest": trained_baselines["Random Forest"],
        "Optimized Decision Tree": best_dt_model,
        "Optimized Random Forest": best_rf_model
    }
    
    final_comparison = evaluate_all_models(opt_models, X_test, y_test)
    print("\n--- BASELINE vs OPTIMIZED MODEL COMPARISON TABLE ---")
    print(final_comparison.to_string(index=False))
    
    # Plot confusion matrix & ROC curve for Optimized Random Forest
    _, opt_preds, opt_probs = evaluate_single_model(best_rf_model, X_test, y_test, model_name="Optimized Random Forest")
    opt_cm_path = os.path.join(figures_dir, "cm_optimized_random_forest.png")
    plot_confusion_matrix(y_test, opt_preds, model_name="Optimized Random Forest", output_path=opt_cm_path)
    
    final_roc_path = os.path.join(figures_dir, "final_roc_curves.png")
    plot_roc_curves(opt_models, X_test, y_test, output_path=final_roc_path)

    # 8. Feature Importance Analysis
    print("\n=================== STEP 8: FEATURE IMPORTANCE ANALYSIS ===================")
    feat_imp_path = os.path.join(figures_dir, "feature_importance_top10.png")
    df_imp = extract_feature_importance(best_rf_model, output_path=feat_imp_path)
    df_biz_imp = generate_feature_business_table(df_imp)
    print("\n--- TOP 10 INFLUENTIAL FEATURES & BUSINESS ACTIONS ---")
    print(df_biz_imp[["Feature", "Importance", "Business Interpretation"]].to_string(index=False))

    # 9. Classification Threshold Analysis & Risk Segmentation
    print("\n=================== STEP 9: THRESHOLD ANALYSIS & RISK SEGMENTATION ===================")
    df_th = threshold_analysis(best_rf_model, X_test, y_test)
    print("\n--- THRESHOLD METRICS TABLE ---")
    print(df_th.head(10).to_string(index=False))

    risk_segmented_df = categorize_purchase_risk(X_test, y_test, best_rf_model)
    print("\n--- CUSTOMER PURCHASE-RISK DISTRIBUTION ---")
    print(risk_segmented_df["PurchaseLikelihoodTier"].value_counts())

    # 10. Save Final Trained Pipeline
    print("\n=================== STEP 10: SAVING FINAL MODEL ===================")
    model_pkl_path = os.path.join(models_dir, "purchase_prediction_model.pkl")
    joblib.dump(best_rf_model, model_pkl_path)
    print(f"[Runner] Final optimized pipeline successfully saved to '{model_pkl_path}'.")

    print("\n Pipeline Execution Completed Successfully!")

if __name__ == "__main__":
    main()
