# Pandas Data Analysis Report

**Dataset:** Sample Superstore (US Retail Orders 2014–2017)  
**Analyst:** Student  
**Date:** 2024

---

## 1. Dataset Overview

| Item | Value |
|---|---|
| Number of rows | 9,994 |
| Number of columns | 21 |
| File format | CSV (latin-1 encoding) |
| Numerical columns | 6 → Row ID, Postal Code, Sales, Quantity, Discount, Profit |
| Categorical columns | 15 → Order ID, Ship Mode, Customer Name, Segment, City, State, Region, Category, Sub-Category, Product Name, etc. |
| Date columns | Order Date, Ship Date |
| Date range | January 2014 – December 2017 |

The dataset contains US retail order transactions across three product categories (Furniture, Office Supplies, Technology) with four geographic regions (East, West, Central, South).

---

## 2. Data Quality Issues

| Column | Issue Found | Number of Records | Suggested Fix |
|---|---|---:|---|
| Profit | Negative values (loss-making orders) | 1,871 | Flag as `is_loss`; retain for analysis |
| Postal Code | Stored as integer — leading zeros may be lost | All | Convert to 5-character zero-padded string |
| Category | Potential inconsistent casing | 3 unique | Apply `str.strip().str.title()` |
| Discount | Checked for invalid values > 1 | 0 (none found) | No action needed |
| Quantity | Checked for zero or negative values | 0 (none found) | No action needed |

**Missing values:** None — the dataset is complete across all 9,994 rows.  
**Duplicate rows:** None detected.

---

## 3. Cleaning Steps

| Cleaning Step | Column Used | Method Applied | Reason |
|---|---|---|---|
| Missing value handling | Postal Code | `fillna(0)` then zero-pad as string | Postal codes must be 5-digit strings |
| Duplicate removal | All columns | `drop_duplicates()` | Remove any accidental duplicate rows |
| Text standardization | Category, Sub-Category, Segment, Ship Mode, Region | `str.strip().str.title()` | Ensure consistent category labels |
| Type conversion | Order Date, Ship Date | `pd.to_datetime(errors='coerce')` | Enable date arithmetic (shipping lag) |
| Column renaming | All columns | `str.lower().str.replace(' ', '_')` | Pythonic snake_case column names |

**Result:** 9,994 rows retained after cleaning (no rows dropped).

---

## 4. Exploratory Data Analysis

| Analysis Question | Pandas Function Used | Key Finding |
|---|---|---|
| Which category appears most often? | `value_counts()` | Office Supplies (6,026 orders — 60% of all orders) |
| Which segment has most customers? | `value_counts()` | Consumer segment dominates with 5,191 orders (52%) |
| Which records have the highest sales? | `sort_values()` | Top order: $22,638 (Technology — Sean Miller) |
| Loss-making orders? | Boolean filter | 1,871 orders (18.7%) have negative profit |
| Which region has the most orders? | `value_counts()` | West region leads with 3,203 orders |

### Summary Statistics (Numerical Columns)

| Metric | Sales | Profit | Discount | Quantity |
|---|---:|---:|---:|---:|
| Mean | $229.86 | $28.66 | 15.6% | 3.79 |
| Median | $54.49 | $8.67 | 20.0% | 3.00 |
| Min | $0.44 | -$6,599.98 | 0% | 1 |
| Max | $22,638.48 | $8,399.98 | 80% | 14 |

---

## 5. Grouping and Aggregation Results

### Category Summary

| Category | Orders | Total Sales | Total Profit | Profit Margin |
|---|---:|---:|---:|---:|
| Office Supplies | 6,026 | $719,047 | $122,491 | 17.0% |
| Furniture | 2,121 | $742,000 | $18,451 | 2.5% |
| Technology | 1,847 | $836,154 | $145,455 | 17.4% |

### Top 5 Sub-Categories by Sales

| Sub-Category | Total Sales | Total Profit |
|---|---:|---:|
| Phones | $330,007 | $44,516 |
| Chairs | $328,449 | $26,590 |
| Storage | $223,844 | $21,279 |
| Tables | $206,966 | **-$17,725** |
| Binders | $203,413 | $30,222 |

> ⚠️ Tables is a loss-making sub-category despite high revenue.

---

## 6. Feature Engineering

| New Feature | Logic Used | Why It Is Useful |
|---|---|---|
| `profit_margin_pct` | `(profit / sales) * 100` | Measures profitability efficiency per order |
| `revenue_tier` | `pd.cut` on sales into 4 bins (Low/Medium/High/Premium) | Segments orders by revenue size |
| `order_year`, `order_month` | `dt.year`, `dt.month` from `order_date` | Enables time-series and seasonal analysis |
| `is_loss` | `profit < 0` | Flags unprofitable orders for immediate review |
| `discount_tier` | `pd.cut` on discount into No/Low/Medium/High tiers | Studies discount impact on profitability |
| `ship_lag_days` | `ship_date - order_date` in days | Measures fulfilment speed by ship mode |

---

## 7. Visualizations

| Chart Title | Columns Used | Chart Type | Key Insight |
|---|---|---|---|
| Total Sales by Product Category | category, sales | Bar chart | Technology leads in sales despite fewer orders |
| Monthly Sales Trend by Year | order_month, order_year, sales | Multi-line chart | Q4 (Oct–Dec) consistently spikes every year |
| Top 10 Sub-Categories by Profit | sub-category, profit | Horizontal bar | Tables and Bookcases are loss-making sub-categories |
| Distribution of Order Sales | sales | Histogram | Heavily right-skewed; most orders are under $500 |
| Profit Distribution by Region | region, profit | Box plot | Central region has the most spread/volatility in profit |

---

## 8. Correlation Analysis

### Correlation Matrix (Key Pairs)

| Variable Pair | Correlation | Interpretation |
|---|---:|---|
| Sales ↔ Profit | +0.479 | Moderate positive — higher sales generally means more profit |
| Discount ↔ Profit | -0.220 | Negative — discounts erode margins |
| Quantity ↔ Sales | +0.201 | Weak positive — volume matters but price matters more |
| Discount ↔ Sales | -0.028 | Near zero — discounts do not significantly drive volume |

### Observations

**Observation 1:**  
Sales and Profit have a moderate positive correlation (~0.48). While higher-revenue orders generally produce more profit, the relationship is not linear because discounting and product mix create significant variance — a $1,000 order in Furniture may yield far less profit than a $1,000 Technology order.

**Observation 2:**  
Discount and Profit have a negative correlation (~-0.22), confirming that larger discounts consistently destroy profitability. This is especially severe in the Central region where average discounts reach 25–30%.

**Observation 3:**  
Quantity and Sales share a weak positive correlation (~0.20), indicating that many high-value orders are driven by high unit price rather than order volume. This is consistent with Technology items (e.g., Copiers, Machines) commanding high prices on low quantity.

---

## 9. Key Insights

**Insight 1:**  
*Technology drives the most revenue but Office Supplies is the volume leader.*  
Technology accounts for $836K in sales (36% of total) from only 1,847 orders. Office Supplies accounts for 60% of all orders but only 31% of revenue. Technology offers the highest revenue per order.  
→ *Prioritize upselling high-ticket Technology items to existing customers.*

---

**Insight 2:**  
*Tables sub-category is consistently loss-making (-$17,725 total).*  
Despite generating $207K in sales, Tables produce negative profit due to high discounts (average ~30%) and likely unfavourable cost structure.  
→ *Review the pricing strategy for Tables; consider reducing maximum discount depth.*

---

**Insight 3:**  
*18.7% of all orders are loss-making (1,871 orders).*  
Loss-making orders are concentrated in heavily discounted transactions. Orders with discounts above 30% are almost entirely unprofitable.  
→ *Implement a discount approval workflow for any discount > 25%.*

---

**Insight 4:**  
*Q4 (October–December) is the strongest quarter every year.*  
November consistently shows the highest monthly sales each year (~$118K in 2017), aligned with holiday and year-end procurement cycles.  
→ *Increase inventory and staffing in Q4; run targeted promotions in September to warm up the pipeline.*

---

**Insight 5:**  
*The West region generates the highest total sales ($725K) and the East region is second ($678K).*  
The South region lags significantly at $391K, despite being comparable in geography.  
→ *Investigate market penetration strategy in the South; consider targeted sales campaigns in underperforming states.*

---

**Insight 6:**  
*Furniture has a profit margin of only 2.5%, vs 17% for Technology and Office Supplies.*  
The low margin is driven by sub-categories Tables (-8.6% margin) and Bookcases (-3.0% margin), while Chairs and Furnishings remain healthy.  
→ *Consider phasing out or repricing Tables and Bookcases, or apply tighter discount caps on these sub-categories.*

---

**Insight 7:**  
*Consumer segment accounts for 52% of orders but Corporate segment delivers higher average order values.*  
Corporate average order value is ~$257, compared to ~$212 for Consumer. Home Office averages ~$222.  
→ *Develop a dedicated B2B sales programme to grow the Corporate segment's share of revenue.*

---

**Insight 8:**  
*Sales are heavily right-skewed — 11.7% of orders exceed $499 but account for a disproportionate share of total revenue.*  
The top 468 orders (>$1,000 each) collectively represent a significant revenue concentration risk.  
→ *Build customer loyalty programs targeted at high-value customers to reduce churn risk.*

---

## 10. Recommendations

1. **Discount Governance:** Cap discounts at 25% and require manager approval above 20%. The data shows that discounts above 30% almost always generate losses.

2. **Product Portfolio Review:** Discontinue or reprice the Tables sub-category. It has never been profitable in this dataset and is dragging down Furniture's overall margin.

3. **Regional Growth in South:** The South region consistently underperforms. Investigate whether this is a sales coverage issue or a product-market fit issue, and allocate resources accordingly.

4. **Q4 Preparedness:** Given the clear Q4 seasonal spike, build a demand planning model using this historical data to optimise inventory levels for October–December.

5. **Corporate Segment Expansion:** Corporate customers order at higher average values with fewer (lower) discount requests. Invest in a dedicated B2B account management team.

6. **Technology Focus:** With a 17.4% margin and growing YoY revenue, Technology is the star category. Ensure adequate stock of high-demand items like Phones, Copiers, and Accessories.

---

## 11. Conclusion

The Superstore dataset reveals a business with strong revenue growth from 2014–2017, but with a profit challenge concentrated in Furniture (particularly Tables), heavily discounted orders, and geographic imbalance. By addressing discount governance, refining the product portfolio, and targeting high-value segments, the business can materially improve overall profitability without sacrificing revenue growth.

The data is well-structured and largely clean, making it an excellent foundation for predictive modelling (e.g., profit forecasting, churn prediction, or demand planning) as a next step.

