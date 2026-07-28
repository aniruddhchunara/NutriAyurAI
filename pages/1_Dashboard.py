import streamlit as st
import pandas as pd
import plotly.express as px

from analytics.data_loader import load_data
from components.theme import load_theme

# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏥",
    layout="wide"
)

load_theme()

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("🏥 NutriAyurAI Dashboard")
st.caption("Professional Healthcare Analytics Dashboard")

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = load_data()

# Calculate BMI
df["BMI"] = df["weight"] / ((df["height"] / 100) ** 2)


# ----------------------------------------------------
# BMI CATEGORY FUNCTION
# ----------------------------------------------------

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

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Patients",
        len(df)
    )

with col2:
    st.metric(
        "❤️ Average BMI",
        f"{df['BMI'].mean():.2f}"
    )

with col3:
    st.metric(
        "⚖️ Average Weight",
        f"{df['weight'].mean():.1f} kg"
    )

with col4:
    st.metric(
        "📏 Average Height",
        f"{df['height'].mean():.1f} cm"
    )

st.divider()

# ----------------------------------------------------
# CHARTS
# ----------------------------------------------------

left, right = st.columns(2)

# ---------------- Donut Chart ---------------- #

with left:

    bmi_chart = px.pie(
        df,
        names="BMI Category",
        title="BMI Category Distribution",
        hole=0.45,
        color="BMI Category",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(
        bmi_chart,
        use_container_width=True
    )

# ---------------- Age Histogram ---------------- #

with right:

    age_chart = px.histogram(
        df,
        x="age",
        nbins=10,
        title="Age Distribution",
        color_discrete_sequence=["#4CAF50"]
    )

    st.plotly_chart(
        age_chart,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# RECENT PATIENTS
# ----------------------------------------------------

st.subheader("📋 Recent Patients")

st.dataframe(
    df.tail(10),
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# HEALTH SUMMARY
# ----------------------------------------------------

st.subheader("💡 Health Summary")

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
Total Patients : {len(df)}

Average BMI : {df['BMI'].mean():.2f}

Normal BMI Patients :
{len(df[df['BMI Category']=='Normal'])}
"""
    )

with col2:

    st.info(
        f"""
Underweight :
{len(df[df['BMI Category']=='Underweight'])}

Overweight :
{len(df[df['BMI Category']=='Overweight'])}

Obese :
{len(df[df['BMI Category']=='Obese'])}
"""
    )

st.divider()

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.caption("© 2026 NutriAyurAI | Professional Healthcare Analytics Dashboard")