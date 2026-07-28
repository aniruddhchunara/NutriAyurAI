import streamlit as st


def load_theme():

    st.markdown(
        """
        <style>

        .main {
            padding-top: 1rem;
        }

        .block-container{
            padding-top:2rem;
            padding-bottom:2rem;
            padding-left:2rem;
            padding-right:2rem;
        }

        div[data-testid="stMetric"]{
            background-color:#1E293B;
            border:1px solid #334155;
            padding:20px;
            border-radius:18px;
        }

        div[data-testid="stMetric"]:hover{
            border:1px solid #3B82F6;
        }

        </style>
        """,
        unsafe_allow_html=True
    )