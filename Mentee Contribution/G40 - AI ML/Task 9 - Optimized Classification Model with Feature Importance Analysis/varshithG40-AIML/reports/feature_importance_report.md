# Feature Importance Report

## Top 10 Most Important Features

Based on the optimized LogisticRegression model:

| Rank | Feature | Importance | Direction | Business Interpretation |
|------|---------|------------|-----------|-------------------------|
| 1 | CartItems | 0.1895 | Positive (+) | More items in cart strongly indicates purchase intent |
| 2 | TimeOnSite | 0.1396 | Positive (+) | Longer engagement correlates with higher purchase likelihood |
| 3 | DiscountUsed | 0.1281 | Positive (+) | Discount sensitivity drives purchase decisions |
| 4 | EmailClicked | 0.1254 | Positive (+) | Email engagement shows active customer interest |
| 5 | PreviousPurchases | 0.1038 | Positive (+) | Repeat customers are more likely to purchase again |
| 6 | ProductsViewed | 0.0499 | Positive (+) | More product browsing indicates serious interest |
| 7 | PagesViewed | 0.0405 | Positive (+) | More page views indicate deeper engagement |
| 8 | DaysSinceLastVisit | 0.0324 | Negative (-) | Recent visitors are more likely to purchase |
| 9 | TrafficSource_Direct | 0.0238 | Negative (-) | Contributes to purchase prediction |
| 10 | TrafficSource_Email | 0.0205 | Positive (+) | Contributes to purchase prediction |


## Key Insights

1. **Cart and Engagement Metrics Dominate**: Cart items, time on site, and products viewed are the strongest predictors
2. **Customer History Matters**: Previous purchases and session count indicate loyal, likely-to-buy customers
3. **Marketing Touchpoints**: Email clicks and discount usage show responsive customers
4. **Recency Effect**: Days since last visit negatively impacts purchase probability

## Recommended Actions

1. **Cart Recovery**: Implement abandoned cart emails for customers with high cart items
2. **Engagement Incentives**: Reward longer browsing sessions with personalized offers
3. **Loyalty Programs**: Focus on repeat customers (high previous purchases)
4. **Email Marketing**: Increase email campaign frequency for engaged users
5. **Win-Back Campaigns**: Target customers with long absence (high days since last visit)

Generated from the optimized model with F1-score of 0.6502 and ROC-AUC of 0.8296.
