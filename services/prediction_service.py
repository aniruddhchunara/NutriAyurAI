from math import isfinite


# ==========================================================
# PREDICT HEALTH STATUS
# ==========================================================

def predict_health_status(
    age,
    weight,
    height,
    activity_factor
):
    """
    Predict health status and nutrition requirements.
    """

    # ======================================================
    # INPUT VALIDATION
    # ======================================================

    # ------------------------------------------------------
    # AGE
    # ------------------------------------------------------

    if not isinstance(age, (int, float)) or isinstance(age, bool):
        raise ValueError(
            "Age must be a valid number."
        )

    if not isfinite(float(age)):
        raise ValueError(
            "Age must be a valid finite number."
        )

    if age < 1 or age > 120:
        raise ValueError(
            "Age must be between 1 and 120 years."
        )

    # ------------------------------------------------------
    # WEIGHT
    # ------------------------------------------------------

    if not isinstance(weight, (int, float)) or isinstance(weight, bool):
        raise ValueError(
            "Weight must be a valid number."
        )

    if not isfinite(float(weight)):
        raise ValueError(
            "Weight must be a valid finite number."
        )

    if weight < 2 or weight > 300:
        raise ValueError(
            "Weight must be between 2 and 300 kg."
        )

    # ------------------------------------------------------
    # HEIGHT
    # ------------------------------------------------------

    if not isinstance(height, (int, float)) or isinstance(height, bool):
        raise ValueError(
            "Height must be a valid number."
        )

    if not isfinite(float(height)):
        raise ValueError(
            "Height must be a valid finite number."
        )

    if height < 50 or height > 250:
        raise ValueError(
            "Height must be between 50 and 250 cm."
        )

    # ------------------------------------------------------
    # ACTIVITY FACTOR
    # ------------------------------------------------------

    if not isinstance(
        activity_factor,
        (int, float)
    ) or isinstance(activity_factor, bool):
        raise ValueError(
            "Activity factor must be a valid number."
        )

    if not isfinite(float(activity_factor)):
        raise ValueError(
            "Activity factor must be a valid finite number."
        )

    valid_activity_factors = {
        1.2,
        1.375,
        1.55,
        1.725,
        1.9
    }

    if activity_factor not in valid_activity_factors:
        raise ValueError(
            "Invalid activity level."
        )

    # ======================================================
    # BMI
    # ======================================================

    height_m = height / 100

    bmi = weight / (height_m ** 2)

    if not isfinite(float(bmi)):
        raise ValueError(
            "Unable to calculate a valid BMI."
        )

    if bmi < 18.5:

        status = "Underweight"

        recommendation = (
            "Increase calorie intake and "
            "eat a balanced diet."
        )

    elif bmi < 25:

        status = "Healthy"

        recommendation = (
            "Maintain your current healthy lifestyle."
        )

    elif bmi < 30:

        status = "Overweight"

        recommendation = (
            "Exercise regularly and "
            "reduce sugar intake."
        )

    else:

        status = "Obese"

        recommendation = (
            "Consult a healthcare professional "
            "and follow a structured weight "
            "management plan."
        )

    # ======================================================
    # BMR
    # Mifflin-St Jeor Equation
    # ======================================================

    bmr = (
        (10 * weight)
        + (6.25 * height)
        - (5 * age)
        + 5
    )

    if not isfinite(float(bmr)):
        raise ValueError(
            "Unable to calculate a valid BMR."
        )

    # ======================================================
    # TDEE / CALORIES
    # ======================================================

    calories = bmr * activity_factor

    if not isfinite(float(calories)):
        raise ValueError(
            "Unable to calculate daily calories."
        )

    # ======================================================
    # PROTEIN
    # ======================================================

    protein = weight * 1.2

    if not isfinite(float(protein)):
        raise ValueError(
            "Unable to calculate protein requirement."
        )

    # ======================================================
    # WATER
    # ======================================================

    water = (weight * 35) / 1000

    if not isfinite(float(water)):
        raise ValueError(
            "Unable to calculate water requirement."
        )

    # ======================================================
    # HEALTH SCORE
    # ======================================================

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

    # ======================================================
    # IDEAL WEIGHT RANGE
    # ======================================================

    ideal_min = 18.5 * (height_m ** 2)

    ideal_max = 24.9 * (height_m ** 2)

    if not isfinite(float(ideal_min)):
        raise ValueError(
            "Unable to calculate ideal weight."
        )

    if not isfinite(float(ideal_max)):
        raise ValueError(
            "Unable to calculate ideal weight."
        )

    # ======================================================
    # WEIGHT GOAL
    # ======================================================

    if weight > ideal_max:

        goal = (
            f"Lose {round(weight - ideal_max, 1)} kg"
        )

    elif weight < ideal_min:

        goal = (
            f"Gain {round(ideal_min - weight, 1)} kg"
        )

    else:

        goal = "Maintain Current Weight"

    # ======================================================
    # RETURN RESULT
    # ======================================================

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