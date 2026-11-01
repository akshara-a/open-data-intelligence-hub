# AI/ML Regression Interview Questions & Answers

**Date:** July 10, 2026  
**Topic:** Regression Analysis in Machine Learning

---

## Q1: What is regression in machine learning, and when is it used?

**Answer:**

Regression is a supervised learning technique used to predict continuous numerical values based on input features. It models the relationship between a dependent variable (target) and one or more independent variables (predictors).

**When it's used:**
- Predicting house prices based on features like size, location, bedrooms
- Forecasting sales revenue for a business
- Estimating temperature or weather conditions
- Predicting stock prices and financial trends
- Estimating customer lifetime value in marketing
- Risk assessment in insurance and banking

---

## Q2: What is the difference between simple linear regression and multiple linear regression?

**Answer:**

| Aspect | Simple Linear Regression | Multiple Linear Regression |
|--------|--------------------------|---------------------------|
| Number of predictors | One independent variable | Two or more independent variables |
| Equation | y = β₀ + β₁x | y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ |
| Visualization | 2D straight line | Hyperplane in n-dimensional space |
| Example | Price vs. size of house | Price vs. size, location, age, bedrooms |

---

## Q3: What assumptions are made by linear regression?

**Answer:**

1. **Linearity** - The relationship between independent and dependent variables is linear
2. **Independence** - Observations are independent of each other (no autocorrelation)
3. **Homoscedasticity** - Constant variance of residuals across all levels of predictors
4. **Normality** - Residuals should be approximately normally distributed (important for inference)
5. **No perfect multicollinearity** - Independent variables should not be perfectly correlated with each other

---

## Q4: What is the difference between a dependent variable and an independent variable?

**Answer:**

| Aspect | Dependent Variable | Independent Variable |
|--------|-------------------|---------------------|
| Also called | Target, Response, Outcome, y | Predictor, Feature, Covariate, x |
| Definition | What we want to predict | What we use to make predictions |
| Relationship | Depends on independent variables | Are manipulated or observed |
| Example | House price | Square footage, number of bedrooms |

---

## Q5: What do the slope and intercept represent in a linear regression model?

**Answer:**

In the equation **y = β₀ + β₁x**:

**Intercept (β₀)**:
- The expected value of y when all predictors equal 0
- The point where the regression line crosses the y-axis
- Example: If x = 0, the predicted house price would be β₀

**Slope (β₁)**:
- The change in y for a 1-unit increase in x
- Represents the effect of x on y
- Example: If slope = 200, each additional square foot increases house price by $200

---

## Q6: What is the purpose of the cost function in regression?

**Answer:**

The cost function measures how well the regression model fits the training data by quantifying the error between predicted and actual values.

**Purpose:**
- Provides a numerical measure of model performance
- Guides optimization algorithms (like gradient descent) to find optimal parameters
- Minimizing the cost function yields the best-fitting regression coefficients
- Helps compare different models

---

## Q7: What is Mean Squared Error, and why is it commonly used for regression?

**Answer:**

**MSE = (1/n) × Σ(actual - predicted)²**

**Why it's commonly used:**
- **Differentiable** - Makes it easy to optimize using gradient descent
- **Convex** - Has a single global minimum
- **Penalizes large errors** - Squaring gives more weight to outliers
- **Mathematically convenient** - Works well with Ordinary Least Squares
- **Variance interpretation** - Relates to the variance of errors

---

## Q8: What is the difference between Mean Absolute Error, Mean Squared Error, and Root Mean Squared Error?

**Answer:**

| Metric | Formula | Pros | Cons |
|--------|---------|------|------|
| **MAE** | (1/n)Σ\|y - ŷ\| | Robust to outliers, intuitive interpretation | Not differentiable at 0 |
| **MSE** | (1/n)Σ(y - ŷ)² | Differentiable, penalizes large errors | Sensitive to outliers |
| **RMSE** | √[(1/n)Σ(y - ŷ)²] | Same units as target variable, interpretable | Sensitive to outliers |

**Key Differences:**
- MAE treats all errors equally
- MSE/RMSE penalize larger errors more severely
- RMSE is in the same scale as the target variable
- Use MAE when outliers are not important; use RMSE when large errors are costly

---

## Q9: What is the R-squared score, and how should it be interpreted?

**Answer:**

**R² = 1 - (SS_res / SS_total)**

Where SS_res = sum of squared residuals, SS_total = total sum of squares

**Interpretation:**
- Represents the proportion of variance in the dependent variable explained by the model
- Ranges from 0 to 1 (0% to 100%)
- R² = 0.75 means 75% of the variance is explained by the model

**Caveats:**
- High R² doesn't guarantee a good model (could indicate overfitting)
- R² always increases with more predictors, even if they're useless
- Doesn't indicate if coefficients are statistically significant
- Should be used with other metrics for complete evaluation

---

## Q10: What is adjusted R-squared, and why is it useful?

**Answer:**

**Adjusted R² = 1 - [(1 - R²)(n - 1) / (n - k - 1)]**

Where n = sample size, k = number of predictors

**Why it's useful:**
- Penalizes adding unnecessary predictors
- Only increases when a new predictor actually improves the model
- Helps with model selection between models with different numbers of features
- More conservative and reliable than regular R²

---

## Q11: What is overfitting in a regression model?

**Answer:**

Overfitting occurs when a model learns training data too well, capturing noise and random fluctuations instead of the underlying pattern.

**Symptoms:**
- Very high R² on training data, but poor performance on test data
- Complex models with many features
- Coefficients that are too large or unstable

**Solutions:**
- Use regularization (Ridge/Lasso)
- Cross-validation
- Simplify the model
- Get more training data
- Use feature selection

---

## Q12: What is underfitting in a regression model?

**Answer:**

Underfitting occurs when a model is too simple to capture the underlying patterns in the data.

**Symptoms:**
- Poor performance on both training and test data
- High bias, low variance
- Very simple model that doesn't capture relationships

**Solutions:**
- Use more complex models (add polynomial terms)
- Add more relevant features
- Reduce regularization
- Increase model capacity

---

## Q13: What is multicollinearity, and how does it affect regression?

**Answer:**

Multicollinearity is a high correlation between two or more independent variables in a regression model.

**Effects:**
- Unstable coefficient estimates with large standard errors
- Difficulty in determining individual effects of predictors
- Coefficients may change dramatically when adding/removing variables
- Reduced statistical significance (higher p-values)
- Unreliable feature importance interpretation

---

## Q14: How can multicollinearity be detected?

**Answer:**

**Detection methods:**

1. **Correlation matrix** - Look for correlations > 0.8 or < -0.8

2. **Variance Inflation Factor (VIF)**:
   - VIF = 1/(1 - R²ᵢ)
   - VIF > 5-10 indicates multicollinearity
   - VIF > 10 indicates severe multicollinearity

3. **Condition Number** - Values > 30 indicate multicollinearity

4. **Eigenvalues** - Near-zero eigenvalues of correlation matrix indicate multicollinearity

---

## Q15: What is regularization, and why is it used?

**Answer:**

Regularization adds a penalty term to the cost function to discourage complex models and prevent overfitting.

**General form:** Loss = MSE + λ × Penalty

**Why it's used:**
- Prevents overfitting by reducing model complexity
- Reduces model variance
- Improves generalization to unseen data
- Handles multicollinearity
- Can perform feature selection (Lasso)

---

## Q16: What is the difference between Ridge, Lasso, and Elastic Net regression?

**Answer:**

| Method | Penalty Term | Properties |
|--------|--------------|------------|
| **Ridge** | λΣβ² (L2) | Shrinks coefficients toward zero but never to zero, handles multicollinearity, groups correlated features |
| **Lasso** | λΣ\|β\| (L1) | Can shrink coefficients to exactly zero, performs feature selection, picks one from correlated features |
| **Elastic Net** | λ₁Σ\|β\| + λ₂Σβ² (L1 + L2) | Combines both L1 and L2 penalties, handles correlated features better, performs feature selection, useful when p > n |

---

## Q17: How does Lasso regression perform feature selection?

**Answer:**

Lasso uses L1 regularization (λΣ|β|) which has a diamond-shaped constraint region.

**How it works:**
- The penalty is based on absolute value of coefficients
- Diamond-shaped constraint region has corners on the axes
- When minimizing the cost function, the solution often falls on these corners
- This causes some coefficients to become exactly zero
- Effectively removes irrelevant features

**Benefits:**
- Sparse models
- Easier interpretation
- Reduced overfitting
- Automatic feature selection

---

## Q18: What is polynomial regression?

**Answer:**

Polynomial regression extends linear regression by adding polynomial terms of the predictors.

**Equation:** y = β₀ + β₁x + β₂x² + β₃x³ + ... + βₙxⁿ

**Key points:**
- Still linear in parameters (β's) - it's technically a linear model
- Captures non-linear relationships between variables
- More flexible as degree increases
- Risk of overfitting with high-degree polynomials
- Use cross-validation to select optimal degree

---

## Q19: How do outliers affect a regression model?

**Answer:**

**Effects of outliers:**
- MSE/RMSE gives disproportionate weight to outliers
- Coefficient estimates can be pulled toward outliers
- R² can be artificially inflated or deflated
- Statistical significance can be affected
- Model interpretation can be misleading

**Handling outliers:**
- Use robust regression (Huber, quantile regression)
- Use MAE instead of MSE
- Winsorization or trimming
- Transform variables (log transformation)
- Remove them with justification

---

## Q20: How would you evaluate the performance of a regression model?

**Answer:**

**Comprehensive evaluation approach:**

1. **Data splitting** - Train/validation/test sets (e.g., 70/15/15)

2. **Error metrics**:
   - MSE, RMSE, MAE (magnitude of errors)
   - MAPE (relative error percentage)

3. **Variance explained**:
   - R² and Adjusted R²

4. **Cross-validation** - k-fold for robust assessment

5. **Check assumptions**:
   - Residual plots for homoscedasticity
   - Q-Q plots for normality
   - VIF for multicollinearity

6. **Learning curves** - Diagnose bias/variance

7. **Business context** - Assess if errors are acceptable

8. **Feature importance** - Ensure meaningful predictors

9. **Model comparison** - Compare with baseline and other algorithms

---