import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Load Dataset
df = pd.read_excel("data/WHR26_Data_Figure_2.1.xlsx")

print("Original Shape:", df.shape)

# Keep only rows where all ML features exist
model_df = df.dropna(
    subset=[
        "Explained by: Log GDP per capita",
        "Explained by: Social support",
        "Explained by: Healthy life expectancy",
        "Explained by: Freedom to make life choices",
        "Explained by: Generosity",
        "Explained by: Perceptions of corruption",
        "Dystopia + residual"
    ]
)

print("Model Shape:", model_df.shape)

# Features (7 Features)
features = [
    "Explained by: Log GDP per capita",
    "Explained by: Social support",
    "Explained by: Healthy life expectancy",
    "Explained by: Freedom to make life choices",
    "Explained by: Generosity",
    "Explained by: Perceptions of corruption",
    "Dystopia + residual"
]

X = model_df[features]

# Target
y = model_df["Life evaluation (3-year average)"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nModel Performance")
print("-------------------")
print("MAE:", round(mae, 4))
print("RMSE:", round(rmse, 4))
print("R2 Score:", round(r2, 4))

# Save Model
joblib.dump(model, "models/happiness_model.pkl")
print("\nModel saved successfully!")