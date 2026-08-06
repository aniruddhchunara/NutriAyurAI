import streamlit as st
import plotly.express as px

from components import (
    load_theme,
    navbar,
    app_sidebar,
    footer
)

from services.analytics_service import (
    get_dashboard_summary,
    get_bmi_distribution,
    get_patient_age_data,
    get_appointment_trends,
    get_business_insights
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD UI
# ==========================================================

load_theme()

app_sidebar()

navbar(
    "Analytics Dashboard",
    "Healthcare Analytics Overview"
)

# ==========================================================
# LOAD DATA
# ==========================================================

summary = get_dashboard_summary()
bmi_df = get_bmi_distribution()
age_df = get_patient_age_data()
trend_df = get_appointment_trends()
insights = get_business_insights()

# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("📊 Dashboard KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👥 Patients",
        summary["patient_count"]
    )

with col2:
    st.metric(
        "📅 Appointments",
        summary["appointment_count"]
    )

with col3:
    st.metric(
        "❤️ Average BMI",
        summary["average_bmi"]
    )

with col4:
    st.metric(
        "⚖ Average Weight",
        f"{summary['average_weight']} kg"
    )

with col5:
    st.metric(
        "📏 Average Height",
        f"{summary['average_height']} cm"
    )


st.divider()

st.subheader("📊 BMI Distribution")

bmi_chart = px.bar(
    bmi_df,
    x="Category",
    y="Patients",
    color="Category",
    text="Patients",
    title="BMI Category Distribution"
)

st.plotly_chart(
    bmi_chart,
    use_container_width=True
)

st.divider()

st.subheader("🥧 BMI Category Percentage")

pie_chart = px.pie(
    bmi_df,
    names="Category",
    values="Patients",
    title="BMI Category Percentage",
    hole=0.4
)

st.plotly_chart(
    pie_chart,
    use_container_width=True
)

st.divider()

st.subheader("📅 Appointment Trends")

trend_chart = px.line(
    trend_df,
    x="Date",
    y="Appointments",
    markers=True,
    title="Appointments Over Time"
)

st.plotly_chart(
    trend_chart,
    use_container_width=True
)

st.divider()

st.subheader("💡 Business Insights")

for insight in insights:

    st.info(insight)




# ==========================================================
# FOOTER
# ==========================================================

footer()