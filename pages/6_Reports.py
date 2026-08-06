import os
import streamlit as st

from services.patient_service import fetch_all_patients
from utils.pdf_generator import generate_health_report
from services.prediction_service import predict_health_status
from components import (
    load_theme,
    navbar,
    app_sidebar,
    footer
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)

# ==========================================================
# LOAD UI
# ==========================================================

load_theme()
app_sidebar()

navbar(
    "Reports",
    "Generate Professional Health Reports"
)

# ==========================================================
# PAGE TITLE
# ==========================================================

st.subheader("📄 Patient Reports")

st.write(
    "Generate professional health reports for registered patients."
)

# ==========================================================
# LOAD PATIENTS
# ==========================================================

patients = fetch_all_patients()

if not patients:

    st.warning("No patients available.")

    st.stop()

patient_names = [patient.name for patient in patients]

# ==========================================================
# SELECT PATIENT
# ==========================================================

selected_patient = st.selectbox(
    "👤 Select Patient",
    patient_names,
    index=None,
    placeholder="Choose a patient..."
)

# ==========================================================
# GET SELECTED PATIENT
# ==========================================================

patient = None

for p in patients:

    if p.name == selected_patient:

        patient = p

        break

# ==========================================================
# PATIENT PREVIEW
# ==========================================================

if patient:

    st.divider()

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"**Name:** {patient.name}")
        st.write(f"**Age:** {patient.age} Years")
        st.write(f"**Weight:** {patient.weight} kg")

    with col2:

        st.write(f"**Height:** {patient.height} cm")
        st.write(f"**BMI:** {patient.calculate_bmi():.2f}")
        st.write(f"**Activity Factor:** {patient.activity_factor}")


# ==========================================================
# REPORT OPTIONS
# ==========================================================

st.divider()

st.subheader("📄 Report Options")

report_type = st.selectbox(
    "Select Report Type",
    [
        "AI Health Report",
        "Patient Summary",
        "Nutrition Report",
        "Appointment History"
    ]
)

report_date = st.date_input(
    "Report Date"
)

generate_report = st.button(
    "📄 Generate Report",
    use_container_width=True
)

# ==========================================================
# GENERATE REPORT
# ==========================================================

if generate_report:

    activity_factor = patient.activity_factor

    result = predict_health_status(
        patient.age,
        patient.weight,
        patient.height,
        activity_factor
    )

    result["Name"] = patient.name
    result["Activity Level"] = activity_factor

    if not os.path.exists("reports"):
        os.makedirs("reports")

    pdf_path = os.path.join(
        "reports",
        f"{patient.name}_Health_Report.pdf"
    )

    generate_health_report(
        result,
        pdf_path
    )

    st.success("✅ Report generated successfully!")

    with open(pdf_path, "rb") as pdf:

        st.download_button(
            "📥 Download Report",
            pdf,
            file_name=f"{patient.name}_Health_Report.pdf",
            mime="application/pdf",
            key="report_download"
        )