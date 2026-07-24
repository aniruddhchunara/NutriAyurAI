class Patient:

    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    def calculate_bmi(self):
        bmi = self.weight / (self.height ** 2)
        return bmi

    def health_status(self):
        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "Underweight"

        elif bmi < 25:
            return "Normal Weight"

        elif bmi < 30:
            return "Overweight"

        else:
            return "Obese"

    def calculate_water_intake(self):
        water_ml = self.weight * 35
        water_litre = water_ml / 1000
        return round(water_litre, 2)

    def get_recommendation(self):

        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return [
                "Increase calorie intake",
                "Eat protein-rich foods",
                "Drink milk regularly",
                "Strength training 3 times/week"
            ]

        elif bmi < 25:
            return [
                "Maintain balanced diet",
                "Exercise regularly",
                "Drink at least 2-3 litres of water",
                "Sleep 7-8 hours daily"
            ]

        elif bmi < 30:
            return [
                "Reduce sugar intake",
                "Walk 30 minutes daily",
                "Increase vegetables in meals",
                "Avoid junk food"
            ]

        else:
            return [
                "Consult a nutritionist",
                "Exercise daily",
                "Reduce processed foods",
                "Monitor BMI regularly"
            ]

    def save_to_file(self):

        with open("patients.txt", "a") as file:
            file.write(
                f"{self.name},{self.age},{self.weight},{self.height}\n"
            )

    def display(self):

        print("\n========== Patient Details ==========")
        print("Name              :", self.name)
        print("Age               :", self.age)
        print("Weight            :", self.weight, "kg")
        print("Height            :", self.height, "m")
        print("BMI               :", round(self.calculate_bmi(), 2))
        print("Health Status     :", self.health_status())
        print("Water Intake      :", self.calculate_water_intake(), "Litres")

        print("\nRecommendations:")

        for item in self.get_recommendation():
            print("•", item)

        print("=====================================")