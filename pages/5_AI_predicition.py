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

if "prediction_reset" not in st.session_state:
    st.session_state.prediction_reset = 0

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
    placeholder="Select a patient...",
    key="prediction_patient"
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
    clear_on_submit=True
):

    col1, col2 = st.columns(2)

    # ======================================================
    # PATIENT HEALTH INPUTS
    # ======================================================

    with col1:

        age = st.number_input(
            "Age",
            value=None,
            placeholder= "Enter age (1-120 years)",
            min_value=1,
            max_value=120,
            step=1,
            key="prediction_age_{reset_id}"
        )

        weight = st.number_input(
            "Weight (kg)",
            value=None,
            placeholder="Enter Weight (2-300kg)",
            min_value=2.0,
            max_value=300.0,
            step=0.1,
            key="prediction_weight_{reset_id}"
        )

    with col2:

        height = st.number_input(
            "Height (cm)",
            value=None,
            placeholder= "Enter a height (50-250 cm)",
            min_value=50.0,
            max_value=250.0,
            step=0.1,
            key="prediction_height_{reset_id}"
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

    # ======================================================
    # REQUIRED INPUT VALIDATION
    # ======================================================

    if age is None:
        st.error(
            "Please enter your age."
        )
        st.stop()

    if weight is None:
        st.error(
            "Please enter your weight."
        )
        st.stop()

    if height is None:
        st.error(
            "Please enter your height."
        )
        st.stop()

    # ======================================================
    # HEIGHT VALIDATION
    # ======================================================

    if height < 50 or height > 250:
        st.error(
            "Height must be between 50 and 250 cm."
        )
        st.stop()

    # ======================================================
    # PREDICTION
    # ======================================================

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

    except Exception:

        st.error(
            "Unable to generate the health prediction. "
            "Please check your inputs and try again."
        )

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

        st.divider()

    if st.button(
        "➕ New Prediction",
        use_container_width=True
    ):
        st.session_state.prediction_result = None
        st.session_state.prediction_reset += 1
        st.rerun()