from repository import get_all_patients, get_patient
from database.database import add_patient
from repository import update_existing_patient
from repository import delete_existing_patient

def fetch_all_patients():
    """
    Fetch all patients from repository.
    """
    return get_all_patients()


def fetch_patient(name):
    """
    Fetch one patient from repository.
    """
    return get_patient(name)


def create_patient(patient):
    """
    Save patient to database.
    """
    add_patient(patient)


def edit_patient(
    name,
    age,
    weight,
    height,
    activity_factor
):
    
    """
    Update patient information.
    """
    return update_existing_patient(
        name,
        age,
        weight,
        height,
        activity_factor
    )


def remove_patient(name):
    """
    Delete patient.
    """
    return delete_existing_patient(name)

