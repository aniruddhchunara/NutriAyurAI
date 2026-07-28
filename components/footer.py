import streamlit as st
from datetime import datetime


def footer():

    st.divider()

    current_year = datetime.now().year

    st.markdown(
        f"""
        <div style="text-align:center; color:gray; font-size:14px;">

        © {current_year} <b>NutriAyurAI</b>

        <br>

        Professional Healthcare Analytics Platform

        <br><br>

        Version <b>2.0</b>

        </div>
        """,
        unsafe_allow_html=True
    )