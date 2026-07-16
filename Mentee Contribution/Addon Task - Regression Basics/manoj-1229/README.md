# AI/ML Interview Preparation: Regression Basics
**Candidate:** Venkata Sai Manoj Kumar Indraganti  
**Batch:** G40 AIML  

This document contains comprehensive, technical answers to essential regression interview questions covering fundamental concepts, mathematical assumptions, evaluation metrics, data challenges, and regularization techniques.

---

## 📘 Section 1: Fundamental Regression Concepts

### 1. What is regression in machine learning, and when is it used?
* **Definition:** Regression is a supervised learning approach used to predict a continuous numerical output variable based on one or more input features.
* **When to use:** It is used whenever the target variable is quantitative (e.g., predicting real estate prices, stock values, product ratings, or sales forecasting).

### 2. What is the difference between simple linear regression and multiple linear regression?
* **Simple Linear Regression:** Models the relationship between a single independent variable ($X$) and a continuous dependent variable ($y$). 
  * *Equation:* $y = \beta_0 + \beta_1 x + \epsilon$
* **Multiple Linear Regression:** Models the relationship between two or more independent variables ($x_1, x_2, \dots, x_n$) and a continuous dependent variable ($y$).
  * *Equation:* $y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_n x_n + \epsilon$

### 3. What assumptions are made by linear regression?
Linear regression relies on four fundamental statistical assumptions (often recalled via the acronym **LINE**):
1. **Linearity:** The relationship between the independent variables and the mean of the dependent variable is linear.
2. **Independence:** The residuals (errors) are independent of each other (no autocorrelation).
3. **Normality:** For any fixed value of $X$, the residuals are normally distributed.
4. **Homoscedasticity:** The variance of the residual errors is constant across all levels of the independent variables.

### 4. What is the difference between a dependent variable and an independent variable?
* **Independent Variable ($X$):** The input feature, predictor, or controlled variable used to explain variations in the target.
* **Dependent Variable ($y$):** The output target, response, or outcome variable that changes in response to variations in the independent variables.

### 5. What do the slope and intercept represent in a linear regression model?
* **Intercept ($\beta_0$):** The expected value of the dependent variable ($y$) when all independent variables ($X$) are equal to zero.
* **Slope ($\beta_1$):** The expected change in the dependent variable ($y$) for every one-unit increase in the corresponding independent variable ($X$), assuming all other variables remain constant.

### 6. What is the purpose of the cost function in regression?
* The cost function quantifies the prediction error of the model by measuring the difference between actual values and predicted values. Its primary purpose is to provide a metric that optimization algorithms (like Gradient Descent) can minimize to determine the optimal weights ($\beta$ coefficients) for the line of best fit.

---

## 📊 Section 2: Evaluation Metrics

### 7. What is Mean Squared Error, and why is it commonly used for regression?
* **Definition:** Mean Squared Error (MSE) calculates the average of the squared differences between the actual and predicted values.
  * *Formula:* $MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$
* **Why it's used:** Squaring the errors penalizes larger discrepancies heavily. This makes MSE highly effective when large errors are especially undesirable from a business standpoint.

### 8. What is the difference between Mean Absolute Error, Mean Squared Error, and Root Mean Squared Error?
* **Mean Absolute Error (MAE):** The average of the absolute differences between actual and predicted values. It treats all errors equally, is highly robust to outliers, and maintains the original target scale.
* **Mean Squared Error (MSE):** The average of the squared differences. It heavily penalizes outliers, but converts the final unit to a squared scale, making direct business interpretation difficult.
* **Root Mean Squared Error (RMSE):** The square root of MSE. It preserves the outlier-penalization nature of MSE while returning the metric to the original unit scale of the target variable.

### 9. What is the R-squared score, and how should it be interpreted?
* **Definition:** The Coefficient of Determination ($R^2$) measures the proportion of variance in the dependent variable that is predictable from the independent variables.
* **Interpretation:** It ranges from 0 to 1. An $R^2$ score of 0.85 indicates that 85% of the variance in the target variable is successfully explained by the model's features, while the remaining 15% is due to noise or unmeasured elements.

### 10. What is adjusted R-squared, and why is it useful?
* **The Problem:** Standard $R^2$ will always stay the same or increase when new features are added to a model, even if those features have zero predictive power.
* **The Solution:** Adjusted $R^2$ accounts for the number of predictors in the model. It incorporates a penalty factor and will only increase if a new feature improves the model's predictive power beyond random chance, making it essential for comparing multiple regression configurations.

---

## ⚠️ Section 3: Data Challenges & Performance Limitations

### 11. What is overfitting in a regression model?
* **Definition:** Overfitting occurs when a regression model learns the noise and random fluctuations within the training dataset instead of capturing only the underlying trend.
* **Signs:** Exceptionally low error metrics on training data, coupled with poor predictive accuracy (high error) on validation or testing datasets (high variance, low bias).

### 12. What is underfitting in a regression model?
* **Definition:** Underfitting happens when a model is structurally too simple to map the true underlying trend present in the data.
* **Signs:** Poor performance metrics on both the training data and the test data simultaneously (high bias, low variance).

### 13. What is multicollinearity, and how does it affect regression?
* **Definition:** A phenomenon where two or more independent features are highly correlated with one another.
* **Effect:** It inflates the variance of the coefficient estimates, making the model highly sensitive to minor data variations. As a result, the individual impact of each feature cannot be accurately isolated, making p-values unreliable.

### 14. How can multicollinearity be detected?
* **Correlation Matrices:** Reviewing linear correlation coefficients between independent features to check for high values ($|r| > 0.8$).
* **Variance Inflation Factor (VIF):** A metric determining how much the variance of an estimated regression coefficient is increased due to collinearity. A $VIF > 5$ or $10$ points to severe multicollinearity requiring correction.

### 15. How do outliers affect a regression model?
* Since linear regression models typically use Ordinary Least Squares (OLS) to minimize squared residuals, a single significant outlier can warp the path of the regression line. The model will skew its coefficients away from the general population trend simply to reduce the large squared error introduced by that single outlier point.

---

## 🛠️ Section 4: Regularization & Advanced Architectures

### 16. What is regularization, and why is it used?
* Regularization introduces a penalty term to the model's cost function to constrain or shrink large coefficient values. It is applied to mitigate overfitting, handle multicollinearity, and improve model generalization on unseen data.

### 17. What is the difference between Ridge, Lasso, and Elastic Net regression?
* **Ridge Regression (L2):** Adds a penalty equal to the square of the magnitude of coefficients ($\lambda \sum \beta^2$). It shrinks coefficients close to zero but keeps all features active.
* **Lasso Regression (L1):** Adds a penalty equal to the absolute value of the magnitude of coefficients ($\lambda \sum |\beta|$). It can shrink unhelpful coefficients exactly to zero.
* **Elastic Net:** A hybrid approach combining both L1 and L2 regularization penalties, controlled by a mixing ratio, to handle situations where multiple features are correlated.

### 18. How does Lasso regression perform feature selection?
* The L1 absolute penalty introduces a geometric constraint window containing sharp corners along the axes. During cost optimization, the weights are frequently driven exactly to coordinate axes, reducing the coefficients of non-essential or highly redundant features to exactly $0$, effectively removing them from the final equations.

### 19. What is polynomial regression?
* An extension of linear regression where the relationship between the independent feature $X$ and dependent target $y$ is modeled as an $n$-th degree polynomial expression (e.g., $y = \beta_0 + \beta_1 x + \beta_2 x^2 + \dots$). It introduces non-linear feature curves while preserving a linear parameter estimation structure.

### 20. How would you evaluate the performance of a regression model?
A robust evaluation requires a cross-validated review of performance metrics balanced against business objectives:
1. **Error Evaluation:** Compute MAE for general real-unit accuracy, and RMSE to assess the impact of severe outliers.
2. **Explanatory Fit:** Check the Adjusted $R^2$ score to measure variance capture relative to feature count.
3. **Residual Diagnostics:** Plot residual distributions to verify linearity, normality, and homoscedasticity assumptions.
