from sklearn.cluster import KMeans

def train_kmeans(data, clusters=4):
    model = KMeans(
        n_clusters=clusters,
        random_state=42,
        n_init=10
    )
    model.fit(data)
    return model