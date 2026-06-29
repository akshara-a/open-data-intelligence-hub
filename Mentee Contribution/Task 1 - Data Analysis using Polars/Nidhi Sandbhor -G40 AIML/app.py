import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# Page Config
st.set_page_config(
    page_title="Travel Industry Analytics Platform",
    layout="wide"
)

# Load Data
df = pd.read_csv("clean_tourism.csv")

# Clean Guests Column
df["Guests"] = df["Guests"].astype(str).str.replace(",", "")
df["Guests"] = pd.to_numeric(df["Guests"], errors="coerce")

# Convert Year to int
df["Year"] = pd.to_numeric(df["Year"])

# Sidebar
st.sidebar.title("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All Countries"] + sorted(df["Country"].unique())
)

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Year"].unique())
)

# Filter Data
if country == "All Countries":
    filtered_df = df
else:
    filtered_df = df[df["Country"] == country]

# Title
st.title("🌍 Travel Industry Analytics Platform")

# KPIs
total_guests = filtered_df["Guests"].sum()
total_countries = filtered_df["Country"].nunique()
avg_guests = int(filtered_df["Guests"].mean())

col1, col2, col3 = st.columns(3)

col1.metric("Total Guests", f"{int(total_guests):,}")
col2.metric("Countries", total_countries)
col3.metric("Average Guests", f"{avg_guests:,}")

max_country = (
    df.groupby("Country")["Guests"]
    .sum()
    .idxmax()
)

st.info(f"🌟 Highest Tourism Country: {max_country}")

# -----------------------------
# Top 10 Countries by Guests
# -----------------------------
st.subheader("🏆 Top 10 Countries by Guests")

top_countries = (
    df[df["Year"] == year]
    .groupby("Country")["Guests"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1 = px.bar(
    x=top_countries.index,
    y=top_countries.values,
    labels={"x": "Country", "y": "Guests"},
    title=f"Top 10 Countries in {year}"
)

st.plotly_chart(fig1, use_container_width=True)
st.subheader("🥧 Tourism Share by Country")

top10 = (
    df.groupby("Country")["Guests"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig_pie = px.pie(
    top10,
    names="Country",
    values="Guests"
)

st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# Global Tourism Trend
# -----------------------------
st.subheader("📈 Global Tourism Trend")

year_data = (
    df.groupby("Year")["Guests"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    year_data,
    x="Year",
    y="Guests",
    markers=True,
    title="Global Tourism Trend"
)

st.plotly_chart(fig2, use_container_width=True)
st.subheader("🌍 Tourism World Map")

country_map = (
    df.groupby("Country")["Guests"]
    .sum()
    .reset_index()
)

fig_map = px.choropleth(
    country_map,
    locations="Country",
    locationmode="country names",
    color="Guests",
    hover_name="Country"
)

st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------
# Country Tourism Trend
# -----------------------------
if country != "All Countries":

    st.subheader(f"📊 {country} Tourism Trend")

    fig3 = px.line(
        filtered_df,
        x="Year",
        y="Guests",
        markers=True,
        title=f"{country} Guest Trend"
    )

    st.plotly_chart(fig3, use_container_width=True)
    
    # -----------------------------
# Country Comparison
# -----------------------------
st.subheader("⚔️ Country Comparison")

compare_countries = st.multiselect(
    "Select Countries to Compare",
    sorted(df["Country"].unique())
)

if len(compare_countries) > 0:

    compare_df = df[df["Country"].isin(compare_countries)]

    fig_compare = px.line(
        compare_df,
        x="Year",
        y="Guests",
        color="Country",
        markers=True,
        title="Country Comparison"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

# -----------------------------
# Year Analysis
# -----------------------------
st.subheader(f"📅 Top Countries in {year}")

year_df = df[df["Year"] == year]

top_year = (
    year_df.groupby("Country")["Guests"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4 = px.bar(
    x=top_year.index,
    y=top_year.values,
    labels={"x": "Country", "y": "Guests"},
    title=f"Top Countries in {year}"
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# COVID Impact Analysis
# -----------------------------
st.subheader("🦠 COVID Impact Analysis (2019-2022)")

covid_df = df[df["Year"].isin([2019, 2020, 2021, 2022])]

covid_trend = (
    covid_df.groupby("Year")["Guests"]
    .sum()
    .reset_index()
)

fig5 = px.line(
    covid_trend,
    x="Year",
    y="Guests",
    markers=True,
    title="Tourism Before and After COVID"
)
fig5.update_xaxes(
    tickmode="linear",
    dtick=1
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# Tourism Forecast (2023-2025)
# -----------------------------
st.subheader("🔮 Experimental Tourism Forecast (2023-2025)")
st.caption(
    "Predictions generated using Linear Regression based on historical tourism data."
)
forecast_data = (
    df.groupby("Year")["Guests"]
    .sum()
    .reset_index()
)

X = forecast_data[["Year"]]
y = forecast_data["Guests"]

model = LinearRegression()
model.fit(X, y)

future_years = pd.DataFrame({
    "Year": [2023, 2024, 2025]
})

predictions = model.predict(future_years)

forecast_df = pd.DataFrame({
    "Year": [2023, 2024, 2025],
    "Predicted Guests": predictions.astype(int)
})

actual_df = forecast_data.copy()
actual_df["Type"] = "Actual"

future_df = forecast_df.rename(
    columns={"Predicted Guests": "Guests"}
)
future_df["Type"] = "Predicted"

combined_df = pd.concat(
    [actual_df, future_df],
    ignore_index=True
)

fig6 = px.line(
    combined_df,
    x="Year",
    y="Guests",
    color="Type",
    markers=True,
    title="Tourism Forecast (2023-2025)"
)
st.metric(
    "Expected Guests in 2025",
    f"{int(predictions[2]):,}"
)

st.plotly_chart(fig6, use_container_width=True)

st.dataframe(forecast_df)  
forecast_csv = forecast_df.to_csv(index=False)

st.download_button(
    "📥 Download Forecast",
    forecast_csv,
    "forecast.csv",
    "text/csv"
) 

st.subheader("🏆 Country Rankings")

ranking = (
    df.groupby("Country")["Guests"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

ranking.index += 1

st.dataframe(ranking)


# -----------------------------
# Top 5 Countries Table
st.subheader("🏅 Top 5 Countries")

top5 = (
    df.groupby("Country")["Guests"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

# Format Guests column
top5["Guests"] = top5["Guests"].astype(int)
top5["Guests"] = top5["Guests"].apply(lambda x: f"{x:,}")

st.table(top5)

st.subheader("🌍 Country Insights")

top_country = (
    df.groupby("Country")["Guests"]
    .sum()
    .idxmax()
)

top_value = (
    df.groupby("Country")["Guests"]
    .sum()
    .max()
)

st.success(
    f"Highest Tourism Country: {top_country} ({int(top_value):,} Guests)"
)

# -----------------------------
# Dataset
# -----------------------------
st.subheader("📄 Dataset")

st.dataframe(filtered_df)
search = st.text_input("🔍 Search Country")

st.subheader("📋 Key Insights")

st.success("""
• The COVID-19 pandemic caused a major drop in tourism activity in 2020.
• Tourism gradually recovered during 2021 and 2022.
• Japan, Germany, and France recorded the highest number of tourist guests.
• Historical tourism data was analyzed to identify trends and patterns.
• A Linear Regression model was applied to predict tourism demand for 2023–2025.
""")
# Download Dataset
# -----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="tourism_data.csv",
    mime="text/csv"
)