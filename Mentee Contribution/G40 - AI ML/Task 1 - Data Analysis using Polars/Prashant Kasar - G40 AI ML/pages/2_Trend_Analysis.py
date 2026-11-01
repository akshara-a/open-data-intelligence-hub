import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("literacy_data.csv")

df = df[['geoUnit','year','value']]
df.columns = ['Country','Year','LiteracyRate']

st.title("📈 Trend Analysis")

country = st.selectbox(
    "Select Country",
    sorted(df.Country.unique())
)

country_df = df[
    df.Country == country
]

fig = px.line(
    country_df,
    x="Year",
    y="LiteracyRate",
    markers=True,
    title=f"{country} Literacy Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

c1,c2,c3 = st.columns(3)

c1.metric(
    "Maximum Literacy",
    round(country_df.LiteracyRate.max(),2)
)

c2.metric(
    "Minimum Literacy",
    round(country_df.LiteracyRate.min(),2)
)

c3.metric(
    "Average Literacy",
    round(country_df.LiteracyRate.mean(),2)
)