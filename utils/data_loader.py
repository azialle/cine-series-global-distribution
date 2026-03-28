import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/netflix_titles_cleaned.csv")
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    df["title"] = df["title"].str.title()
    return df