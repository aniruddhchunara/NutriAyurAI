import streamlit as st


def app_sidebar():

    with st.sidebar:

        st.markdown("# 🥗 NutriAyurAI")

        st.caption("Professional Healthcare Platform")

        st.divider()

        st.subheader("📌 Project")

        st.write("✔ Patient Management")
        st.write("✔ Analytics")
        st.write("✔ Machine Learning")
        st.write("✔ Reports")

        st.divider()

        st.subheader("📊 Quick Stats")

        st.info(
            """
Current Version

v2.0

Status

Development
"""
        )

        st.divider()

        st.caption("© 2026 NutriAyurAI")