import sqlite3

def connect():

    conn = sqlite3.connect("patients.db")

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
            height REAL

        )
    """)

    conn.commit()

    conn.close()

def add_patient(patient):

    conn, cursor = connect()

    cursor.execute("""
        INSERT INTO patients (
        name,age ,weight, height)

        VALUES (?, ?, ?,?)
        """, (
            patient.name,
            patient.age,
            patient.weight,
            patient.height
        ))

    conn.commit()
    conn.close()

def get_patients():

    conn, cursor = connect()

    cursor.execute(
        "SELECT * FROM patients"
    )

    data = cursor.fetchall()

    conn.close()

    return data


def search_patient(name):

    conn, cursor = connect()

    cursor.execute(
        """
        SELECT * FROM patients
        WHERE name LIKE ?
        """, (f"%{name}%",)
    )

    patients = cursor.fetchall()

    conn.close()

    return patient

def delete_patient(name):

    conn, cursor = connect()

    cursor.execute(
        """,
        DELETE FROM patients
        WHERE LOWER(name) =LOWER(?)
        """,
        (name,)
    )

    conn.commit()

    deleted = cursor.rowcut

    conn.close()


def update_patient(name, age, weight, height):

    conn, cursor = connect()

    cursor.execute(
        """
        UPDATE patients

        SET age = ?,
            weight =?,
            height =?

    WHERE LOWER(name) = LOWER(?)
    """,
    (
            age,
            weight,
            height,
            name,
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
        "SELECT AVG(weight/(height*height)) FROM patients"
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