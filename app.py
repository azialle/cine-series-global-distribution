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

card_col1, card_col2, card_col3, card_col4 = st.columns(4) 

with card_col1:
    st.markdown(total_title_card(total_val), unsafe_allow_html=True)
with card_col2:
    st.markdown(total_movie_card(total_movies), unsafe_allow_html=True)
with card_col3:
    st.markdown(total_tv_show_card(total_tv_shows), unsafe_allow_html=True)
with card_col4:
    st.markdown(total_reach_card(total_countries), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

chart_col1, chart_col2, chart_col3 = st.columns([2, 1, 1])

with chart_col1:
    with st.container(border=True):
        st.subheader("Content Added Per Year", text_alignment="center")
        content_metrics = df.groupby(["year_added", "type"]).size().reset_index(name="count")
        
        fig1 = px.bar(
            data_frame=content_metrics,
            x="year_added", 
            y="count", 
            color="type",
            barmode="group",
            color_discrete_sequence=[px.colors.sequential.Reds_r[0], px.colors.sequential.Reds_r[5]],
            template="plotly_dark"
        )

        min_yr = content_metrics["year_added"].min()
        max_yr = content_metrics["year_added"].max()

        fig1.update_layout(
            xaxis_title="",
            yaxis_title="Total Titles",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=30, b=0),
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=""),
            xaxis=dict(tickmode="linear", tick0=min_yr, dtick=1, range=[min_yr - 0.5, max_yr + 0.5])
        )
        st.plotly_chart(fig1, width="stretch")

with chart_col2:
    with st.container(border=True):
        st.subheader("Top 10 Genres", text_alignment="center")
        top_genres = df["genre"].str.split(", ").explode().value_counts().head(10).reset_index()
        top_genres.columns = ["genre", "total_titles"]
        
        fig2 = px.bar(
            top_genres, x="total_titles", y="genre", orientation="h",
            template="plotly_dark", color="total_titles", color_continuous_scale="Reds"
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=10, t=30, b=0), coloraxis_showscale=False,
            yaxis={"categoryorder":"total ascending"}, height=450
        )
        fig2.update_xaxes(visible=False)
        fig2.update_yaxes(title_text="")
        st.plotly_chart(fig2, width="stretch")

with chart_col3:
    with st.container(border=True):
        st.subheader("Rating Distribution", text_alignment="center")
        rating_counts = df["rating"].value_counts().head(10).reset_index()
        rating_counts.columns = ["rating", "total_titles"]

        fig3 = px.pie(
            rating_counts, values="total_titles", names="rating", hole=0.5,
            color_discrete_sequence=px.colors.sequential.Reds_r, template="plotly_dark"
        )
        fig3.update_traces(textposition="inside", textinfo="percent", textfont_size=14, marker=dict(line=dict(color="#111", width=2)))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=30, b=100), height=450,
            legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig3, width="stretch")

st.markdown("<br>", unsafe_allow_html=True)

map_col, table_col = st.columns(2)

with map_col:
    with st.container(border=True):
        st.subheader("Global Content Reach", text_alignment="center")
        
        country_counts = df["country"].str.split(", ").explode().value_counts().reset_index()
        country_counts.columns = ["country", "count"]
        
        iso_lookup = px.data.gapminder().query("year == 2007")[["country", "iso_alpha"]].set_index("country")["iso_alpha"].to_dict()
        iso_lookup.update({"United States": "USA", "United Kingdom": "GBR", "South Korea": "KOR"})
        
        country_counts["iso_alpha"] = country_counts["country"].map(iso_lookup)
        country_counts = country_counts.dropna(subset=["iso_alpha"])

        fig_map = px.choropleth(
            country_counts, locations="iso_alpha", locationmode="ISO-3",
            color="count", hover_name="country", color_continuous_scale="Reds", template="plotly_dark"
        )
        fig_map.update_layout(
            geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False, projection_type="equirectangular"),
            paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0), height=450
        )
        st.plotly_chart(fig_map, width="stretch")

with table_col:
    with st.container(border=True):
        st.subheader("Latest Titles", text_alignment="center")
        display_df = df[["title", "type", "release_year", "genre"]].sort_values(by="release_year", ascending=False)
        st.dataframe(
            display_df,
            column_config={"title": "Title", "type": "Type", "release_year": "Year", "genre": "Genre"},
            hide_index=True, width="stretch", height=450
        )