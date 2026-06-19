# Pandas Data Analysis Report

## 1. Dataset Overview

The dataset used for this project is the Sample Superstore Dataset. It contains sales transactions from a retail superstore and includes customer information, product categories, sales, quantity, discounts, and profits.

- Number of Rows: 9994
- Number of Columns: 21
- File Format: CSV
- Numerical Columns: Sales, Quantity, Discount, Profit, Postal Code
- Categorical Columns: Category, Sub-Category, Segment, Region, State, City, Customer Name, etc.
- Date Columns: Order Date, Ship Date

---

## 2. Data Quality Issues

The following issues were identified during data quality analysis:

| Column | Issue Found | Suggested Fix |
|----------|-------------|---------------|
| Quantity | Zero or negative values | Remove or correct records |
| Profit | Negative values | Investigate loss-making orders |
| Text Columns | Leading and trailing spaces | Use strip() |
| Date Columns | Invalid date format | Convert using datetime |
| Duplicate Records | Duplicate rows present | Remove duplicates |

---

## 3. Cleaning Steps

The following cleaning operations were performed:

- Checked and handled missing values.
- Removed duplicate rows.
- Standardized text columns.
- Converted date columns into datetime format.
- Renamed columns for consistency.
- Verified data types.

---

## 4. Exploratory Data Analysis

Exploratory analysis was performed to understand the structure and distribution of the dataset.

Major analyses included:

- Category-wise frequency analysis.
- Segment-wise distribution.
- Region-wise analysis.
- High-sales order identification.
- Loss-making order analysis.
- Sorting top sales and profits.

Key findings:

- Office Supplies appears most frequently.
- Consumer segment has the highest number of customers.
- Binders are the most common sub-category.

---

## 5. Grouping and Aggregation Results

Grouping operations were performed using category, segment, and region.

### Category Summary

Metrics calculated:

- Record Count
- Total Sales
- Average Sales
- Minimum Sales
- Maximum Sales

### Multi-level Grouping

- Region and Category
- Segment and Category

These summaries help identify top-performing groups and areas requiring improvement.

---

## 6. Feature Engineering

Several new features were created:

| Feature | Purpose |
|----------|---------|
| sales_category | Categorize orders into High, Medium, and Low sales |
| year | Year-wise trend analysis |
| month | Monthly trend analysis |
| day_name | Weekly pattern analysis |
| profit_margin | Measure profitability |
| discount_category | Analyze discount effects |
| quantity_category | Understand order volume |

---

## 7. Visualizations

Several charts were created:

1. Bar Chart – Total Sales by Category
2. Histogram – Distribution of Sales
3. Line Chart – Monthly Sales Trend
4. Box Plot – Sales Distribution by Category
5. Pie Chart – Segment Contribution
6. Count Plot – Orders by Region
7. Scatter Plot – Sales vs Profit
8. Correlation Heatmap

These visualizations help identify trends and patterns within the dataset.

---

## 8. Correlation Analysis

Correlation analysis was performed on numerical columns.

Observations:

1. Sales and Profit show a moderate positive correlation.
2. Discount and Profit have a negative correlation.
3. Quantity and Sales have a weak positive correlation.

The heatmap provides a visual representation of these relationships.

---

## 9. Key Insights

### Insight 1
Technology category generates the highest sales revenue.

### Insight 2
Consumer segment contributes the highest sales.

### Insight 3
Several orders result in negative profit.

### Insight 4
Higher discounts reduce profitability.

### Insight 5
Sales vary across months.

### Insight 6
West region has the highest number of orders.

### Insight 7
Most orders are small-value transactions.

### Insight 8
Sales and profit are positively related.

---

## 10. Recommendations

- Increase focus on Technology products.
- Strengthen customer retention strategies for Consumer segment customers.
- Investigate loss-making orders.
- Limit excessive discounts.
- Optimize inventory according to seasonal trends.
- Improve support in high-performing regions.
- Promote bundle offers and upselling strategies.
- Maintain healthy profit margins.

---

## 11. Conclusion

This project demonstrates the use of Pandas for real-world data analysis. The dataset was cleaned, transformed, and analyzed to generate meaningful insights. Visualizations and correlation analysis provided a better understanding of customer behavior and business performance. The results can help improve decision-making and profitability.
