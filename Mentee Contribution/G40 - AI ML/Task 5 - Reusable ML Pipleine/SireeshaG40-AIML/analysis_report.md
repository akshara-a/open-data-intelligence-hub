# Sample Superstore Sales Analysis Report

## Project Overview

This project analyzes the **Sample Superstore** dataset using the **Polars** library. The objective is to perform data cleaning, preprocessing, exploratory data analysis (EDA), aggregation, feature engineering, visualization, and derive meaningful business insights.

---

# Dataset Information

| Attribute | Value |
|-----------|-------|
| Dataset Name | Sample Superstore |
| File Format | CSV |
| Analysis Tool | Polars |
| Visualization | Matplotlib |
| Domain | Retail Sales |

The dataset contains information related to customer orders, products, sales, discounts, profits, shipping, and geographical regions.

---

# Objectives

- Load the dataset using Polars.
- Inspect and clean the data.
- Handle missing values and duplicates.
- Convert date columns into proper format.
- Perform filtering and sorting.
- Create new features for analysis.
- Perform grouping and aggregation.
- Create summary tables.
- Generate visualizations.
- Export processed datasets.
- Generate business insights.

---

# Data Cleaning

The following preprocessing steps were performed:

- Loaded CSV dataset using Polars.
- Checked dataset dimensions.
- Examined column names and data types.
- Converted **Order Date** and **Ship Date** into Date format.
- Removed duplicate records.
- Checked missing values.
- Renamed columns for easier processing.
- Exported cleaned dataset.

---

# Exploratory Data Analysis

The following analyses were carried out:

- Dataset Overview
- Summary Statistics
- Missing Value Analysis
- Duplicate Record Analysis
- Sales Distribution
- Profit Analysis
- Category Analysis
- Region-wise Analysis
- Customer Analysis
- Product Analysis

Several filters were applied to analyze:

- High Sales Orders
- Technology Category
- West Region Orders
- High Profit Orders
- High Discount Orders

---

# Feature Engineering

New columns were created to improve analysis:

- Year
- Month
- Weekday
- Sales Category

Sales were classified into:

- High Sales
- Medium Sales
- Low Sales

These additional features help identify seasonal trends and customer purchasing behavior.

---

# Aggregation and Grouping

The following aggregation operations were performed using Polars:

## Category-wise Summary

Calculated:

- Total Orders
- Total Sales
- Total Profit
- Average Sales

## Region-wise Summary

Calculated:

- Number of Orders
- Total Sales
- Total Profit

## Region and Category Summary

Grouped by:

- Region
- Category

Calculated:

- Total Sales
- Total Profit
- Average Discount

---

# Join Operation

A join operation was performed to merge category-level average sales back into the original dataset for enhanced analysis.

---

# Pivot Table

A pivot table was generated to compare sales across different regions and product categories.

---

# Visualizations

The following charts were created:

- Bar Chart – Sales by Category
- Pie Chart – Category-wise Sales Contribution
- Histogram – Sales Distribution
- Line Chart – Monthly Sales Trend
- Box Plot – Sales Distribution

These visualizations help understand customer purchasing patterns and business performance.

---

# Business Insights

### Insight 1

Technology products generate a significant portion of total sales.

### Insight 2

The West region contributes one of the highest sales among all regions.

### Insight 3

Higher discounts do not always result in higher profits.

### Insight 4

A small number of products generate a large percentage of overall revenue.

### Insight 5

Monthly sales show seasonal trends that can help forecast demand.

### Insight 6

Some customers contribute significantly more revenue than others.

### Insight 7

Furniture products often generate lower profit despite higher sales.

### Insight 8

Regional sales performance varies across different product categories.

---

# Recommendations

- Increase inventory for high-demand products.
- Optimize discount strategies to improve profitability.
- Focus marketing campaigns on high-performing regions.
- Improve performance of low-profit product categories.
- Monitor customer purchasing trends regularly.
- Build dashboards for continuous business monitoring.
- Use predictive models for sales forecasting.
- Continue performing periodic data quality checks.

---

# Exported Files

The following output files were generated:

- cleaned_dataset.csv
- category_summary.csv
- region_summary.csv
- region_category_summary.csv
- pivot_region_category.csv
- top_products.csv

---

# Conclusion

The Sample Superstore dataset was successfully analyzed using the Polars library.

The project demonstrated:

- Data Cleaning
- Data Transformation
- Filtering
- Sorting
- Aggregation
- Feature Engineering
- GroupBy Operations
- Join Operations
- Pivot Tables
- Data Visualization
- Business Insight Generation

The exported datasets and summaries can be used for future reporting, dashboard creation, and predictive analytics.