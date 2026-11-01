# Walmart Sales Data Analysis Report

## 1. Dataset Overview

This project analyzes the Walmart sales dataset using the Pandas library. The objective is to clean the dataset, perform exploratory data analysis (EDA), identify meaningful business insights, and generate visualizations.

### Dataset Information

| Item | Value |
|------|-------|
| Dataset Name | Walmart Sales Dataset |
| File Format | CSV |
| Number of Rows | 6435 |
| Number of Columns | 8 |
| Numerical Columns | Weekly_Sales, Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment |
| Categorical Columns | Store, Date |

---

# 2. Data Quality Issues

The dataset was inspected for data quality problems.

### Issues Identified

- Missing values were checked for all columns.
- Duplicate records were identified.
- Negative weekly sales were checked.
- Invalid temperature values were checked.
- Date column was converted to datetime format.

---

# 3. Cleaning Steps

The following preprocessing steps were performed:

- Converted the Date column into datetime format.
- Renamed column names to lowercase.
- Removed duplicate records.
- Checked missing values.
- Verified numerical columns for invalid values.
- Exported cleaned dataset into CSV and Excel formats.

---

# 4. Exploratory Data Analysis (EDA)

The following analyses were performed:

- Dataset overview
- Summary statistics
- Missing value analysis
- Duplicate record analysis
- Value counts
- Data filtering
- Data sorting
- Column selection
- Weekly sales analysis

Five different filters were applied, including:

- High weekly sales
- Holiday sales
- High temperature records
- High unemployment records
- High CPI records

---

# 5. Grouping and Aggregation Results

Grouping operations were performed using Pandas.

### Single-Level Grouping

Grouped by Store:

- Record Count
- Total Sales
- Average Sales
- Minimum Sales
- Maximum Sales

### Multi-Level Grouping

Grouped by:

- Store
- Holiday Flag

Aggregated:

- Total Sales
- Average Sales
- Record Count

A Pivot Table was also created to compare sales across stores during holiday and non-holiday weeks.

---

# 6. Feature Engineering

The following new features were created:

| Feature | Description |
|---------|-------------|
| Year | Extracted from Date |
| Month | Extracted from Date |
| Day_Name | Day of the week |
| Sales_Category | High, Medium, Low sales classification |

These features improve data analysis and trend identification.

---

# 7. Visualizations

The following charts were created:

1. Bar Chart – Top 10 Stores by Total Sales
2. Histogram – Weekly Sales Distribution
3. Line Chart – Monthly Sales Trend
4. Box Plot – Weekly Sales by Holiday Flag
5. Correlation Heatmap

These visualizations help understand sales trends and relationships between variables.

---

# 8. Correlation Analysis

Correlation analysis was performed on all numerical columns.

### Observations

- Weekly Sales have a moderate relationship with economic indicators.
- CPI and Unemployment show relationships with sales trends.
- Fuel Price has relatively weak correlation with Weekly Sales.
- Temperature has little direct correlation with Weekly Sales.

A heatmap was generated to visualize these correlations.

---

# 9. Key Insights

### Insight 1

Store-wise sales differ significantly.

**Business Meaning:** Some stores contribute much more revenue than others.

---

### Insight 2

Holiday weeks influence weekly sales.

**Business Meaning:** Sales strategies should be adjusted during holidays.

---

### Insight 3

Certain months generate higher sales.

**Business Meaning:** Seasonal demand affects business performance.

---

### Insight 4

Top-performing stores consistently generate high revenue.

**Business Meaning:** These stores can be used as benchmarks.

---

### Insight 5

Economic indicators such as CPI and unemployment impact sales.

**Business Meaning:** External economic conditions should be monitored.

---

### Insight 6

Most sales fall within a normal range, while some outliers exist.

**Business Meaning:** Exceptional sales weeks require further investigation.

---

### Insight 7

Feature engineering provides better time-based analysis.

**Business Meaning:** Monthly and yearly trends become easier to analyze.

---

### Insight 8

The cleaned dataset is suitable for predictive analytics and machine learning.

**Business Meaning:** Future forecasting models can be built using this dataset.

---

# 10. Recommendations

- Increase inventory during high-demand months.
- Improve marketing during holiday periods.
- Focus on underperforming stores.
- Monitor unusual sales outliers.
- Track economic indicators before planning promotions.
- Use predictive analytics for sales forecasting.
- Continue regular data quality checks.
- Build dashboards for real-time sales monitoring.

---

# 11. Conclusion

The Walmart Sales dataset was successfully cleaned, analyzed, and visualized using the Pandas library.

The project demonstrated various data analysis techniques including:

- Data cleaning
- Missing value analysis
- Duplicate removal
- Feature engineering
- Filtering and sorting
- Grouping and aggregation
- Correlation analysis
- Visualization
- Business insight generation

The cleaned dataset and summary reports were exported successfully and are suitable for further business analysis and machine learning applications.