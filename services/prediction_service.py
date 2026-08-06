import streamlit as st

# from services.prediction_service import predict_health_status

from components import (
    load_theme,
    navbar,
    app_sidebar,
    footer
)
st.set_page_config(
    page_title="AI Prediction",
    page_icon="🤖",
    layout="wide"
)

load_theme()
app_sidebar()

navbar(
    "AI Prediction",
    "Health Prediction using AI"
)


def predict_health_status(age, weight, height, activity_factor):
    """
    Predict health status and nutrition requirements.
    """

    # ==========================================
    # BMI
    # ==========================================

    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        status = "Underweight"
        recommendation = (
            "Increase calorie intake and eat a balanced diet."
        )

    elif bmi < 25:
        status = "Healthy"
        recommendation = (
            "Maintain your current healthy lifestyle."
        )

    elif bmi < 30:
        status = "Overweight"
        recommendation = (
            "Exercise regularly and reduce sugar intake."
        )

    else:
        status = "Obese"
        recommendation = (
            "Consult a healthcare professional and follow a structured weight management plan."
        )

    # ==========================================
    # BMR (Mifflin-St Jeor Equation)
    # ==========================================

    bmr = (
        (10 * weight)
        + (6.25 * height)
        - (5 * age)
        + 5
    )

    # ==========================================
    # TDEE
    # ==========================================

    calories = bmr * activity_factor

    # ==========================================
    # Protein
    # ==========================================

    protein = weight * 1.2

    # ==========================================
    # Water
    # ==========================================

    water = (weight * 35) / 1000

    # ==========================================
    # Health Score
    # ==========================================

    if 18.5 <= bmi < 25:
        health_score = 100

    elif 25 <= bmi < 30:
        health_score = 80

    elif 30 <= bmi < 35:
        health_score = 60

    elif bmi >= 35:
        health_score = 40

    else:
        health_score = 70

    # ==========================================
    # Ideal Weight Range
    # ==========================================

    height_m = height / 100

    ideal_min = 18.5 * (height_m ** 2)
    ideal_max = 24.9 * (height_m ** 2)

    # ==========================================
    # Weight Goal
    # ==========================================

    if weight > ideal_max:

        goal = f"Lose {round(weight - ideal_max, 1)} kg"

    elif weight < ideal_min:

        goal = f"Gain {round(ideal_min - weight, 1)} kg"

    else:

        goal = "Maintain Current Weight"

    # ==========================================
    # Return Result
    # ==========================================

    return {

        "Name": "",

        "Age": age,

        "Weight": weight,

        "Height": height,

        "Activity Factor": activity_factor,

        "BMI": round(bmi, 2),

        "Status": status,

        "Recommendation": recommendation,

        "BMR": round(bmr),

        "Calories": round(calories),

        "Protein": round(protein, 1),

        "Water": round(water, 2),

        "Health Score": health_score,

        "Ideal Min": round(ideal_min, 1),

        "Ideal Max": round(ideal_max, 1),

        "Goal": goal

    }