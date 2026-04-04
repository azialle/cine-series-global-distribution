import plotly.express as px

class Figures:
    def __init__(self, df):
        self.df = df
        self.colors = [px.colors.sequential.Reds_r[0], px.colors.sequential.Reds_r[5]]

    def _apply_theme(self, figure):
        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            margin={"l": 10, "r": 10, "t": 30, "b": 10},
            height=300,
            font=dict(color="white")
        )
        return figure

    def content_added_figure(self):
        content_metrics = (
            self.df.assign(year=self.df["date_added"].dt.year)
                .groupby(["year", "type"])
                .size()
                .reset_index(name="count")
                .dropna(subset=["year"])
        )

        figure = px.bar(
            content_metrics,
            x="year",
            y="count",
            color="type",
            barmode="group",
            color_discrete_sequence=self.colors,
            labels={"year": "Year", "count": "Total Titles", "type": "Type"}
        )

        figure.update_layout(
            legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1, "title_text": ""},
            xaxis=dict(tickmode="linear", dtick=1)
        )
        return self._apply_theme(figure)

    def genre_figure(self):
        top_genres = (
            self.df["genre"].str.split(", ")
            .explode()
            .value_counts()
            .head(10)
            .reset_index(name="total_titles"))
        
        figure = px.bar(
            top_genres, 
            x="total_titles", 
            y="genre", 
            orientation="h",
            color="total_titles", 
            color_continuous_scale="Reds",
        )
        
        figure.update_layout(coloraxis_showscale=False, yaxis={"categoryorder": "total ascending"})
        figure.update_xaxes(visible=False)
        figure.update_yaxes(title_text="")

        return self._apply_theme(figure)

    def rating_figure(self):
        rating_counts = self.df["rating"].value_counts().head(10).reset_index(name="total_titles")

        figure = px.pie(
            rating_counts, 
            values="total_titles", 
            names="rating", 
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Reds_r, 
        )
        
        figure.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="#111", width=2)))
        figure.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5))
        return self._apply_theme(figure)

    def map_figure(self):
        country_counts = self.df.groupby("ISO").size().reset_index(name="count")
        figure = px.choropleth(
            country_counts,
            locations="ISO",
            locationmode="ISO-3",
            color="count",
            color_continuous_scale="Reds",
        )
        
        figure.update_layout(
            geo=dict(bgcolor="rgba(0,0,0,0)", projection_type="robinson"),
            coloraxis_showscale=False
        )

        return self._apply_theme(figure)