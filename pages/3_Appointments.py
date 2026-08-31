import streamlit as st
import pandas as pd
from datetime import date

from models.appointment import Appointment

from components import (
    load_theme,
    navbar,
    app_sidebar,
    footer,
    data_table
)

from services.appointment_service import (
    fetch_all_appointments,
    create_new_appointment,
    fetch_appointment,
    edit_existing_appointment,
    delete_existing_appointment
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Appointment Management",
    page_icon="📅",
    layout="wide"
)

# ==========================================================
# LOAD UI
# ==========================================================

load_theme()

app_sidebar()

navbar(
    "Appointment Management",
    "Manage all appointments"
)

# ==========================================================
# LOAD DATA
# ==========================================================

appointments = fetch_all_appointments()

# ==========================================================
# APPOINTMENT TABLE
# ==========================================================

st.subheader("📋 Appointment Records")

if not appointments:

    st.warning("No appointments found.")

else:

    appointment_data = []

    for appointment in appointments:

        appointment_data.append({

            "Patient": appointment.patient_name,
            "Doctor": appointment.doctor_name,
            "Date": appointment.appointment_date,
            "Time": appointment.appointment_time,
            "Reason": appointment.reason

        })

    df = pd.DataFrame(appointment_data)

    data_table(
        df,
        title="All Appointments"
    )



st.divider()

st.subheader("🔍 Search Appointment")

search_patient = st.text_input(
    "Enter Patient Name"
)

if search_patient:

    appointment = fetch_appointment(search_patient)

    if appointment:

        st.success("✅ Appointment Found")

        col1, col2 = st.columns(2)

        with col1:

            st.write(f"**Patient:** {appointment.patient_name}")
            st.write(f"**Doctor:** {appointment.doctor_name}")
            st.write(f"**Date:** {appointment.appointment_date}")

        with col2:

            st.write(f"**Time:** {appointment.appointment_time}")
            st.write(f"**Reason:** {appointment.reason}")

    else:

        st.error("❌ Appointment not found.")


st.divider()

st.subheader("✏️ Update Appointment")

with st.form(
    "update_appointment_form",
    clear_on_submit=True
):

    update_patient = st.text_input("Patient Name")

    update_doctor = st.text_input("Doctor Name")

    update_date = st.date_input("New Appointment Date")

    update_time = st.time_input("New Appointment Time")

    update_reason = st.text_area("Reason")

    update_submit = st.form_submit_button(
        "✏️ Update Appointment"
    )
    if update_submit:

        updated = edit_existing_appointment(
            update_patient,
            update_doctor,
            str(update_date),
            str(update_time),
            update_reason
        )

        if updated:

            st.success(
                "✅ Appointment updated successfully!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Appointment not found."
            )

# ==========================================================
# DELETE APPOINTMENT
# ==========================================================

st.divider()

st.subheader("🗑 Delete Appointment")

with st.form(
    "delete_appointment_form",
    clear_on_submit=True
):

    delete_patient = st.text_input(
        "Patient Name"
    )

    delete_submit = st.form_submit_button(
        "🗑 Delete Appointment"
    )

    if delete_submit:

        deleted = delete_existing_appointment(
            delete_patient
        )

        if deleted:

            st.success(
                "✅ Appointment deleted successfully!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Appointment not found."
            )


# ==========================================================
# ADD APPOINTMENT
# ==========================================================

st.divider()

st.subheader("➕ Add Appointment")

with st.form("appointment_form", clear_on_submit=True):

    patient_name = st.text_input(
        "Patient Name"
    )

    doctor_name = st.text_input(
        "Doctor Name"
    )

    appointment_date = st.date_input(
        "Appointment Date"
    )

    appointment_time = st.time_input(
        "Appointment Time"
    )

    reason = st.text_area(
        "Reason"
    )

    submit = st.form_submit_button(
        "➕ Add Appointment", 
    )

    if submit:

        if patient_name.strip() == "":

            st.error("Patient name is required.")

        elif doctor_name.strip() == "":

            st.error("Doctor name is required.")

        else:

            appointment = Appointment(

                patient_name=patient_name,

                doctor_name=doctor_name,

                appointment_date=str(appointment_date),

                appointment_time=str(appointment_time),

                reason=reason.strip()

            )

            try:

                create_new_appointment(
                    appointment
                )

                st.success(
                    "✅ Appointment created successfully!"
                )

                st.rerun()

            except ValueError as e:

                st.error(str(e))



# ==========================================================
# FOOTER
# ==========================================================

footer()