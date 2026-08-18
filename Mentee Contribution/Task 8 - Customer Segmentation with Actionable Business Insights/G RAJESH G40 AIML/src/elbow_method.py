import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def plot_elbow(scaled_data):
    inertia = []

    for k in range(1, 11):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(scaled_data)
        inertia.append(model.inertia_)

    plt.figure(figsize=(8,5))
    plt.plot(range(1,11), inertia, marker="o")
    plt.title("Elbow Method")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.grid(True)

    plt.savefig("outputs/charts/elbow_method.png")
    plt.show()