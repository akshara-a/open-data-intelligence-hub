import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\ELCOT\Desktop\Sasirekha-G40 AIML 7\data\SmartShop_Portfolio_Dataset.csv")
    return df