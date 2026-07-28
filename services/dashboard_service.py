from repository import get_all_patients
from utils import calculate_bmi


def get_dashboard_data_data(repository):
    """
    Load patient data and prepare dashboard metrics.
    """

    df = repository.get_all_patients()

    df["BMI"] = df.apply(
        lambda row: calculate_bmi(
            row["weight"],
            row["height"]
        ),
        axis=1
    )

    return df