from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future(country_df):

    X = country_df[['Year']]
    y = country_df['LiteracyRate']

    model = LinearRegression()
    model.fit(X, y)

    future_years = np.arange(
        country_df['Year'].max() + 1,
        country_df['Year'].max() + 6
    ).reshape(-1, 1)

    predictions = model.predict(future_years)

    return future_years.flatten(), predictions