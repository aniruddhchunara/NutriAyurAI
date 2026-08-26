import os
import sqlite3
from models.patient import Patient

def connect():

    conn = sqlite3.connect("database/nutriayurai.db")

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    cursor = conn.cursor()

    return conn,cursor



def create_table():

    conn, cursor = connect()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            weight REAL,
            height REAL,
            activity_factor REAL DEFAULT 1.55

        )
    """)

    conn.commit()

    conn.close()

def add_patient(patient):

    conn, cursor = connect()

    cursor.execute("""
        INSERT INTO patients (
        name,age ,weight, height, activity_factor)

        VALUES (?, ?, ?,?,?)
        """, (
            patient.name,
            patient.age,
            patient.weight,
            patient.height,
            patient.activity_factor
        ))

    conn.commit()
    conn.close()



def get_patients():

    conn, cursor = connect()

    cursor.execute("SELECT * FROM patients")

    rows = cursor.fetchall()

    conn.close()

    patients = []

    for row in rows:

        patient = Patient(
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        )

        patients.append(patient)

    return patients


def search_patient(name):

    conn, cursor = connect()

    cursor.execute(

        """
        SELECT * FROM patients
        WHERE LOWER(name)=LOWER(?)
        """,

        (name,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return Patient(

            row[1],
            row[2],
            row[3],
            row[4],
            row[5]

        )

    return None

def delete_patient(name):

    conn, cursor = connect()

    cursor.execute(
        """
        DELETE FROM patients
        WHERE LOWER(name) =LOWER(?)
        """ ,
        (name,))


    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted


def update_patient(name, age, weight, height, activity_factor):

    conn, cursor = connect()

    cursor.execute(
        """
        UPDATE patients

        SET
            age = ?,
            weight =?,
            height =?,
            activity_factor =?

    WHERE LOWER(name) = LOWER(?)
    """,
    (
            age,
            weight,
            height,
            activity_factor,
            name
    )
)

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated



def statistics():

    conn, cursor = connect()

    cursor.execute(
        "SELECT COUNT(*) FROM patients"
    )
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT AVG(weight / ((height / 100.0) * (height / 100.0))) FROM patients"
    )

    avg_bmi = cursor.fetchone()[0]

    conn.close()

    return total, avg_bmi


def senior_citizen():

    conn, cursor = connect()

    cursor.execute(
        "SELECT COUNT(*)FROM patients WHERE age > 60"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

def create_appointment_table():

    conn, cursor = connect()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient_name TEXT NOT NULL,

        doctor_name TEXT NOT NULL,

        appointment_date TEXT NOT NULL,

        appointment_time TEXT NOT NULL,

        reason TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()


def add_appointment(appointment):

    conn, cursor = connect()

    cursor.execute(
        """

        INSERT INTO appointments
        (
            patient_name,
            doctor_name,
            appointment_date,
            appointment_time,
            reason
    )
    VALUES (?,?,?,?,?)
    """,
    (
        appointment.patient_name,
        appointment.doctor_name,
        appointment.appointment_date,
        appointment.appointment_time,
        appointment.reason
    )
)

    conn.commit()
    conn.close()


from models.appointment import Appointment

def get_appointments():

    conn, cursor = connect()

    cursor.execute("SELECT * FROM appointments")

    rows = cursor.fetchall()

    conn.close()

    appointments = []

    for row in rows:

        appointment = Appointment(
            row[1],  #patient_name
            row[2],  #doctor_name
            row[3],  #appointment_date
            row[4],  #appointment_time
            row[5]   #reason
        )


        appointments.append(appointment)

    return appointments


def search_appointment(patient_name):

        conn, cursor = connect()

        cursor.execute(
            """
            SELECT * FROM appointments
            WHERE LOWER(patient_name) = LOWER(?)
            """,
            (patient_name,)
        )

        row = cursor.fetchone()

        conn.close()

        if row:
            return Appointment(
                row[1],  #patient_name
                row[2],  #doctor_name
                row[3],  #appointment_date
                row[4],  #appointment_time
                row[5]   #reasson
            )

        return None


def update_appointment(
    patient_name,
    doctor_name,
    appointment_date,
    appointment_time,
    reason
):

    conn, cursor = connect()

    cursor.execute(
        """
        UPDATE appointments
        SET
            doctor_name = ?,
            appointment_date = ?,
            appointment_time = ?,
            reason = ?
        WHERE LOWER(patient_name) = LOWER(?)
        """,
        (
            doctor_name,
            appointment_date,
            appointment_time,
            reason,
            patient_name
        )
    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated

def delete_appointment(patient_name):

    conn, cursor = connect()

    cursor.execute(
        """
        DELETE FROM appointments
        WHERE LOWER(patient_name) = LOWER(?)
        """,
        (patient_name,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted



# ==========================================================
# DIET PLAN TABLES
# ==========================================================

def create_diet_plan_tables():

    conn, cursor = connect()

    # ======================================================
    # DIET PLANS TABLE
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diet_plans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_name TEXT NOT NULL,

            plan_name TEXT NOT NULL,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # ======================================================
    # DIET PLAN MEALS TABLE
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diet_plan_meals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            diet_plan_id INTEGER NOT NULL,

            meal_type TEXT NOT NULL,

            meal_time TEXT NOT NULL,

            calories REAL DEFAULT 0,

            protein REAL DEFAULT 0,

            food_items TEXT,

            rasa TEXT,

            virya TEXT,

            digestion TEXT,

            notes TEXT,

            FOREIGN KEY (diet_plan_id)
            REFERENCES diet_plans(id)

        )
    """)

    # ======================================================
    # CHECK EXISTING COLUMNS
    # ======================================================

    cursor.execute(
        "PRAGMA table_info(diet_plan_meals)"
    )

    existing_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    # ======================================================
    # ADD STATUS COLUMN
    # ======================================================

    if "status" not in existing_plan_columns:

        cursor.execute("""
            ALTER TABLE diet_plans
            ADD COLUMN status TEXT DEFAULT 'Active'
        """)

    # ======================================================
    # ADD UPDATED DATE COLUMN
    # ======================================================

    if "updated_at" not in existing_plan_columns:

        cursor.execute("""
            ALTER TABLE diet_plans
            ADD COLUMN updated_at TEXT
        """)




    # ======================================================
    # ADD NEW COLUMNS SAFELY
    # ======================================================

    if "protein" not in existing_columns:

        cursor.execute("""
            ALTER TABLE diet_plan_meals
            ADD COLUMN protein REAL DEFAULT 0
        """)

    if "rasa" not in existing_columns:

        cursor.execute("""
            ALTER TABLE diet_plan_meals
            ADD COLUMN rasa TEXT
        """)

    if "virya" not in existing_columns:

        cursor.execute("""
            ALTER TABLE diet_plan_meals
            ADD COLUMN virya TEXT
        """)

    if "digestion" not in existing_columns:

        cursor.execute("""
            ALTER TABLE diet_plan_meals
            ADD COLUMN digestion TEXT
        """)

    # ======================================================
    # SAVE CHANGES
    # ======================================================

    conn.commit()

    conn.close()


if __name__ == "__main__":

    create_diet_plan_tables()

    print("Diet plan tables created successfully!")