import streamlit as st
import pandas as pd

st.set_page_config(page_title="Netflix Analytics", page_icon="🍿", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/netflix_titles_cleaned.csv")
    return df

df = load_data()

st.sidebar.header("Filter Options")

st.title("🍿 Netflix Content Dashboard")
st.markdown("Exploring trends in Movies and TV Shows")