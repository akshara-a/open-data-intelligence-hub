# Task 6 – Building a Recommendation System for E-Commerce

## Project Overview

This project demonstrates the development of a machine learning pipeline for an e-commerce recommendation system using the **Sample Superstore** dataset. The notebook performs data preprocessing, exploratory data analysis (EDA), feature engineering, predictive modeling, customer segmentation, and model evaluation.

The objective is to analyze customer purchasing behavior, predict sales and purchase status, identify customer segments, and generate useful business insights for decision-making.

---

## Dataset

**Dataset Name:** Sample - Superstore

The dataset contains information related to:

* Order Details
* Customer Information
* Product Categories
* Sales
* Profit
* Discount
* Quantity
* Region
* Shipping Details

---

## Objectives

* Load and preprocess the dataset.
* Perform Exploratory Data Analysis (EDA).
* Create useful features from existing data.
* Build a Linear Regression model for sales prediction.
* Build a Logistic Regression model for purchase classification.
* Perform customer segmentation using K-Means Clustering.
* Tune model parameters using GridSearchCV.
* Compare model performance.
* Export prediction results and analysis files.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Jupyter Notebook

---

## Machine Learning Algorithms

### Regression

* Linear Regression

### Classification

* Logistic Regression

### Clustering

* K-Means Clustering

### Hyperparameter Tuning

* GridSearchCV

---

## Project Workflow

1. Import Libraries
2. Load Dataset
3. Data Cleaning
4. Handle Missing Values
5. Remove Duplicate Records
6. Feature Engineering
7. Exploratory Data Analysis
8. Data Visualization
9. Feature Encoding
10. Feature Scaling
11. Train-Test Split
12. Linear Regression
13. Logistic Regression
14. K-Means Clustering
15. Hyperparameter Tuning
16. Model Evaluation
17. Export Results

---

## Output Files

The notebook generates the following output files:

* cleaned_superstore.csv
* regression_predictions.csv
* classification_predictions.csv
* clustered_customers.csv
* category_summary.csv
* region_summary.csv
* region_category_summary.csv
* pivot_region_category.csv
* top_products.csv
* model_comparison.csv
* best_hyperparameters.csv

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
* F1-Score

### Clustering

* Silhouette Score

---

## Business Insights

* Identifies high-performing product categories.
* Analyzes regional sales performance.
* Predicts future sales using regression.
* Predicts purchase likelihood using classification.
* Segments customers into different clusters.
* Supports better inventory planning and targeted marketing.
* Helps improve customer engagement and sales strategies.

---

## Folder Structure

```
Task 6 - Building a Recommendation System for E-Commerce/
│
├── Task6.ipynb
├── Sample - Superstore.csv
├── README.md
├── analysis_report.md
├── cleaned_superstore.csv
├── regression_predictions.csv
├── classification_predictions.csv
├── clustered_customers.csv
├── category_summary.csv
├── region_summary.csv
├── region_category_summary.csv
├── pivot_region_category.csv
├── top_products.csv
├── model_comparison.csv
└── best_hyperparameters.csv
```

---

## Conclusion

This project demonstrates a complete machine learning workflow for an e-commerce recommendation system. By applying regression, classification, clustering, and hyperparameter tuning techniques, the project provides meaningful insights into customer behavior, sales trends, and business performance. The generated outputs can assist organizations in making data-driven decisions and improving customer satisfaction through more effective recommendation strategies.