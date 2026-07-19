# Task 9 - Optimized Classification Model with Feature Importance Analysis

## 1. Project Objective
Predict e-commerce purchase likelihood using an optimized classification model,
identify key influencing features, and translate results into business actions.

## 2. Dataset
Synthetic e-commerce dataset (3000 rows), purchase rate 0.25.

## 3. Baseline Model Comparison
                         Model  Accuracy  Precision  Recall  F1-Score  ROC-AUC
Logistic Regression (Baseline)     0.823      0.677   0.560     0.613    0.864
      Decision Tree (Baseline)     0.755      0.510   0.493     0.502    0.668
      Random Forest (Baseline)     0.815      0.767   0.373     0.502    0.845

## 4. Optimization Metric
F1-Score was selected because accuracy is misleading under class imbalance
(~75% non-purchasers), and the business needs a balance between not missing
buyers (recall) and not wasting marketing spend on unlikely buyers (precision).

## 5. Hyperparameter Optimization
- Random Forest best params: {'classifier__class_weight': 'balanced', 'classifier__max_depth': 5, 'classifier__min_samples_leaf': 2, 'classifier__min_samples_split': 10, 'classifier__n_estimators': 300}, best CV F1: 0.642, test F1: 0.621
- Logistic Regression best params: {'classifier__C': 10, 'classifier__class_weight': 'balanced', 'classifier__penalty': 'l2', 'classifier__solver': 'liblinear'}, best CV F1: 0.645, test F1: 0.628
- Logistic Regression was selected as the final model: it achieved the highest
  test-set F1-Score (0.628) and ROC-AUC (0.864) among all baseline and tuned
  models, despite Random Forest having a marginally different CV score. This
  follows the rule that model selection must be validated against held-out
  test performance, not cross-validation scores alone.

## 6. Final Model Comparison
                                     Model  Accuracy  Precision  Recall  F1-Score  ROC-AUC
            Logistic Regression (Baseline)     0.823      0.677   0.560     0.613    0.864
                  Decision Tree (Baseline)     0.755      0.510   0.493     0.502    0.668
                  Random Forest (Baseline)     0.815      0.767   0.373     0.502    0.845
                 Random Forest (Optimized)     0.780      0.545   0.720     0.621    0.852
Logistic Regression (Optimized) - SELECTED     0.765      0.520   0.793     0.628    0.864

## 7. Top Features Influencing Purchase
                    Feature  Coefficient                     Direction
numeric__DaysSinceLastVisit    -1.300135 Decreases purchase likelihood
         numeric__CartItems     1.200997 Increases purchase likelihood
       numeric__PagesViewed     0.877650 Increases purchase likelihood
 numeric__PreviousPurchases     0.812533 Increases purchase likelihood
      numeric__DiscountUsed     0.524779 Increases purchase likelihood

## 8. Business Recommendations

### High-Likelihood Customers
- Send personalized discounts and cart reminders.
- Prioritize in paid remarketing campaigns.

### Medium-Likelihood Customers
- Provide product reviews/comparisons and small incentives.
- Use personalized email campaigns highlighting free shipping.

### Low-Likelihood Customers
- Avoid expensive campaigns; use low-cost awareness content only.
- Investigate usability/product-discovery improvements.

## 9. Limitations
- Synthetic dataset; real customer data may show different feature relationships.
- Feature importance indicates association, not causation.
- Class imbalance means metrics should be monitored over time as purchase 
  patterns shift.

## 10. Final Conclusion
The optimized Logistic Regression model outperformed Random Forest and Decision
Tree on F1-Score and ROC-AUC on the held-out test set, despite Random Forest's
similar cross-validation score, illustrating why final model selection must
rely on test-set evaluation. DaysSinceLastVisit, CartItems, PreviousPurchases,
and PagesViewed emerged as the strongest predictors of purchase likelihood,
giving the business clear, actionable levers for improving conversion.
