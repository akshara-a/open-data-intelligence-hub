import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_feature_importance(model, feature_names):

    importance = pd.Series(
        model.feature_importances_,
        index=feature_names
    ).sort_values(ascending=False)

    os.makedirs("outputs/charts", exist_ok=True)

    plt.figure(figsize=(10,6))
    importance.plot(kind="bar")

    plt.title("Feature Importance")
    plt.xlabel("Features")
    plt.ylabel("Importance")

    plt.tight_layout()

    plt.savefig("outputs/charts/feature_importance.png")
    plt.close()

    print("Feature Importance graph saved successfully!")