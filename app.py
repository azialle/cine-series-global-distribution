import streamlit as st
import pandas as pd
from components import total_title_card, total_movie_card, total_tv_show_card, total_reach_card, total_years_card

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


col1, col2, col3 = st.columns([1, 1, 1], gap='small') 

with col1:
    st.markdown(total_title_card(total_val), unsafe_allow_html=True)
with col2:
    side_col2 = f"{total_movie_card(total_movies)}{total_tv_show_card(total_tv_shows)}"
    st.markdown(side_col2, unsafe_allow_html=True)
with col3:
    side_col3 = f"{total_reach_card(total_countries)}{total_years_card(min_year, max_year)}"
    st.markdown(side_col3, unsafe_allow_html=True)