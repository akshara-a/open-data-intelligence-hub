import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Dataset Explorer")

df = pd.read_csv("data/processed/ecommerce_clustered.csv")

st.write("Dataset Shape")

st.write(df.shape)

st.dataframe(df)

st.markdown("---")

st.subheader("Category Distribution")

fig = px.histogram(
    df,
    x="Category",
    color="Category"
)

st.plotly_chart(fig,use_container_width=True)

st.subheader("Purchase Distribution")

fig2 = px.pie(
    df,
    names="Purchase_Status"
)

st.plotly_chart(fig2,use_container_width=True)

st.download_button(
"Download Dataset",
df.to_csv(index=False),
"ecommerce_clustered.csv",
"text/csv"
)

st.markdown("---")

st.caption(

"© 2026 Ecommerce Recommendation System | Built with Streamlit"

)