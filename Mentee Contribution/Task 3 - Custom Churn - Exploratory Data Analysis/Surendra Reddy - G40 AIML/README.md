# Customer Churn - Exploratory Data Analysis

**Student:** Surendra Reddy - G40 AIML
**Task:** Task 3 - Customer Churn EDA

## Dataset
- **Name:** Telco Customer Churn (IBM sample dataset)
- **Size:** 7,043 customers, 21 columns
- **Target column:** Churn (Yes/No)

## What I Did
- Loaded and inspected the dataset (shape, types, missing values)
- Found and cleaned 11 blank `TotalCharges` values (new customers with 0 tenure, converted to numeric and filled with 0)
- Confirmed 0 duplicate rows in the dataset
- Analyzed churn distribution (count plot, pie chart)
- Explored numeric feature distributions (tenure, MonthlyCharges, TotalCharges)
- Checked for outliers using boxplots (no extreme outliers found)
- Compared churn against Contract type, Payment method, Internet service type
- Compared tenure and monthly charges between churned and retained customers
- Built a correlation heatmap of numeric features vs churn
- Compared churn by gender and senior citizen status
- Wrote 5 business insights and 5 feature engineering ideas
- Prepared a full written EDA report following the assignment's 7-section format

## Key Findings
- Overall churn rate is 26.54% (1,869 churned out of 7,043 customers)
- Month-to-month contract customers churn far more than yearly contract customers
- Electronic check users churn more than automatic payment method users
- Fiber optic customers churn more than DSL customers
- Lower tenure customers are much more likely to churn
- Tenure correlates negatively with churn (-0.35); monthly charges correlates positively (+0.19)

## Files
| File | Description |
|---|---|
| `Customer_Churn_EDA_Surendra.ipynb` | Full EDA notebook with code, charts, and analysis |
| `Customer_Churn_EDA_Report_Surendra.pdf` | Final written report (Introduction, Dataset Overview, Data Cleaning, EDA, Business Insights, Feature Engineering, Conclusion) |
| `data/Customer_Churn_Dataset_Surendra.csv` | Raw dataset |
| `data/Cleaned_Customer_Churn_Dataset_Surendra.csv` | Cleaned dataset after handling missing values and data type fixes |
| `README.md` | This file |