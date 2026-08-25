import sqlite3

# Old database
old_conn = sqlite3.connect("patients.db")
old_cursor = old_conn.cursor()

# New database
new_conn = sqlite3.connect("database/nutriayurai.db")
new_cursor = new_conn.cursor()

# -------------------------
# Create Patients Table
# -------------------------

new_cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    weight REAL,
    height REAL,
    activity_factor REAL DEFAULT 1.55
)
""")

# -------------------------
# Create Appointments Table
# -------------------------

new_cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    doctor_name TEXT,
    appointment_date TEXT,
    appointment_time TEXT,
    reason TEXT
)
""")

# -------------------------
# Copy Patients
# -------------------------

patients = old_cursor.execute(
    "SELECT * FROM patients"
).fetchall()

new_cursor.executemany(
    """
    INSERT INTO patients
    VALUES (?,?,?,?,?,?)
    """,
    patients
)

# -------------------------
# Copy Appointments
# -------------------------

appointments = old_cursor.execute(
    "SELECT * FROM appointments"
).fetchall()

new_cursor.executemany(
    """
    INSERT INTO appointments
    VALUES (?,?,?,?,?,?)
    """,
    appointments
)

new_conn.commit()

old_conn.close()
new_conn.close()

print("✅ Database migration completed successfully!")