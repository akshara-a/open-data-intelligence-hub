# Task 7 - Multi-Algorithm Recommendation System Comparison

## Overview

This project demonstrates the implementation and comparison of multiple Machine Learning algorithms using the **Mall Customers Dataset**. The objective is to preprocess customer data, perform exploratory analysis, build predictive models, cluster customers into segments, and compare the performance of different algorithms.

---

## Dataset

**Dataset Name:** Mall Customers Dataset

**File Used:**

* `Mall_Customers.csv`

### Dataset Features

* CustomerID
* Gender
* Age
* Annual Income (k$)
* Spending Score (1-100)

---

## Project Objectives

* Load and preprocess the dataset
* Perform Exploratory Data Analysis (EDA)
* Create a customer segmentation feature
* Predict customer spending score using Ridge Regression
* Classify customers as High Spenders using Logistic Regression
* Segment customers using K-Means Clustering
* Perform Hyperparameter Tuning using GridSearchCV
* Compare model performance
* Export processed datasets and prediction results

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Jupyter Notebook

---

## Machine Learning Algorithms

### Ridge Regression

* Predicts customer Spending Score.
* Hyperparameter tuning performed using GridSearchCV.

### Logistic Regression

* Classifies customers into High Spender and Low Spender categories.
* Performance evaluated using classification metrics.

### K-Means Clustering

* Segments customers based on Age, Annual Income, and Spending Score.
* Cluster quality evaluated using Silhouette Score.

---

## Evaluation Metrics

### Regression

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

### Classification

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

### Clustering

* Silhouette Score

---

## Files Included

* `Task7.ipynb`
* `README.md`
* `Mall_Customers.csv`
* `cleaned_dataset.csv`
* `category_summary.csv`
* `regression_predictions.csv`
* `classification_predictions.csv`
* `clustered_customers.csv`
* `model_comparison.csv`
* `best_hyperparameters.csv`

---

## Workflow

1. Load the dataset.
2. Clean and preprocess the data.
3. Perform Exploratory Data Analysis.
4. Generate customer features.
5. Train Ridge Regression model.
6. Train Logistic Regression model.
7. Apply K-Means Clustering.
8. Tune model hyperparameters using GridSearchCV.
9. Compare model performance.
10. Save prediction results and processed datasets.

---

## Results

* Successfully cleaned and analyzed the customer dataset.
* Built regression, classification, and clustering models.
* Compared the performance of multiple algorithms.
* Generated customer segments for business analysis.
* Exported prediction results and summary CSV files.

---

## Conclusion

This project demonstrates a complete machine learning workflow, including preprocessing, visualization, predictive modeling, clustering, hyperparameter tuning, and model evaluation. The generated outputs can support customer segmentation and data-driven decision-making for retail analytics.
