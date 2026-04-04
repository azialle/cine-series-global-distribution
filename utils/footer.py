import streamlit as st

def footer():
    footer_html = """
    <div style="text-align: center; color: grey; font-size: 0.8rem;">
        <p><strong>Data Source:</strong> <a href="https://www.kaggle.com/datasets/shivamb/netflix-shows" target="_blank" style="color: #e50914; text-decoration: none;">Kaggle: Netflix Movies and TV Shows</a></p>
        <p><em>Disclaimer: This dashboard is for educational purposes only. The data provided is based on a snapshot of the Netflix library and may not reflect real-time updates or official Netflix corporate statistics.</em></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)