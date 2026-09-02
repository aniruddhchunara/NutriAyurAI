class Patient:

    def __init__(self, name, age, weight, height, activity_factor=1.55 , patient_id=None):
        self.id = patient_id
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.activity_factor = activity_factor

    def calculate_bmi(self):
        height_m = self.height / 100
        bmi = self.weight / (height_m ** 2)
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

    def calculate_bmr(self):
        height_cm = self.height

        bmr = (
            (10 * self.weight)
            + (6.25 * height_cm)
            - (5* self.age)
            + 5
        )

        return round(bmr, 2)

    def maintenance_calories(self):

        calories = self.calculate_bmr() * self.activity_factor

        return round(calories, 2)

    def weight_loss_calories(self):

        calories = self.maintenance_calories() - 500

        return round(calories, 2)

    def weight_gain_calories(self):

        calories = self.maintenance_calories() + 300

        return round(calories, 2)

    def risk_level(self):

        bmi = self.calculate_bmi()

        if bmi >= 30:
            return "High Risk"

        elif self.age >= 60:
            return "High Risk"

        elif bmi >= 25:
            return "Moderate Risk"

        elif bmi < 18.5:
            return "Moderate Risk"

        else:
            return "Low Risk"

    def risk_reason(self):

        reasons = []

        bmi = self.calculate_bmi()

        if bmi >= 30:
            reasons.append("BMI indicates obesity.")

        elif bmi >= 25:
            reasons.append("BMI indicates overweight.")

        elif bmi < 18.5:
            reasons.append("BMI is underweight.")

        else:
            reasons.append("BMI is within the healthy range")

        if self.age >= 60:
            reasons.append("Age is above 60 years. ")

        return reasons

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
        print("Height            :", self.height, "cm")
        print("Activity Factor   :", self.activity_factor)
        print("BMI               :", round(self.calculate_bmi(), 2))
        print("Health Status     :", self.health_status())
        print("Water Intake      :", self.calculate_water_intake(), "Litres")
        print("BMR               :", self.calculate_bmr(),"kcal/day")
        print("Maintenance Calories :", self.maintenance_calories(), "kcal/day")
        print("Weight loss Calories :", self.weight_loss_calories(), "kcal/day")
        print("Weight gain Calories :", self.weight_gain_calories(), "kcal/day")

        print("\n===== Health Risk Assesement =====")

        if self.risk_level() == "Low Risk":
            print("🟢 Risk Level :", self.risk_level())

        elif self.risk_level() == "Moderate Risk":
            print("🟡 Risk Level :", self.risk_level())

        else:
            print("🔴 Risk Level :", self.risk_level())

        print("Risk Level :", self.risk_level())

        print("\nReason(s):")

        print("\nRecommendations:")

        for item in self.get_recommendation():
            print("•", item)

        print("=" * 40)