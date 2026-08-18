# Multi-Algorithm Recommendation System Comparison

This project builds an e-commerce recommendation system utilizing multiple machine learning techniques: **Regression** (to predict product ratings), **Classification** (to predict purchase likelihood), and **Clustering** (to segment users based on shopping behaviors).

## Project Structure

- `data/ecommerce_data.csv`: Source dataset with customer interaction history.
- `src/preprocessing.py`: Modules for data cleaning, scaling, and train-test splits.
- `src/regression.py`: Ridge Regression training, tuning, and evaluation.
- `src/classification.py`: Logistic Regression training, tuning, and evaluation.
- `src/clustering.py`: K-Means clustering, Elbow method, and segment profiling.
- `src/utils.py`: Chart generation utilities.
- `src/report_generator.py`: PDF report generation module.
- `app.py`: Main pipeline orchestrator.
- `requirements.txt`: Python package requirements.
- `outputs/`: Output folder containing `.pkl` serialized models and evaluation results.
- `images/`: High-resolution figures showing model outcomes and segment breakdowns.
- `report.pdf`: The final compiled PDF report.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main pipeline:
   ```bash
   python app.py
   ```

## Results Summary

- **Ridge Regression**: Achieved an MAE of `0.5034` predicting product ratings, optimized using GridSearchCV (`alpha = 10.0`).
- **Logistic Regression**: Achieved `81.40%` accuracy and `78.27%` F1 score on predicting purchase status (`C = 1.0`, solver: `liblinear`).
- **K-Means Clustering**: Grouped customer behavior into 2 optimal clusters representing High-Value Loyalists and Window Shoppers, yielding a silhouette score of `0.2908`.
