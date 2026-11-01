def top_countries(df, indicator, year):

    filtered = df[
        (df["INDICATOR_ID"] == indicator)
        & (df["YEAR"] == year)
    ]

    return filtered.sort_values(
        by="VALUE",
        ascending=False
    ).head(10)


def global_average(df):

    return round(
        df["VALUE"].mean(),
        2
    )