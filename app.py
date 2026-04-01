import streamlit as st
from utils.data_loader import load_data
from utils.charts import content_added_chart, genre_chart, rating_chart, map_chart

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

with open("style.css") as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

df = load_data()

min_date = df["date_added"].min().date()
max_date = df["date_added"].max().date()

if "date_range_input" not in st.session_state:
    st.session_state.date_range_input = (min_date, max_date)

if "show_type_key" not in st.session_state:
    st.session_state.show_type_key = "All"

def reset_all_filters():
    st.session_state.date_range_input = (min_date, max_date)
    st.session_state.show_type_key = "All"
    st.session_state.country_filter = []
    st.session_state.genre_filter = []
    st.session_state.rating_filter = []

st.sidebar.header("Netflix Dashboard Filters")

date_range_filter = st.sidebar.date_input(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    key="date_range_input" 
)
if isinstance(date_range_filter, tuple) and len(date_range_filter) == 2:
    start_date, end_date = date_range_filter
    df = df[
        (df["date_added"].dt.date >= start_date) & 
        (df["date_added"].dt.date <= end_date)
    ]

show_type_filter = st.sidebar.segmented_control(
    "Show Type", 
    options=("All", "TV Show", "Movie"), 
    width="stretch",
    key="show_type_key"
)
if show_type_filter != "All":
    df = df[df["type"] == show_type_filter]

all_countries = df["country"].str.split(",").explode().str.strip(", ")
country_options = sorted([country for country in all_countries.unique() if country and country != "Unknown"])
countries_filter = st.sidebar.multiselect(
    "Select Countries", 
    options=country_options,
    placeholder="All",
    key="country_filter"
)
if countries_filter:
    countries_expanded = df["country"].str.split(",").explode().str.strip(", ")
    country_matches = countries_expanded[countries_expanded.isin(countries_filter)].index.unique()
    df = df.loc[country_matches]

all_genres = df["genre"].str.split(",").explode().str.strip().unique()
genre_options = sorted([genre for genre in all_genres if genre != "Unknown" and str(genre).strip() != ""])
genres_filter = st.sidebar.multiselect(
    "Select Genres",
    options=genre_options,
    placeholder="All",
    key="genre_filter"
)
if genres_filter:
    genres_expanded = df["genre"].str.split(",").explode().str.strip()
    genre_matches = genres_expanded[genres_expanded.isin(genres_filter)].index.unique()
    df = df.loc[genre_matches]

rating_options = sorted([rating for rating in df["rating"].unique() if rating != "Unknown"])
ratings_filter = st.sidebar.multiselect(
    "Select Content Ratings",
    options=rating_options,
    placeholder="All",
    key="rating_filter"
)
if ratings_filter:
    df = df[df["rating"].isin(ratings_filter)]

st.sidebar.button("Reset All Filters", on_click=reset_all_filters, width="content")

if df.empty:
    st.warning("**No data available!** Please adjust your filters.")

total_val = len(df)

movie_df = df[df["type"] == "Movie"]
total_movies = len(movie_df)
avg_movie_duration = movie_df["duration"].str.replace(" min", "").astype(int).mean()

tv_df = df[df["type"] == "TV Show"]
total_tv_shows = len(tv_df)
avg_tv_seasons = tv_df["duration"].str.replace(" Season", "").str.replace("s", "").astype(int).mean()

total_countries = df["ISO"].str.split(", ").explode().nunique()

card_col1, card_col2, card_col3, card_col4 = st.columns(4) 

with card_col1:
    st.metric(
        label="Total Titles", 
        value=f"{total_val:,}", 
        border=True,
         height=120
    )
with card_col2:
    st.metric(
        label="Total Movies", 
        value=f"{total_movies:,}", 
        delta=f"Avg. Duration: {avg_movie_duration:.1f} mins" if total_movies > 0 else "—",
        delta_color="off",
        border=True,
         height=120
    )
with card_col3:
    st.metric(
        label="Total TV Shows", 
        value=f"{total_tv_shows:,}", 
        delta=f"Avg. Duration: {avg_tv_seasons:.1f} Seasons" if total_tv_shows > 0 else "—",
        delta_color="off",
        border=True,
        height=120
    )
with card_col4:
    st.metric(
        label="Total Countries Reach", 
        value=total_countries,
        border=True,
         height=120
    )


chart_col1, chart_col2, chart_col3 = st.columns([2, 1, 1])

if "selected_year" not in st.session_state:
    st.session_state.selected_year = None

with chart_col1:
    with st.container(border=True):
        if st.session_state.selected_year:
            if st.button("⬅ Back", width="content"):
                st.session_state.selected_year = None
                st.rerun()

        st.subheader("Content Added Over Time", text_alignment="center")
    
        fig_year = content_added_chart(df, selected_year=st.session_state.selected_year)
        select_event = st.plotly_chart(fig_year, on_select="rerun", key="main_chart")

        if select_event and select_event["selection"]["points"]:
            new_year = select_event["selection"]["points"][0]["x"]
            if not st.session_state.selected_year:
                st.session_state.selected_year = new_year
                st.rerun()
with chart_col2:
    with st.container(border=True):
        st.subheader("Top 10 Genres", text_alignment="center")
        st.plotly_chart(genre_chart(df), width="stretch")
with chart_col3:
    with st.container(border=True):
        st.subheader("Rating Distribution", text_alignment="center")
        st.plotly_chart(rating_chart(df), width="stretch")

map_col, table_col = st.columns(2)

with map_col:
    with st.container(border=True):
        st.subheader("Global Content Reach", text_alignment="center")
        df_map = df.assign(ISO=df["ISO"].str.split(", ")).explode("ISO")
        st.plotly_chart(map_chart(df_map), width="stretch")

with table_col:
    with st.container(border=True):
        st.subheader("Latest Titles", text_alignment="center")
        st.dataframe(
            df.sort_values("release_year", ascending=False),
            column_order=("title", "type", "release_year",  "country", "genre", "rating", "duration"),
            column_config={
                "title": "Title",
                "type": "Type",
                "release_year": st.column_config.NumberColumn("Year", format="%d"),
                "country": "Country",
                "genre": "Genre",
                "rating": "Rating",
                "duration": "Duration"
            },
            hide_index=True,
            width="stretch",
            height=300
        )