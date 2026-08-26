from repository.diet_plan_repository import (
    create_diet_plan,
    add_diet_plan_meal,
    get_diet_plans,
    get_diet_plan_meals,
    update_diet_plan_meal,
    delete_diet_plan_meal,
    update_diet_plan_status,
    get_diet_plan,
    find_duplicate_diet_plan
)
from datetime import date

# ==========================================================
# CREATE DIET PLAN
# ==========================================================

def create_new_diet_plan(
    patient_name,
    plan_name,
    start_date=None,
    end_date=None,
    duration_days=None
):

    if not patient_name:
        raise ValueError(
            "Patient name is required."
        )

from repository.diet_plan_repository import (
    create_diet_plan,
    add_diet_plan_meal,
    get_diet_plans,
    get_diet_plan_meals,
    update_diet_plan_meal,
    delete_diet_plan_meal,
    delete_diet_plan,
    update_diet_plan_status,
    get_diet_plan
)

# ==========================================================
# CREATE DIET PLAN
# ==========================================================

def create_new_diet_plan(
    patient_name,
    plan_name,
    start_date=None,
    end_date=None,
    duration_days=None
):

    # ======================================================
    # BASIC VALIDATION
    # ======================================================

    if not patient_name:
        raise ValueError(
            "Patient name is required."
        )

    if not plan_name or not plan_name.strip():
        raise ValueError(
            "Diet plan name is required."
        )

    # ======================================================
    # DURATION VALIDATION
    # ======================================================

    if duration_days is not None:

        if duration_days <= 0:
            raise ValueError(
                "Duration must be greater than 0 days."
            )

    if isinstance(start_date, str) and start_date:
        start_date = date.fromisoformat(start_date)

    if isinstance(end_date, str) and end_date:
        end_date = date.fromisoformat(end_date)

    # ======================================================
    # DATE VALIDATION
    # ======================================================

    if start_date is not None and end_date is not None:

        if end_date < start_date:
            raise ValueError(
                "End date cannot be before start date."
            )

        calculated_duration = (
            end_date - start_date
        ).days + 1

        if duration_days is not None:

            if duration_days != calculated_duration:
                raise ValueError(
                    "Duration does not match the selected dates."
                )

    # ======================================================
    # DUPLICATE PLAN VALIDATION
    # ======================================================

    if (
        start_date is not None
        and end_date is not None
    ):

        duplicate_plan = find_duplicate_diet_plan(
            patient_name,
            plan_name.strip(),
            start_date,
            end_date
        )

        if duplicate_plan:

            raise ValueError(
                "A diet plan with the same patient, "
                "plan name, and schedule already exists."
            )

    # ======================================================
    # CREATE DIET PLAN
    # ======================================================

    return create_diet_plan(
        patient_name,
        plan_name.strip(),
        start_date,
        end_date,
        duration_days
    )


# ==========================================================
# FETCH PATIENT DIET HISTORY
# ==========================================================

def fetch_patient_diet_history(
    patient_name
):

    if not patient_name:
        raise ValueError(
            "Patient name is required."
        )

    plans = fetch_diet_plans(
        patient_name
    )

    history = []

    for plan in plans:

        plan_id = plan[0]
        plan_name = plan[2]
        created_at = plan[3]

        status = (
            plan[4]
            if plan[4]
            else "Active"
        )

        updated_at = (
            plan[5]
            if plan[5]
            else "Not updated yet"
        )

        meals = fetch_diet_plan_meals(
            plan_id
        )

        total_calories = sum(
            float(meal[3] or 0)
            for meal in meals
        )

        total_protein = sum(
            float(meal[4] or 0)
            for meal in meals
        )

        history.append(
            {
                "plan_id": plan_id,
                "plan_name": plan_name,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
                "meal_count": len(meals),
                "total_calories": total_calories,
                "total_protein": total_protein
            }
        )

    return history


# ==========================================================
# GET PATIENT HISTORY SUMMARY
# ==========================================================

def get_patient_history_summary(
    patient_name
):

    history = fetch_patient_diet_history(
        patient_name
    )

    return {
        "total_plans": len(history),

        "active_plans": sum(
            1
            for plan in history
            if plan["status"] == "Active"
        ),

        "paused_plans": sum(
            1
            for plan in history
            if plan["status"] == "Paused"
        ),

        "completed_plans": sum(
            1
            for plan in history
            if plan["status"] == "Completed"
        ),

        "archived_plans": sum(
            1
            for plan in history
            if plan["status"] == "Archived"
        )
    }


# ==========================================================
# ADD MEAL TO DIET PLAN
# ==========================================================

def add_meal_to_plan(
    diet_plan_id,
    meal_type,
    meal_time,
    calories,
    protein,
    food_items,
    rasa,
    virya,
    digestion,
    notes
):

    # ======================================================
    # BASIC VALIDATION
    # ======================================================

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    if not meal_type or not meal_type.strip():
        raise ValueError(
            "Meal type is required."
        )

    if not meal_time or not meal_time.strip():
        raise ValueError(
            "Meal time is required."
        )

    if not food_items or not food_items.strip():
        raise ValueError(
            "Food items are required."
        )

# ==========================================================
# ADD MEAL TO DIET PLAN
# ==========================================================

def add_meal_to_plan(
    diet_plan_id,
    meal_type,
    meal_time,
    calories,
    protein,
    food_items,
    rasa,
    virya,
    digestion,
    notes
):

    # ======================================================
    # BASIC VALIDATION
    # ======================================================

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    if not meal_type or not meal_type.strip():
        raise ValueError(
            "Meal type is required."
        )

    if not meal_time or not meal_time.strip():
        raise ValueError(
            "Meal time is required."
        )

    if not food_items or not food_items.strip():
        raise ValueError(
            "Food items are required."
        )

    # ======================================================
    # DEFAULT NUTRITION VALUES
    # ======================================================

    if calories is None:
        calories = 0

    if protein is None:
        protein = 0

    # ======================================================
    # NUTRITION VALIDATION
    # ======================================================

    if calories < 0:
        raise ValueError(
            "Calories cannot be negative."
        )

    if protein < 0:
        raise ValueError(
            "Protein cannot be negative."
        )

    # ======================================================
    # SAVE MEAL
    # ======================================================

    return add_diet_plan_meal(
        diet_plan_id,
        meal_type.strip(),
        meal_time.strip(),
        calories,
        protein,
        food_items.strip(),
        rasa,
        virya,
        digestion,
        notes.strip() if notes else ""
    )



# ==========================================================
# FETCH DIET PLANS
# ==========================================================

def fetch_diet_plans(
    patient_name=None
):

    return get_diet_plans(
        patient_name
    )


# ==========================================================
# FETCH DIET PLAN MEALS
# ==========================================================

def fetch_diet_plan_meals(
    diet_plan_id
):

    return get_diet_plan_meals(
        diet_plan_id
    )


# ==========================================================
# UPDATE DIET PLAN MEAL
# ==========================================================

def update_meal(
    meal_id,
    meal_type,
    meal_time,
    calories,
    protein,
    food_items,
    rasa,
    virya,
    digestion,
    notes
):

    if not meal_id:
        raise ValueError(
            "Meal ID is required."
        )

    if not meal_type:
        raise ValueError(
            "Meal type is required."
        )

    if not food_items or not food_items.strip():
        raise ValueError(
            "Food items are required."
        )

    if calories < 0:
        raise ValueError(
            "Calories cannot be negative."
        )

    if protein < 0:
        raise ValueError(
            "Protein cannot be negative."
        )

    return update_diet_plan_meal(
        meal_id,
        meal_type,
        meal_time,
        calories,
        protein,
        food_items.strip(),
        rasa,
        virya,
        digestion,
        notes.strip() if notes else ""
    )


# ==========================================================
# DELETE DIET PLAN MEAL
# ==========================================================

def delete_meal(
    meal_id
):

    if not meal_id:
        raise ValueError(
            "Meal ID is required."
        )

    return delete_diet_plan_meal(
        meal_id
    )


# ==========================================================
# DELETE DIET PLAN
# ==========================================================

def delete_existing_diet_plan(
    diet_plan_id
):

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    return delete_diet_plan(
        diet_plan_id
    )


# ==========================================================
# FETCH SINGLE DIET PLAN
# ==========================================================

def fetch_diet_plan(
    diet_plan_id
):

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    return get_diet_plan(
        diet_plan_id
    )


# ==========================================================
# UPDATE DIET PLAN STATUS
# ==========================================================

def update_plan_status(
    diet_plan_id,
    status
):

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    allowed_statuses = [
        "Active",
        "Paused",
        "Completed",
        "Archived"
    ]

    if status not in allowed_statuses:
        raise ValueError(
            "Invalid diet plan status."
        )

    return update_diet_plan_status(
        diet_plan_id,
        status
    )


# ==========================================================
# APPLY DIET PLAN TEMPLATE
# ==========================================================

def apply_diet_plan_template(
    diet_plan_id,
    template_name
):

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    if not template_name:
        raise ValueError(
            "Template name is required."
        )

    from services.diet_plan_template_service import (
        get_diet_plan_template
    )

    template = get_diet_plan_template(
        template_name
    )

    meals = template["meals"]

    added_meals = []

    for meal in meals:

        meal_id = add_diet_plan_meal(
            diet_plan_id,
            meal["meal_type"],
            meal["meal_time"],
            meal["calories"],
            meal["protein"],
            meal["food_items"],
            meal["rasa"],
            meal["virya"],
            meal["digestion"],
            meal["notes"]
        )

        added_meals.append(
            meal_id
        )

    return added_meals

    if not plan_name or not plan_name.strip():
        raise ValueError(
            "Diet plan name is required."
        )

    if duration_days is not None and duration_days <= 0:
        raise ValueError(
            "Duration must be greater than 0 days."
        )

    return create_diet_plan(
        patient_name,
        plan_name.strip(),
        start_date,
        end_date,
        duration_days
    )


# ==========================================================
# FETCH PATIENT DIET HISTORY
# ==========================================================

def fetch_patient_diet_history(
    patient_name
):

    if not patient_name:
        raise ValueError(
            "Patient name is required."
        )

    plans = fetch_diet_plans(
        patient_name
    )

    history = []

    for plan in plans:

        plan_id = plan[0]
        plan_name = plan[2]
        created_at = plan[3]
        status = plan[4] if plan[4] else "Active"
        updated_at = plan[5] if plan[5] else "Not updated yet"

        meals = fetch_diet_plan_meals(
            plan_id
        )

        total_calories = sum(
            float(meal[3] or 0)
            for meal in meals
        )

        total_protein = sum(
            float(meal[4] or 0)
            for meal in meals
        )

        history.append(
            {
                "plan_id": plan_id,
                "plan_name": plan_name,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
                "meal_count": len(meals),
                "total_calories": total_calories,
                "total_protein": total_protein
            }
        )

    return history


# ==========================================================
# GET PATIENT HISTORY SUMMARY
# ==========================================================

def get_patient_history_summary(
    patient_name
):

    history = fetch_patient_diet_history(
        patient_name
    )

    return {
        "total_plans": len(history),

        "active_plans": sum(
            1
            for plan in history
            if plan["status"] == "Active"
        ),

        "paused_plans": sum(
            1
            for plan in history
            if plan["status"] == "Paused"
        ),

        "completed_plans": sum(
            1
            for plan in history
            if plan["status"] == "Completed"
        ),

        "archived_plans": sum(
            1
            for plan in history
            if plan["status"] == "Archived"
        )
    }


# ==========================================================
# ADD MEAL TO DIET PLAN
# ==========================================================

def add_meal_to_plan(
    diet_plan_id,
    meal_type,
    meal_time,
    calories,
    protein,
    food_items,
    rasa,
    virya,
    digestion,
    notes
):

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    # ======================================================
    # DIET PLAN EXISTENCE VALIDATION
    # ======================================================

    diet_plan = get_diet_plan(
        diet_plan_id
    )

    if not diet_plan:
        raise ValueError(
            "The selected diet plan does not exist."
        )

    if not meal_type or not meal_type.strip():
        raise ValueError(
            "Meal type is required."
        )

    if not meal_time or not meal_time.strip():
        raise ValueError(
            "Meal time is required."
        )

    if not food_items or not food_items.strip():
        raise ValueError(
            "Food items are required."
        )

    if calories is None:
        calories = 0

    if protein is None:
        protein = 0

    if calories < 0:
        raise ValueError(
            "Calories cannot be negative."
        )

    if protein < 0:
        raise ValueError(
            "Protein cannot be negative."
        )

    return add_diet_plan_meal(
        diet_plan_id,
        meal_type.strip(),
        meal_time.strip(),
        calories,
        protein,
        food_items.strip(),
        rasa,
        virya,
        digestion,
        notes.strip() if notes else ""
    )




# ==========================================================
# FETCH DIET PLANS
# ==========================================================

def fetch_diet_plans(
    patient_name=None
):

    return get_diet_plans(
        patient_name
    )


# ==========================================================
# FETCH DIET PLAN MEALS
# ==========================================================

def fetch_diet_plan_meals(
    diet_plan_id
):

    return get_diet_plan_meals(
        diet_plan_id
    )


# ==========================================================
# UPDATE DIET PLAN MEAL
# ==========================================================

def update_meal(
    meal_id,
    meal_type,
    meal_time,
    calories,
    protein,
    food_items,
    rasa,
    virya,
    digestion,
    notes
):

    if not meal_id:
        raise ValueError(
            "Meal ID is required."
        )

    if not meal_type:
        raise ValueError(
            "Meal type is required."
        )

    if not food_items or not food_items.strip():
        raise ValueError(
            "Food items are required."
        )

    if calories < 0:
        raise ValueError(
            "Calories cannot be negative."
        )

    if protein < 0:
        raise ValueError(
            "Protein cannot be negative."
        )

    return update_diet_plan_meal(
        meal_id,
        meal_type,
        meal_time,
        calories,
        protein,
        food_items.strip(),
        rasa,
        virya,
        digestion,
        notes.strip() if notes else ""
    )


# ==========================================================
# DELETE DIET PLAN MEAL
# ==========================================================

def delete_meal(meal_id):

    if not meal_id:
        raise ValueError(
            "Meal ID is required."
        )

    return delete_diet_plan_meal(
        meal_id
    )



# ==========================================================
# FETCH SINGLE DIET PLAN
# ==========================================================

def fetch_diet_plan(
    diet_plan_id
):

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    return get_diet_plan(
        diet_plan_id
    )



# ==========================================================
# UPDATE DIET PLAN STATUS
# ==========================================================

def update_plan_status(
    diet_plan_id,
    status
):

    if not diet_plan_id:
        raise ValueError(
            "Diet plan ID is required."
        )

    allowed_statuses = [
        "Active",
        "Paused",
        "Completed",
        "Archived"
    ]

    if status not in allowed_statuses:
        raise ValueError(
            "Invalid diet plan status."
        )

    return update_diet_plan_status(
        diet_plan_id,
        status
    )


    # ======================================================
    # CREATE PLAN
    # ======================================================

    diet_plan_id = create_new_diet_plan(
        patient_name,
        plan_name.strip()
    )

    # ======================================================
    # ADD TEMPLATE MEALS
    # ======================================================

    for meal in template["meals"]:

        add_meal_to_plan(
            diet_plan_id,
            meal["meal_type"],
            meal["meal_time"],
            meal["calories"],
            meal["protein"],
            meal["food_items"],
            meal["rasa"],
            meal["virya"],
            meal["digestion"],
            meal["notes"]
        )

    return diet_plan_id


# ==========================================================
# APPLY DIET PLAN TEMPLATE
# ==========================================================

def apply_diet_plan_template(
    diet_plan_id,
    template_name
):

    from services.diet_plan_template_service import (
        get_diet_plan_template
    )

    template = get_diet_plan_template(
        template_name
    )

    meals = template["meals"]

    added_meals = []

    for meal in meals:

        meal_id = add_diet_plan_meal(
            diet_plan_id,
            meal["meal_type"],
            meal["meal_time"],
            meal["calories"],
            meal["protein"],
            meal["food_items"],
            meal["rasa"],
            meal["virya"],
            meal["digestion"],
            meal["notes"]
        )

        added_meals.append(meal_id)

    return added_meals