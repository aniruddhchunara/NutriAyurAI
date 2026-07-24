with open("patients.txt" ,"r") as file:

    data = file.readlines()

    for patient in data:
        print(patient)
