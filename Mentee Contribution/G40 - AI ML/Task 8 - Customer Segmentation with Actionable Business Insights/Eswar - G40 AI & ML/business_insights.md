# Business Insights & Recommendations — Customer Segmentation

## Overview

Five customer segments were identified using K-Means clustering (k=5, chosen via the elbow method and confirmed with a silhouette score of **0.458**) on Recency, Frequency, Monetary value, Average Order Value, Website Visits, Discount Usage, and Customer Rating.

## Segment Summary

| Segment | Customers | Revenue Share | Avg. Recency (days) | Avg. Frequency | Avg. Spending | Avg. Discount Use | Avg. Rating |
|---|---|---|---|---|---|---|---|
| High-Value Loyal | 220 | 46.4% | 9.7 | 26.4 | $5,836 | 7.8% | 4.48 |
| At-Risk | 227 | 26.4% | 147.1 | 14.2 | $3,226 | 25.2% | 3.37 |
| Discount-Driven | 240 | 14.6% | 25.8 | 11.9 | $1,684 | 60.5% | 3.63 |
| New & Promising | 260 | 8.7% | 12.8 | 4.9 | $925 | 17.3% | 4.18 |
| Low-Engagement | 253 | 3.9% | 119.3 | 3.1 | $425 | 12.7% | 3.15 |

## Segment-by-Segment Recommendations

### 1. High-Value Loyal (220 customers, 46.4% of revenue)
Nearly half of all revenue comes from this group, despite being the smallest segment by count. They buy frequently, spend the most per order, and rarely rely on discounts.
- Launch a loyalty rewards tier with early access to new products.
- Avoid broad discounting — it erodes margin without changing behavior for a segment that's already converting.
- Introduce premium/VIP membership perks to increase retention further.

### 2. At-Risk (227 customers, 26.4% of revenue)
This segment has meaningful historical spend (second-highest average order value and lifetime spend) but hasn't purchased in an average of **147 days** — the longest gap of any high-value group.
- Highest priority for a win-back campaign: this segment represents over a quarter of total revenue and is actively drifting away.
- Send personalized comeback incentives referencing past purchase categories.
- Request feedback to diagnose why engagement dropped before offering blanket discounts.

### 3. Discount-Driven (240 customers, 14.6% of revenue)
This group has the highest discount usage (60.5%) by a wide margin, moderate purchase frequency, and the lowest average order value among active buyers.
- Use targeted, time-limited promotions rather than continuous discounting to protect margin.
- Recommend bundled products to increase order value without deepening discounts.
- Avoid unprompted discount offers outside of campaign windows — this segment already seeks out deals.

### 4. New & Promising (260 customers, 8.7% of revenue)
The largest segment by customer count, with very recent activity (avg. 12.8 days since last purchase) but still low frequency and spend — consistent with recently acquired customers.
- Provide onboarding offers and personalized welcome campaigns to encourage a second purchase.
- Recommend popular, well-reviewed products to build trust early.
- Track conversion of this segment into "High-Value Loyal" over time as a growth KPI.

### 5. Low-Engagement (253 customers, 3.9% of revenue)
The lowest-value segment across every metric — long recency, lowest frequency, lowest spend, and the lowest average rating.
- Use low-cost email campaigns rather than expensive advertising.
- Promote entry-level or low-price-point products.
- Periodically reassess whether continued investment in this segment is cost-effective relative to its revenue contribution.

## Supporting Model Results

**Regression (predicting Customer Rating):**
- Ridge Regression (tuned via GridSearchCV): R² ≈ 0.61 on held-out test data.
- Best predictors of rating: purchase frequency, recency, and website engagement.

**Classification (predicting whether a customer will purchase again):**
- Logistic Regression: F1-score ≈ 0.95, ROC-AUC strong on held-out test data.
- This model can be used to score the customer base and prioritize marketing spend toward customers most likely to convert, rather than targeting broadly.

## Overall Business Value

- **Retention over acquisition**: High-Value Loyal and At-Risk together account for ~73% of revenue — retention campaigns aimed at these two groups will have outsized impact compared to broad acquisition spend.
- **Right-sized marketing spend**: The purchase-likelihood classifier lets the marketing team avoid spending on Low-Engagement customers who are statistically unlikely to convert, while doubling down on New & Promising customers showing early positive signals.
- **Discount strategy correction**: Nearly all discount usage is concentrated in one segment (Discount-Driven) that already has the lowest average order value — this suggests current blanket discounting may be subsidizing customers who would buy anyway at a lower price point, and a bundling strategy is likely more profitable than further discounts.
