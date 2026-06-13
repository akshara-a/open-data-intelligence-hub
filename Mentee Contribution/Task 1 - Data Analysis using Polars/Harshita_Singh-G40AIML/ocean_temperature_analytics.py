import xarray as xr
import polars as pl
import matplotlib.pyplot as plt

ds = xr.open_dataset("data/sst.mnmean.nc")
df = ds["sst"].to_dataframe().reset_index()
df = pl.from_pandas(df)
df = df.drop_nulls()
df = df.with_columns(
    pl.col("time").dt.year().alias("year")
)


yearly_avg = (
    df.group_by("year")
    .agg(
        pl.mean("sst").alias("avg_sst")
    )
    .sort("year")
)

print(yearly_avg)

yearly_avg.write_csv("outputs/yearly_ocean_temperature.csv")

print("CSV Saved Successfully!")

years = yearly_avg["year"]
temps = yearly_avg["avg_sst"]

plt.figure(figsize=(12,6))
plt.plot(years, temps)

plt.title("Global Ocean Temperature Trend (1854-Present)")
plt.xlabel("Year")
plt.ylabel("Average SST (°C)")
plt.grid(True)

plt.show()
# ==================================
# TEMPERATURE ANOMALY ANALYSIS
# ==================================

global_mean = df["sst"].mean()

print(f"\nGlobal Mean SST: {global_mean:.2f} °C")

df = df.with_columns(
    (pl.col("sst") - global_mean).alias("anomaly")
)

anomaly_summary = (
    df.group_by("year")
    .agg(
        pl.mean("anomaly").alias("avg_anomaly")
    )
    .sort("year")
)

print("\nAnomaly Summary:")
print(anomaly_summary.head())
plt.figure(figsize=(12,6))

plt.plot(
    anomaly_summary["year"],
    anomaly_summary["avg_anomaly"]
)

plt.title("Global Ocean Temperature Anomaly")
plt.xlabel("Year")
plt.ylabel("Temperature Anomaly (°C)")
plt.grid(True)

plt.show()

df = df.with_columns(
    ((pl.col("year") // 10) * 10).alias("decade")
)

decadal_avg = (
    df.group_by("decade")
    .agg(
        pl.mean("sst").alias("avg_sst")
    )
    .sort("decade")
)

print("\nDecadal Ocean Temperatures:")
print(decadal_avg)
plt.figure(figsize=(12,6))

plt.bar(
    decadal_avg["decade"],
    decadal_avg["avg_sst"]
)

plt.title("Average Ocean Temperature by Decade")
plt.xlabel("Decade")
plt.ylabel("Average SST (°C)")
plt.grid(True)

plt.show()

hotspots = (
    df.group_by(["lat", "lon"])
    .agg(
        pl.mean("sst").alias("avg_temp")
    )
    .sort("avg_temp", descending=True)
)

print("\nTop 20 Ocean Hotspots")
print(hotspots.head(20))
yearly_avg.write_csv("yearly_ocean_temperature.csv")
anomaly_summary.write_csv("temperature_anomalies.csv")
decadal_avg.write_csv("decadal_ocean_temperature.csv")
hotspots.head(100).write_csv("ocean_hotspots.csv")

print("All CSV files saved successfully!")
import plotly.express as px

fig = px.line(
    yearly_avg.to_pandas(),
    x="year",
    y="avg_sst",
    title="Global Ocean Temperature Trend (Interactive)"
)

fig.show()
