import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range(start="2000-01-01", end="2024-12-31", freq="ME")

regions = ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Southern Ocean"]
records = []

for date in dates:
    for region in regions:
        year_factor = (date.year - 2000) * 0.03
        seasonal = np.sin(2 * np.pi * date.month / 12) * 1.2
        noise = np.random.normal(0, 0.3)

        base_temps = {
            "Pacific Ocean": 18.5, "Atlantic Ocean": 16.2,
            "Indian Ocean": 22.1, "Arctic Ocean": -1.5, "Southern Ocean": 4.8
        }
        base_temp = base_temps[region]

        records.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Region": region,
            "Sea_Surface_Temperature_C": round(base_temp + year_factor + seasonal + noise, 2),
            "Sea_Level_Rise_mm": round(3.3 * (date.year - 2000) + np.random.normal(0, 2), 2),
            "Ocean_pH": round(8.18 - (date.year - 2000) * 0.002 + np.random.normal(0, 0.01), 3),
            "Coral_Bleaching_Risk": round(min(100, max(0, 20 + year_factor * 15 + np.random.normal(0, 5))), 1),
            "Salinity_PSU": round(35.0 + np.random.normal(0, 0.5), 2),
            "Dissolved_Oxygen_mgL": round(7.5 - year_factor * 0.5 + np.random.normal(0, 0.3), 2),
            "Wave_Height_m": round(max(0.1, 1.5 + np.random.normal(0, 0.8)), 2),
            "Marine_Heat_Wave_Days": max(0, int(np.random.poisson(year_factor * 5 + 2))),
        })

df = pd.DataFrame(records)
df.to_csv("marine_climate_data.csv", index=False)
print(f"Generated {len(df)} records across {len(regions)} regions from 2000-2024")
print(df.head())
