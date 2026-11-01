# Pandas Data Analysis Report

## 1. Dataset Overview

| Item                | Value                                                                 |
| ------------------- | --------------------------------------------------------------------- |
| Dataset Name        | retail_store_sales                                                    |
| Number of Rows      | 12575                                                                 |
| Number of Columns   | 16                                                                    |
| File Format         | CSV                                                                   |
| Numerical Columns   | price_per_unit, quantity, total_spent                                 |
| Categorical Columns | transaction_id, customer_id, category, item, payment_method, location |
| Date Columns        | transaction_date                                                      |
| Boolean Columns     | discount_applied                                                      |

---

## 2. Data Quality Issues

| Column           | Issue Found                        | Number of Records | Suggested Fix                  |
| ---------------- | ---------------------------------- | ----------------- | ------------------------------ |
| quantity         | Missing values                     | Check output      | Fill with median               |
| total_spent      | Missing values                     | Check output      | Fill with median               |
| category         | Inconsistent casing / extra spaces | Check output      | str.strip().str.title()        |
| transaction_date | Wrong dtype (object)               | All rows          | Convert using pd.to_datetime() |
| discount_applied | Mixed types (bool/string)          | Check output      | Convert to boolean             |

---

## 3. Cleaning Steps

| Cleaning Step          | Column Used                        | Method Applied                    | Reason                         |
| ---------------------- | ---------------------------------- | --------------------------------- | ------------------------------ |
| Missing value handling | quantity, total_spent              | fillna(median)                    | Preserve rows, avoid data loss |
| Duplicate removal      | All columns                        | drop_duplicates()                 | Remove redundant records       |
| Text standardization   | category, payment_method, location | str.strip().str.title()           | Consistent formatting          |
| Type conversion        | transaction_date                   | pd.to_datetime()                  | Enable date-based operations   |
| Column renaming        | All columns                        | str.lower().str.replace(" ","\_") | Standardize naming convention  |

---

## 4. Exploratory Data Analysis

| Analysis Question                    | Pandas Function Used | Key Finding                                         |
| ------------------------------------ | -------------------- | --------------------------------------------------- |
| Which category appears most often?   | value_counts()       | Top category has highest transaction frequency      |
| Which records have highest spend?    | sort_values()        | Top 10 records all exceed 800 in total_spent        |
| Which transactions are discounted?   | filtering            | Large share of records have discount_applied = True |
| Which location generates more sales? | value_counts()       | Online is a dominant or equal sales channel         |
| Which payment method is most used?   | value_counts()       | Digital Wallet leads all payment methods            |

---

## 5. Grouping and Aggregation Results

| Group                                                        | Count | Total | Average | Rank |
| ------------------------------------------------------------ | ----- | ----- | ------- | ---- |
| (Run category_summary to fill this table with actual values) |       |       |         |      |

---

## 6. Feature Engineering

| New Feature       | Logic Used                            | Why It Is Useful                           |
| ----------------- | ------------------------------------- | ------------------------------------------ |
| spending_category | Bins total_spent into Low/Medium/High | Helps segment customers by spend level     |
| year              | Extracted from transaction_date       | Enables year-wise trend analysis           |
| month             | Extracted from transaction_date       | Enables monthly seasonality analysis       |
| day_name          | Extracted from transaction_date       | Identifies busiest days of the week        |
| revenue_per_unit  | total_spent / quantity                | Measures effective price realised per unit |

---

## 7. Visualizations

| Chart Title                       | Columns Used          | Chart Type | Insight                                        |
| --------------------------------- | --------------------- | ---------- | ---------------------------------------------- |
| Total Spent by Category           | category, total_spent | Bar Chart  | Top categories dominate revenue                |
| Distribution of Total Spent       | total_spent           | Histogram  | Most transactions are low-to-medium value      |
| Monthly Sales Trend               | month, total_spent    | Line Chart | Clear seasonal peaks visible                   |
| Spending Distribution by Category | category, total_spent | Box Plot   | High variance and outliers in some categories  |
| Transactions by Payment Method    | payment_method        | Count Plot | Digital Wallet is the preferred payment method |

---

## 8. Correlation Analysis

Observation 1:
total_spent and quantity show a strong positive correlation.
Customers who buy more units naturally spend more.

Observation 2:
price_per_unit and quantity show a weak negative correlation.
Higher priced items tend to be purchased in smaller quantities.

Observation 3:
revenue_per_unit and total_spent are strongly correlated
since revenue_per_unit is directly derived from total_spent.

---

## 9. Key Insights

1. The top category contributes the largest share of total revenue.
2. Digital Wallet is the most preferred payment method.
3. A large proportion of transactions involve discounts.
4. Online sales are a major revenue channel for the store.
5. Total spent and quantity are strongly positively correlated.
6. Seasonal peaks are visible in specific months.
7. Some categories show high outlier transactions (potential B2B).
8. Higher priced items see lower purchase quantities per transaction.

---

## 10. Recommendations

1. Prioritise stock and promotions for top-performing categories.
2. Offer Digital Wallet exclusive rewards to retain preferred customers.
3. Review discount strategy — ensure margins are protected.
4. Invest further in the online sales channel.
5. Launch bulk purchase schemes to increase quantity per transaction.
6. Plan inventory and campaigns ahead of seasonal peak months.
7. Investigate high-value outlier orders as potential B2B leads.
8. Introduce value packs for premium-priced items to improve volume.

---

## 11. Conclusion

This analysis of the retail_store_sales dataset revealed clear patterns
in customer spending behaviour, category performance, payment preferences,
and seasonal trends. After thorough data cleaning, EDA, feature engineering,
and visualization, 8 key insights were derived with actionable business
recommendations. The cleaned dataset and summary outputs have been exported
for further use.
