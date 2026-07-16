# Regression Interview Questions and Answers

## 1. What is regression in machine learning, and when is it used?

Regression is a supervised machine learning algorithm used to predict **continuous numerical values** based on input features. It is commonly used for predicting house prices, salaries, sales, stock prices, and temperatures.

---

## 2. What is the difference between simple linear regression and multiple linear regression?

- **Simple Linear Regression:** Uses one independent variable to predict the target.
- **Multiple Linear Regression:** Uses two or more independent variables to predict the target.

---

## 3. What assumptions are made by linear regression?

Linear regression assumes:
- Linearity
- Independence of observations
- Homoscedasticity (constant variance of errors)
- Normally distributed residuals
- No multicollinearity among independent variables

---

## 4. What is the difference between a dependent variable and an independent variable?

- **Independent Variable (X):** Input feature used for prediction.
- **Dependent Variable (Y):** Output or target variable that the model predicts.

---

## 5. What do the slope and intercept represent in a linear regression model?

- **Slope:** Represents the change in the dependent variable for a one-unit increase in the independent variable.
- **Intercept:** Represents the predicted value of the dependent variable when the independent variable is zero.

---

## 6. What is the purpose of the cost function in regression?

The cost function measures how far the predicted values are from the actual values. The objective of training is to minimize this error.

---

## 7. What is Mean Squared Error (MSE), and why is it commonly used for regression?

Mean Squared Error (MSE) is the average of the squared differences between actual and predicted values. It is widely used because it penalizes larger errors more heavily and is easy to optimize.

---

## 8. What is the difference between Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE)?

- **MAE:** Average absolute difference between actual and predicted values.
- **MSE:** Average squared difference between actual and predicted values.
- **RMSE:** Square root of MSE, expressed in the same units as the target variable.

MAE is less sensitive to outliers, while MSE and RMSE penalize larger errors more.

---

## 9. What is the R-squared score, and how should it be interpreted?

R-squared (R²) measures how well the regression model explains the variance in the target variable. Its value ranges from 0 to 1, where higher values indicate a better fit.

---

## 10. What is adjusted R-squared, and why is it useful?

Adjusted R² is a modified version of R² that considers the number of features in the model. It prevents unnecessary features from artificially improving the model score.

---

## 11. What is overfitting in a regression model?

Overfitting occurs when a model learns both the underlying patterns and the noise in the training data, resulting in excellent training performance but poor performance on unseen data.

---

## 12. What is underfitting in a regression model?

Underfitting occurs when a model is too simple to capture the underlying relationship in the data, leading to poor performance on both training and testing data.

---

## 13. What is multicollinearity, and how does it affect regression?

Multicollinearity occurs when independent variables are highly correlated with each other. It can make coefficient estimates unstable and reduce the interpretability of the model.

---

## 14. How can multicollinearity be detected?

Common methods include:
- Variance Inflation Factor (VIF)
- Correlation matrix

A high VIF (typically greater than 5 or 10) indicates multicollinearity.

---

## 15. What is regularization, and why is it used?

Regularization adds a penalty to the model's loss function to reduce overfitting and improve generalization by controlling model complexity.

---

## 16. What is the difference between Ridge, Lasso, and Elastic Net regression?

- **Ridge Regression:** Uses L2 regularization and reduces coefficient values without removing features.
- **Lasso Regression:** Uses L1 regularization and can reduce some coefficients to zero, performing feature selection.
- **Elastic Net Regression:** Combines both L1 and L2 regularization.

---

## 17. How does Lasso regression perform feature selection?

Lasso regression applies an L1 penalty, which shrinks some feature coefficients to exactly zero. Features with zero coefficients are automatically removed from the model.

---

## 18. What is polynomial regression?

Polynomial regression extends linear regression by adding polynomial terms, allowing it to model non-linear relationships between variables.

---

## 19. How do outliers affect a regression model?

Outliers can significantly influence the regression line, leading to inaccurate predictions and increased error, especially in linear regression.

---

## 20. How would you evaluate the performance of a regression model?

A regression model is commonly evaluated using:
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R-squared (R²)
- Adjusted R-squared

Lower error values and higher R² values generally indicate better model performance.
