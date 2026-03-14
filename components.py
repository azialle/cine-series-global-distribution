def total_title_card(value, label="Total Titles"):
    return f"""
    <div class="hero-card">
        <div class="hero-label">{label}</div>
        <div class="hero-value">{value:,}</div>
    </div>
    """


def total_movie_card(value, label="Total Movies"):
    return f"""
    <div class="side-card">
        <div class="side-label">{label}</div>
        <div class="side-value">{value:,}</div>
    </div>
    """


def total_tv_show_card(value, label="Total TV Shows"):
    return f"""
    <div class="side-card">
        <div class="side-label">{label}</div>
        <div class="side-value">{value:,}</div>
    </div>
    """

def total_reach_card(value, label="Global Reach"):
    return f"""
    <div class="side-card">
        <div class="side-label">{label}</div>
        <div class="side-value">{value:,}</div>
    </div>
    """

def total_years_card(min_year, max_year, label="Year Range"):
    return f"""
    <div class="side-card">
        <div class="side-label">{label}</div>
        <div class="side-value" style="font-size: 28px;">{min_year} - {max_year}</div>
    </div>
    """