# Customer Segmentation - Business Recommendations Report
> Generated automatically from K-Means clustering results.

---

## Executive Summary

| Cluster | Segment | Customers | Avg Spending | Revenue % | Avg Rating |
|---------|---------|-----------|-------------|-----------|------------|
| 0 | ⚠️ At-Risk Customers | 204 | $4,429 | 13.1% | 4.32 |
| 1 | 🏷️ Discount-Driven Customers | 216 | $4,590 | 14.4% | 4.12 |
| 2 | 👑 High-Value Loyal Customers | 223 | $14,496 | 46.9% | 3.78 |
| 3 | ⚠️ At-Risk Customers (Group 3) | 168 | $8,575 | 20.9% | 3.17 |
| 4 | 🏷️ Discount-Driven Customers (Group 4) | 189 | $1,717 | 4.7% | 3.22 |

---

## Segment Profiles & Recommendations

### ⚠️ Cluster 0: At-Risk Customers

**Description:** Previously active customers with increasing days since last purchase, declining engagement, but moderate/high historical spending.

#### Key Characteristics

| Metric | Value |
|--------|-------|
| Number of Customers | 204 |
| Average Total Spending | $4,429.19 |
| Average Purchase Frequency | 13.8 |
| Avg Days Since Last Purchase | 204.6 days |
| Average Customer Rating | 4.32 / 5.0 |
| Avg Discount Usage | 48.0% |
| Revenue Contribution | 13.1% |
| Total Revenue | $903,555 |

#### Recommended Actions

1. Run automated re-engagement email campaigns ('We miss you' series).
2. Offer a personalised come-back incentive based on purchase history.
3. Request feedback on what caused them to stop - exit survey.
4. Highlight new arrivals or improvements since their last visit.
5. Set a 60-day win-back window; if no purchase, consider lower-cost channel.

**Target KPI:** Reactivate at least 20% of at-risk customers within 60 days.

---

### 🏷️ Cluster 1: Discount-Driven Customers

**Description:** Customers who primarily purchase during promotions, with high discount usage and moderate purchase frequency.

#### Key Characteristics

| Metric | Value |
|--------|-------|
| Number of Customers | 216 |
| Average Total Spending | $4,590.28 |
| Average Purchase Frequency | 35.0 |
| Avg Days Since Last Purchase | 158.3 days |
| Average Customer Rating | 4.12 / 5.0 |
| Avg Discount Usage | 55.0% |
| Revenue Contribution | 14.4% |
| Total Revenue | $991,500 |

#### Recommended Actions

1. Send targeted limited-time promotional offers and flash sales.
2. Bundle products to increase basket size while maintaining perceived value.
3. Gradually reduce discount depth over time to improve margins.
4. Avoid giving unnecessary discounts outside campaign periods.
5. Test value-based messaging (quality, features) to reduce price sensitivity.

**Target KPI:** Improve margin per order while sustaining purchase frequency.

---

### 👑 Cluster 2: High-Value Loyal Customers

**Description:** Customers with high purchase frequency, high total spending, recent purchases, and high average order value.

#### Key Characteristics

| Metric | Value |
|--------|-------|
| Number of Customers | 223 |
| Average Total Spending | $14,495.86 |
| Average Purchase Frequency | 39.2 |
| Avg Days Since Last Purchase | 159.3 days |
| Average Customer Rating | 3.78 / 5.0 |
| Avg Discount Usage | 50.0% |
| Revenue Contribution | 46.9% |
| Total Revenue | $3,232,576 |

#### Recommended Actions

1. Offer exclusive loyalty rewards and VIP membership benefits.
2. Provide early access to new product launches.
3. Send personalised thank-you campaigns to reinforce brand loyalty.
4. Avoid over-discounting - these customers already show strong purchase intent.
5. Upsell premium or complementary products to increase lifetime value.

**Target KPI:** Increase repeat purchase rate and average order value.

---

### ⚠️ Cluster 3: At-Risk Customers (Group 3)

**Description:** Previously active customers with increasing days since last purchase, declining engagement, but moderate/high historical spending.

#### Key Characteristics

| Metric | Value |
|--------|-------|
| Number of Customers | 168 |
| Average Total Spending | $8,574.52 |
| Average Purchase Frequency | 27.6 |
| Avg Days Since Last Purchase | 234.9 days |
| Average Customer Rating | 3.17 / 5.0 |
| Avg Discount Usage | 40.0% |
| Revenue Contribution | 20.9% |
| Total Revenue | $1,440,519 |

#### Recommended Actions

1. Run automated re-engagement email campaigns ('We miss you' series).
2. Offer a personalised come-back incentive based on purchase history.
3. Request feedback on what caused them to stop - exit survey.
4. Highlight new arrivals or improvements since their last visit.
5. Set a 60-day win-back window; if no purchase, consider lower-cost channel.

**Target KPI:** Reactivate at least 20% of at-risk customers within 60 days.

---

### 🏷️ Cluster 4: Discount-Driven Customers (Group 4)

**Description:** Customers who primarily purchase during promotions, with high discount usage and moderate purchase frequency.

#### Key Characteristics

| Metric | Value |
|--------|-------|
| Number of Customers | 189 |
| Average Total Spending | $1,716.95 |
| Average Purchase Frequency | 12.7 |
| Avg Days Since Last Purchase | 179.0 days |
| Average Customer Rating | 3.22 / 5.0 |
| Avg Discount Usage | 57.0% |
| Revenue Contribution | 4.7% |
| Total Revenue | $324,503 |

#### Recommended Actions

1. Send targeted limited-time promotional offers and flash sales.
2. Bundle products to increase basket size while maintaining perceived value.
3. Gradually reduce discount depth over time to improve margins.
4. Avoid giving unnecessary discounts outside campaign periods.
5. Test value-based messaging (quality, features) to reduce price sensitivity.

**Target KPI:** Improve margin per order while sustaining purchase frequency.

---

## Key Business Insights

- 💰 **Highest Revenue Segment:** 👑 High-Value Loyal Customers contributing **46.9%** of total revenue. Prioritise loyalty programmes for this group.
- 🔁 **Most Recent Buyers:** 🏷️ Discount-Driven Customers purchased on average **158 days** ago - great target for cross-sell campaigns.
- ⚠️ **Highest Churn Risk:** ⚠️ At-Risk Customers (Group 3) with **235 days** since last purchase - activate re-engagement campaigns immediately.
- 🏷️ **Most Discount-Sensitive:** 🏷️ Discount-Driven Customers (Group 4) uses discounts in **57.0%** of purchases - use targeted promotions but protect margins.

---
*Report generated by the Customer Segmentation ML Pipeline.*
