from database.database import connect


# ==========================================================
# CREATE DIET PLAN
# ==========================================================

def create_diet_plan(
    patient_name,
    plan_name,
    start_date=None,
    end_date=None,
    duration_days=None
):

    conn, cursor = connect()

    cursor.execute(
        """
        INSERT INTO diet_plans (
            patient_name,
            plan_name,
            start_date,
            end_date,
            duration_days
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            patient_name,
            plan_name,
            start_date,
            end_date,
            duration_days
        )
    )

    diet_plan_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return diet_plan_id


# ==========================================================
# ADD DIET PLAN MEAL
# ==========================================================

def add_diet_plan_meal(
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

    conn, cursor = connect()

    cursor.execute(
        """
        INSERT INTO diet_plan_meals (
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
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
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
        )
    )

    meal_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return meal_id

# ==========================================================
# GET DIET PLANS
# ==========================================================

def get_diet_plans(
    patient_name=None
):

    conn, cursor = connect()

    if patient_name:

        cursor.execute(
            """
            SELECT
                id,
                patient_name,
                plan_name,
                created_at,
                status,
                updated_at,
                start_date,
                end_date,
                duration_days
            FROM diet_plans
            WHERE LOWER(patient_name) = LOWER(?)
            ORDER BY id DESC
            """,
            (patient_name,)
        )

    else:

        cursor.execute(
            """
            SELECT
                id,
                patient_name,
                plan_name,
                created_at,
                status,
                updated_at,
                start_date,
                end_date,
                duration_days
            FROM diet_plans
            ORDER BY id DESC
            """
        )

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==========================================================
# GET DIET PLAN MEALS
# ==========================================================

def get_diet_plan_meals(diet_plan_id):

    conn, cursor = connect()

    cursor.execute(
        """
        SELECT
            id,
            meal_type,
            meal_time,
            calories,
            protein,
            food_items,
            rasa,
            virya,
            digestion,
            notes
        FROM diet_plan_meals
        WHERE diet_plan_id = ?
        ORDER BY id
        """,
        (diet_plan_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==========================================================
# UPDATE DIET PLAN MEAL
# ==========================================================

def update_diet_plan_meal(
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

    conn, cursor = connect()

    cursor.execute(
        """
        UPDATE diet_plan_meals

        SET
            meal_type = ?,
            meal_time = ?,
            calories = ?,
            protein = ?,
            food_items = ?,
            rasa = ?,
            virya = ?,
            digestion = ?,
            notes = ?

        WHERE id = ?
        """,
        (
            meal_type,
            meal_time,
            calories,
            protein,
            food_items,
            rasa,
            virya,
            digestion,
            notes,
            meal_id
        )
    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated


# ==========================================================
# DELETE DIET PLAN MEAL
# ==========================================================

def delete_diet_plan_meal(meal_id):

    conn, cursor = connect()

    cursor.execute(
        """
        DELETE FROM diet_plan_meals
        WHERE id = ?
        """,
        (meal_id,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted


# ==========================================================
# DELETE DIET PLAN
# ==========================================================

def delete_diet_plan(diet_plan_id):

    conn, cursor = connect()

    try:

        # ==================================================
        # STEP 1: DELETE ALL MEALS
        # ==================================================

        cursor.execute(
            """
            DELETE FROM diet_plan_meals
            WHERE diet_plan_id = ?
            """,
            (diet_plan_id,)
        )

        deleted_meals = cursor.rowcount

        # ==================================================
        # STEP 2: DELETE DIET PLAN
        # ==================================================

        cursor.execute(
            """
            DELETE FROM diet_plans
            WHERE id = ?
            """,
            (diet_plan_id,)
        )

        deleted_plan = cursor.rowcount

        # ==================================================
        # SAVE CHANGES
        # ==================================================

        conn.commit()

        return {
            "deleted_plan": deleted_plan,
            "deleted_meals": deleted_meals
        }

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()


# ==========================================================
# UPDATE DIET PLAN STATUS
# ==========================================================

def update_diet_plan_status(
    diet_plan_id,
    status
):

    conn, cursor = connect()

    cursor.execute(
        """
        UPDATE diet_plans

        SET
            status = ?,
            updated_at = CURRENT_TIMESTAMP

        WHERE id = ?
        """,
        (
            status,
            diet_plan_id
        )
    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated


# ==========================================================
# GET SINGLE DIET PLAN
# ==========================================================

def get_diet_plan(
    diet_plan_id
):

    conn, cursor = connect()

    cursor.execute(
        """
        SELECT
            id,
            patient_name,
            plan_name,
            created_at,
            status,
            updated_at,
            start_date,
            end_date,
            duration_days
        FROM diet_plans
        WHERE id = ?
        """,
        (diet_plan_id,)
    )

    plan = cursor.fetchone()

    conn.close()

    return plan


# ==========================================================
# FIND DUPLICATE DIET PLAN
# ==========================================================

def find_duplicate_diet_plan(
    patient_name,
    plan_name,
    start_date,
    end_date
):

    conn, cursor = connect()

    cursor.execute(
        """
        SELECT
            id,
            patient_name,
            plan_name,
            start_date,
            end_date,
            duration_days,
            status
        FROM diet_plans
        WHERE LOWER(patient_name) = LOWER(?)
        AND LOWER(plan_name) = LOWER(?)
        AND start_date = ?
        AND end_date = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            patient_name,
            plan_name,
            start_date,
            end_date
        )
    )

    duplicate = cursor.fetchone()

    conn.close()

    return duplicate