import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/netflix_titles_cleaned.csv")
    df["title"] = df["title"].str.title()
    return df