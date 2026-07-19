# Model Comparison Table

| Model | Objective | Baseline Performance | Tuned Performance | Selected Model |
|-------|-----------|---------------------|-------------------|----------------|
| K-Means | Customer Segmentation | Silhouette Score: 0.2205 (K=3) | Silhouette Score: 0.2205 (K=3) |  Yes |
| Linear Regression | Predict Customer Revenue | R²: 0.9240, RMSE: $512.00 | R²: 0.9240, RMSE: $512.00 |  Yes |
| Ridge Regression | Predict Customer Revenue | R²: 0.9242, RMSE: $511.43 | R²: 0.9241, RMSE: $511.70 (Alpha=5.0) |  Yes |
| Logistic Regression | Predict Purchase Likelihood | Accuracy: 100%, ROC-AUC: 1.0000 | Accuracy: 100%, ROC-AUC: 1.0000 (C=1.0) |  Yes |

## Model Selection Summary

### K-Means Clustering
- **Selected:** Yes
- **Reason:** Optimal K=3 identified through Elbow Method and Silhouette Score analysis
- **Business Value:** Identifies 3 distinct customer segments with clear actionable characteristics

### Linear Regression
- **Selected:** Yes
- **Reason:** Solid baseline model with strong performance (92.4% R²)
- **Business Value:** Provides reliable revenue prediction for customer value assessment

### Ridge Regression
- **Selected:** Yes
- **Reason:** Slightly better performance than Linear Regression (R²: 0.9242)
- **Best Parameters:** Alpha=5.0, Solver=svd
- **Business Value:** Most accurate revenue predictor with regularization to prevent overfitting

### Logistic Regression
- **Selected:** Yes
- **Reason:** Excellent classification performance (100% accuracy, 100% ROC-AUC)
- **Best Parameters:** C=1.0, Penalty=l2, Solver=saga
- **Business Value:** Perfect identification of potential purchasers with zero wasted marketing spend

## Model Performance Summary

| Model | Key Metric | Value | Interpretation |
|-------|-----------|-------|----------------|
| K-Means | Silhouette Score | 0.2205 | Moderate cluster separation, 3 clear segments |
| Ridge Regression | R² Score | 0.9241 | Model explains 92.4% of revenue variance |
| Ridge Regression | RMSE | $511.70 | Average prediction error of $512 |
| Logistic Regression | Accuracy | 100% | Perfect classification of purchasers |
| Logistic Regression | ROC-AUC | 1.0000 | Perfect discrimination between classes |