from analytics.data_loader import load_data



def dashboard_kpis():

    df = load_data()
    
    print(df[["name", "weight", "height"]])

#   Calculate BMI
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

    print("\n===== Dashboard KPIs=====")

    print("Total Patients :", len(df))
    print("Average BMI :", round(df["bmi"].mean(),2))
    print("Average Age :", round(df["age"].mean(),2))
    print("Average Weight :", round(df["weight"].mean(),2))
    print("Average Height :", round(df["height"].mean(),2))
    
