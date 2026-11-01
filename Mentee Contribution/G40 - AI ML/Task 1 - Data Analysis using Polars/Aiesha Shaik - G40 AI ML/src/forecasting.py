from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_indicator(data):

    if len(data) < 5:
        return None

    years = np.array(
        data["YEAR"]
    ).reshape(-1, 1)

    values = np.array(
        data["VALUE"]
    )

    model = LinearRegression()

    model.fit(
        years,
        values
    )

    pred2030 = model.predict(
        [[2030]]
    )[0]

    return round(pred2030, 2)