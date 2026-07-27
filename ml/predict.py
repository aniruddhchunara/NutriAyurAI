import pickle


def predict_bmi():
    with open("models/bmi_model.pkl" ,"rb") as file:
        model = pickle.load(file)
    
    age = int(input("Enter Age : "))
    
    weight = float(input("Enter Weight (kg) : "))
    
    height = float(input("Enter Height (cm) : "))
    
    new_patient =[[
        age,
        weight,
        height
    ]]

    predicted_bmi = model.predict(new_patient)
    predicted_bmi = predicted_bmi[0]

    category, tips = bmi_recommendation(predicted_bmi)

    print("\n========== BMI PREDICTION ==========\n")

    print(f"Predicted BMI : {predicted_bmi:.2f}")

    print(f"Category      : {category}")

    print("\nRecommendation:")

    for tip in tips:

        print(f"• {tip}")
    
    
    
def bmi_recommendation(bmi):
    
    if bmi < 18.5:
        
        return(
            "Underweight",
            [
                "Increase healthy calorie intake.",
                "Include protein-rich foods.",
                "Consult a dietitian if necessary."
            ]
        )
        
    elif bmi < 25:
        return (
            "Normal",
            [
                "Maintain your current lifestyle.",
                "Exercise regularly.",
                "Continue eating a balanced diet."
            ]
        )
        
    elif bmi < 30:

        return (
            "Overweight",
            [
                "Increase physical activity.",
                "Reduce sugary foods.",
                "Eat more vegetables and fruits."
            ]
        )
        
    else:

         return (
            "Obese",
            [
                "Consult a healthcare professional.",
                "Follow a structured diet plan.",
                "Exercise under professional guidance."
            ]
        )

if __name__ == "__main__":
    predict_bmi()