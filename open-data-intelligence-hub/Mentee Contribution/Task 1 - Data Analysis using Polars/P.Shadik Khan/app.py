import streamlit as st
import pandas as pd

st.title("Extinction Trend Analytics")

df = pd.read_csv("data.csv")

st.subheader("Dataset")
st.dataframe(df)

st.subheader("Category Distribution")
st.bar_chart(df["Category"].value_counts())

st.subheader("Population Trend Distribution")
st.bar_chart(df["Population_Trend"].value_counts())

st.subheader("Dataset Summary")
st.write("Total Species:", len(df))

st.subheader("Category Counts")
st.dataframe(df["Category"].value_counts())

st.subheader("Population Trend Counts")
st.dataframe(df["Population_Trend"].value_counts())

st.subheader("Search Species")
search = st.text_input("Enter Species Name")

if search:
    result = df[df["Species"].astype(str).str.contains(search, case=False, na=False)]
    st.dataframe(result)

if st.checkbox("Show Complete Dataset"):
    st.dataframe(df)

st.subheader("Top 5 Records")
st.dataframe(df.head())

st.subheader("Last 5 Records")
st.dataframe(df.tail())
