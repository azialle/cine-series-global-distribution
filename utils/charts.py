import plotly.express as px

def content_added_chart(df, selected_year=None):
    if selected_year:
        df_filtered = df[df["date_added"].dt.year == int(selected_year)].copy()
        df_filtered["month"] = df_filtered["date_added"].dt.month_name()
        content_metrics = (df_filtered.groupby(["month", "type"])
                          .size()
                          .reset_index(name="count"))
        
        x_axis = "month"
        category_orders = {"month": ["January", "February", "March", "April", "May", "June", 
                                     "July", "August", "September", "October", "November", "December"]}
        title = f"Titles Added in {selected_year} (Monthly)"
    else:
        content_metrics = (df.groupby([df["date_added"].dt.year.rename("year_added"), "type"])
                          .size()
                          .reset_index(name="count"))
        content_metrics = content_metrics.dropna(subset=["year_added"])
        
        x_axis = "year_added"
        category_orders = {}
        title = ""

    fig = px.bar(
        content_metrics,
        x=x_axis,
        y="count",
        color="type",
        barmode="group",
        category_orders=category_orders,
        color_discrete_sequence=[px.colors.sequential.Reds_r[0], px.colors.sequential.Reds_r[5]],
        template="plotly_dark",
    )

    fig.update_layout(
        xaxis_title=title,
        yaxis_title="Total Titles",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 0, "r": 0, "t": 30, "b": 0},
        height=300,
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1, "title_text": ""},
    )
    
    if not selected_year and not content_metrics.empty:
        min_yr, max_yr = int(content_metrics["year_added"].min()), int(content_metrics["year_added"].max())
        fig.update_layout(xaxis={"tickmode": "linear", "dtick": 1, "range": [min_yr - 0.5, max_yr + 0.5]})

    return fig

def genre_chart(df):
    top_genres = df["genre"].str.split(", ").explode().value_counts().head(10).reset_index()
    top_genres.columns = ["genre", "total_titles"]
    fig2 = px.bar(
        data_frame=top_genres, 
        x="total_titles", 
        y="genre", 
        orientation="h",
        template="plotly_dark", 
        color="total_titles", 
        color_continuous_scale="Reds",
    )
    
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 0, "r": 10, "t": 30, "b": 0}, 
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"}, 
        height=300,
    )

    fig2.update_xaxes(visible=False)
    fig2.update_yaxes(title_text="")

    return fig2

def rating_chart(df):
    rating_counts = df["rating"].value_counts().head(10).reset_index()
    rating_counts.columns = ["rating", "total_titles"]
    fig3 = px.pie(
        data_frame=rating_counts, 
        values="total_titles", 
        names="rating", 
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.Reds_r, 
        template="plotly_dark",
    )
    
    fig3.update_traces(
        textposition="inside", 
        textinfo="percent", 
        textfont_size=14, 
        marker={
            "line": {
                "color": "#111", 
                "width": 2,
            },
        },
    )
    
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"l": 10, "r": 10, "t": 30, "b": 100}, 
        height=300,
        legend={
            "orientation": "h", 
            "yanchor": "top", 
            "y": -0.05, 
            "xanchor": "center", 
            "x": 0.5,
        },
    )

    return fig3

def map_chart(df):
    country_counts = df.groupby("ISO").size().reset_index(name="count")
    fig_map = px.choropleth(
        data_frame=country_counts,
        locations="ISO",         
        locationmode="ISO-3",    
        color="count",
        color_continuous_scale="Reds",
        template="plotly_dark",
    )
    
    fig_map.update_layout(
        dragmode="pan", 
        geo={
            "bgcolor": "rgba(0,0,0,0)",
            "projection_type": "robinson",
            "projection_scale": 1,
        },
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        height=300,
    )

    return fig_map