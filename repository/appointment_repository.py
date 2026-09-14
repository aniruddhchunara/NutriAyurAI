from database.database import (
    get_appointments,
    add_appointment,
    search_appointment,
    update_appointment,
    delete_appointment
)


def get_all_appointments():
    return get_appointments()


def create_appointment(appointment):
    return add_appointment(appointment)


def get_appointment(patient_name):
    return search_appointment(patient_name)


def edit_appointment(
    appointment_id,
    doctor_name,
    appointment_date,
    appointment_time,
    reason
):

    return update_appointment(
        appointment_id,
        doctor_name,
        appointment_date,
        appointment_time,
        reason
    )


def remove_appointment(appointment_id):
    return delete_appointment(appointment_id)
