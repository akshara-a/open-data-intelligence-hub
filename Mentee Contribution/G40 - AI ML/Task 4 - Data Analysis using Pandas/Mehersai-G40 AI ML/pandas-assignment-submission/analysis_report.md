# Pandas Data Analysis Report

## 1. Dataset Overview

### Dataset Name

Synthetic E-Commerce Product Dataset

### Objective

The objective of this project is to perform data cleaning, exploratory data analysis (EDA), feature engineering, visualization, and business insight generation using the Pandas library.

### Dataset Summary

| Item                | Value |
| ------------------- | ----- |
| Number of Rows      | 4362  |
| Number of Columns   | 10    |
| File Format         | CSV   |
| Numerical Columns   | 4     |
| Categorical Columns | 5     |
| Date Columns        | 1     |

### Columns Used

* Product_ID
* Category
* Price
* Rating
* Stock
* Discount
* Region
* Payment_Method
* Order_Date
* Quantity

---

## 2. Data Quality Issues

Several data quality issues were identified during the initial inspection.

### Missing Values

| Column   | Issue          |
| -------- | -------------- |
| Category | Missing values |
| Price    | Missing values |
| Rating   | Missing values |
| Stock    | Missing values |
| Discount | Missing values |

### Duplicate Records

Duplicate rows were checked using Pandas and removed during the cleaning process.

### Invalid Values

The following potential issues were examined:

* Missing product categories
* Missing prices
* Missing ratings
* Missing stock information
* Missing discount values

---

## 3. Cleaning Steps

The following cleaning operations were performed:

### Missing Value Handling

* Category → Filled with "Unknown"
* Price → Filled using Median
* Rating → Filled using Median
* Stock → Filled with "Unknown"
* Discount → Filled with 0

### Duplicate Removal

Duplicate records were removed using:

```python
df = df.drop_duplicates()
```

### Text Standardization

Text columns were standardized using:

```python
.str.strip().str.title()
```

### Column Renaming

Column names were converted to a consistent format:

```python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
```

---

## 4. Exploratory Data Analysis

### Summary Statistics

Summary statistics were generated using:

```python
df.describe()
```

### Categorical Analysis

Value counts were performed for:

* Category
* Region
* Payment Method

### Filtering Analysis

Examples of filters used:

* Products priced above 3000
* Products with rating greater than 4
* Discount greater than 20%
* Products from North region
* Low stock products

### Sorting Analysis

Products were sorted based on price to identify premium products.

---

## 5. Grouping and Aggregation Results

### Category-Level Aggregation

The dataset was grouped by Category to calculate:

* Product Count
* Average Price
* Average Rating
* Maximum Price

### Region and Category Analysis

A multi-level grouping was performed using:

* Region
* Category

Metrics calculated:

* Average Price
* Average Rating

### Top Categories

Top categories were identified based on average product price.

---

## 6. Feature Engineering

Three new features were created.

### Feature 1: Final Price

Formula:

```python
Final Price = Price - (Price × Discount / 100)
```

Purpose:

To calculate the effective selling price after discount.

### Feature 2: Month

Extracted from Order Date.

Purpose:

To analyze monthly business trends.

### Feature 3: Price Category

Price groups:

* Low
* Medium
* High

Purpose:

To classify products based on pricing levels.

---

## 7. Visualizations

### Chart 1: Product Count by Category

Type: Bar Chart

Insight:

Shows which product categories contain the highest number of products.

### Chart 2: Price Distribution

Type: Histogram

Insight:

Displays the distribution of product prices.

### Chart 3: Monthly Revenue Trend

Type: Line Chart

Insight:

Shows monthly fluctuations in business revenue.

### Additional Visualization

Correlation Heatmap

Purpose:

To identify relationships between numerical variables.

---

## 8. Correlation Analysis

A correlation matrix was created using all numerical columns.

### Observation 1

Price and Final Price have a strong positive correlation.

### Observation 2

Discount negatively impacts Final Price.

### Observation 3

Rating shows a weak relationship with product price.

---

## 9. Key Insights

### Insight 1

Some product categories contain significantly more products than others.

### Insight 2

High-priced products contribute a major portion of potential revenue.

### Insight 3

Discounted products attract more customer interest.

### Insight 4

Certain regions show higher purchasing activity.

### Insight 5

Digital payment methods are widely used.

### Insight 6

Products with higher ratings tend to maintain stable pricing.

### Insight 7

Monthly revenue trends indicate seasonal demand patterns.

### Insight 8

Low-stock products require closer inventory monitoring.

---

## 10. Recommendations

### Recommendation 1

Increase inventory for high-demand product categories.

### Recommendation 2

Monitor low-stock products regularly to avoid stockouts.

### Recommendation 3

Use targeted discount campaigns for slow-moving products.

### Recommendation 4

Focus marketing efforts on high-performing regions.

### Recommendation 5

Promote digital payment methods to improve customer convenience.

### Recommendation 6

Review pricing strategies for low-rated products.

### Recommendation 7

Plan inventory according to seasonal demand trends.

### Recommendation 8

Use customer ratings to improve product quality and customer satisfaction.

---

## 11. Conclusion

This project demonstrated the complete data analysis workflow using Pandas. The dataset was cleaned, transformed, analyzed, and visualized to generate meaningful business insights. Various techniques such as missing value treatment, grouping, aggregation, feature engineering, visualization, and correlation analysis were applied successfully. The final analysis provides actionable recommendations that can support business decision-making and inventory management.
