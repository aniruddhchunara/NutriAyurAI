from analytics.data_loader import load_data



def search_patient():

    df = load_data()

    name = input("Enter patient name: ").strip()

    result = df[
        df["name"].str.lower() == name.lower()
    ]

    if result.empty:

        print("\npatient not found.\n")

    else:

        patient = result.iloc[0]
        
        bmi = patient["weight"] / ((patient["height"] / 100) ** 2)
        print("\n" + "=" * 45)
        print("           PATIENT DETAILS")
        print("=" * 45)

        print(f"Name              : {patient['name']}")
        print(f"Age               : {patient['age']} years")
        print(f"Weight            : {patient['weight']} kg")
        print(f"Height            : {patient['height']} cm")
        print(f"BMI               : {bmi:.2f}")

        if "activity_factor" in patient.index:
            print(f"Activity Factor   : {patient['activity_factor']}")

        print("=" * 45)



def bmi_category_filter():

    df = load_data()

    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def bmi_category_filter():

    df = load_data()

    # Calculate BMI
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

    # Create BMI Category
    df["BMI Category"] = df["bmi"].apply(bmi_category)

    print("\nAvailable Categories")
    print("--------------------")
    print("Underweight")
    print("Normal")
    print("Overweight")
    print("Obese")

    category = input(
        "\nEnter BMI Category : "
    ).strip().title()

    result = df[
        df["BMI Category"] == category
    ]

    if result.empty:

        print("\nNo patients found.\n")

    else:

        print("\n" + "=" * 55)
        print(f"Patients in '{category}' Category")
        print("=" * 55)

        print(
            result[
                ["name", "age", "weight", "height", "bmi"]
            ].to_string(index=False)
        )

        print("=" * 55)



def age_range_filter():
    
    df = load_data()
    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)
    print("\n" + "=" * 40)
    print("        AGE RANGE FILTER")
    print("=" * 40)

    min_age = int(input("Enter Minimum Age : "))
    max_age = int(input("Enter Maximum Age : "))
    
    result = df[
    (df["age"] >= min_age) &
    (df["age"] <= max_age)
            ]
    
    if result.empty:

       print("\nNo patients found.\n")

    else:

        print("\n" + "=" * 60)
        print(f"Patients Between {min_age} and {max_age} Years")
        print("=" * 60)

        print(
        result[
            ["name", "age", "weight", "height", "bmi"]
        ].to_string(index=False)
        )

        print("=" * 60)

if __name__ == "__main__":
    search_patient()
    bmi_category_filter()
    age_range_filter()