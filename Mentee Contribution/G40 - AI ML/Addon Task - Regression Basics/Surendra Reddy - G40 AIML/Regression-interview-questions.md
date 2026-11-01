# AI/ML Interview Questions: Regression
---

### 1. What is regression in machine learning, and when is it used?

Regression is a supervised learning technique used to predict a continuous numeric output based on one or more input features. Instead of predicting a class label (like classification), regression models learn the relationship between independent variables and a dependent variable so they can estimate a real-valued outcome. It's used whenever the target is continuous — for example, predicting house prices, sales revenue, temperature, or a person's salary based on experience.

### 2. What is the difference between simple linear regression and multiple linear regression?

Simple linear regression models the relationship between a single independent variable and the dependent variable using a straight line (`y = mx + c`). Multiple linear regression extends this to two or more independent variables (`y = b0 + b1x1 + b2x2 + ... + bnxn`), allowing the model to capture the combined effect of several predictors on the outcome.

### 3. What assumptions are made by linear regression?

Linear regression relies on a few key assumptions:
- **Linearity** – the relationship between independent and dependent variables is linear.
- **Independence** – observations (and residuals) are independent of each other.
- **Homoscedasticity** – the variance of residuals is constant across all levels of the independent variables.
- **Normality of residuals** – errors are approximately normally distributed.
- **No/low multicollinearity** – independent variables shouldn't be highly correlated with each other.

Violating these assumptions can make coefficient estimates unreliable or the model's predictions less trustworthy.

### 4. What is the difference between a dependent variable and an independent variable?

The **dependent variable** (also called the target or response variable) is the outcome we're trying to predict — it "depends" on other factors. The **independent variables** (also called features or predictors) are the inputs used to explain or predict changes in the dependent variable. For example, in predicting house price from area and location, price is dependent, while area and location are independent.

### 5. What do the slope and intercept represent in a linear regression model?

In the equation `y = mx + c`, the **slope (m)** represents how much the dependent variable changes for a one-unit increase in the independent variable — it captures the strength and direction of the relationship. The **intercept (c)** is the predicted value of `y` when the independent variable(s) equal zero — it represents the baseline value of the model.

### 6. What is the purpose of the cost function in regression?

The cost function (also called the loss function) measures how far off the model's predictions are from the actual values. It provides a single quantitative score of model error, which the training algorithm (typically gradient descent) tries to minimize by adjusting the model's coefficients. Without a cost function, there'd be no objective way to know if the model is improving during training.

### 7. What is Mean Squared Error, and why is it commonly used for regression?

Mean Squared Error (MSE) is the average of the squared differences between predicted and actual values:

`MSE = (1/n) * Σ(y_actual - y_predicted)²`

It's popular because squaring the errors removes negative signs (so errors don't cancel out) and heavily penalizes larger errors, which pushes the model to avoid big mistakes. It's also mathematically convenient (differentiable), which makes it easy to optimize using gradient-based methods.

### 8. What is the difference between Mean Absolute Error, Mean Squared Error, and Root Mean Squared Error?

- **MAE (Mean Absolute Error)** – average of the absolute differences between actual and predicted values. Treats all errors linearly, so it's less sensitive to outliers.
- **MSE (Mean Squared Error)** – average of squared differences. Penalizes larger errors more heavily due to squaring, making it sensitive to outliers.
- **RMSE (Root Mean Squared Error)** – square root of MSE. It brings the error back to the same unit/scale as the target variable, making it easier to interpret than MSE while still penalizing large errors more than MAE.

### 9. What is the R-squared score, and how should it be interpreted?

R-squared (R²) measures the proportion of variance in the dependent variable that is explained by the independent variables. It ranges from 0 to 1 (can be negative for a poor model), where a value closer to 1 means the model explains most of the variability in the data, and a value closer to 0 means it explains very little. For example, an R² of 0.85 means 85% of the variation in the target is explained by the model's features.

### 10. What is adjusted R-squared, and why is it useful?

Adjusted R-squared modifies R² to account for the number of predictors in the model. Plain R² always increases (or stays the same) as more features are added, even if those features aren't actually useful, which can be misleading. Adjusted R² penalizes the addition of irrelevant predictors, only increasing if a new variable genuinely improves the model more than would be expected by chance. This makes it a better metric for comparing models with different numbers of features.

### 11. What is overfitting in a regression model?

Overfitting occurs when a model learns the training data too well — including its noise and random fluctuations — resulting in excellent performance on training data but poor generalization to new, unseen data. It typically happens when the model is too complex (e.g., too many features or high-degree polynomial terms) relative to the amount of training data available.

### 12. What is underfitting in a regression model?

Underfitting happens when a model is too simple to capture the underlying pattern in the data, resulting in poor performance on both the training and test sets. This often occurs when using an overly simplistic model (like linear regression on clearly nonlinear data) or when important features are missing.

### 13. What is multicollinearity, and how does it affect regression?

Multicollinearity occurs when two or more independent variables in a regression model are highly correlated with each other. This makes it difficult for the model to isolate the individual effect of each variable on the target, leading to unstable and unreliable coefficient estimates, inflated standard errors, and coefficients that can be hard to interpret (sometimes even flipping sign unexpectedly).

### 14. How can multicollinearity be detected?

Common methods include:
- **Correlation matrix** – checking pairwise correlations between independent variables; high values (e.g., above 0.8) suggest a problem.
- **Variance Inflation Factor (VIF)** – quantifies how much a variable's variance is inflated due to correlation with other variables; a VIF above 5 or 10 typically indicates concerning multicollinearity.
- **Eigenvalues/condition number** of the correlation matrix can also reveal multicollinearity.

### 15. What is regularization, and why is it used?

Regularization adds a penalty term to the regression cost function based on the magnitude of the model's coefficients. This discourages the model from assigning excessively large weights to any feature, which helps prevent overfitting and improves generalization to new data, especially when there are many features or multicollinearity present.

### 16. What is the difference between Ridge, Lasso, and Elastic Net regression?

- **Ridge regression** adds an L2 penalty (sum of squared coefficients) to the cost function. It shrinks coefficients toward zero but never makes them exactly zero, so it keeps all features but reduces their impact.
- **Lasso regression** adds an L1 penalty (sum of absolute values of coefficients). It can shrink some coefficients exactly to zero, effectively performing feature selection.
- **Elastic Net** combines both L1 and L2 penalties, balancing Ridge's stability with Lasso's feature-selection ability — useful when there are many correlated features.

### 17. How does Lasso regression perform feature selection?

Because Lasso's L1 penalty is based on the absolute value of coefficients, the optimization process can drive the coefficients of less important features all the way to zero (not just close to zero, as Ridge does). Features with a coefficient of exactly zero are effectively removed from the model, which naturally selects the most relevant features and produces a simpler, more interpretable model.

### 18. What is polynomial regression?

Polynomial regression is an extension of linear regression where the relationship between the independent and dependent variables is modeled as an nth-degree polynomial (e.g., `y = b0 + b1x + b2x² + b3x³ + ...`). It's still considered a form of linear regression because it's linear in the coefficients, but it allows the model to fit curved, nonlinear relationships in the data.

### 19. How do outliers affect a regression model?

Outliers can disproportionately influence a regression model because ordinary least squares minimizes squared errors, and squaring amplifies the impact of large deviations. This can skew the slope and intercept, distort coefficient estimates, and reduce the model's accuracy on the majority of "normal" data points. Outliers can also inflate error metrics like MSE and RMSE, and reduce R².

### 20. How would you evaluate the performance of a regression model?

A regression model's performance is typically evaluated using a combination of:
- **Error metrics** – MAE, MSE, RMSE to quantify prediction error.
- **R² and Adjusted R²** – to understand how much variance is explained.
- **Residual analysis** – plotting residuals to check for patterns, heteroscedasticity, or non-normality, which can reveal violated assumptions.
- **Cross-validation** – to ensure the model generalizes well to unseen data rather than just fitting the training set.
- **Checking for multicollinearity** (VIF) and overfitting/underfitting behavior across train vs. test performance.

Together, these give a complete picture of both accuracy and reliability of the model.
