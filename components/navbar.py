import streamlit as st


def navbar(title, subtitle=""):

    st.title(f"🏥 {title}")

    if subtitle:
        st.caption(subtitle)

    st.divider()