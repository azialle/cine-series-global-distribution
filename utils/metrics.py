import streamlit as st

class Metrics:
    def __init__(self, df):
        self.df = df
        
    def _extract_duration(self, filter_type):
        subset = self.df[self.df["type"] == filter_type]
        if subset.empty:
            return 0, 0
        
        # Use regex to grab only digits
        nums = subset["duration"].str.extract(r'(\d+)').astype(float)
        return len(subset), nums.mean().iloc[0]

    def show(self):
        total_titles = len(self.df)
        movies, average_movie_duration = self._extract_duration("Movie")
        tv_shows, average_tv_seasons = self._extract_duration("TV Show")
        countries = self.df["ISO"].str.split(", ").explode().nunique()

        metric_configs = [
            {"label": "Total Titles", "value": f"{total_titles:,}", "delta": None},
            {"label": "Movies", "value": f"{movies:,}", 
            "delta": f"Avg. Duration: {average_movie_duration:.1f} mins" if movies > 0 else "—"},
            {"label": "TV Shows", "value": f"{tv_shows:,}", 
            "delta": f"Avg. Duration: {average_tv_seasons:.1f} seasons" if tv_shows > 0 else "—"},
            {"label": "Countries Reach", "value": countries, "delta": None},
        ]

        cols = st.columns(len(metric_configs))
        for col, config in zip(cols, metric_configs):
            col.metric(
                label=config["label"],
                value=config["value"],
                delta=config["delta"],
                delta_color="off",
                border=True,
                height=120
            )