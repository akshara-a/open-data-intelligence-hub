# AI/ML Interview Questions - Regression

## 1. What is regression in machine learning, and when is it used?

Regression is a supervised machine learning technique used to predict continuous numerical values. It is used when the target variable is numeric, such as predicting house prices, sales, temperature, or salary.

---

## 2. What is the difference between simple linear regression and multiple linear regression?

- Simple Linear Regression: Uses one independent variable to predict the dependent variable.
- Multiple Linear Regression: Uses two or more independent variables to predict the dependent variable.

---

## 3. What assumptions are made by linear regression?

- Linear relationship between variables
- Independence of observations
- Homoscedasticity (constant variance of errors)
- Normally distributed residuals
- No multicollinearity among independent variables

---

## 4. What is the difference between a dependent variable and an independent variable?

- Dependent Variable: The output or target that we want to predict.
- Independent Variable: The input feature used to predict the target.

---

## 5. What do the slope and intercept represent in a linear regression model?

- Slope:Represents the change in the dependent variable for every one-unit increase in the independent variable.
- Intercept: The predicted value of the dependent variable when all independent variables are zero.

---

## 6. What is the purpose of the cost function in regression?

The cost function measures how well the model fits the data by calculating prediction error. The objective is to minimize this error during training.

---

## 7. What is Mean Squared Error (MSE), and why is it commonly used?

MSE is the average of squared differences between actual and predicted values. It penalizes larger errors more heavily and is widely used because it is differentiable and suitable for optimization.

Formula:

MSE = (1/n) Σ (Actual − Predicted)²

---

## 8. What is the difference between MAE, MSE, and RMSE?

- MAE: Average absolute error.
- MSE: Average squared error.
- RMSE: Square root of MSE, expressed in the same units as the target variable.

---

## 9. What is the R-squared score?

R² measures the proportion of variance explained by the regression model.

- R² = 1 indicates perfect prediction.
- R² = 0 indicates the model explains none of the variance.

---

## 10. What is Adjusted R-squared?

Adjusted R² adjusts the R² value based on the number of features used. It helps prevent overestimating model performance when unnecessary variables are added.

---

## 11. What is overfitting in a regression model?

Overfitting occurs when the model learns noise and details from the training data, resulting in poor performance on unseen data.

---

## 12. What is underfitting in a regression model?

Underfitting occurs when the model is too simple to capture the relationship in the data, leading to poor performance on both training and testing datasets.

---

## 13. What is multicollinearity?

Multicollinearity occurs when independent variables are highly correlated with each other, making coefficient estimates unstable.

---

## 14. How can multicollinearity be detected?

Common methods include:

- Correlation Matrix
- Variance Inflation Factor (VIF)
- Tolerance Value

---

## 15. What is regularization?

Regularization is a technique that reduces model complexity by adding a penalty term to the cost function to prevent overfitting.

---

## 16. What is the difference between Ridge, Lasso, and Elastic Net Regression?

- Ridge Regression: Uses L2 penalty and reduces coefficient values.
- Lasso Regression: Uses L1 penalty and can reduce some coefficients to zero.
- Elastic Net: Combines both L1 and L2 penalties.

---

## 17. How does Lasso Regression perform feature selection?

Lasso applies an L1 penalty that forces some coefficients to become exactly zero, automatically removing less important features.

---

## 18. What is Polynomial Regression?

Polynomial Regression models nonlinear relationships by adding polynomial terms such as x², x³, etc., while still using linear regression techniques.

---

## 19. How do outliers affect a regression model?

Outliers can significantly influence the regression line, increase prediction errors, and reduce model accuracy because regression minimizes squared errors.

---

## 20. How would you evaluate the performance of a regression model?

Regression models are commonly evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R-squared (R²)
- Adjusted R-squared
- Cross-validation

These metrics help determine how accurately the model predicts continuous values.