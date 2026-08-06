import streamlit as st
import pandas as pd

from models.patient import Patient

from services.patient_service import (
    fetch_all_patients,
    fetch_patient,
    create_patient,
    edit_patient,
    remove_patient
)

from components import (
    load_theme,
    navbar,
    app_sidebar,
    footer,
    data_table
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Patient Management",
    page_icon="👤",
    layout="wide"
)

# ==========================================================
# LOAD UI
# ==========================================================

load_theme()
app_sidebar()

navbar(
    "Patient Management",
    "Manage all patient records"
)

# ==========================================================
# LOAD PATIENTS
# ==========================================================

patients = fetch_all_patients()

# ==========================================================
# DISPLAY PATIENT TABLE
# ==========================================================

st.subheader("📋 Patient Records")

if not patients:

    st.warning("No patients found.")

else:

    patient_data = []

    for patient in patients:

        patient_data.append({
            "Name": patient.name,
            "Age": patient.age,
            "Weight (kg)": patient.weight,
            "Height (cm)": patient.height,
            "BMI": round(patient.calculate_bmi(), 2)
        })

    df = pd.DataFrame(patient_data)

    data_table(
        df,
        title="All Patients"
    )

# ==========================================================
# SEARCH PATIENT
# ==========================================================

st.divider()

st.subheader("🔍 Search Patient")

search_name = st.text_input(
    "Enter Patient Name"
)

if search_name:

    patient = fetch_patient(search_name)

    if patient:

        st.success("✅ Patient Found")

        col1, col2 = st.columns(2)

        with col1:

            st.write(f"**Name:** {patient.name}")
            st.write(f"**Age:** {patient.age}")
            st.write(f"**Weight:** {patient.weight} kg")

        with col2:

            st.write(f"**Height:** {patient.height} cm")
            st.write(f"**BMI:** {patient.calculate_bmi():.2f}")
            st.write(f"**Activity Factor:** {patient.activity_factor}")

    else:

        st.error("❌ Patient not found.")

# ==========================================================
# ADD NEW PATIENT
# ==========================================================

st.divider()

st.subheader("➕ Add New Patient")

with st.form("add_patient_form", clear_on_submit=True):

    name = st.text_input("Patient Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        step=1
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        step=0.1
    )

    height = st.number_input(
        "Height (cm)",
        min_value=1.0,
        step=0.1
    )

    activity_factor = st.selectbox(
        "Activity Factor",
        [1.2, 1.375, 1.55, 1.725, 1.9]
    )

    add_submit = st.form_submit_button("➕ Add Patient")

    if add_submit:

        if not name.strip():

            st.error("❌ Patient name cannot be empty.")

        else:

            patient = Patient(
                name=name,
                age=age,
                weight=weight,
                height=height,
                activity_factor=activity_factor
            )

            create_patient(patient)

            st.success("✅ Patient added successfully!")

# ==========================================================
# UPDATE PATIENT
# ==========================================================

st.divider()

st.subheader("✏️ Update Patient")

with st.form("update_patient_form"):

    update_name = st.text_input("Patient Name")

    update_age = st.number_input(
        "New Age",
        min_value=1,
        max_value=120,
        step=1
    )

    update_weight = st.number_input(
        "New Weight (kg)",
        min_value=1.0,
        step=0.1
    )

    update_height = st.number_input(
        "New Height (cm)",
        min_value=1.0,
        step=0.1
    )

    update_activity = st.selectbox(
        "New Activity Factor",
        [1.2, 1.375, 1.55, 1.725, 1.9],
        key="update_activity"
    )

    update_submit = st.form_submit_button("✏️ Update Patient")

    if update_submit:

        updated = edit_patient(
            update_name,
            update_age,
            update_weight,
            update_height,
            update_activity
        )

        if updated:

            st.success("✅ Patient updated successfully!")

        else:

            st.error("❌ Patient not found.")

# ==========================================================
# DELETE PATIENT
# ==========================================================

st.divider()

st.subheader("🗑 Delete Patient")

with st.form("delete_patient_form"):

    delete_name = st.text_input("Patient Name")

    delete_submit = st.form_submit_button("🗑 Delete Patient")

    if delete_submit:

        deleted = remove_patient(delete_name)

        if deleted:

            st.success("✅ Patient deleted successfully!")

        else:

            st.error("❌ Patient not found.")

# ==========================================================
# FOOTER
# ==========================================================

footer()