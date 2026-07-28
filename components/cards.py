import streamlit as st


def kpi_card(title, value):
    """
    Reusable KPI Card
    """

    st.metric(
        label=title,
        value=value
    )