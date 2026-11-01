import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import plotly.express as px

from src.preprocessing import load_data
from src.forecasting import forecast_indicator

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Global Education Analytics",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🌍 Global Education Analytics Platform")

st.markdown("""
### Project Goal

Analyze UNESCO education indicators across countries,
identify trends, compare performance,
and forecast future educational outcomes.
""")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df, countries, labels = load_data()

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Country Comparison",
        "Insights",
        "Forecasting"
    ]
)

# ==================================================
# OVERVIEW PAGE
# ==================================================

if page == "Overview":

    country = st.sidebar.selectbox(
        "Country",
        sorted(
            df["COUNTRY_NAME_EN"]
            .dropna()
            .unique()
        )
    )

    indicator = st.sidebar.selectbox(
        "Indicator",
        sorted(
            df["INDICATOR_LABEL_EN"]
            .dropna()
            .unique()
        )
    )

    year = st.sidebar.selectbox(
        "Year",
        sorted(
            df["YEAR"]
            .dropna()
            .unique()
        )
    )

    # KPIs

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Countries",
        df["COUNTRY_NAME_EN"].nunique()
    )

    col2.metric(
        "Indicators",
        df["INDICATOR_LABEL_EN"].nunique()
    )

    col3.metric(
        "Average Value",
        round(df["VALUE"].mean(), 2)
    )

    # Trend Analysis

    st.subheader("📈 Trend Analysis")

    trend = df[
        (df["COUNTRY_NAME_EN"] == country)
        &
        (df["INDICATOR_LABEL_EN"] == indicator)
    ]

    fig = px.line(
        trend,
        x="YEAR",
        y="VALUE",
        markers=True,
        title=f"{country} - {indicator}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Top Countries

    st.subheader("🏆 Top 10 Countries")

    top10 = df[
        (df["INDICATOR_LABEL_EN"] == indicator)
        &
        (df["YEAR"] == year)
    ].sort_values(
        by="VALUE",
        ascending=False
    ).head(10)

    fig2 = px.bar(
        top10,
        x="COUNTRY_NAME_EN",
        y="VALUE",
        title=f"Top Countries ({year})"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Dataset Preview

    st.subheader("📊 Dataset Preview")

    st.dataframe(
        df.head(100)
    )

    # Download Button

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Dataset",
        data=csv,
        file_name="education_analysis.csv",
        mime="text/csv"
    )

# ==================================================
# COUNTRY COMPARISON PAGE
# ==================================================

elif page == "Country Comparison":

    st.header("🌎 Country Comparison")

    country1 = st.selectbox(
        "Country 1",
        sorted(
            df["COUNTRY_NAME_EN"]
            .dropna()
            .unique()
        )
    )

    country2 = st.selectbox(
        "Country 2",
        sorted(
            df["COUNTRY_NAME_EN"]
            .dropna()
            .unique()
        )
    )

    indicator = st.selectbox(
        "Indicator",
        sorted(
            df["INDICATOR_LABEL_EN"]
            .dropna()
            .unique()
        )
    )

    compare = df[
        (
            df["COUNTRY_NAME_EN"]
            .isin([country1, country2])
        )
        &
        (
            df["INDICATOR_LABEL_EN"]
            == indicator
        )
    ]

    fig = px.line(
        compare,
        x="YEAR",
        y="VALUE",
        color="COUNTRY_NAME_EN",
        markers=True,
        title=f"{country1} vs {country2}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# INSIGHTS PAGE
# ==================================================

elif page == "Insights":

    st.header("📊 Education Insights")

    highest = df.loc[
        df["VALUE"].idxmax()
    ]

    lowest = df.loc[
        df["VALUE"].idxmin()
    ]

    st.success(
        f"""
        Highest Value Country:
        {highest['COUNTRY_NAME_EN']}

        Value:
        {highest['VALUE']}
        """
    )

    st.warning(
        f"""
        Lowest Value Country:
        {lowest['COUNTRY_NAME_EN']}

        Value:
        {lowest['VALUE']}
        """
    )

# ==================================================
# FORECASTING PAGE
# ==================================================

elif page == "Forecasting":

    st.header("🔮 Forecasting")

    country = st.selectbox(
        "Country",
        sorted(
            df["COUNTRY_NAME_EN"]
            .dropna()
            .unique()
        )
    )

    indicator = st.selectbox(
        "Indicator",
        sorted(
            df["INDICATOR_LABEL_EN"]
            .dropna()
            .unique()
        )
    )

    temp = df[
        (df["COUNTRY_NAME_EN"] == country)
        &
        (
            df["INDICATOR_LABEL_EN"]
            == indicator
        )
    ]

    prediction = forecast_indicator(
        temp
    )

    if prediction is not None:

        st.success(
            f"""
            Predicted Value in 2030:
            {prediction}
            """
        )

    else:

        st.error(
            "Not enough data available for forecasting."
        )
