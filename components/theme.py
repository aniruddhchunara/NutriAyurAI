import streamlit as st

from services.settings_service import load_settings


# ==========================================================
# LOAD APPLICATION THEME
# ==========================================================

def load_theme():
    """
    Load and apply the theme saved in Settings.

    Supported themes:
        - Light
        - Dark

    Invalid or missing themes automatically fall back to Light.
    """

    settings = load_settings()

    # ======================================================
    # DEFAULT THEME
    # ======================================================

    theme = "Light"

    if settings and settings[7] in ("Light", "Dark"):
        theme = settings[7]

    # ======================================================
    # LIGHT THEME
    # ======================================================

    if theme == "Light":

        st.markdown(
            """
            <style>

            .main {
                padding-top: 1rem;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }

            div[data-testid="stMetric"] {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                padding: 20px;
                border-radius: 18px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            }

            div[data-testid="stMetric"]:hover {
                border: 1px solid #3B82F6;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

    # ======================================================
    # DARK THEME
    # ======================================================

    else:

        st.markdown(
            """
            <style>

            .main {
                padding-top: 1rem;
                background-color: #0F172A;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }

            div[data-testid="stMetric"] {
                background-color: #1E293B;
                border: 1px solid #334155;
                padding: 20px;
                border-radius: 18px;
            }

            div[data-testid="stMetric"]:hover {
                border: 1px solid #3B82F6;
            }

            </style>
            """,
            unsafe_allow_html=True
        )