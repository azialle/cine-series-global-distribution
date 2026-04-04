import streamlit as st
from utils.data_loader import load_data
from utils.filters import Filters
from utils.metrics import Metrics
from utils.charts import Charts
from styles.page_config import page_config


page_config()

df_raw = load_data()
df = Filters(df_raw).apply_filter()

Metrics(df).show()
charts = Charts(df)

chart_col, genre_col, rating_col = st.columns([2, 1, 1])
with chart_col:
    charts.content_added_chart()

with genre_col:
    charts.top_genre_chart()

with rating_col:
    charts.rating_distribution_chart()


map_col, table_col = st.columns(2)
with map_col:
    charts.global_content_reach_chart()

with table_col:
    charts.table_display()