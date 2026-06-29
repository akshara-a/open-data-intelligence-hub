# Customer Churn Exploratory Data Analysis

## Overview

This project performs Exploratory Data Analysis (EDA) on a Customer Churn dataset to identify patterns and factors that influence customer attrition. The analysis helps understand customer behavior and provides insights that can be useful for churn prediction and business decision-making.

## Objectives

* Understand the structure of the customer churn dataset.
* Perform data cleaning and preprocessing.
* Analyze customer demographics and service usage patterns.
* Identify factors that contribute to customer churn.
* Visualize key insights using charts and graphs.

## Dataset

The dataset used in this project contains customer information such as:

* Customer demographics
* Subscription details
* Contract type
* Monthly charges
* Tenure
* Churn status

Dataset file:
`dataset/customer_churn.csv`

## Project Structure

```text
P Harshitha - G40 AIML/
│
├── churn_eda.ipynb
├── README.md
├── dataset/
│   └── customer_churn.csv
└── images/
    ├── churn_distribution.png
    ├── contract_vs_churn.png
    ├── correlation_heatmap.png
    └── histogram.png
```

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

## Exploratory Data Analysis Performed

1. Data loading and inspection
2. Missing value analysis
3. Statistical summary of the dataset
4. Churn distribution analysis
5. Contract type vs churn analysis
6. Correlation analysis
7. Numerical feature distribution analysis

## Visualizations

### 1. Churn Distribution

Shows the proportion of customers who stayed and those who churned.

### 2. Contract Type vs Churn

Analyzes how different contract types impact customer churn.

### 3. Correlation Heatmap

Displays relationships between numerical features.

### 4. Histograms

Shows the distribution of numerical variables.

## Key Insights

* Customers with month-to-month contracts are more likely to churn.
* Long-term customers generally have lower churn rates.
* Certain service and billing patterns are associated with higher churn.

## Conclusion

The exploratory analysis provides valuable insights into customer behavior and highlights important features that can be used for building machine learning models to predict customer churn.

## Author

**P Harshitha**
G40 AI & ML
