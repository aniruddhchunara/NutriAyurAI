from datetime import date

from repository import *


def fetch_all_appointments():
    return get_all_appointments()


def fetch_appointment(patient_name):
    return get_appointment(patient_name)


def create_new_appointment(appointment):

    if not appointment.patient_name.strip():
        raise ValueError("Patient name is required.")

    if not appointment.doctor_name.strip():
        raise ValueError("Doctor name is required.")

    appointment_date = date.fromisoformat(
        str(appointment.appointment_date)
    )

    if appointment_date < date.today():
        raise ValueError(
            "Appointment date cannot be in the past."
        )

    return create_appointment(appointment)


def edit_existing_appointment(
    patient_name,
    doctor_name,
    appointment_date,
    appointment_time,
    reason
):

    return edit_appointment(
        patient_name,
        doctor_name,
        appointment_date,
        appointment_time,
        reason
    )


def delete_existing_appointment(patient_name):
    return remove_appointment(patient_name)