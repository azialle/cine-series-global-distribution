import streamlit as st
from utils.figures import Figures

class Charts(Figures):
    def __init__(self, df):
        super().__init__(df)

    def _render_chart(self, title, figure_method, interactive=False):
        with st.container(border=True):
            st.subheader(title, text_alignment="center")
            
            figure = getattr(self, figure_method)()
            
            st.plotly_chart(
                figure, 
                on_select="rerun" if interactive else "ignore", 
                key=f"key_{figure_method}", 
                use_container_width=True
            )

    def content_added_chart(self):
        self._render_chart("Content Added Over Time", "content_added_figure", interactive=True)

    def top_genre_chart(self):
        self._render_chart("Top 10 Genres", "genre_figure")

    def rating_distribution_chart(self):
        self._render_chart("Rating Distribution", "rating_figure")

    def global_content_reach_chart(self):
        self._render_chart("Global Content Reach", "map_figure")

    def table_display(self):
        with st.container(border=True):
            st.subheader("Latest Titles", text_alignment="center")
            st.dataframe(
                self.df.sort_values("release_year", ascending=False),
                column_order=("title", "type", "release_year", "country", "genre", "rating", "duration"),
                column_config={"release_year": st.column_config.NumberColumn("Year", format="%d")},
                hide_index=True,
                height=300,
                use_container_width=True
            )