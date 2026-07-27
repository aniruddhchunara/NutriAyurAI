from models.patient import Patient
from utils.menu import menu
from ml.predict import predict_bmi
from utils.validators import (
    get_age,
    get_weight,
    get_height,
    get_activity_factor,
    pause
)
from services.report import generate_report
from models.appointment import Appointment
from database.database import (
    create_table,
    create_appointment_table,
    add_patient,
    get_patients,
    search_patient,
    delete_patient,
    update_patient,
    statistics,
    add_appointment,
    get_appointments,
    search_appointment,
    update_appointment,
    delete_appointment
)

create_table()
create_appointment_table()

while True:

    menu()

    choice = input("Enter choice: ")

    if choice == "1":

        name = input("Enter name: ")

        age = get_age()
        weight = get_weight()
        height = get_height()


        activity_factor = get_activity_factor()

        patient = Patient(
            name,
            age,
            weight,
            height,
            activity_factor
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
        activity_factor = get_activity_factor()

        updated = update_patient(
            name,
            age,
            weight,
            height,
            activity_factor
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

        search_name = input("Enter Patient Name: ")

        patient = search_patient(search_name)

        if patient:

            generate_report(patient)

        else:

            print("Patient not found. ")

    elif choice == "8":

        patient_name = input("Enter Patient Name: ")
        doctor_name = input("Enter Doctor Name: ")
        appointment_date = input("Enter Appointment Date (DD-MM-YYYY): ")
        appointment_time = input("Enter Appointment Time (HH:MM AM/PM): ")
        reason = input("Enter Reason: ")

        appointment = Appointment(
            patient_name,
            doctor_name,
            appointment_date,
            appointment_time,
            reason
        )

        add_appointment(appointment)

        print("\n✅ Appointment Added Successfully!")

    elif choice =="9":

            appointments = get_appointments()

            if not appointments:
                print("\nNo appointments found.")

            else:
                for appointment in appointments:
                    appointment.display()

            pause()

    elif choice =="10":

        patient_name = input("Enter Patient Name: ")

        appointment = search_appointment(patient_name)

        if appointment:
            appointment.display()


        else:
            print("\n❌ Appointment not found.")

        pause()



    elif choice == "11":

        patient_name = input("Enter Patient Name: ")

        doctor_name = input("Enter New Doctor Name: ")

        appointment_date = input("Enter New Date (DD-MM-YYYY): ")

        appointment_time = input("Enter New Time: ")

        reason = input("Enter New Reason: ")

        updated = update_appointment(
            patient_name,
            doctor_name,
            appointment_date,
            appointment_time,
            reason
    )

        if updated:
            print("\n✅ Appointment Updated Successfully!")

        else:
            print("\n❌ Appointment Not Found!")

        pause()

    elif choice == "12":

            patient_name = input("Enter Patient Name: ")

            deleted = delete_appointment(patient_name)

            if deleted:
                print("\n✅ Appointment Deleted Successfully!")
            else:
                print("\n❌ Appointment Not Found!")

            pause()


    elif choice == "13":

        predict_bmi()

        pause()


    elif choice == "14":

        print("Thank you for using NutriAyur AI.")
        break

    else:

        print("Invalid choice.")