# AI/ML Interview Questions: Regression

## 1. What is regression in machine learning, and when is it used?
Regression is a supervised machine learning algorithm used to predict continuous numerical values. It learns the relationship between input features and a target variable. Unlike classification, regression predicts numbers instead of categories. It is commonly used for predicting house prices, salaries, stock prices, and temperatures.

## 2. What is the difference between simple linear regression and multiple linear regression?
Simple linear regression uses one independent variable to predict the dependent variable. Multiple linear regression uses two or more independent variables for prediction. Multiple regression provides better predictions when several factors influence the target value.

## 3. What assumptions are made by linear regression?
Linear regression assumes that there is a linear relationship between the input and output variables. The observations should be independent, the error terms should have constant variance (homoscedasticity), and the residuals should be normally distributed. It also assumes that independent variables are not highly correlated with each other (no multicollinearity).

## 4. What is the difference between a dependent variable and an independent variable?
The dependent variable is the output or target value that we want to predict. Independent variables are the input features that influence the target variable. For example, when predicting house prices, house price is the dependent variable, while area and number of rooms are independent variables.

## 5. What do the slope and intercept represent in a linear regression model?
The slope represents the amount of change in the dependent variable for every one-unit increase in the independent variable. It indicates the strength and direction of the relationship. The intercept is the predicted value of the dependent variable when the independent variable is zero.

## 6. What is the purpose of the cost function in regression?
The cost function measures the difference between the actual and predicted values. During model training, the algorithm tries to minimize this error. A lower cost function value indicates a better-performing model with more accurate predictions.

## 7. What is Mean Squared Error (MSE), and why is it commonly used?
Mean Squared Error (MSE) is the average of the squared differences between actual and predicted values. Squaring the errors gives more importance to larger mistakes. It is widely used because it is easy to calculate and works well with optimization algorithms.

## 8. What is the difference between MAE, MSE, and RMSE?
MAE calculates the average absolute difference between actual and predicted values. MSE calculates the average squared difference, giving more weight to larger errors. RMSE is the square root of MSE and expresses the error in the same unit as the target variable, making it easier to understand.

## 9. What is the R-squared score, and how should it be interpreted?
R-squared measures how well the regression model explains the variation in the target variable. Its value ranges from 0 to 1. A value closer to 1 indicates that the model explains most of the variation, while a value closer to 0 means poor model performance.

## 10. What is adjusted R-squared, and why is it useful?
Adjusted R-squared improves upon R-squared by considering the number of independent variables used in the model. It prevents unnecessary features from increasing the score. Therefore, it provides a more reliable measure when comparing regression models with different numbers of features.

## 11. What is overfitting in a regression model?
Overfitting occurs when a regression model learns both the actual patterns and the noise in the training data. As a result, it performs very well on training data but poorly on unseen test data. Regularization and cross-validation can help reduce overfitting.

## 12. What is underfitting in a regression model?
Underfitting occurs when the model is too simple to capture the relationship between input and output variables. It performs poorly on both training and testing data because it cannot learn the underlying patterns effectively.

## 13. What is multicollinearity, and how does it affect regression?
Multicollinearity occurs when two or more independent variables are highly correlated with each other. This makes it difficult for the model to estimate the effect of each variable accurately. It can produce unstable coefficients and reduce the interpretability of the model.

## 14. How can multicollinearity be detected?
Multicollinearity can be detected using a Correlation Matrix or Variance Inflation Factor (VIF). A high correlation between variables or a VIF value greater than 5 or 10 usually indicates multicollinearity. Removing highly correlated features can improve the model.

## 15. What is regularization, and why is it used?
Regularization is a technique used to reduce overfitting by adding a penalty to the cost function. It prevents the model from assigning very large coefficients to features. This helps improve the model's ability to generalize to new data.

## 16. What is the difference between Ridge, Lasso, and Elastic Net regression?
Ridge Regression uses L2 regularization and reduces the size of coefficients without making them zero. Lasso Regression uses L1 regularization and can set some coefficients to zero, performing feature selection. Elastic Net combines both L1 and L2 regularization to achieve the advantages of both methods.

## 17. How does Lasso regression perform feature selection?
Lasso regression applies an L1 penalty to the regression coefficients. During training, it shrinks less important feature coefficients to exactly zero. As a result, only the most useful features remain in the model, making it simpler and easier to interpret.

## 18. What is polynomial regression?
Polynomial regression is an extension of linear regression that models nonlinear relationships by adding polynomial terms such as x², x³, and higher powers. It is useful when the data follows a curved trend instead of a straight line.

## 19. How do outliers affect a regression model?
Outliers are data points that differ significantly from the rest of the dataset. They can strongly influence the regression line, resulting in incorrect predictions and higher error values. Detecting and handling outliers improves model accuracy.

## 20. How would you evaluate the performance of a regression model?
Regression models are commonly evaluated using MAE, MSE, RMSE, R-squared, and Adjusted R-squared. Residual analysis and cross-validation are also used to check whether the model generalizes well to unseen data. A good regression model should have low error values and a high R-squared score.
