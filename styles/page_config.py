import streamlit as st

def page_config():
    st.set_page_config(page_title="Cine-Series: Global Distribution", layout="wide", page_icon="🎬")
    with open("styles/style.css", encoding="UTF-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)