import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Biodiversity Analytics Engine",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Biodiversity Analytics Engine")
st.subheader("IUCN European Red List of Reptiles 2025")

# Load Dataset
df = pd.read_csv("data/reptiles_data.csv")

# Dataset Preview
st.header("Dataset Preview")
st.dataframe(df.head(20))

# Basic Metrics
total_species = df["Species name"].nunique()
total_families = df["Family"].nunique()
total_orders = df["Order"].nunique()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Species", total_species)

with col2:
    st.metric("Total Families", total_families)

with col3:
    st.metric("Total Orders", total_orders)

# Red List Category Analysis
st.header("European Red List Categories")

category_counts = df["European category"].value_counts()

st.dataframe(category_counts)

fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_title("Species by Red List Category")
ax.set_xlabel("Category")
ax.set_ylabel("Count")
st.pyplot(fig)

# Family Analysis
st.header("Top 10 Families")

family_counts = df["Family"].value_counts().head(10)

fig2, ax2 = plt.subplots()
family_counts.plot(kind="bar", ax=ax2)
ax2.set_title("Top 10 Families")
st.pyplot(fig2)

# Endemic Species
st.header("Endemic Species Analysis")

endemic_counts = df["Endemic to Europe"].value_counts()

st.dataframe(endemic_counts)

fig3, ax3 = plt.subplots()
endemic_counts.plot(kind="pie", autopct="%1.1f%%", ax=ax3)
ax3.set_ylabel("")
st.pyplot(fig3)

# Search Species
st.header("Search Species")

species_search = st.text_input("Enter Species Name")

if species_search:
    result = df[
        df["Species name"]
        .astype(str)
        .str.contains(species_search, case=False, na=False)
    ]

    st.dataframe(result)

st.success("Biodiversity Analysis Completed Successfully!")