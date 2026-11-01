# Task 9: Optimized Classification Model with Feature Importance Analysis

## Overview
This project implements an optimized Random Forest classification pipeline predicting e-commerce purchase intention.

## Performance Metrics
- **Accuracy:** 0.94
- **ROC-AUC:** 0.9892
- **Key Features:** PageValues, ExitRates, ProductRelated

## Folder Layout
- `data/`: Contains `online_shoppers_intention.csv`
- `notebooks/`: Contains `purchase_prediction_analysis.ipynb`
- `models/`: Contains trained pipeline & preprocessor (`.pkl`)
- `reports/`: Contains feature importance report (`RESULTS.md`)
# Task 10: Apache Parquet Data Processing & Performance Benchmarking

## Overview
This project demonstrates Apache Parquet columnar data processing, filtering, column pruning, and compression benchmarking using Pandas and PyArrow.

## Performance Benchmark Summary
- **Compression Efficiency:** `zstd` reduced CSV file size from 3.44 MB to 0.89 MB (74.26% space saving).
- **Column Pruning Speedup:** Reading selective columns from Parquet was **6.40x faster** than reading from CSV.

## Deliverables Layout
- `task10_apache_parquet.ipynb`
- `parquet_assignment.py`
- `employees.parquet`
- `high_salary_employees.parquet`
- `reports/benchmark_results.md`
- `requirements.txt`
- `README.md`
# Task 9: Optimized Classification Model with Feature Importance Analysis

## Overview
This project implements an optimized Random Forest classification pipeline predicting e-commerce purchase intention.

## Performance Metrics
- **Accuracy:** 0.94
- **ROC-AUC:** 0.9892
- **Key Features:** PageValues, ExitRates, ProductRelated

## Folder Layout
- `data/`: Contains `online_shoppers_intention.csv`
- `notebooks/`: Contains `purchase_prediction_analysis.ipynb`
- `models/`: Contains trained pipeline & preprocessor (`.pkl`)
- `reports/`: Contains feature importance report (`RESULTS.md`)
