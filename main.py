from patient import Patient
from menu import menu
from utils import get_age
from utils import get_weight
from utils import get_height
from database import delete_patient

from database import (
    create_table,
    add_patient,
    get_patients,
    search_patient,
    delete_patient,
    update_patient,
    statistics
)

create_table()

while True:

    menu()

    choice = input("Enter choice: ")

    if choice == "1":

        name = input("Enter name: ")

        age = get_age()
        weight = get_weight()
        height = get_height()

        patient = Patient(
            name,
            age,
            weight,
            height
        )

        add_patient(patient)

        print("\nPatient Added Successfully!")

    elif choice == "2":

        data = get_patients()

        if len(data) == 0:

            print("No patients found.")

        else:

            for patient in data:

                print("\nID:", patient[0])
                print("Name:", patient[1])
                print("Age:", patient[2])
                print("Weight:", patient[3])
                print("Height:", patient[4])

    elif choice == "3":

        search_name = input("Enter patient name: ")

        patient = search_patients(search_name)

        if patient:

            print("\nPatient Found")

            print("ID:", patient[0])
            print("Name:",patient[1])
            print("Age:",patient[2])
            print("Weight:",patient[3])
            print("Height:",patient[4])

            bmi = patient[3] / (patient[4] **2)

            print("BMI:", round(bmi,2))

        else:

            print("Patient not found ")

        print("Search module coming next.")

    elif choice == "4":

        name = input("Enter patient name: ")
        deleted = delete_patient(name)

        if deleted:
            print("Patient deleted successfully.")

        else:
            print("Patient not Found.")

        print("Delete module coming next.")

    elif choice == "5":

        name = input("Enter patient name: ")

        age = get_age()
        weight = get_weight()
        height = get_height()

        updated = update_patient(
            name,
            age,
            weight,
            height
        )

        if updated:

            print("patient updated successfully.")

        else:

            print("patient not found.")

        print("Update module coming next.")

    elif choice == "6":

        total, avg_bmi = statistics()

        print("===== Statistics=====")

        print("total Patients:",total)

        if avg_bmi:
            print("Average BMI:", round(avg_bmi, 2))
        else:
            print("Average BMI:, No data")

        print("Thank you for using NutriAyur AI.")
        break

    else:

        print("Invalid choice.")