"""Orchestrate the full pipeline: generate/load data, preprocess, EDA, clustering, models, and recommendations."""
from src.utils import load_data, save_model, save_dataframe
from src.data_processing import load_and_preprocess
from src.eda import basic_summary
from src.clustering import find_best_k, run_kmeans
from src.regression import run_regressions
from src.classification import run_classification
import os


def main():
    data_path = "data/customer_data.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run scripts/generate_data.py first.")

    X, y_dict, preprocessor = load_and_preprocess(data_path)
    raw = y_dict["raw"]

    print("Running EDA...")
    basic_summary(raw)

    print("Fitting preprocessor and finding best K for clustering...")
    X_trans = preprocessor.fit_transform(X)
    best_k = find_best_k(X_trans)
    print(f"Best K determined: {best_k}")
    km_model, clustered = run_kmeans(X_trans, best_k, raw)
    save_dataframe(clustered, "outputs/clustered_customers.csv")
    save_model(km_model, "models/kmeans.joblib")

    print("Running regression experiments...")
    reg_results, lr_model, ridge_model = run_regressions(X, y_dict["regression"], preprocessor)
    print("Regression results:", reg_results)
    save_model(lr_model, "models/linear_regression.joblib")
    save_model(ridge_model, "models/ridge_regression.joblib")

    print("Running classification experiments...")
    clf_metrics, clf_model = run_classification(X, y_dict["classification"], preprocessor)
    print("Classification metrics:", clf_metrics)
    save_model(clf_model, "models/logistic_regression.joblib")

    print("Pipeline complete. Models stored in models/, outputs in outputs/.")


if __name__ == "__main__":
    main()
