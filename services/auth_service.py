import hashlib
import hmac
import secrets

from database.database import (
    connect,
    link_user_to_patient
)

# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password):

    if not password:
        raise ValueError("Password is required.")

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(password, stored_hash):

    if not password or not stored_hash:
        return False

    try:
        salt_hex, hash_hex = stored_hash.split(":")

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        )

        return hmac.compare_digest(
            password_hash,
            expected_hash
        )

    except (ValueError, TypeError):
        return False


# ==========================================
# CREATE USER
# ==========================================

def create_user(
    name,
    email,
    password,
    role="patient",
    patient_id=None
):

    name = name.strip()
    email = email.strip().lower()

    if not name:
        raise ValueError("Name is required.")

    if not email:
        raise ValueError("Email is required.")

    if not password:
        raise ValueError("Password is required.")

    if role not in ("patient", "admin"):
        raise ValueError("Invalid user role.")

    password_hash = hash_password(password)

    conn, cursor = connect()

    try:

        cursor.execute(
            """
            INSERT INTO users (
                name,
                email,
                password_hash,
                role,
                patient_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                password_hash,
                role,
                patient_id
            )
        )

        conn.commit()

        return cursor.lastrowid

    except Exception as error:

        conn.rollback()

        if "UNIQUE constraint failed" in str(error):
            raise ValueError(
                "An account with this email already exists."
            )

        raise

    finally:
        conn.close()


# ==========================================
# LOGIN
# ==========================================

def authenticate_user(email, password, role=None):

    email = email.strip().lower()

    if not email or not password:
        return None

    conn, cursor = connect()

    try:

        if role:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    email,
                    password_hash,
                    role,
                    patient_id
                FROM users
                WHERE LOWER(email) = ?
                AND role = ?
                """,
                (
                    email,
                    role
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    email,
                    password_hash,
                    role,
                    patient_id
                FROM users
                WHERE LOWER(email) = ?
                """,
                (email,)
            )

        user = cursor.fetchone()

        if not user:
            return None

        if not verify_password(
            password,
            user[3]
        ):
            return None

        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[4],
            "patient_id": user[5]
        }

    finally:
        conn.close()