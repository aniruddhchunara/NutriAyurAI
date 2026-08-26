import pandas as pd

from database.database import connect


def load_data():

    conn, _ = connect()

    df = pd.read_sql_query(
        "SELECT * FROM patients",
        conn
    )

    conn.close()

    return df