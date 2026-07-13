# RFM Analysis for Customer Segmentation

## 1. Introduction

**RFM analysis** is a customer segmentation technique used to group customers based on their purchasing behaviour.

RFM stands for:

* **R — Recency:** How recently the customer made a purchase
* **F — Frequency:** How often the customer makes purchases
* **M — Monetary Value:** How much money the customer spends

RFM analysis helps businesses identify:

* High-value customers
* Loyal customers
* New customers
* At-risk customers
* Inactive customers
* Customers who may respond to promotions

---

# 2. Recency

## Definition

Recency measures how many days have passed since the customer’s most recent purchase.

```text
Recency = Reference Date - Last Purchase Date
```

A lower recency value is generally better because it indicates that the customer purchased recently.

## Example

Assume the reference date is `31 December 2025`.

| Customer   | Last Purchase Date |  Recency |
| ---------- | ------------------ | -------: |
| Customer A | 28 December 2025   |   3 days |
| Customer B | 1 December 2025    |  30 days |
| Customer C | 1 June 2025        | 213 days |

## Interpretation

* Customer A purchased recently and is highly active.
* Customer B has moderate recent activity.
* Customer C has not purchased for a long time and may be inactive.

## Business Importance

Customers with low recency values are generally:

* More engaged
* More likely to purchase again
* More likely to respond to offers

Customers with high recency values may require:

* Re-engagement campaigns
* Comeback offers
* Personalized reminders
* Customer feedback surveys

---

# 3. Frequency

## Definition

Frequency measures how many purchases a customer made during a selected period.

```text
Frequency = Number of Unique Orders
```

A higher frequency value is generally better because it indicates repeated purchasing behaviour.

## Example

| Customer   | Number of Orders |
| ---------- | ---------------: |
| Customer A |               15 |
| Customer B |                6 |
| Customer C |                1 |

## Important Consideration

Frequency should usually count unique orders, not individual product rows.

For example:

| Order ID | Customer ID | Product  |
| -------- | ----------- | -------- |
| O101     | C001        | Laptop   |
| O101     | C001        | Mouse    |
| O101     | C001        | Keyboard |

Although the order contains three products, it represents only one purchase.

Therefore:

```text
Frequency = 1
```

## Business Importance

High-frequency customers may be:

* Loyal customers
* Repeat buyers
* Subscription customers
* Strong candidates for loyalty programs

Low-frequency customers may be:

* First-time buyers
* Occasional buyers
* Customers who need additional encouragement

---

# 4. Monetary Value

## Definition

Monetary value measures the total amount spent by a customer during the selected period.

```text
Monetary Value = Sum of Purchase Amounts
```

A higher monetary value generally indicates that the customer contributes more revenue.

## Example

| Customer   | Total Spending |
| ---------- | -------------: |
| Customer A |        ₹80,000 |
| Customer B |        ₹25,000 |
| Customer C |         ₹2,500 |

## Monetary Value Can Represent

Depending on the business requirement, monetary value may represent:

* Total revenue
* Net revenue
* Total profit
* Average order value
* Customer lifetime value
* Revenue after refunds and returns

## Business Importance

High monetary-value customers may receive:

* Premium offers
* Loyalty benefits
* Personalized support
* Cross-selling recommendations
* Upselling opportunities

However, high revenue does not always mean high profit.

A customer who purchases only during heavy discounts may generate less profit than another customer with lower total spending.

---

# 5. Example RFM Calculation

Assume the transaction dataset contains the following records:

| Customer ID | Order ID | Order Date | Amount |
| ----------- | -------- | ---------- | -----: |
| C001        | O101     | 2025-12-20 | ₹2,000 |
| C001        | O105     | 2025-12-28 | ₹3,000 |
| C002        | O110     | 2025-11-10 | ₹1,500 |
| C002        | O115     | 2025-12-01 | ₹2,500 |
| C003        | O120     | 2025-06-15 | ₹8,000 |

Using `31 December 2025` as the reference date:

| Customer |  Recency | Frequency | Monetary |
| -------- | -------: | --------: | -------: |
| C001     |   3 days |         2 |   ₹5,000 |
| C002     |  30 days |         2 |   ₹4,000 |
| C003     | 199 days |         1 |   ₹8,000 |

## Interpretation

### Customer C001

* Purchased recently
* Made two purchases
* Spent ₹5,000
* May be an active and promising customer

### Customer C002

* Made two purchases
* Has not purchased as recently as C001
* May require a reminder or promotional offer

### Customer C003

* Has the highest spending
* Has not purchased for a long time
* May be a high-value customer at risk

This example shows why all three RFM values must be considered together.

Monetary value alone would make C003 appear to be the best customer, but the recency value shows that the customer may be inactive.

---

# 6. RFM Scoring

After calculating the raw RFM values, each customer can be assigned an RFM score.

A common approach is to score each dimension from `1` to `5`.

| Score | Meaning                        |
| ----: | ------------------------------ |
|     5 | Best-performing customer group |
|     4 | Above-average group            |
|     3 | Average group                  |
|     2 | Below-average group            |
|     1 | Lowest-performing group        |

---

# 7. Recency Score

For recency, lower values receive higher scores.

| Recency Category            | Recency Score |
| --------------------------- | ------------: |
| Most recent customers       |             5 |
| Recent customers            |             4 |
| Moderately recent customers |             3 |
| Inactive customers          |             2 |
| Long-inactive customers     |             1 |

Example:

```text
Customer purchased 3 days ago → Recency Score = 5
Customer purchased 200 days ago → Recency Score = 1
```

---

# 8. Frequency Score

For frequency, higher values receive higher scores.

| Purchase Behaviour  | Frequency Score |
| ------------------- | --------------: |
| Very frequent buyer |               5 |
| Frequent buyer      |               4 |
| Moderate buyer      |               3 |
| Occasional buyer    |               2 |
| One-time buyer      |               1 |

Example:

```text
Customer made 20 purchases → Frequency Score = 5
Customer made 1 purchase → Frequency Score = 1
```

---

# 9. Monetary Score

For monetary value, higher spending receives higher scores.

| Spending Category      | Monetary Score |
| ---------------------- | -------------: |
| Highest-spending group |              5 |
| High-spending group    |              4 |
| Medium-spending group  |              3 |
| Low-spending group     |              2 |
| Lowest-spending group  |              1 |

Example:

```text
Customer spent ₹90,000 → Monetary Score = 5
Customer spent ₹1,500 → Monetary Score = 1
```

---

# 10. Combined RFM Score

The three scores can be combined into a three-digit RFM code.

Example:

```text
Recency Score = 5
Frequency Score = 4
Monetary Score = 5

RFM Score = 545
```

The score `545` means:

* The customer purchased very recently.
* The customer purchases frequently.
* The customer spends a high amount.

Another example:

```text
RFM Score = 155
```

This means:

* The customer has not purchased recently.
* The customer previously purchased frequently.
* The customer previously spent a high amount.

This customer may be a high-value customer at risk.

## Why RFM Scores Should Not Always Be Added

Consider:

```text
5 + 4 + 5 = 14
```

The total score `14` does not clearly show which dimension received which value.

The code `545` is more informative because it preserves the individual recency, frequency, and monetary scores.

---

# 11. Assigning Scores Using Quantiles

Customers can be divided into groups using quantiles.

Common approaches include:

* Quartiles: scores from 1 to 4
* Quintiles: scores from 1 to 5

With quintiles, customers are divided into five groups:

* Lowest 20%
* Next 20%
* Middle 20%
* Next 20%
* Highest 20%

## Recency Scoring

Recency scoring is reversed because lower recency values are better.

```python
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q=5,
    labels=[5, 4, 3, 2, 1]
)
```

## Frequency Scoring

Higher frequency receives a higher score.

```python
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
)
```

## Monetary Scoring

Higher spending receives a higher score.

```python
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    q=5,
    labels=[1, 2, 3, 4, 5]
)
```

The `rank()` method is useful for frequency because many customers may have the same number of purchases.

For example, many customers may have only one purchase, which can cause duplicate-bin errors in `qcut()`.

---

# 12. Common RFM Customer Segments

## 12.1 Champions

Typical score:

```text
R = 5
F = 5
M = 5
```

### Characteristics

* Purchased very recently
* Purchase very frequently
* Spend a high amount
* Highly engaged with the business

### Recommended Actions

* Offer VIP benefits.
* Provide early access to products.
* Reward them through loyalty programs.
* Ask for reviews and referrals.
* Avoid unnecessary heavy discounts.

---

## 12.2 Loyal Customers

Typical pattern:

```text
High Frequency
High Monetary Value
Moderate or High Recency
```

### Characteristics

* Purchase repeatedly
* Generate consistent revenue
* Show strong loyalty

### Recommended Actions

* Offer loyalty rewards.
* Recommend complementary products.
* Provide personalized offers.
* Use cross-selling and upselling strategies.

---

## 12.3 Potential Loyalists

Typical pattern:

```text
High Recency
Medium Frequency
Medium Monetary Value
```

### Characteristics

* Purchased recently
* Made more than one purchase
* Have the potential to become loyal customers

### Recommended Actions

* Encourage the next purchase.
* Offer loyalty-program registration.
* Send personalized recommendations.
* Provide onboarding content.

---

## 12.4 New Customers

Typical pattern:

```text
High Recency
Low Frequency
Low or Medium Monetary Value
```

### Characteristics

* Purchased recently
* Have only one or very few purchases
* Are still developing a relationship with the business

### Recommended Actions

* Send welcome messages.
* Provide product guidance.
* Offer a second-purchase incentive.
* Recommend popular products.
* Avoid sending too many promotions immediately.

---

## 12.5 Promising Customers

### Characteristics

* Recent customer activity
* Moderate or low spending
* Potential for increased engagement

### Recommended Actions

* Recommend affordable products.
* Offer limited-time promotions.
* Promote related items.
* Encourage repeat purchases.

---

## 12.6 Customers Needing Attention

Typical pattern:

```text
Medium Recency
Medium Frequency
Medium Monetary Value
```

### Characteristics

* Previously active
* Engagement is beginning to decline
* May become inactive without intervention

### Recommended Actions

* Send personalized reminders.
* Recommend relevant products.
* Provide limited-time offers.
* Request feedback.

---

## 12.7 At-Risk Customers

Typical pattern:

```text
Low Recency Score
High Frequency Score
High Monetary Score
```

### Characteristics

* Previously purchased frequently
* Previously spent a high amount
* Have not purchased recently

### Recommended Actions

* Run re-engagement campaigns.
* Provide personalized comeback offers.
* Contact them through customer support.
* Ask why they stopped purchasing.
* Highlight new products or services.

These customers are important because the business may lose customers who previously generated significant value.

---

## 12.8 Cannot-Lose Customers

### Characteristics

* Very high historical spending
* Very high historical purchase frequency
* Long period of inactivity

### Recommended Actions

* Contact them directly.
* Provide special retention offers.
* Offer priority customer service.
* Review their purchase history individually.
* Provide highly personalized recommendations.

---

## 12.9 Hibernating Customers

### Characteristics

* Long time since the last purchase
* Low or moderate purchase frequency
* Low or moderate spending

### Recommended Actions

* Use low-cost email campaigns.
* Send product updates.
* Provide a limited comeback discount.
* Avoid expensive advertising campaigns.

---

## 12.10 Lost Customers

Typical score:

```text
R = 1
F = 1
M = 1
```

### Characteristics

* Have not purchased for a long time
* Purchased infrequently
* Spent very little

### Recommended Actions

* Use only low-cost reactivation campaigns.
* Send one final promotional offer.
* Remove them from expensive campaigns if they remain inactive.
* Focus marketing resources on more valuable segments.

---

# 13. Complete Python Example

```python
import pandas as pd

# Load transaction data
df = pd.read_csv("transactions.csv")

# Convert OrderDate into datetime format
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# Remove transactions with invalid amounts
df = df[df["Amount"] > 0]

# Select a reference date
reference_date = df["OrderDate"].max() + pd.Timedelta(days=1)

# Calculate Recency, Frequency, and Monetary values
rfm = (
    df.groupby("CustomerID")
      .agg(
          Recency=(
              "OrderDate",
              lambda dates: (reference_date - dates.max()).days
          ),
          Frequency=("OrderID", "nunique"),
          Monetary=("Amount", "sum")
      )
      .reset_index()
)

# Assign Recency score
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    q=5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

# Assign Frequency score
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Assign Monetary score
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    q=5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Create combined RFM code
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

print(rfm.head())
```

---

# 14. Example Output

| Customer ID | Recency | Frequency | Monetary | R Score | F Score | M Score | RFM Score |
| ----------- | ------: | --------: | -------: | ------: | ------: | ------: | --------- |
| C001        |       5 |        12 |  ₹45,000 |       5 |       5 |       5 | 555       |
| C002        |      20 |         6 |  ₹18,000 |       4 |       4 |       4 | 444       |
| C003        |     160 |         9 |  ₹38,000 |       1 |       5 |       5 | 155       |
| C004        |       4 |         1 |   ₹2,000 |       5 |       1 |       1 | 511       |

## Interpretation

* **C001:** Champion
* **C002:** Loyal customer
* **C003:** High-value customer at risk
* **C004:** New customer

---

# 15. Assigning Segment Names

```python
def assign_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champion"

    if r >= 3 and f >= 4:
        return "Loyal Customer"

    if r >= 4 and f <= 2:
        return "New Customer"

    if r <= 2 and f >= 4 and m >= 4:
        return "At-Risk High-Value Customer"

    if r <= 2 and f <= 2:
        return "Lost Customer"

    if r == 3:
        return "Needs Attention"

    return "Potential Customer"


rfm["Segment"] = rfm.apply(assign_segment, axis=1)

print(rfm[[
    "CustomerID",
    "RFM_Score",
    "Segment"
]])
```

The segmentation rules should be customized based on:

* Business type
* Customer purchase cycle
* Product price
* Marketing objectives
* Customer lifetime
* Industry characteristics

---

# 16. RFM with K-Means Clustering

RFM scoring is rule-based.

K-Means clustering can also be applied to the three RFM features:

```text
Recency
Frequency
Monetary
```

Because the three values use different scales, they should be standardized before clustering.

## Example

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

features = rfm[[
    "Recency",
    "Frequency",
    "Monetary"
]]

scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)

model = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["Cluster"] = model.fit_predict(scaled_features)
```

---

# 17. Summarizing the Clusters

```python
cluster_summary = (
    rfm.groupby("Cluster")
       .agg(
           CustomerCount=("CustomerID", "count"),
           AverageRecency=("Recency", "mean"),
           AverageFrequency=("Frequency", "mean"),
           AverageMonetary=("Monetary", "mean")
       )
       .round(2)
)

print(cluster_summary)
```

## Example Cluster Summary

| Cluster | Customer Count | Average Recency | Average Frequency | Average Monetary |
| ------: | -------------: | --------------: | ----------------: | ---------------: |
|       0 |            500 |              18 |                12 |          ₹35,000 |
|       1 |            850 |             145 |                 2 |           ₹4,500 |
|       2 |            300 |              95 |                15 |          ₹42,000 |
|       3 |            600 |              22 |                 3 |           ₹7,000 |

## Possible Interpretation

* **Cluster 0:** Loyal high-value customers
* **Cluster 1:** Inactive low-value customers
* **Cluster 2:** High-value customers at risk
* **Cluster 3:** Recent and promising customers

K-Means cluster numbers do not automatically carry business meaning.

The cluster names must be assigned after reviewing the average recency, frequency, and monetary values.

---

# 18. RFM Scoring vs K-Means

| Aspect             | RFM Scoring                     | K-Means Clustering                |
| ------------------ | ------------------------------- | --------------------------------- |
| Approach           | Rule-based                      | Machine-learning-based            |
| Interpretation     | Easy to understand              | Requires cluster analysis         |
| Number of segments | Defined through business rules  | Selected using evaluation methods |
| Scaling required   | Usually not required            | Required                          |
| Flexibility        | Highly customizable             | Data-driven                       |
| Best use case      | Marketing reports and campaigns | Behaviour-based segmentation      |
| Output             | RFM scores and segment names    | Cluster labels                    |

---

# 19. Combining RFM and K-Means

RFM and K-Means can be used together.

Recommended process:

1. Calculate recency, frequency, and monetary values.
2. Perform exploratory data analysis.
3. Handle outliers.
4. Scale the RFM values.
5. Use K-Means to create clusters.
6. Compare multiple values of `k`.
7. Evaluate clusters using the silhouette score.
8. Profile every cluster.
9. Use RFM scores to interpret the clusters.
10. Assign meaningful business names.
11. Recommend actions for each segment.

---

# 20. Important Data Preparation Rules

## Remove Cancelled Orders

Cancelled transactions should not increase purchase frequency or spending.

## Handle Returns and Refunds

Use net spending where possible.

```text
Net Monetary Value = Purchases - Returns - Refunds
```

## Count Unique Orders

Frequency should count unique order IDs.

```python
Frequency=("OrderID", "nunique")
```

## Handle Missing Customer IDs

Transactions without a valid customer ID should normally be removed because they cannot be assigned to a customer segment.

## Remove Test and Internal Accounts

Exclude:

* Test accounts
* Employee accounts
* Internal orders
* Fraudulent transactions
* Duplicate transactions

## Select a Suitable Analysis Period

Possible analysis periods include:

* Last 3 months
* Last 6 months
* Last 12 months
* Last 24 months

The selected period should match the business purchase cycle.

For example:

* A grocery customer inactive for 60 days may be at risk.
* A car customer inactive for 60 days may be completely normal.

## Choose the Reference Date Carefully

The reference date can be:

* One day after the latest transaction
* The reporting date
* The end of the financial period
* The end of the campaign period

Example:

```python
reference_date = df["OrderDate"].max() + pd.Timedelta(days=1)
```

---

# 21. Handling Outliers

RFM data often contains extreme values.

Examples include:

* One customer with extremely high spending
* Wholesale customers mixed with retail customers
* Customers with hundreds of transactions
* Invalid negative transaction values

Outliers can strongly influence K-Means clustering because K-Means uses distances.

Possible approaches include:

* Removing invalid records
* Capping extreme values
* Applying logarithmic transformation
* Using percentile-based limits
* Separating wholesale and retail customers

## Log Transformation Example

```python
import numpy as np

rfm["Frequency_Log"] = np.log1p(rfm["Frequency"])
rfm["Monetary_Log"] = np.log1p(rfm["Monetary"])
rfm["Recency_Log"] = np.log1p(rfm["Recency"])
```

---

# 22. Limitations of RFM Analysis

RFM is useful, but it does not include every customer characteristic.

RFM does not directly consider:

* Customer age
* Customer location
* Product preferences
* Profit margin
* Website activity
* Email engagement
* Customer satisfaction
* Return behaviour
* Complaints
* Product reviews
* Reasons for inactivity
* Future purchase intention

RFM also depends on:

* The selected analysis period
* The selected reference date
* The scoring rules
* The company’s purchase cycle
* The quality of transaction data

---

# 23. Additional Features for Better Segmentation

RFM can be combined with additional features such as:

* Average order value
* Product-category preference
* Discount usage
* Website visits
* Number of returned orders
* Customer ratings
* Profit contribution
* Customer lifetime value
* Churn probability
* Purchase likelihood
* Customer tenure
* Number of products purchased
* Email campaign response

---

# 24. Business Actions by Segment

| Segment                     | Business Objective         | Recommended Action                    |
| --------------------------- | -------------------------- | ------------------------------------- |
| Champions                   | Retain and reward          | VIP benefits and early product access |
| Loyal Customers             | Increase customer value    | Cross-sell and upsell                 |
| Potential Loyalists         | Build loyalty              | Personalized recommendations          |
| New Customers               | Encourage second purchase  | Welcome campaign                      |
| Promising Customers         | Increase engagement        | Relevant limited-time offers          |
| Customers Needing Attention | Prevent inactivity         | Personalized reminders                |
| At-Risk Customers           | Prevent customer loss      | Re-engagement campaign                |
| Cannot-Lose Customers       | Recover valuable customers | Direct personalized contact           |
| Hibernating Customers       | Test reactivation          | Low-cost comeback campaign            |
| Lost Customers              | Reduce marketing cost      | Exclude from expensive campaigns      |

---

# 25. Expected Project Deliverables

Students should submit:

## 1. RFM Dataset

The final dataset should contain:

* Customer ID
* Recency
* Frequency
* Monetary value
* Recency score
* Frequency score
* Monetary score
* Combined RFM score
* Segment name

## 2. Exploratory Data Analysis

Include:

* Recency distribution
* Frequency distribution
* Monetary-value distribution
* Outlier analysis
* Correlation analysis
* Customer-count analysis

## 3. Customer Segment Summary

For every segment, show:

* Number of customers
* Average recency
* Average frequency
* Average monetary value
* Revenue contribution
* Recommended business action

## 4. Visualizations

Recommended visualizations include:

* Recency histogram
* Frequency histogram
* Monetary-value histogram
* RFM scatter plot
* Segment-wise customer count
* Segment-wise revenue
* Cluster visualization
* Segment comparison chart

## 5. Business Insight Report

The report should explain:

* Which segment produces the most revenue
* Which customers are at risk
* Which customers should receive rewards
* Which customers should receive discounts
* Which customers should receive re-engagement messages
* Which customers should be excluded from expensive campaigns

---

# 26. Final Outcome

At the end of the RFM analysis, students should be able to:

* Calculate recency, frequency, and monetary values
* Assign RFM scores
* Create meaningful customer segments
* Apply K-Means clustering to RFM data
* Interpret customer behaviour
* Identify valuable and at-risk customers
* Recommend marketing actions
* Convert transaction data into actionable business insights
