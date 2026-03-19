import streamlit as st
import pandas as pd
from components import total_title_card, total_movie_card, total_tv_show_card, total_reach_card

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

with open("style.css") as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/netflix_titles_cleaned.csv')
    return df

df = load_data()

st.title("Netflix Data Dashboard")

total_val = len(df)
total_movies = len(df[df['type'] == 'Movie'])
total_tv_shows = len(df[df['type'] == 'TV Show'])

total_countries = df['country'].nunique()
min_year = df['release_year'].min()
max_year = df['release_year'].max()


col1, col2, col3, col4 = st.columns(4, gap='small') 

with col1:
    st.markdown(total_title_card(total_val), unsafe_allow_html=True)
with col2:
    st.markdown(total_movie_card(total_movies), unsafe_allow_html=True)
with col3:
    st.markdown(total_tv_show_card(total_tv_shows), unsafe_allow_html=True)
with col4:
    st.markdown(total_reach_card(total_countries), unsafe_allow_html=True)