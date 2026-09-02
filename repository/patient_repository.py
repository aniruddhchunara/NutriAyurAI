from database.database import (
    get_patients,
    search_patient,
    search_patient_by_id,
    update_patient,
    delete_patient
)


def get_all_patients():
    """
    Return all patients from the database.
    """
    return get_patients()


def get_patient(name):
    """
    Return one patient by name.
    """
    return search_patient(name)


def update_existing_patient(
    patient_id,
    age,
    weight,
    height,
    activity_factor
):
    """
    Update an existing patient by ID.
    """
    return update_patient(
        patient_id,
        age,
        weight,
        height,
        activity_factor
    )


def delete_existing_patient(patient_id):
    """
    Delete a patient by ID.
    """
    return delete_patient(patient_id)


def get_patient_by_id(patient_id):
    """
    Return one patient by ID.
    """
    return search_patient_by_id(patient_id)