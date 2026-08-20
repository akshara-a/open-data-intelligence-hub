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