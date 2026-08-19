from services.diet_plan_service import (
    fetch_diet_plans,
    fetch_diet_plan_meals
)


# ==========================================================
# FETCH PATIENT DIET HISTORY
# ==========================================================

def fetch_patient_diet_history(
    patient_name
):
    """
    Fetch all diet plans belonging to a patient.

    Returns a list containing:
        - plan
        - status
        - created date
        - updated date
        - meal count
        - total calories
        - total protein
    """

    if not patient_name:
        return []

    # ======================================================
    # FETCH PATIENT PLANS
    # ======================================================

    plans = fetch_diet_plans(
        patient_name
    )

    history = []

    # ======================================================
    # PROCESS EACH PLAN
    # ======================================================

    for plan in plans:

        plan_id = plan[0]
        plan_name = plan[2]
        created_at = plan[3]

        status = (
            plan[4]
            if len(plan) > 4 and plan[4]
            else "Active"
        )

        updated_at = (
            plan[5]
            if len(plan) > 5 and plan[5]
            else "Not updated"
        )

        # ==================================================
        # FETCH MEALS
        # ==================================================

        meals = fetch_diet_plan_meals(
            plan_id
        )

        total_meals = len(meals)

        total_calories = 0
        total_protein = 0

        # ==================================================
        # CALCULATE NUTRITION TOTALS
        # ==================================================

        for meal in meals:

            # Calories
            if len(meal) > 3:

                try:

                    total_calories += float(
                        meal[3] or 0
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # Protein
            if len(meal) > 4:

                try:

                    total_protein += float(
                        meal[4] or 0
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

        # ==================================================
        # ADD HISTORY RECORD
        # ==================================================

        history.append(
            {
                "plan_id": plan_id,
                "plan_name": plan_name,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
                "meal_count": total_meals,
                "total_calories": total_calories,
                "total_protein": total_protein
            }
        )

    return history


# ==========================================================
# GET HISTORY SUMMARY
# ==========================================================

def get_patient_history_summary(
    patient_name
):

    history = fetch_patient_diet_history(
        patient_name
    )

    total_plans = len(history)

    active_plans = sum(
        1
        for plan in history
        if plan["status"] == "Active"
    )

    completed_plans = sum(
        1
        for plan in history
        if plan["status"] == "Completed"
    )

    paused_plans = sum(
        1
        for plan in history
        if plan["status"] == "Paused"
    )

    archived_plans = sum(
        1
        for plan in history
        if plan["status"] == "Archived"
    )

    return {
        "total_plans": total_plans,
        "active_plans": active_plans,
        "completed_plans": completed_plans,
        "paused_plans": paused_plans,
        "archived_plans": archived_plans
    }