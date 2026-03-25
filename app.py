import streamlit as st
import pandas as pd
import plotly.express as px
from components import total_title_card, total_movie_card, total_tv_show_card, total_reach_card

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

with open("style.css") as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/netflix_titles_cleaned.csv")
    return df

df = load_data()

st.title("Netflix Data Dashboard")

total_val = len(df)
total_movies = len(df[df["type"] == "Movie"])
total_tv_shows = len(df[df["type"] == "TV Show"])
total_countries = df["country"].nunique()


card_col1, card_col2, card_col3, card_col4 = st.columns(4, gap="small") 

with card_col1:
    st.markdown(total_title_card(total_val), unsafe_allow_html=True)
with card_col2:
    st.markdown(total_movie_card(total_movies), unsafe_allow_html=True)
with card_col3:
    st.markdown(total_tv_show_card(total_tv_shows), unsafe_allow_html=True)
with card_col4:
    st.markdown(total_reach_card(total_countries), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    content_metrics = df.groupby(["year_added", "type"]).size().reset_index(name="count")
    
    fig1 = px.bar(data_frame=content_metrics,
        x="year_added", 
        y="count", 
        color="type",
        barmode="group",
        color_discrete_map={'Movie': '#E50914', 'TV Show': '#0071eb'},
        title="Content Added Per Year"
    )
    
    min_yr = content_metrics["year_added"].min()
    max_yr = content_metrics["year_added"].max()

    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Titles",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    
        xaxis=dict(
            tickmode="linear", 
            tick0=min_yr,     
            dtick=1,           
            range=[min_yr - 0.5, max_yr + 0.5] 
        )
    )

    st.plotly_chart(fig1, width="stretch")
