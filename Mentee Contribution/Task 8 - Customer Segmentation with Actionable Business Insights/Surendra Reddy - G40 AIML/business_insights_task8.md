# Task 8 - Customer Segmentation with Actionable Business Insights

## 1. Business Problem
Segment customers by purchasing behavior (RFM) and predict rating/purchase
likelihood to support targeted marketing, retention, and product recommendations.

## 2. Dataset
Synthetic dataset (1500 rows) with demographics, spending, frequency,
recency, website activity, discount usage, and rating.

## 3. Clustering (K-Means on RFM features)
- Features: DaysSinceLastPurchase (Recency), PurchaseFrequency, TotalSpending (Monetary)
- Silhouette scores: K=2: 0.356, K=3: 0.374 (highest), K=4: 0.338 (selected), K=5: 0.309, K=6: 0.319, K=7: 0.327
- K=4 was selected over the mathematically higher-scoring K=3 because it produces
  four distinct, business-actionable segments (High-Value Loyal, At-Risk,
  New/Promising, Low-Engagement) rather than a coarser 3-way split.
- Final Silhouette Score (K=4): 0.338
- Segment profiles saved in segment_profile_task8.csv

## 4. Regression (Ridge - Predict Customer Rating)
- Before tuning: R2=0.264
- Best alpha: 10
- After tuning: R2=0.265
- Tuning produced negligible change, indicating the default alpha was already
  near-optimal for this dataset.

## 5. Classification (Logistic Regression - Predict Purchase Likelihood)
- Before tuning (default params): Accuracy=0.773, F1=0.819, ROC-AUC=0.853
- GridSearchCV best params (by CV F1): {'C': 0.01, 'max_iter': 100, 'solver': 'lbfgs'}
- After tuning (on held-out test set): Accuracy=0.753, F1=0.814, ROC-AUC=0.841
- The tuned model performed marginally worse on the test set than the baseline,
  because GridSearchCV selected a more heavily regularized model (C=0.01) based
  on cross-validated F1 during training, which slightly underfit this particular
  test split. The baseline (default) Logistic Regression is therefore selected
  as the final model for this task, since it generalizes better here.

## 6. Business Insights
- High-Value Loyal Customers generate the most revenue and should receive
  loyalty rewards and early access to new products.
- At-Risk Customers show high past value but rising recency, and should
  receive re-engagement campaigns before they churn.
- New and Promising Customers should get onboarding offers to encourage a
  second purchase.
- Low-Engagement Customers should only receive low-cost campaigns to avoid
  wasting marketing budget.

## 7. Final Conclusion
Combining RFM-based clustering with regression and classification gives a
complete view of customer value, satisfaction, and buying intent - enabling
segment-specific, actionable marketing strategies rather than one-size-fits-all
campaigns. Hyperparameter tuning improved neither the regression nor
classification model meaningfully in this case, which itself is a useful
finding: default scikit-learn parameters were already well-suited to this
dataset, and model selection should always be validated against held-out
test performance rather than cross-validation scores alone.
