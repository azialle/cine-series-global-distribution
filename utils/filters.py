import streamlit as st


class Filters:
    def __init__(self, df):
        self.df = df
        self.min_date = df["date_added"].min().date()
        self.max_date = df["date_added"].max().date() 

    def _init_session_state(self):
        if "date_range_input" not in st.session_state:
            st.session_state.date_range_input = (self.min_date, self.max_date)
        if "show_type_key" not in st.session_state:
            st.session_state.show_type_key = "All"
        if "selected_year" not in st.session_state:
            st.session_state.selected_year = None

    def _date_range_filter(self):
        date_range_filter = st.sidebar.date_input(
            "Select Date Range",
            min_value=self.min_date,
            max_value=self.max_date,
            key="date_range_input" 
        )
        if isinstance(date_range_filter, tuple) and len(date_range_filter) == 2:
            start_date, end_date = date_range_filter
            self.df = self.df[
                (self.df["date_added"].dt.date >= start_date) & 
                (self.df["date_added"].dt.date <= end_date)
            ]

    def _show_type_filter(self):
        show_type_filter = st.sidebar.segmented_control(
            "Filter Show Type", 
            options=("All", "TV Show", "Movie"), 
            width="stretch",
            key="show_type_key"
        )
        if show_type_filter != "All":
            self.df = self.df[self.df["type"] == show_type_filter]

    def _countries_filter(self):
        all_countries = self.df["country"].str.split(",").explode().str.strip(", ")
        country_options = sorted([country for country in all_countries.unique() if country and country != "Unknown"])
        countries_filter = st.sidebar.multiselect(
            "Filter Countries", 
            options=country_options,
            placeholder="All",
            key="country_filter"
        )
        if countries_filter:
            countries_expanded = self.df["country"].str.split(",").explode().str.strip(", ")
            country_matches = countries_expanded[countries_expanded.isin(countries_filter)].index.unique()
            self.df = self.df.loc[country_matches]

    def _genres_filter(self):
        all_genres = self.df["genre"].str.split(",").explode().str.strip().unique()
        genre_options = sorted([genre for genre in all_genres if genre != "Unknown" and str(genre).strip() != ""])
        genres_filter = st.sidebar.multiselect(
            "Filter Genres",
            options=genre_options,
            placeholder="All",
            key="genre_filter"
        )
        if genres_filter:
            genres_expanded = self.df["genre"].str.split(",").explode().str.strip()
            genre_matches = genres_expanded[genres_expanded.isin(genres_filter)].index.unique()
            self.df = self.df.loc[genre_matches]

    def _ratings_filter(self):
        rating_options = sorted([rating for rating in self.df["rating"].unique() if rating != "Unknown"])
        ratings_filter = st.sidebar.multiselect(
            "Filter Content Ratings",
            options=rating_options,
            placeholder="All",
            key="rating_filter"
        )
        if ratings_filter:
            self.df = self.df[self.df["rating"].isin(ratings_filter)]


    def _reset_all_filters(self):
            st.session_state.date_range_input = (self.min_date, self.max_date)
            st.session_state.show_type_key = "All"
            st.session_state.country_filter = []
            st.session_state.genre_filter = []
            st.session_state.rating_filter = []

    def apply_filter(self):
        st.sidebar.header("Dashboard Filters")
        
        self._init_session_state()
        self._date_range_filter()
        self._show_type_filter()
        self._countries_filter()
        self._genres_filter()
        self._ratings_filter()
        
        st.sidebar.button("Reset All Filters", on_click=self._reset_all_filters, width="content")
        if self.df.empty:
            st.warning("**No data available!** Please adjust your filters.")
        
        return self.df
            