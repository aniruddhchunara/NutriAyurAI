import os
import sqlite3


DATABASE = "database/nutriayurai.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    print(
        "Using database:",
        os.path.abspath(DATABASE)
    )

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# ==========================================================
# CREATE SETTINGS TABLE
# ==========================================================

def create_settings_table():
    """
    Create the settings table if it doesn't exist.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (

            id INTEGER PRIMARY KEY,

            clinic_name TEXT,

            dietitian_name TEXT,

            phone TEXT,

            email TEXT,

            address TEXT,

            report_title TEXT,

            report_footer TEXT,

            theme TEXT
        )
        """
    )

    conn.commit()
    conn.close()


# ==========================================================
# SAVE SETTINGS
# ==========================================================

def save_settings(
    clinic_name,
    dietitian_name,
    phone,
    email,
    address,
    report_title,
    report_footer,
    theme
):
    """
    Save application settings.

    The application maintains one settings record
    using id = 1.
    """

    # ======================================================
    # VALIDATION
    # ======================================================

    clinic_name = (
        clinic_name.strip()
        if clinic_name
        else ""
    )

    dietitian_name = (
        dietitian_name.strip()
        if dietitian_name
        else ""
    )

    phone = (
        phone.strip()
        if phone
        else ""
    )

    email = (
        email.strip()
        if email
        else ""
    )

    address = (
        address.strip()
        if address
        else ""
    )

    report_title = (
        report_title.strip()
        if report_title
        else ""
    )

    report_footer = (
        report_footer.strip()
        if report_footer
        else ""
    )

    theme = (
        theme.strip()
        if theme
        else "Light"
    )

    allowed_themes = [
        "Light",
        "Dark"
    ]

    if theme not in allowed_themes:

        raise ValueError(
            "Invalid theme. Choose Light or Dark."
        )

    # ======================================================
    # DATABASE
    # ======================================================

    create_settings_table()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO settings (
            id,
            clinic_name,
            dietitian_name,
            phone,
            email,
            address,
            report_title,
            report_footer,
            theme
        )
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(id)
        DO UPDATE SET
            clinic_name = excluded.clinic_name,
            dietitian_name = excluded.dietitian_name,
            phone = excluded.phone,
            email = excluded.email,
            address = excluded.address,
            report_title = excluded.report_title,
            report_footer = excluded.report_footer,
            theme = excluded.theme
        """,
        (
            clinic_name,
            dietitian_name,
            phone,
            email,
            address,
            report_title,
            report_footer,
            theme
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# LOAD SETTINGS
# ==========================================================

def load_settings():
    """
    Load application settings.
    """

    create_settings_table()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            clinic_name,
            dietitian_name,
            phone,
            email,
            address,
            report_title,
            report_footer,
            theme
        FROM settings
        WHERE id = 1
        LIMIT 1
        """
    )

    settings = cursor.fetchone()

    conn.close()

    return settings


# ==========================================================
# GET SETTINGS AS DICTIONARY
# ==========================================================

def get_settings():
    """
    Return application settings as a dictionary.
    """

    settings = load_settings()

    if not settings:

        return {
            "clinic_name": "NutriAyurAI",
            "dietitian_name": "Dietitian",
            "phone": "",
            "email": "",
            "address": "",
            "report_title": "AI Health Report",
            "report_footer": "Generated by NutriAyurAI",
            "theme": "Light"
        }

    return {
        "clinic_name": settings[0],
        "dietitian_name": settings[1],
        "phone": settings[2],
        "email": settings[3],
        "address": settings[4],
        "report_title": settings[5],
        "report_footer": settings[6],
        "theme": settings[7]
    }


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    create_settings_table()

    print(
        "Settings table created successfully!"
    )

    print(
        "Database Path:",
        os.path.abspath(DATABASE)
    )