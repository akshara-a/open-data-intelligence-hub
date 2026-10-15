import pandas as pd
import matplotlib.pyplot as plt
import joblib



df = pd.read_csv(
    "data/heart.csv"
)



X = df.drop(
    "target",
    axis=1
)



model = joblib.load(
    "models/heart_model.pkl"
)



importance = pd.DataFrame({

    "Feature":X.columns,

    "Importance":
    model.feature_importances_

})


importance = importance.sort_values(
    by="Importance",
    ascending=False
)



print(importance)



plt.figure(figsize=(10,6))


plt.bar(
    importance["Feature"],
    importance["Importance"]
)


plt.xticks(rotation=90)

plt.title(
    "Feature Importance"
)


plt.show()
