import os
import streamlit as st

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

patient_names = [
    patient.name
    for patient in patients
]


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

with st.form(
    "prediction_form",
    clear_on_submit=False
):

    col1, col2 = st.columns(2)

    # ======================================================
    # PATIENT HEALTH INPUTS
    # ======================================================

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
            value=float(patient.weight)
            if patient
            else 60.0,
            min_value=1.0,
            step=0.1
        )

    with col2:

        height = st.number_input(
            "Height (cm)",
            value=float(patient.height)
            if patient
            else 170.0,
            min_value=1.0,
            step=0.1
        )

        if height < 50:

            st.warning(
                "⚠️ Please enter height in centimeters "
                "(e.g. 170), not meters (1.70)."
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

    # ======================================================
    # ACTIVITY FACTOR
    # ======================================================

    activity_map = {

        "Sedentary": 1.2,

        "Lightly Active": 1.375,

        "Moderately Active": 1.55,

        "Very Active": 1.725,

        "Extra Active": 1.9
    }

    activity_factor = activity_map[activity]

    # ======================================================
    # PREDICT BUTTON
    # ======================================================

    predict = st.form_submit_button(
        "🤖 Predict Health",
        use_container_width=True
    )


# ==========================================================
# PREDICTION
# ==========================================================

if predict:

    # Prevent obviously invalid height values.
    if height < 50:

        st.error(
            "Height must be at least 50 cm. "
            "Please enter height in centimeters."
        )

        st.stop()

    try:

        result = predict_health_status(
            age,
            weight,
            height,
            activity_factor
        )

        result["Name"] = (
            patient.name
            if patient
            else "Guest Patient"
        )

        result["Activity Level"] = activity

        st.session_state.prediction_result = result

    except ValueError as error:

        st.error(str(error))

        st.session_state.prediction_result = None


# ==========================================================
# SHOW RESULT
# ==========================================================

if st.session_state.prediction_result:

    result = st.session_state.prediction_result

    # ======================================================
    # REPORT DIRECTORY
    # ======================================================

    os.makedirs(
        "reports",
        exist_ok=True
    )

    # ======================================================
    # GENERATE HEALTH REPORT
    # ======================================================

    pdf_path = os.path.join(
        "reports",
        "Health_Report.pdf"
    )

    generate_health_report(
        result,
        pdf_path
    )

    # ======================================================
    # SUCCESS MESSAGE
    # ======================================================

    st.success(
        "✅ Prediction Completed"
    )

    # ======================================================
    # HEALTH METRICS
    # ======================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "⚖️ BMI",
            result["BMI"]
        )

    with c2:

        st.metric(
            "📊 Status",
            result["Status"]
        )

    with c3:

        st.metric(
            "🔥 Calories",
            result["Calories"]
        )

    c4, c5 = st.columns(2)

    with c4:

        st.metric(
            "🥩 Protein",
            f"{result['Protein']} g"
        )

    with c5:

        st.metric(
            "💧 Water",
            f"{result['Water']} L"
        )

    # ======================================================
    # IDEAL WEIGHT
    # ======================================================

    st.metric(
        "⚖️ Ideal Weight",
        f"{result['Ideal Min']} - "
        f"{result['Ideal Max']} kg"
    )

    # ======================================================
    # GOAL
    # ======================================================

    st.info(
        f"🎯 Goal: {result['Goal']}"
    )

    # ======================================================
    # RECOMMENDATION
    # ======================================================

    st.success(
        result["Recommendation"]
    )

    # ======================================================
    # DOWNLOAD HEALTH REPORT
    # ======================================================

    with open(
        pdf_path,
        "rb"
    ) as pdf_file:

        st.download_button(
            label="📄 Download Health Report",
            data=pdf_file,
            file_name="NutriAyurAI_Health_Report.pdf",
            mime="application/pdf",
            key="download_health_report"
        )