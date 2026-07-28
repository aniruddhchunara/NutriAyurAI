import streamlit as st

from analytics.data_loader import load_data

from components.theme import load_theme
from components.sidebar import app_sidebar
from components.navbar import navbar
from components.cards import kpi_card
from components.charts import (
    bmi_distribution_chart,
    age_distribution_chart
)
from components.tables import recent_patients
from components.footer import footer


# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ----------------------------------------
# LOAD THEME
# ----------------------------------------

load_theme()

# ----------------------------------------
# SIDEBAR
# ----------------------------------------

app_sidebar()

# ----------------------------------------
# NAVBAR
# ----------------------------------------

navbar(
    "Dashboard",
    "Professional Healthcare Analytics Dashboard"
)

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

df = load_data()

# BMI
df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)


def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


df["BMI Category"] = df["BMI"].apply(bmi_category)

# ----------------------------------------
# KPI
# ----------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "👥 Total Patients",
        len(df)
    )

with c2:
    kpi_card(
        "❤️ Average BMI",
        f"{df['BMI'].mean():.2f}"
    )

with c3:
    kpi_card(
        "⚖ Average Weight",
        f"{df['weight'].mean():.1f} kg"
    )

with c4:
    kpi_card(
        "📏 Average Height",
        f"{df['height'].mean():.1f} cm"
    )

# ----------------------------------------
# CHARTS
# ----------------------------------------

left, right = st.columns(2)

with left:
    bmi_distribution_chart(df)

with right:
    age_distribution_chart(df)

# ----------------------------------------
# TABLE
# ----------------------------------------

recent_patients(df)

# ----------------------------------------
# FOOTER
# ----------------------------------------

footer()