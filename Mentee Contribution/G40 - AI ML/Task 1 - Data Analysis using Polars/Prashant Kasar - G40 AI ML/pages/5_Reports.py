import streamlit as st
import pandas as pd

df = pd.read_csv("literacy_data.csv")

df = df[['geoUnit','year','value']]
df.columns = ['Country','Year','LiteracyRate']

st.title("📄 Reports & Downloads")

country = st.selectbox(
    "Country",
    sorted(df.Country.unique())
)

country_df = df[
    df.Country == country
]

st.dataframe(country_df)

csv = country_df.to_csv(
    index=False
)

st.download_button(
    "Download CSV Report",
    csv,
    file_name=f"{country}.csv"
)