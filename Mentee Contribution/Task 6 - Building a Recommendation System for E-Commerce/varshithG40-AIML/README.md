# E-Commerce Recommendation System

A machine learning project that implements and compares multiple algorithms to build an e-commerce recommendation system.

## Features

- **Rating Prediction** — Linear & Ridge Regression to predict product ratings
- **Purchase Prediction** — Logistic Regression to predict purchase likelihood
- **Customer Segmentation** — K-Means Clustering to group customers by behavior
- **Hyperparameter Tuning** — GridSearchCV & RandomizedSearchCV for optimization
- **Model Evaluation** — Comprehensive metrics and business alignment

## Project Structure

```
e-commers/
├── data/                       # Generated dataset
├── src/                        # Source code modules
│   ├── data_generation.py      # Synthetic data generation
│   ├── data_preprocessing.py   # Cleaning, encoding, scaling
│   ├── eda.py                  # Exploratory Data Analysis
│   ├── regression_model.py     # Part A: Rating Prediction
│   ├── classification_model.py # Part B: Purchase Prediction
│   ├── clustering_model.py     # Part C: Customer Segmentation
│   ├── hyperparameter_tuning.py# Part D: Hyperparameter Optimization
│   ├── model_evaluation.py     # Part E: Model Comparison
│   └── main.py                 # Master orchestrator
├── outputs/
│   ├── plots/                  # Saved visualizations
│   └── results/                # Saved metrics and reports
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

This runs the entire pipeline: data generation → preprocessing → EDA → regression → classification → clustering → hyperparameter tuning → model evaluation.

## Dataset

A synthetic dataset of ~5,000 e-commerce records with realistic correlations between features like browsing time, cart additions, discounts, and purchase behavior.

## Models & Metrics

| Model | Task | Key Metrics |
|-------|------|-------------|
| Linear Regression | Rating prediction | MAE, RMSE, R² |
| Ridge Regression | Rating prediction | MAE, RMSE, R² |
| Logistic Regression | Purchase prediction | Accuracy, F1, ROC-AUC |
| K-Means Clustering | Customer segmentation | Silhouette Score, Inertia |

## Author

Built as a case study for implementing and comparing ML algorithms in an e-commerce recommendation context.
