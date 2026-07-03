class Patient:

    def __init__(self , name ,age, weight, height):

     self.name = name
     self.age = age
     self.weight = weight
     self.height = height

    def calculate_bmi(self):

        bmi = self.weight /(self.height ** 2)

        return bmi

    def health_status(self):

        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "underweight"

        elif bmi < 25:
            return "normal weight"

        elif bmi  < 30:
            return "overweight"

        else:
            return "obese"



    def save_to_file(self):

        with open("patients.txt", "a") as  file:

            file.write(
                f"{self.name},{self.age},{self.weight},{self.height}\n"
            )

    def display(self):

     print("\n===== patient details=====")
     print("patient Name:", self.name)
     print("Age:", self.age)
     print("weight:",self.weight)
     print("Height:",self.height)


     bmi = self.calculate_bmi()

     print("BMI:", round(bmi, 2))
     print("Health Status:", self.health_status())






