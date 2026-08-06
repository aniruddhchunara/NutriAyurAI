from analytics.data_loader import load_data
from database.database import update_patient

class PatientRepository:

    def get_all_patients(self):

        return load_data()
    
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