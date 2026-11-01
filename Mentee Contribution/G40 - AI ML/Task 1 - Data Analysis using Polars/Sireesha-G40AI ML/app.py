import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Climate Anomaly Detection")

st.title("🌍 Climate Anomaly Detection")
st.write("Detect unusual weather patterns compared to historical averages")

# Load Data
historical = pd.read_csv("historical_weather.csv")
current = pd.read_csv("current_weather.csv")

# Historical Average
historical_avg = historical["Temperature"].mean()

# Anomaly Calculation
current["Difference"] = current["Temperature"] - historical_avg

threshold = 5

current["Anomaly"] = current["Difference"].apply(
    lambda x: "Yes" if abs(x) > threshold else "No"
)

st.subheader("Historical Average Temperature")
st.write(round(historical_avg, 2))

st.subheader("Current Weather Analysis")
st.dataframe(current)

#Graph
fig, ax = plt.subplots()

ax.plot(
    current["Date"],
    current["Temperature"],
    marker="o"
)

ax.axhline(
    historical_avg,
    linestyle="--"
)

ax.set_title("Temperature vs Historical Average")

st.pyplot(fig)

# Show anomalies only
anomalies = current[current["Anomaly"] == "Yes"]

st.subheader("Detected Anomalies")

if len(anomalies) > 0:
    st.dataframe(anomalies)
else:
    st.success("No anomalies detected")