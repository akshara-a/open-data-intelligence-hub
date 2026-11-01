
AI/ML Interview Questions: Regression
1. What is regression in machine learning, and when is it used?
Ans.Regression is a supervised learning technique used to predict a continuous, numerical value. we use it whenever we need to estimate an exact quantity rather than sorting data into categories. Good examples include forecasting next month's sales, predicting house prices based on location, or estimating crop yields using weather patterns.

2. What is the difference between simple linear regression and multiple linear regression?
Ans.The main difference comes down to the number of inputs. Simple linear regression uses just one independent variable to predict a single target variable. Multiple linear regression uses two or more independent variables to predict that same single target variable.

3. What assumptions are made by linear regression?
Ans.Linear regression relies on four main assumptions to work reliably:
Linearity: The relationship between your inputs and our output must follow a straight-line pattern.
Independence: The error or mistake in one prediction should not depend on or affect the error in another prediction.
Normality: The errors made by the model should be normally distributed around zero.
Homoscedasticity: The variance or spread of our errors needs to stay constant across all data points.

4. What is the difference between a dependent variable and an independent variable?
Ans.An independent variable is the input or feature that we measure and feed into the model, usually labeled as X. A dependent variable is the final target or output you are trying to predict, usually labeled as Y. Its value depends entirely on what happens to the independent variables.

5. What do the slope and intercept represent in a linear regression model?
Ans.The intercept is the baseline starting value of our target variable when all your inputs are set to zero. The slope represents the rate of change, showing exactly how much and in what direction the target variable will shift for every one-unit increase in an input variable.

6. What is the purpose of the cost function in regression?
Ans.The cost function acts as a mathematical scorecard that measures how many mistakes your model is making during training. The ultimate goal of training a regression model is to tweak the parameters until this cost value is as low as possible, meaning the predictions are highly accurate.

7. What is Mean Squared Error, and why is it commonly used for regression?
Ans.Mean Squared Error calculates the average of the squared differences between the actual values and the model's predictions. It is popular because squaring the errors removes negative signs, makes the math much easier to optimize, and heavily penalizes large mistakes so the model learns to avoid massive errors.

8. What is the difference between Mean Absolute Error, Mean Squared Error, and Root Mean Squared Error?
Ans.MAE calculates the simple average of the absolute errors and is highly robust against outliers. MSE squares the errors to punish bigger mistakes, but it changes the measurement unit into units squared. RMSE takes the square root of MSE, keeping the strict penalty for large errors while bringing the final metric back to the original unit so it is easy to understand.

9. What is the R-squared score, and how should it be interpreted?
Ans.The R-squared score tells you what percentage of the variation in your target variable can be explained by our input features. For example, an R-squared score of 0.85 means your features successfully account for 85 percent of the variation in the data, while the remaining 15 percent is just unexplained noise.

10. What is adjusted R-squared, and why is it useful?
Ans.Standard R-squared has a flaw where it will artificially go up every time you add a new input feature, even if that feature is complete garbage. Adjusted R-squared fixes this by penalizing the score for adding useless features, meaning it will only increase if a new variable genuinely improves the model's performance.

11. What is overfitting in a regression model?
Ans.Overfitting happens when a model learns the training data a bit too well, accidentally memorizing both the real underlying patterns and the random noise. Because it memorizes the training data, it performs perfectly on your training set but fails completely when you give it new, unseen test data.

12. What is underfitting in a regression model?
Ans.Underfitting happens when a model is way too simple to capture the underlying trend of the data. An example would be trying to force a perfectly straight line through data that naturally curves. As a result, the model performs poorly on both the training data and the test data.

13. What is multicollinearity, and how does it affect regression?
Ans.Multicollinearity occurs when two or more of our input features are heavily correlated with each other. While it does not hurt the overall predictive power of the model, it causes the model's internal coefficients to become highly unstable and makes it incredibly difficult to figure out which feature is actually driving the predictions.

14. How can multicollinearity be detected?
Ans.We can spot multicollinearity using two main approaches. The first is a correlation matrix, where we look for high correlation scores between inputs. The second is the Variance Inflation Factor. A VIF value above 5 flags moderate collinearity, while a value above 10 points to severe multicollinearity that needs to be fixed.

15. What is regularization, and why is it used?
Ans.Regularization is a technique used to stop a model from overfitting. It does this by adding a penalty to the cost function that discourages the model from getting too complex or relying too heavily on a single feature, sacrificing a tiny bit of training accuracy for much better performance on new data.

16. What is the difference between Ridge, Lasso, and Elastic Net regression?
Ans.Ridge regression adds a penalty based on the square of the coefficients, shrinking them close to zero but never erasing them. Lasso regression adds a penalty based on the absolute value of the coefficients, which can shrink less important features all the way to absolute zero. Elastic Net simply combines both techniques to get the best of both worlds.

17. How does Lasso regression perform feature selection?
Ans.Because of the specific geometry of the absolute value penalty used in Lasso, the optimization process naturally forces the coefficients of less important or redundant features down to exactly zero. Once a feature's weight hits zero, it is completely dropped from the model, effectively performing automatic feature selection.

18. What is polynomial regression?
Ans.Polynomial regression is a variation of linear regression used when the relationship between our inputs and outputs is curved rather than a straight line. By adding powers of your original features, the model can successfully fit non-linear data while still keeping the underlying math linear in terms of its coefficients.

19. How do outliers affect a regression model?
Ans.Because standard regression works by minimizing squared errors, a single extreme outlier sitting far away from the rest of the data points will heavily pull the regression line toward itself. This tilts the entire line, ruins the slope, and hurts the model's accuracy for all the normal data points.

20. How would you evaluate the performance of a regression model?
Ans.To evaluate a model thoroughly, we should combine numerical metrics like MAE, RMSE, and Adjusted R-squared to gauge error sizes and variance. Alongside these, you should look at a residual plot to ensure your errors are randomly scattered around the zero line without forming any distinct, non-random patterns.

