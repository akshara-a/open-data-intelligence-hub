from models.popularity import popularity_recommendations
from models.content_based import recommend as content_recommend
from models.collaborative import recommend_products as collaborative_recommend
from models.svd_model import recommend_products as svd_recommend
from models.knn_model import recommend_products as knn_recommend

import pandas as pd


def hybrid_recommend(product_name, username):

    recommendations = []

    # ------------------------
    # Popularity
    # ------------------------
    try:
        pop = popularity_recommendations(5)
        recommendations.extend(pop["product_name"].tolist())
    except Exception:
        pass

    # ------------------------
    # Content-Based
    # ------------------------
    try:
        content = content_recommend(product_name, 5)
        recommendations.extend(content["product_name"].tolist())
    except Exception:
        pass

    # ------------------------
    # Collaborative
    # ------------------------
    try:
        collaborative = collaborative_recommend(username, 5)
        recommendations.extend([p[0] for p in collaborative])
    except Exception:
        pass

    # ------------------------
    # SVD
    # ------------------------
    try:
        svd = svd_recommend(username, 5)
        recommendations.extend([p[0] for p in svd])
    except Exception:
        pass

    # ------------------------
    # KNN
    # ------------------------
    try:
        knn = knn_recommend(username, 5)
        recommendations.extend([p[0] for p in knn])
    except Exception:
        pass

    # Remove duplicates while preserving order
    recommendations = list(dict.fromkeys(recommendations))

    return pd.DataFrame(
        {"Recommended Products": recommendations}
    )


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    username = "Cristina M"

    product = "Kindle Paperwhite"

    result = hybrid_recommend(product, username)

    print(result)