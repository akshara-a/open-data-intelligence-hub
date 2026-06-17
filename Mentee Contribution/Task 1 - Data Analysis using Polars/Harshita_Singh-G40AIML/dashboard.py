import streamlit as st
import polars as pl
import plotly.express as px



st.set_page_config(
    page_title="Global Ocean Temperature Analytics",
    page_icon="🌊",
    layout="wide"
)



st.title("🌊 Global Ocean Temperature Analytics")
st.markdown("""
Analyze long-term ocean warming trends using NOAA ERSST v5 data and Polars.
""")

yearly_avg = pl.read_csv("yearly_ocean_temperature.csv")
anomaly = pl.read_csv("temperature_anomalies.csv")
decadal = pl.read_csv("decadal_ocean_temperature.csv")
hotspots = pl.read_csv("ocean_hotspots.csv")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Years Covered",
        int(yearly_avg["year"].max() - yearly_avg["year"].min())
    )

with col2:
    st.metric(
        "Average SST",
        round(yearly_avg["avg_sst"].mean(), 2)
    )

with col3:
    st.metric(
        "Hotspots Identified",
        len(hotspots)
    )
st.header("📈 Global Ocean Temperature Trend")

fig1 = px.line(
    yearly_avg.to_pandas(),
    x="year",
    y="avg_sst",
    title="Global Ocean Temperature Trend"
)

st.plotly_chart(fig1, use_container_width=True)
st.header("🔥 Temperature Anomalies")

fig2 = px.line(
    anomaly.to_pandas(),
    x="year",
    y="avg_anomaly",
    title="Ocean Temperature Anomaly"
)

st.plotly_chart(fig2, use_container_width=True)

st.header("📊 Decadal Warming Analysis")

fig3 = px.bar(
    decadal.to_pandas(),
    x="decade",
    y="avg_sst",
    title="Average SST by Decade"
)

st.plotly_chart(fig3, use_container_width=True)
st.header("🌍 Ocean Hotspots")

fig4 = px.scatter(
    hotspots.head(100).to_pandas(),
    x="lon",
    y="lat",
    size="avg_temp",
    color="avg_temp",
    title="Top Ocean Hotspots"
)

st.plotly_chart(fig4, use_container_width=True)
st.header("📄 Top Hotspots")

st.dataframe(
    hotspots.head(50).to_pandas(),
    use_container_width=True
)
st.markdown("---")
st.markdown(
    "Built with NOAA ERSST v5 + Polars + Streamlit"
)
