# Business Recommendations Report - Task 9

## 1. Business Objective

The objective of this project is to identify e-commerce customers who are likely to make a purchase. The predictions can help the company prioritize customers for marketing campaigns and improve conversion rates.

## 2. Model Performance Summary

Four model configurations were evaluated:

- Logistic Regression Baseline
- Decision Tree Baseline
- Random Forest Baseline
- Optimized Random Forest

The optimized Random Forest achieved an accuracy of approximately 85.75%. However, at the default classification threshold of 0.50, it produced no positive purchase predictions.

Because the dataset is imbalanced, accuracy alone is not sufficient for evaluating the business usefulness of the model.

## 3. Threshold Analysis

The threshold analysis produced the following results:

- Threshold 0.30: Precision = 0.1374, Recall = 0.5319, F1 Score = 0.2183
- Threshold 0.40: Precision = 0.1961, Recall = 0.2128, F1 Score = 0.2041
- Threshold 0.50: Precision = 0.0000, Recall = 0.0000, F1 Score = 0.0000

A threshold of 0.30 identified more potential purchasers and achieved the highest recall and F1 score among the tested thresholds.

## 4. Key Business Insights

The feature-importance analysis identified the following important predictive signals:

- Time spent on the website.
- Days since the customer's previous visit.
- Product review activity.
- Average order value.
- Customer session activity.
- Number of pages and products viewed.
- Previous purchase behavior.
- Number of items added to the cart.

These features suggest that customer engagement and recent interaction behavior are useful signals for customer prioritization.

## 5. Business Recommendations

### Customer Prioritization

Customers with stronger engagement signals can be prioritized for personalized marketing campaigns.

### Re-engagement Campaigns

Customers who have not visited recently can receive reminder emails, product recommendations or limited-time offers.

### Improve Product Information

Since review-related behavior was an important feature, the company should improve the visibility and quality of product reviews.

### Cart Recovery

Customers who add products to their cart but do not purchase can be targeted with cart reminder campaigns.

### Threshold-Based Marketing

The default classification threshold may not be optimal for the business objective.

For broader customer targeting, a lower threshold such as 0.30 can identify more potential purchasers. However, this also increases the number of false-positive predictions.

The company should select the threshold based on campaign cost, marketing capacity and the relative cost of false positives and false negatives.

## 6. Recommended Model Usage

The model should not be deployed using accuracy alone as the selection criterion.

The evaluation shows that class imbalance significantly affects model predictions. Before production deployment, the following improvements are recommended:

- Use class weighting or resampling techniques.
- Improve positive-class detection.
- Optimize the classification threshold.
- Collect additional purchase examples.
- Monitor precision, recall and F1 score after deployment.

## 7. Limitations

The dataset may not represent all customer behavior patterns.

Feature importance indicates predictive association and does not prove causation.

The optimized Random Forest did not improve positive-class detection at the default threshold. Therefore, additional model improvement is required before automated high-stakes decisions are made using the predictions.

## 8. Final Recommendation

The company can use the model as a customer-prioritization tool rather than relying on it as a fully automated purchase-decision system.

Customer engagement and recency signals should be combined with threshold tuning and business campaign constraints to improve conversion-focused targeting.

Further work should focus on improving positive-class recall while maintaining an acceptable precision level.
