import streamlit as st
import pandas as pd


# ----------------------------------------
# PROFESSIONAL DATA TABLE
# ----------------------------------------

def data_table(
    df: pd.DataFrame,
    title="",
    width="stretch"
):

    if title:
        st.subheader(title)

    st.dataframe(
        df,
        width=width,
        hide_index=True
    )


# ----------------------------------------
# RECENT PATIENTS TABLE
# ----------------------------------------

def recent_patients(df):

    st.subheader("📋 Recent Patients")

    st.dataframe(
        df.tail(10),
        width="stretch",
        hide_index=True
    )


# ----------------------------------------
# TOP BMI TABLE
# ----------------------------------------

def top_bmi_table(df):

    st.subheader("🏆 Top BMI Patients")

    top = df.sort_values(
        "BMI",
        ascending=False
    )

    st.dataframe(
        top,
        width="stretch",
        hide_index=True
    )