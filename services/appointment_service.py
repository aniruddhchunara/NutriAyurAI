from repository import *


def fetch_all_appointments():
    return get_all_appointments()


def fetch_appointment(patient_name):
    return get_appointment(patient_name)


def create_new_appointment(appointment):
    create_appointment(appointment)


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