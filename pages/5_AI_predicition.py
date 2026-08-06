import streamlit as st
import os

from services.prediction_service import predict_health_status
from services.patient_service import fetch_all_patients
from utils.pdf_generator import generate_health_report

# ==========================================================
# SESSION STATE
# ==========================================================

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None


# ==========================================================
# HELPER FUNCTION
# ==========================================================

def get_patient_by_name(patients, name):
    """
    Return a patient object using patient name.
    """
    for patient in patients:
        if patient.name == name:
            return patient
    return None


# ==========================================================
# LOAD PATIENTS
# ==========================================================

patients = fetch_all_patients()

patient_names = []

for patient in patients:
    patient_names.append(patient.name)


# ==========================================================
# PAGE TITLE
# ==========================================================

st.subheader("🤖 AI Health Prediction")


# ==========================================================
# PATIENT SELECTION
# ==========================================================

selected_patient = st.selectbox(
    "👤 Select Patient",
    patient_names,
    index=None,
    placeholder="Select a patient..."
)

patient = None

if selected_patient:
    patient = get_patient_by_name(
        patients,
        selected_patient
    )


# ==========================================================
# PREDICTION FORM
# ==========================================================

with st.form("prediction_form", clear_on_submit=False):

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            value=patient.age if patient else 18,
            min_value=1,
            max_value=120,
            step=1
        )

        weight = st.number_input(
            "Weight (kg)",
            value=float(patient.weight) if patient else 60.0,
            min_value=1.0,
            step=0.1
        )

    with col2:

        height = st.number_input(
            "Height (cm)",
            value=float(patient.height) if patient else 170.0,
            min_value=1.0,
            step=0.1
        )

        if height < 50:
            st.warning(
                "⚠ Please enter height in centimeters (e.g. 170), not meters (1.70)."
            )

        activity = st.selectbox(
            "Activity Level",
            [
                "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active",
                "Extra Active"
            ]
        )

    activity_map = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }

    activity_factor = activity_map[activity]

    predict = st.form_submit_button("🤖 Predict Health")


# ==========================================================
# PREDICTION
# ==========================================================

if predict:

    result = predict_health_status(
        age,
        weight,
        height,
        activity_factor
    )

    result["Name"] = patient.name if patient else "Guest Patient"
    result["Activity Level"] = activity

    st.session_state.prediction_result = result

if not os.path.exists("reports"):
    os.makedirs("reports")
# ==========================================================
# SHOW RESULT
# ==========================================================

if st.session_state.prediction_result:

    result = st.session_state.prediction_result

    pdf_path = os.path.join(
        "reports",
        "Health_Report.pdf"
    )


with open(pdf_path, "rb") as pdf_file:

    st.download_button(
        label="📄 Download Health Report",
        data=pdf_file,
        file_name="NutriAyurAI_Health_Report.pdf",
        mime="application/pdf",
        key="download_health_report"
    )

    st.success("✅ Prediction Completed")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("❤️ BMI", result["BMI"])

    with c2:
        st.metric("📊 Status", result["Status"])

    with c3:
        st.metric("⭐ Health Score", result["Health Score"])

    c4, c5, c6 = st.columns(3)

    with c4:
        st.metric("🔥 BMR", result["BMR"])

    with c5:
        st.metric("🍽 Calories", result["Calories"])

    with c6:
        st.metric("🥩 Protein", result["Protein"])

    c7, c8 = st.columns(2)

    with c7:
        st.metric("💧 Water", result["Water"])

    with c8:
        st.metric(
            "⚖ Ideal Weight",
            f"{result['Ideal Min']} - {result['Ideal Max']} kg"
        )

    st.info(f"🎯 Goal: {result['Goal']}")

    st.success(result["Recommendation"])


