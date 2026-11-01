import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

df = pd.read_csv("literacy_data.csv")

df = df[['geoUnit','year','value']]
df.columns = ['Country','Year','LiteracyRate']

st.title("📊 Global Dashboard")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Countries",
    df.Country.nunique()
)

c2.metric(
    "Records",
    len(df)
)

c3.metric(
    "Start Year",
    int(df.Year.min())
)

c4.metric(
    "Latest Year",
    int(df.Year.max())
)

st.divider()

st.subheader("🏆 Top Literacy Countries")

latest = df[df.Year == df.Year.max()]

top10 = latest.sort_values(
    "LiteracyRate",
    ascending=False
).head(10)

st.dataframe(top10)