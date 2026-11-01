# Pandas Data Analysis Report

## 1. Dataset Overview
- Dataset: Sample Superstore Sales
- Rows: 9,994 | Columns: 21
- Format: CSV
- Numerical columns: Sales, Quantity, Discount, Profit
- Categorical columns: Category, Region, Segment, Sub-Category
- Date columns: Order Date, Ship Date

## 2. Data Quality Issues
- No missing values found in this dataset
- No duplicate rows found
- Discount values range 0–0.8 (some orders heavily discounted)
- Some orders have negative profit (loss-making)

## 3. Cleaning Steps
| Step | Column | Method | Reason |
|---|---|---|---|
| Type conversion | Order Date, Ship Date | pd.to_datetime() | Enable date operations |
| Column renaming | All columns | str.lower().str.replace() | Consistent naming |
| No missing value handling needed | — | — | Dataset was clean |

## 4. Exploratory Data Analysis
- Office Supplies is the most ordered category
- West region has the highest number of orders
- Consumer segment dominates with ~52% of orders
- 5,909 high-discount orders (>=30%) risk reducing profit

## 5. Grouping and Aggregation Results
- Technology has the highest total sales despite fewer orders
- Furniture has the lowest profit margin across all regions
- West + Technology combination generates highest average sales

## 6. Feature Engineering
| New Feature | Logic | Why Useful |
|---|---|---|
| sales_category | High/Medium/Low based on sales value | Segment orders by value |
| order_year | Extracted from order_date | Year-wise trend analysis |
| order_month | Extracted from order_date | Monthly seasonality |
| profit_margin | profit / sales | Efficiency per order |

## 7. Visualizations
| Chart | Columns Used | Type | Insight |
|---|---|---|---|
| Top 10 Sub-Categories by Sales | sub_category, sales | Bar | Phones and Chairs lead |
| Distribution of Sales | sales | Histogram | Most orders are under $500 |
| Monthly Sales Trend | order_date, sales | Line | Sales peak in Nov-Dec |

## 8. Correlation Analysis
- Sales and Profit: moderate positive correlation (~0.48)
- Discount and Profit: negative correlation (~-0.22) — discounts hurt profit
- Quantity and Sales: weak positive correlation

## 9. Key Insights
1. Technology has the highest total sales — it is the top revenue driver.
2. Discounts negatively impact profit — higher discounts lead to lower or negative profit.
3. Furniture has the lowest profit margin — Tables and Bookcases are often sold at a loss.
4. 5,909 orders have discounts above 30% — too many heavily discounted orders.
5. Sales peak in November and December — strong holiday season trend.
6. West region leads in order volume — it is the strongest performing region.
7. Most orders are below $500 in value — business depends on high volume of small orders.
8. Consumer segment makes up ~52% of orders — B2C dominates over corporate buyers.

## 10. Recommendations
1. Reduce discounts on Furniture — they are eroding margins.
2. Focus marketing on Technology in the West region.
3. Plan Q4 inventory well in advance for holiday sales spike.
4. Introduce minimum order value thresholds to improve average sales.

## 11. Conclusion
The Superstore dataset reveals a business heavily dependent on the Consumer segment
and Technology category. While sales volumes are healthy, profitability is being
undermined by aggressive discounting — particularly in Furniture. Seasonal trends
are strong, offering clear windows for targeted campaigns.
