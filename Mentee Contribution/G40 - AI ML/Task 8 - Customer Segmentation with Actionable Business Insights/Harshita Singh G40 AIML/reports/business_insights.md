# Business Insights — Customer Segmentation

## Key findings
- **Highest revenue segment:** High-Value Loyal Customers contributes the largest share of total revenue
  (45.6%) despite not always being the largest group by size.
- **Highest churn/inactivity risk:** Low-Engagement Customers has the longest average time since last purchase
  and needs a re-engagement push before the relationship is lost.
- **Most discount-responsive:** Discount-Driven Customers shows the highest discount usage rate and
  responds best to time-limited promotions rather than everyday low pricing.
- **Loyalty rewards target:** High-Value Loyal Customers should receive loyalty perks and premium access
  instead of discounts, since they already convert at full price.
- **Premium recommendations target:** High-Value Loyal Customers are also the best audience for premium
  product recommendations, given their high average order value.

## Model performance summary
- K-Means silhouette score: 0.418 at k=5.
- Ridge Regression (tuned) RMSE: 0.659,
  R2: 0.225 for predicting CustomerRating.
- Logistic Regression (tuned) F1: 0.821,
  ROC-AUC: 0.824 for predicting PurchaseLikelihood.

## Recommended actions by segment

### New & Promising Customers (308 customers, 20.5% of base)
Send personalized onboarding offers and popular-product recommendations to convert them into repeat buyers before engagement fades.

### At-Risk Customers (289 customers, 19.3% of base)
Launch a win-back campaign with a personalized comeback incentive and a short feedback survey to diagnose why engagement dropped.

### High-Value Loyal Customers (225 customers, 15.0% of base)
Offer loyalty rewards, early access to new products, and a premium membership tier. Avoid discounting — these customers already convert at full price.

### Low-Engagement Customers (379 customers, 25.3% of base)
Use low-cost email nurture and entry-level product recommendations; reassess whether heavier investment in this group is worthwhile.

### Discount-Driven Customers (299 customers, 19.9% of base)
Target with time-limited promotions and bundles during campaign windows; avoid standing discounts outside campaigns to protect margin.
