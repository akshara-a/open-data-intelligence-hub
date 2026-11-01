import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("literacy_data.csv")

df = df[['geoUnit','year','value']]
df.columns = ['Country','Year','LiteracyRate']

st.title("🌍 Country Comparison")

countries = st.multiselect(
    "Choose Countries",
    sorted(df.Country.unique())
)

if countries:

    compare = df[
        df.Country.isin(countries)
    ]

    fig = px.line(
        compare,
        x="Year",
        y="LiteracyRate",
        color="Country",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )