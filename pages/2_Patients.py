import re

import streamlit as st
import pandas as pd

from models.patient import Patient

from services.patient_service import (
    fetch_all_patients,
    fetch_patient,
    fetch_patient_by_id,
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
# VALIDATION HELPERS
# ==========================================================

def validate_patient_name(name):
    """
    Validate patient name.
    """

    name = name.strip()

    if not name:
        return "Patient name is required."

    if len(name) < 2:
        return "Patient name must contain at least 2 characters."

    if len(name) > 100:
        return "Patient name must not exceed 100 characters."

    if not re.fullmatch(
        r"[A-Za-zÀ-ÖØ-öø-ÿ\s.'-]+",
        name
    ):
        return (
            "Patient name can contain letters, spaces, "
            "'.', '-' and apostrophe only."
        )

    return None


def validate_age(age):
    """
    Validate patient age.
    """

    if age is None:
        return "Age is required."

    if age < 1 or age > 120:
        return "Age must be between 1 and 120 years."

    return None


def validate_weight(weight):
    """
    Validate patient weight.
    """

    if weight is None:
        return "Weight is required."

    if weight < 2 or weight > 300:
        return "Weight must be between 2 and 300 kg."

    return None


def validate_height(height):
    """
    Validate patient height.
    """

    if height is None:
        return "Height is required."

    if height < 50 or height > 250:
        return "Height must be between 50 and 250 cm."

    return None


# ==========================================================
# LOAD PATIENTS
# ==========================================================

patients = fetch_all_patients()


# ==========================================================
# PATIENT RECORDS
# ==========================================================

st.subheader("📋 Patient Records")

if not patients:

    st.info("No patients found.")

else:

    patient_data = []

    for patient in patients:

        patient_data.append({
            "ID": patient.id,
            "Name": patient.name,
            "Age": patient.age,
            "Weight (kg)": patient.weight,
            "Height (cm)": patient.height,
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


# ==========================================================
# SEARCH PATIENT
# ==========================================================

st.divider()

st.subheader("🔍 Search Patient")

search_type = st.radio(
    "Search By",
    ["Patient Name", "Patient ID"],
    horizontal=True
)


if search_type == "Patient Name":

    search_name = st.text_input(
        "Patient Name",
        placeholder="e.g. Rahul Patel"
    )

    if search_name.strip():

        patient = fetch_patient(
            search_name.strip()
        )

        if patient:

            st.success("✅ Patient Found")

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Patient ID:** {patient.id}"
                )

                st.write(
                    f"**Name:** {patient.name}"
                )

                st.write(
                    f"**Age:** {patient.age}"
                )

                st.write(
                    f"**Weight:** {patient.weight} kg"
                )

            with col2:

                st.write(
                    f"**Height:** {patient.height} cm"
                )

                st.write(
                    f"**BMI:** {patient.calculate_bmi():.2f}"
                )

                st.write(
                    f"**Activity Factor:** "
                    f"{patient.activity_factor}"
                )

        else:

            st.error(
                "❌ Patient not found."
            )


else:

    search_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1,
        value=None,
        placeholder="e.g. 25"
    )

    if search_id is not None:

        try:

            search_id = int(search_id)

            patient = fetch_patient_by_id(
                search_id
            )

            if patient:

                st.success("✅ Patient Found")

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Patient ID:** {patient.id}"
                    )

                    st.write(
                        f"**Name:** {patient.name}"
                    )

                    st.write(
                        f"**Age:** {patient.age}"
                    )

                    st.write(
                        f"**Weight:** {patient.weight} kg"
                    )

                with col2:

                    st.write(
                        f"**Height:** {patient.height} cm"
                    )

                    st.write(
                        f"**BMI:** "
                        f"{patient.calculate_bmi():.2f}"
                    )

                    st.write(
                        f"**Activity Factor:** "
                        f"{patient.activity_factor}"
                    )

            else:

                st.error(
                    f"❌ No patient found with ID {search_id}."
                )

        except (ValueError, TypeError):

            st.error(
                "❌ Please enter a valid Patient ID."
            )


# ==========================================================
# ADD NEW PATIENT
# ==========================================================

st.divider()

st.subheader("➕ Add New Patient")

st.caption(
    "Enter the patient's details below. "
    "All fields must contain valid information."
)


with st.form(
    "add_patient_form",
    clear_on_submit=True
):

    add_col1, add_col2 = st.columns(2)

    with add_col1:

        name = st.text_input(
            "Patient Name",
            placeholder="e.g. Rahul Patel"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=None,
            step=1,
            placeholder="Enter age (1–120 years)"
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=2.0,
            max_value=300.0,
            value=None,
            step=0.1,
            placeholder="Enter weight (2–300 kg)"
        )

    with add_col2:

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=None,
            step=0.1,
            placeholder="Enter height (50–250 cm)"
        )

        activity_options = {
            "Sedentary — Little or no exercise": 1.2,
            "Lightly Active — Exercise 1–3 days/week": 1.375,
            "Moderately Active — Exercise 3–5 days/week": 1.55,
            "Very Active — Exercise 6–7 days/week": 1.725,
            "Extra Active — Very intense exercise/physical job": 1.9
        }

        activity_label = st.selectbox(
            "Activity Level",
            list(activity_options.keys())
        )

        activity_factor = activity_options[
            activity_label
        ]

    add_submit = st.form_submit_button(
        "➕ Add Patient"
    )

    if add_submit:

        name_error = validate_patient_name(name)
        age_error = validate_age(age)
        weight_error = validate_weight(weight)
        height_error = validate_height(height)

        if name_error:

            st.error(
                f"❌ {name_error}"
            )

        elif age_error:

            st.error(
                f"❌ {age_error}"
            )

        elif weight_error:

            st.error(
                f"❌ {weight_error}"
            )

        elif height_error:

            st.error(
                f"❌ {height_error}"
            )

        else:

            try:

                patient = Patient(
                    name=name.strip(),
                    age=age,
                    weight=weight,
                    height=height,
                    activity_factor=activity_factor
                )

                create_patient(patient)

                st.success(
                    "✅ Patient added successfully!"
                )

                st.rerun()

            except ValueError as error:

                st.error(
                    f"❌ {error}"
                )

            except Exception:

                st.error(
                    "❌ Unable to add patient. "
                    "Please try again."
                )
# ==========================================================
# UPDATE EXISTING PATIENT
# ==========================================================

st.divider()

st.subheader("✏️ Update Existing Patient")

st.caption(
    "Select the exact patient record you want to update. "
    "The current patient information will be loaded automatically."
)


if not patients:

    st.info(
        "No patients available to update."
    )

else:

    patient_options = {
        f"{patient.name} | ID: {patient.id}": patient.id
        for patient in patients
    }

    selected_patient = st.selectbox(
        "Select Existing Patient",
        list(patient_options.keys()),
        index=None,
        placeholder="Select a patient..."
    )

    if selected_patient is not None:

        patient_id = patient_options[
            selected_patient
        ]

        selected_patient_data = next(
            (
                patient
                for patient in patients
                if patient.id == patient_id
            ),
            None
        )

        if selected_patient_data:

            activity_labels = {
                1.2: "Sedentary — Little or no exercise",
                1.375: "Lightly Active — Exercise 1–3 days/week",
                1.55: "Moderately Active — Exercise 3–5 days/week",
                1.725: "Very Active — Exercise 6–7 days/week",
                1.9: "Extra Active — Very intense exercise/physical job"
            }

            activity_map = {
                "Sedentary — Little or no exercise": 1.2,
                "Lightly Active — Exercise 1–3 days/week": 1.375,
                "Moderately Active — Exercise 3–5 days/week": 1.55,
                "Very Active — Exercise 6–7 days/week": 1.725,
                "Extra Active — Very intense exercise/physical job": 1.9
            }

            current_activity = activity_labels.get(
                selected_patient_data.activity_factor,
                "Moderately Active — Exercise 3–5 days/week"
            )

            with st.form("update_patient_form"):

                update_col1, update_col2 = st.columns(2)

                with update_col1:

                    update_age = st.number_input(
                        "Age",
                        min_value=1,
                        max_value=120,
                        value=int(selected_patient_data.age),
                        step=1,
                        help="Enter age between 1 and 120 years."
                    )

                    update_weight = st.number_input(
                        "Weight (kg)",
                        min_value=2.0,
                        max_value=300.0,
                        value=float(selected_patient_data.weight),
                        step=0.1,
                        help="Enter weight between 2 and 300 kg."
                    )

                with update_col2:

                    update_height = st.number_input(
                        "Height (cm)",
                        min_value=50.0,
                        max_value=250.0,
                        value=float(selected_patient_data.height),
                        step=0.1,
                        help="Enter height between 50 and 250 cm."
                    )

                    update_activity = st.selectbox(
                        "Activity Level",
                        list(activity_map.keys()),
                        index=list(activity_map.keys()).index(
                            current_activity
                        ),
                        help="Select the patient's normal activity level."
                    )

                update_submit = st.form_submit_button(
                    "✏️ Update Patient",
                    use_container_width=True
                )

                if update_submit:

                    age_error = validate_age(
                        update_age
                    )

                    weight_error = validate_weight(
                        update_weight
                    )

                    height_error = validate_height(
                        update_height
                    )

                    if age_error:

                        st.error(
                            f"❌ {age_error}"
                        )

                    elif weight_error:

                        st.error(
                            f"❌ {weight_error}"
                        )

                    elif height_error:

                        st.error(
                            f"❌ {height_error}"
                        )

                    else:

                        try:

                            update_activity_factor = activity_map[
                                update_activity
                            ]

                            updated = edit_patient(
                                patient_id,
                                update_age,
                                update_weight,
                                update_height,
                                update_activity_factor
                            )

                            if updated:

                                st.success(
                                    "✅ Patient updated successfully!"
                                )

                                st.rerun()

                            else:

                                st.error(
                                    "❌ Patient not found."
                                )

                        except ValueError as error:

                            st.error(
                                f"❌ {error}"
                            )

                        except Exception:

                            st.error(
                                "❌ Unable to update patient. "
                                "Please try again."
                            )


# ==========================================================
# DELETE PATIENT
# ==========================================================

st.divider()

st.subheader("🗑 Delete Patient")

st.caption(
    "Select the exact patient record you want to delete."
)


if not patients:

    st.info(
        "No patients available to delete."
    )

else:

    delete_options = {
        f"{patient.name} | ID: {patient.id}": patient.id
        for patient in patients
    }

    with st.form("delete_patient_form"):

        selected_delete_patient = st.selectbox(
            "Select Patient to Delete",
            list(delete_options.keys()),
            index=None,
            placeholder="Select a patient..."
        )

        delete_submit = st.form_submit_button(
            "🗑 Delete Patient"
        )

        if delete_submit:

            if selected_delete_patient is None:

                st.error(
                    "❌ Please select a patient."
                )

            else:

                patient_id = delete_options[
                    selected_delete_patient
                ]

                try:

                    deleted = remove_patient(
                        patient_id
                    )

                    if deleted:

                        st.success(
                            "✅ Patient deleted successfully!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "❌ Patient not found."
                        )

                except ValueError as error:

                    st.error(
                        f"❌ {error}"
                    )

                except Exception:

                    st.error(
                        "❌ Unable to delete patient. "
                        "Please try again."
                    )


# ==========================================================
# FOOTER
# ==========================================================

footer()