import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Load embedding model
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(
    MODEL_NAME
)


# --------------------------------------------------
# Generate embedding
# --------------------------------------------------

def generate_embedding(text):

    embedding = model.encode(
        text
    )

    return embedding


# --------------------------------------------------
# Generate embeddings for multiple texts
# --------------------------------------------------

def generate_embeddings(texts):

    embeddings = model.encode(
        texts
    )

    return embeddings


# --------------------------------------------------
# Calculate similarity
# --------------------------------------------------

def calculate_similarity(
    text1,
    text2
):

    embedding1 = generate_embedding(
        text1
    )

    embedding2 = generate_embedding(
        text2
    )

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return similarity


# --------------------------------------------------
# Find most similar feedback
# --------------------------------------------------

def find_similar_feedback(
    query,
    feedback_list,
    top_n=5
):

    query_embedding = generate_embedding(
        query
    )

    feedback_embeddings = generate_embeddings(
        feedback_list
    )

    similarities = cosine_similarity(
        [query_embedding],
        feedback_embeddings
    )[0]

    ranked_indices = np.argsort(
        similarities
    )[::-1]

    results = []

    for index in ranked_indices[:top_n]:

        results.append(
            (
                feedback_list[index],
                similarities[index]
            )
        )

    return results


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    text1 = (
        "My payment failed during checkout."
    )

    text2 = (
        "The transaction did not work "
        "when I tried to buy something."
    )

    similarity = calculate_similarity(
        text1,
        text2
    )

    print("Text 1:")
    print(text1)

    print("\nText 2:")
    print(text2)

    print(
        f"\nSemantic similarity: {similarity:.4f}"
    )