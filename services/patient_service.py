from repository import get_all_patients
from database.database import add_patient

def fetch_all_patients():
    """
    Fetch all patients from the repository.
    """
    return get_all_patients()

def create_patient(patient):
    """
    Save a patient using the database layer.
    """
    add_patient(patient)