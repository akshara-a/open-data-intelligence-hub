import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

def load_data():

    data = pd.read_csv(
        os.path.join(BASE_DIR, "data", "SDG_DATA_NOTATION.csv"),
        low_memory=False
    )

    countries = pd.read_csv(
        os.path.join(BASE_DIR, "data", "SDG_COUNTRY.csv")
    )

    labels = pd.read_csv(
        os.path.join(BASE_DIR, "data", "SDG_LABEL.csv")
    )

    # Merge country names
    data = data.merge(
        countries,
        on="COUNTRY_ID",
        how="left"
    )

    # Merge indicator names
    data = data.merge(
        labels,
        on="INDICATOR_ID",
        how="left"
    )

    return data, countries, labels