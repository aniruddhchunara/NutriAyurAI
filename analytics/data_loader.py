import sqlite3
import pandas as pd

def load_data():

    conn = sqlite3.connect("patients.db")

    df = pd.read_sql_query(
        "SELECT * FROM patients",
        conn
    )

    conn.close()

    return df
    