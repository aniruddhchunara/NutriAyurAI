from database.database import (
    get_patients,
    search_patient,
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
    name,
    age,
    weight,
    height,
    activity_factor
):
    """
    Update an existing patient.
    """
    return update_patient(
        name,
        age,
        weight,
        height,
        activity_factor
    )

def delete_existing_patient(name):
    """
    Delete patient from database.
    """
    return delete_patient(name)