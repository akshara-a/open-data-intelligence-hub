from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def perform_clustering(scaled_data):

    scores = []

    for k in range(2, 8):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(scaled_data)

        score = silhouette_score(scaled_data, labels)
        scores.append(score)

        print(f"k={k}  Silhouette Score={score:.3f}")

    best_k = scores.index(max(scores)) + 2

    print(f"\nBest number of clusters = {best_k}")

    final_model = KMeans(n_clusters=best_k, random_state=42, n_init=10)

    return final_model.fit_predict(scaled_data)