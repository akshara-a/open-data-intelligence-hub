# Feature Importance Report - Task 9

## 1. Objective

This report analyzes the features that influenced the purchase prediction model. Feature importance is used to understand which customer behavior and session characteristics contributed most to the model's predictions.

## 2. Most Important Features

The top features identified by the model were:

1. TimeOnSite - 0.1323
2. DaysSinceLastVisit - 0.1287
3. ReviewScoreViewed - 0.0889
4. AverageOrderValue - 0.0883
5. Age - 0.0790
6. SessionCount - 0.0596
7. PagesViewed - 0.0558
8. ProductsViewed - 0.0456
9. PreviousPurchases - 0.0383
10. CartItems - 0.0330

## 3. Interpretation

Time spent on the website and the number of days since the customer's last visit were the most influential features in the model.

Customer engagement variables such as TimeOnSite, SessionCount, PagesViewed and ProductsViewed were also important. These results suggest that customer interaction behavior may help identify customers who are more likely to purchase.

ReviewScoreViewed and AverageOrderValue also had relatively high importance, indicating that product evaluation and transaction-related information contributed to the prediction process.

Feature importance represents predictive association within this trained model and does not prove that a feature directly causes a customer to make a purchase.

## 4. Business Implications

The company can use these findings to:

- Identify highly engaged customers for targeted campaigns.
- Re-engage customers based on time since their previous visit.
- Improve product review visibility.
- Personalize offers based on browsing and purchase behavior.
- Prioritize customers who show stronger engagement signals.

## 5. Limitation

Feature importance should not be interpreted as causation. The importance values depend on the dataset, preprocessing approach and trained model.

Further analysis using additional data and validation experiments is recommended.

## 6. Conclusion

The feature-importance analysis highlights customer engagement and recency variables as important predictive signals. These insights can support targeted marketing and customer-prioritization strategies.
