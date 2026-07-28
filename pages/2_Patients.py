import streamlit as st
import pandas as pd

from components import (
    load_theme,
    navbar,
    app_sidebar,
    footer,
    data_table
)

from services.patient_service import fetch_all_patients


# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Patients",
    page_icon="👤",
    layout="wide"
)

load_theme()

app_sidebar()

navbar(
    "Patient Management",
    "Manage all patient records"
)

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

patients = fetch_all_patients()

# ---------------------------------------
# PAGE CONTENT
# ---------------------------------------

st.subheader("📋 Patient Records")

if len(patients) == 0:

    st.warning("No patients found.")

else:

    patient_data = []

    for patient in patients:

        patient_data.append({

            "Name": patient.name,

            "Age": patient.age,

            "Weight": patient.weight,

            "Height": patient.height,

            "BMI": round(
                patient.calculate_bmi(),
                2
            )

        })

    df = pd.DataFrame(patient_data)

    data_table(
        df,
        title="All Patients"
    )

footer()