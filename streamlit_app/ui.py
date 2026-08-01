import streamlit as st


def page_config():

    st.set_page_config(
        page_title="Trip Planner Assistant AI",
        page_icon="🌍",
        layout="wide",
    )


def header():

    st.title("🌍 Trip Planner Assistant AI")

    st.caption(
        "Generate complete AI-powered travel itineraries."
    )