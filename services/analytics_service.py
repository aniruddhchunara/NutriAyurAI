import pandas as pd

from services.patient_service import fetch_all_patients
from services.appointment_service import fetch_all_appointments


# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

def get_dashboard_summary():
    """
    Prepare dashboard KPI data.
    """

    patients = fetch_all_patients()
    appointments = fetch_all_appointments()

    patient_count = len(patients)
    appointment_count = len(appointments)

    if patient_count == 0:

        avg_bmi = 0
        avg_weight = 0
        avg_height = 0

    else:

        bmi_list = []
        weight_list = []
        height_list = []

        for patient in patients:

            bmi_list.append(
                patient.calculate_bmi()
            )

            weight_list.append(
                patient.weight
            )

            height_list.append(
                patient.height
            )

        avg_bmi = sum(bmi_list) / len(bmi_list)
        avg_weight = sum(weight_list) / len(weight_list)
        avg_height = sum(height_list) / len(height_list)

    return {

        "patient_count": patient_count,

        "appointment_count": appointment_count,

        "average_bmi": round(avg_bmi, 2),

        "average_weight": round(avg_weight, 2),

        "average_height": round(avg_height, 2)

    }


# ==========================================================
# BMI DISTRIBUTION
# ==========================================================

def get_bmi_distribution():
    """
    Count patients in each BMI category.
    """

    patients = fetch_all_patients()

    bmi_data = {
        "Underweight": 0,
        "Normal": 0,
        "Overweight": 0,
        "Obese": 0
    }

    for patient in patients:

        bmi = patient.calculate_bmi()

        if bmi < 18.5:

            bmi_data["Underweight"] += 1

        elif bmi < 25:

            bmi_data["Normal"] += 1

        elif bmi < 30:

            bmi_data["Overweight"] += 1

        else:

            bmi_data["Obese"] += 1

    return pd.DataFrame({

        "Category": list(bmi_data.keys()),

        "Patients": list(bmi_data.values())

    })


# ==========================================================
# AGE DISTRIBUTION
# ==========================================================

def get_patient_age_data():
    """
    Return patient age data.
    """

    patients = fetch_all_patients()

    age_list = []

    for patient in patients:

        age_list.append(
            patient.age
        )

    return pd.DataFrame({

        "Age": age_list

    })


# ==========================================================
# APPOINTMENT TRENDS
# ==========================================================

def get_appointment_trends():
    """
    Return appointment counts grouped by date.
    """

    appointments = fetch_all_appointments()

    if len(appointments) == 0:

        return pd.DataFrame({

            "Date": [],

            "Appointments": []

        })

    date_list = []

    for appointment in appointments:

        date_list.append(
            appointment.appointment_date
        )

    df = pd.DataFrame({

        "Date": date_list

    })

    trend_df = (
        df.groupby("Date")
        .size()
        .reset_index(name="Appointments")
        .sort_values("Date")
    )

    return trend_df


# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

def get_business_insights():
    """
    Generate simple business insights.
    """

    patients = fetch_all_patients()

    if len(patients) == 0:

        return [

            "No patient data available."

        ]

    bmi_values = []
    age_values = []

    for patient in patients:

        bmi_values.append(
            patient.calculate_bmi()
        )

        age_values.append(
            patient.age
        )

    average_age = round(
        sum(age_values) / len(age_values),
        1
    )

    average_bmi = round(
        sum(bmi_values) / len(bmi_values),
        2
    )

    insights = []

    insights.append(
        f"👥 Total Registered Patients : {len(patients)}"
    )

    insights.append(
        f"📊 Average Age : {average_age} Years"
    )

    insights.append(
        f"❤️ Average BMI : {average_bmi}"
    )

    if average_bmi < 18.5:

        insights.append(
            "⚠ Most patients are Underweight."
        )

    elif average_bmi < 25:

        insights.append(
            "✅ Most patients are within the Healthy BMI range."
        )

    elif average_bmi < 30:

        insights.append(
            "⚠ Many patients are Overweight."
        )

    else:

        insights.append(
            "🚨 High Obesity Risk detected."
        )

    return insights