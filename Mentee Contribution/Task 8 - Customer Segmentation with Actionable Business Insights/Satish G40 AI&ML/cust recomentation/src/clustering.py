"""K-Means clustering workflow: elbow, silhouette, assign clusters."""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def find_best_k(X_transformed, k_range=range(2, 9), out_dir="outputs/plots"):
    os.makedirs(out_dir, exist_ok=True)
    inertias = []
    silhouettes = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_transformed)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_transformed, labels))

    plt.figure()
    plt.plot(list(k_range), inertias, marker='o')
    plt.title("Elbow Method: Inertia by K")
    plt.xlabel("K")
    plt.ylabel("Inertia")
    plt.savefig(os.path.join(out_dir, "elbow_inertia.png"))
    plt.close()

    plt.figure()
    plt.plot(list(k_range), silhouettes, marker='o')
    plt.title("Silhouette Score by K")
    plt.xlabel("K")
    plt.ylabel("Silhouette Score")
    plt.savefig(os.path.join(out_dir, "silhouette_by_k.png"))
    plt.close()

    best_k = int(k_range[np.argmax(silhouettes)])
    return best_k


def run_kmeans(X_transformed, k, raw_df, out_dir="outputs"):
    os.makedirs(out_dir, exist_ok=True)
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_transformed)
    raw_df["Cluster"] = labels
    # Save cluster sizes
    cluster_sizes = raw_df["Cluster"].value_counts().sort_index()
    cluster_sizes.to_csv(os.path.join(out_dir, "cluster_sizes.csv"))

    return km, raw_df
