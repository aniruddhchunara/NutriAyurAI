from patient import Patient
from menu import menu
from utils import get_age
from utils import get_weight
from utils import get_height
from utils import pause
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

            patients = get_patients()

            for patient in patients:

                patient.display()

    elif choice == "3":

        search_name = input("Enter patient name: ")

        patient = search_patient(search_name)

        if patient:

            print("\nPatient Found")

            print("Name:",patient.name)
            print("Age:",patient.age)
            print("Weight:",patient.weight)
            print("Height:",patient.height)
            print("BMI:", round(patient.calculate_bmi(),2))
            

        else:

            print("Patient not found ")

        pause()


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


    elif choice == "7":

        print("Thank you for using NutriAyur AI.")
        break

    else:

        print("Invalid choice.")