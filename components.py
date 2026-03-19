def create_stat_card(value, label):
    return f"""
    <div class="stat-card">
        <div class="card-label">{label}</div>
        <div class="card-value">{value}</div>
    </div>
    """

def total_title_card(value):
    return create_stat_card(f"{value:,}", "Total Titles")

def total_movie_card(value):
    return create_stat_card(f"{value:,}", "Total Movies")

def total_tv_show_card(value):
    return create_stat_card(f"{value:,}", "Total TV Shows")

def total_reach_card(value):
    return create_stat_card(f"{value:,}", "Total Countries")