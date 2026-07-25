import os

def create_reports_folder():

    folder = "reports/graphs"

    os.makedirs(folder, exist_ok=True)

    return folder


