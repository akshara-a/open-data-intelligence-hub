import streamlit as st
import pandas as pd
import plotly.express as px

from models.predictor import predict_future

df = pd.read_csv("literacy_data.csv")

df = df[['geoUnit','year','value']]
df.columns = ['Country','Year','LiteracyRate']

st.title("🤖 AI Forecasting")

country = st.selectbox(
    "Country",
    sorted(df.Country.unique())
)

country_df = df[
    df.Country == country
]

if len(country_df) > 2:

    years,predictions = predict_future(country_df)

    forecast = pd.DataFrame({
        "Year":years,
        "Prediction":predictions
    })

    st.dataframe(forecast)

    fig = px.line(
        forecast,
        x="Year",
        y="Prediction",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )