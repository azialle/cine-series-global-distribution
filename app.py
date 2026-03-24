import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

st.markdown("<br>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Content Added Per Year")
    added_counts = df.groupby(['year_added', 'type']).size().reset_index(name='count')
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=added_counts, x='year_added', y='count', hue='type',  ax=ax1)
    ax1.set_xlabel("Year Added")
    ax1.set_ylabel("Count")
    ax1.legend(title="Type")
    fig1.patch.set_alpha(0)
    ax1.set_facecolor((0,0,0,0))
    st.pyplot(fig1)