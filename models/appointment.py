from datetime import datetime



class Appointment:

    def __init__(
        self,
        patient_name,
        doctor_name,
        appointment_date,
        appointment_time,
        reason
    ):

     self.patient_name = patient_name
     self.doctor_name = doctor_name
     self.appointment_date = appointment_date
     self.appointment_time = appointment_time
     self.reason = reason


    def display(self):


        print("\n========== Appointment ==========")

        print(f"Patient : {self.patient_name}")

        print(f"Doctor  : {self.doctor_name}")

        print(f"Date    : {self.appointment_date}")

        print(f"Time    : {self.appointment_time}")

        print(f"Reason  : {self.reason}")

        print("=" * 35)

