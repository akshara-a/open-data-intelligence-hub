# AI/ML Interview Questions: Regression

## Name: P.Shadik Khan - G40 AI ML

---

## 1. What is regression in machine learning, and when is it used?

Regression is a supervised machine learning technique used to predict continuous numerical values. It is used when the output variable is a number, such as predicting house prices, sales, temperature, or salary.

---

## 2. What is the difference between simple linear regression and multiple linear regression?

- **Simple Linear Regression:** Uses one independent variable to predict the dependent variable.
- **Multiple Linear Regression:** Uses two or more independent variables to predict the dependent variable.

---

## 3. What assumptions are made by linear regression?

The assumptions of linear regression are:
- Linear relationship between variables.
- Independence of observations.
- Homoscedasticity (constant variance of errors).
- Errors are normally distributed.
- No multicollinearity among independent variables.

---

## 4. What is the difference between a dependent variable and an independent variable?

- **Dependent Variable:** The value we want to predict.
- **Independent Variable:** The input feature used to make predictions.

Example:
If predicting salary based on experience:
- Experience = Independent Variable
- Salary = Dependent Variable

---

## 5. What do the slope and intercept represent in a linear regression model?

- **Slope:** Indicates how much the dependent variable changes for every one-unit increase in the independent variable.
- **Intercept:** The predicted value of the dependent variable when the independent variable is zero.

---

## 6. What is the purpose of the cost function in regression?

The cost function measures how well the regression model fits the data. It helps the algorithm minimize prediction errors by finding the best values for the model parameters.

---

## 7. What is Mean Squared Error (MSE), and why is it commonly used for regression?

Mean Squared Error (MSE) is the average of the squared differences between actual and predicted values. It is commonly used because it heavily penalizes large prediction errors.

Formula:

MSE = (1/n) × Σ(actual − predicted)²

---

## 8. What is the difference between Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE)?

- **MAE:** Average of absolute errors.
- **MSE:** Average of squared errors.
- **RMSE:** Square root of MSE.

MAE is easier to interpret, while MSE and RMSE penalize larger errors more.

---

## 9. What is the R-squared score, and how should it be interpreted?

R-squared measures how well the model explains the variation in the target variable.

- 0 = No explanatory power.
- 1 = Perfect prediction.

Higher R-squared values indicate a better-fitting model.

---

## 10. What is adjusted R-squared, and why is it useful?

Adjusted R-squared modifies the R-squared value by considering the number of independent variables. It prevents misleading improvements caused by adding unnecessary features.

---

## 11. What is overfitting in a regression model?

Overfitting occurs when the model learns both the actual patterns and the noise in the training data, resulting in excellent training performance but poor performance on new data.

---

## 12. What is underfitting in a regression model?

Underfitting occurs when the model is too simple to capture the underlying relationship in the data, resulting in poor performance on both training and testing data.

---

## 13. What is multicollinearity, and how does it affect regression?

Multicollinearity occurs when independent variables are highly correlated with each other. It makes it difficult to determine the effect of each variable and can reduce the model's reliability.

---

## 14. How can multicollinearity be detected?

Common methods include:
- Variance Inflation Factor (VIF)
- Correlation Matrix
- Pair Plot
- Heatmap

A high VIF value usually indicates multicollinearity.

---

## 15. What is regularization, and why is it used?

Regularization is a technique used to reduce overfitting by adding a penalty to the regression model. It helps improve model generalization and prevents excessively large coefficients.

---

## 16. What is the difference between Ridge, Lasso, and Elastic Net regression?

- **Ridge Regression:** Uses L2 regularization and reduces coefficient values.
- **Lasso Regression:** Uses L1 regularization and can reduce some coefficients to zero, performing feature selection.
- **Elastic Net Regression:** Combines both L1 and L2 regularization.

---

## 17. How does Lasso regression perform feature selection?

Lasso applies L1 regularization, which can shrink some coefficients exactly to zero. Features with zero coefficients are effectively removed from the model.

---

## 18. What is polynomial regression?

Polynomial regression is an extension of linear regression that models nonlinear relationships by adding polynomial terms such as x², x³, etc.

---

## 19. How do outliers affect a regression model?

Outliers can significantly influence the regression line, resulting in inaccurate predictions and reduced model performance. Detecting and handling outliers improves model accuracy.

---

## 20. How would you evaluate the performance of a regression model?

A regression model can be evaluated using:
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R-squared Score
- Adjusted R-squared
- Residual Analysis

These metrics help determine the accuracy and reliability of the regression model.

---

## Conclusion

Regression is a fundamental supervised machine learning technique used for predicting continuous values. Understanding regression concepts, evaluation metrics, assumptions, and regularization methods is essential for building accurate and reliable predictive models.