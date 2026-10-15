import streamlit as st
import pickle
import pandas as pd

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="E-Commerce Recommendation System",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Recommendation System")
st.write("Discover products similar to the one you select.")

# -------------------------
# Load Data
# -------------------------
products = pickle.load(open("notebook/products.pkl", "rb"))
similarity = pickle.load(open("notebook/similarity.pkl", "rb"))

# If products.pkl is a DataFrame
if not isinstance(products, pd.DataFrame):
    products = pd.DataFrame(products)

# -------------------------
# Identify Product Name Column
# -------------------------
possible_columns = [
    "name",
    "product_name",
    "title",
    "product",
    "Product Name"
]

product_column = None

for col in possible_columns:
    if col in products.columns:
        product_column = col
        break

if product_column is None:
    product_column = products.columns[0]

# -------------------------
# Recommendation Function
# -------------------------
def recommend(product_name):
    index = products[products[product_column] == product_name].index[0]

    distances = list(enumerate(similarity[index]))

    distances = sorted(
        distances,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_products = []

    for i in distances[1:6]:
        recommended_products.append(
            products.iloc[i[0]][product_column]
        )

    return recommended_products

# -------------------------
# Product Selection
# -------------------------
selected_product = st.selectbox(
    "Select a Product",
    products[product_column].values
)

# -------------------------
# Recommend Button
# -------------------------
if st.button("Recommend"):

    recommendations = recommend(selected_product)

    st.subheader("Recommended Products")

    cols = st.columns(5)

    for col, product in zip(cols, recommendations):
        with col:
            st.markdown("### 📦")
            st.write(product)