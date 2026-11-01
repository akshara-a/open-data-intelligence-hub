# AI/ML Interview Questions: Regression

## 1. What is regression in machine learning, and when is it used?

Regression is a supervised machine learning technique used to predict continuous numerical values. It is used when the target variable is numeric, such as predicting house prices, salaries, temperatures, or sales.

---

## 2. What is the difference between simple linear regression and multiple linear regression?

- **Simple Linear Regression:** Uses one independent variable to predict the dependent variable.
- **Multiple Linear Regression:** Uses two or more independent variables to predict the dependent variable.

Example:
- Simple: Predict salary based on years of experience.
- Multiple: Predict salary based on years of experience, education, and age.

---

## 3. What assumptions are made by linear regression?

The assumptions of linear regression are:
- Linear relationship between variables.
- Independence of observations.
- Homoscedasticity (constant variance of errors).
- Normally distributed residuals.
- No multicollinearity among independent variables.

---

## 4. What is the difference between a dependent variable and an independent variable?

- **Dependent Variable (Target):** The variable we want to predict.
- **Independent Variable (Feature):** The variable(s) used to make predictions.

Example:
- Independent Variable: Years of Experience
- Dependent Variable: Salary

---

## 5. What do the slope and intercept represent in a linear regression model?

The equation is:

**Y = mX + c**

- **Slope (m):** Represents the change in Y for every one-unit increase in X.
- **Intercept (c):** Represents the predicted value of Y when X equals zero.

---

## 6. What is the purpose of the cost function in regression?

The cost function measures how well the regression model predicts the target values. The goal is to minimize the cost function to improve prediction accuracy.

---

## 7. What is Mean Squared Error (MSE), and why is it commonly used for regression?

Mean Squared Error is the average of the squared differences between actual and predicted values.

Formula:

**MSE = (1/n) Σ (Actual − Predicted)²**

It is commonly used because it heavily penalizes larger errors, making the model more accurate.

---

## 8. What is the difference between Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE)?

| Metric | Description |
|---------|-------------|
| MAE | Average of absolute errors. |
| MSE | Average of squared errors. |
| RMSE | Square root of MSE; expressed in the same units as the target variable. |

MAE is less sensitive to outliers, while MSE and RMSE penalize larger errors more strongly.

---

## 9. What is the R-squared score, and how should it be interpreted?

R-squared measures how well the independent variables explain the variation in the dependent variable.

- R² = 1 → Perfect fit.
- R² = 0 → Model explains none of the variance.

Higher R² values indicate better model performance.

---

## 10. What is adjusted R-squared, and why is it useful?

Adjusted R-squared modifies the R² value by considering the number of independent variables. It prevents unnecessary features from making the model appear better than it actually is.

---

## 11. What is overfitting in a regression model?

Overfitting occurs when the model learns the training data too well, including noise and outliers. It performs well on training data but poorly on unseen test data.

---

## 12. What is underfitting in a regression model?

Underfitting occurs when the model is too simple to capture the relationship in the data. It performs poorly on both training and testing data.

---

## 13. What is multicollinearity, and how does it affect regression?

Multicollinearity occurs when two or more independent variables are highly correlated. It makes the model unstable and affects the accuracy of coefficient estimates.

---

## 14. How can multicollinearity be detected?

Multicollinearity can be detected using:
- Correlation Matrix
- Variance Inflation Factor (VIF)
- Heatmaps
- Pair Plots

A high VIF value (greater than 5 or 10) usually indicates multicollinearity.

---

## 15. What is regularization, and why is it used?

Regularization is a technique used to reduce overfitting by adding a penalty to the regression model. It improves the model's ability to generalize to new data.

---

## 16. What is the difference between Ridge, Lasso, and Elastic Net regression?

| Regression | Description |
|------------|-------------|
| Ridge | Uses L2 regularization; reduces coefficient values but does not eliminate features. |
| Lasso | Uses L1 regularization; can reduce some coefficients to zero, performing feature selection. |
| Elastic Net | Combines both L1 and L2 regularization. |

---

## 17. How does Lasso regression perform feature selection?

Lasso regression applies L1 regularization, which forces some feature coefficients to become exactly zero. Features with zero coefficients are effectively removed, resulting in automatic feature selection.

---

## 18. What is polynomial regression?

Polynomial regression is an extension of linear regression that models nonlinear relationships by adding polynomial terms (such as X², X³, etc.) to the regression equation.

---

## 19. How do outliers affect a regression model?

Outliers can significantly influence the regression line, leading to inaccurate predictions and increased error values. They may reduce the overall performance of the model.

---

## 20. How would you evaluate the performance of a regression model?

A regression model can be evaluated using:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R-squared (R²)
- Adjusted R-squared
- Residual Analysis
- Cross-validation

A good regression model generally has low MAE, MSE, and RMSE values, along with a high R² score.

---

# Conclusion

Regression is one of the most important supervised machine learning techniques used to predict continuous values. Understanding regression algorithms, evaluation metrics, assumptions, and regularization methods is essential for building accurate and reliable predictive models.