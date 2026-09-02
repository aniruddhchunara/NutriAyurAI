from repository import (
    get_all_patients,
    get_patient,
    update_existing_patient,
    get_patient_by_id,
    delete_existing_patient
)
from database.database import add_patient


def fetch_all_patients():
    """
    Fetch all patients from repository.
    """
    return get_all_patients()


def fetch_patient(name):
    """
    Fetch one patient by name.
    """
    return get_patient(name)


def create_patient(patient):
    """
    Save patient to database.
    """
    return add_patient(patient)


def edit_patient(
    patient_id,
    age,
    weight,
    height,
    activity_factor
):
    """
    Update patient information by ID.
    """
    return update_existing_patient(
        patient_id,
        age,
        weight,
        height,
        activity_factor
    )


def remove_patient(patient_id):
    """
    Delete patient by ID.
    """
    return delete_existing_patient(patient_id)


def fetch_patient_by_id(patient_id):
    """
    Fetch one patient directly from database by ID.
    """
    return get_patient_by_id(patient_id)