import streamlit as st
from PIL import Image
import os

st.title("📈 Exploratory Data Analysis")

st.write("The following charts were generated during Exploratory Data Analysis.")

figure_folder = "../outputs/figures"

charts = [
    "category_distribution.png",
    "membership_distribution.png",
    "price_distribution.png",
    "rating_distribution.png",
    "correlation_heatmap.png"
]

for chart in charts:

    image_path = os.path.join(
        figure_folder,
        chart
    )

    if os.path.exists(image_path):

        st.subheader(chart.replace(".png","").replace("_"," "))

        image = Image.open(image_path)

        st.image(
            image,
            use_container_width=True
        )

    else:

        st.warning(f"{chart} not found.")