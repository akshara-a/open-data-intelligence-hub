

### 1. What is regression in machine learning, and when is it used?

Regression is a supervised machine learning algorithm used to predict continuous numerical values. It learns the relationship between input features and the target variable. It is commonly used for predicting values such as house prices, salaries, sales, and temperatures.

---

### 2. What is the difference between simple linear regression and multiple linear regression?

Simple linear regression uses only one independent variable to predict the dependent variable. Multiple linear regression uses two or more independent variables for prediction. Multiple regression is more suitable when several factors influence the target value.

---

### 3. What assumptions are made by linear regression?

Linear regression assumes that there is a linear relationship between the input variables and the output variable. It also assumes that the errors are independent and normally distributed with constant variance. Additionally, the independent variables should not be highly correlated with each other.

---

### 4. What is the difference between a dependent variable and an independent variable?

The dependent variable is the value that the model tries to predict. The independent variables are the input features used to make the prediction. For example, house price is the dependent variable, while area and number of bedrooms are independent variables.

---

### 5. What do the slope and intercept represent in a linear regression model?

The slope represents how much the dependent variable changes when the independent variable increases by one unit. The intercept represents the predicted value of the dependent variable when the independent variable is zero. Together, they define the regression equation.

---

### 6. What is the purpose of the cost function in regression?

The cost function measures the difference between the predicted values and the actual values. It helps evaluate how well the model is performing. During training, the objective is to minimize the cost function to improve prediction accuracy.

---

### 7. What is Mean Squared Error (MSE), and why is it commonly used for regression?

Mean Squared Error (MSE) is the average of the squared differences between actual and predicted values. It penalizes larger errors more heavily than smaller ones. It is commonly used because it is easy to calculate and works well with optimization algorithms.

---

### 8. What is the difference between Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE)?

MAE calculates the average absolute difference between actual and predicted values. MSE calculates the average squared difference, giving more importance to large errors. RMSE is the square root of MSE and expresses the error in the same units as the target variable, making it easier to interpret.

---

### 9. What is the R-squared score, and how should it be interpreted?

R-squared measures how well the regression model explains the variation in the target variable. Its value ranges from 0 to 1, where higher values indicate a better fit. For example, an R-squared value of 0.90 means the model explains 90% of the variation in the data.

---

### 10. What is adjusted R-squared, and why is it useful?

Adjusted R-squared is a modified version of R-squared that considers the number of independent variables in the model. It increases only when a new feature improves the model significantly. This helps prevent unnecessary features from making the model appear better than it actually is.

---

### 11. What is overfitting in a regression model?

Overfitting occurs when the model learns the training data too closely, including its noise and outliers. As a result, it performs very well on training data but poorly on unseen data. This reduces the model's ability to generalize.

---

### 12. What is underfitting in a regression model?

Underfitting occurs when the model is too simple to capture the underlying pattern in the data. It performs poorly on both the training and testing datasets. This usually happens when the model has not learned enough from the data.

---

### 13. What is multicollinearity, and how does it affect regression?

Multicollinearity occurs when two or more independent variables are highly correlated with each other. This makes it difficult to determine the individual effect of each feature. It can lead to unstable coefficient estimates and reduce the reliability of the model.

---

### 14. How can multicollinearity be detected?

Multicollinearity can be detected using a correlation matrix or the Variance Inflation Factor (VIF). A high correlation coefficient or a high VIF value indicates multicollinearity. These methods help identify redundant features in the dataset.

---

### 15. What is regularization, and why is it used?

Regularization is a technique used to reduce the complexity of a regression model by adding a penalty to the loss function. It helps prevent overfitting and improves the model's ability to generalize. Common regularization methods include Ridge and Lasso regression.

---

### 16. What is the difference between Ridge, Lasso, and Elastic Net regression?

Ridge regression uses L2 regularization and reduces the magnitude of coefficients without making them zero. Lasso regression uses L1 regularization and can reduce some coefficients to zero, which performs feature selection. Elastic Net combines both L1 and L2 regularization to gain the advantages of both methods.

---

### 17. How does Lasso regression perform feature selection?

Lasso regression uses L1 regularization, which adds a penalty to the model coefficients. During training, it shrinks some coefficients to exactly zero. Features with zero coefficients are automatically removed, making the model simpler.

---

### 18. What is polynomial regression?

Polynomial regression is an extension of linear regression that models nonlinear relationships between variables. It adds polynomial terms such as squared or cubic features to the regression equation. This allows the model to fit curved patterns in the data.

---

### 19. How do outliers affect a regression model?

Outliers are data points that are very different from the rest of the dataset. They can significantly influence the regression line and reduce prediction accuracy. Detecting and handling outliers helps improve the performance of the regression model.

---

### 20. How would you evaluate the performance of a regression model?

The performance of a regression model is evaluated using metrics such as MAE, MSE, RMSE, and R-squared. Lower values of MAE, MSE, and RMSE indicate better prediction accuracy. A higher R-squared value indicates that the model explains a larger portion of the variation in the data.
