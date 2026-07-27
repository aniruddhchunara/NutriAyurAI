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
    df["BMI category"] = df["bmi"].apply(bmi_category)

    print("\nAvailable Categories")
    print("--------------------")
    print("Underweight")
    print("Normal")
    print("Overweight")
    print("Obese")

    category = input(
        "\nEnter BMI category : "
    ).strip().title()

    result = df[
        df["BMI category"] == category
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
    
    while True:
        try:

            min_age = int(input("Enter Minimum Age : "))
            max_age = int(input("Enter Maximum Age : "))

            if min_age > max_age:
                print("Minimum age cannot be greater than maximum age.\n")
                continue
            break

        except ValueError:
            print("Please enter valid integer values.\n")

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

def top_5_highest_bmi():

    df = load_data()

    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

    top_patients = df.sort_values(
        by = "bmi",
        ascending=False
    )

    top_patients = top_patients.head(5)

    print("\n" + "=" * 60)
    print("      TOP 5 HIGHEST BMI PATIENTS")
    print("=" * 60)

    print(
        top_patients[
            ["name", "age", "weight", "height", "bmi"]
        ].to_string(index=False)
    )
print("=" * 60)


def top_5_lowest_bmi():

    df = load_data()

    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)

    lowest_patients = df.sort_values(
        by="bmi",
        ascending=True
    )
    lowest_patients = lowest_patients.head(5)

    print("\n" + "=" * 60)
    print("        TOP 5 LOWEST BMI PATIENTS")
    print("=" * 60)

    print(
         lowest_patients[
                ["name", "age", "weight", "height", "bmi"]
        ].to_string(index=False)
    )

print("=" * 60)


def health_summary():
    df = load_data()

    df["bmi"] = df["weight"] / ((df["height"] / 100) ** 2)
    df["BMI category"] = df["bmi"].apply(bmi_category)


    total_patients = len(df)

    average_age = df["age"].mean()
    average_weight = df["weight"].mean()
    average_height = df["height"].mean()
    average_bmi = df["bmi"].mean()
    highest_bmi = df["bmi"].max()
    lowest_bmi = df["bmi"].max()
    bmi_counts = df["BMI category"].value_counts()

    print("\n" + "=" * 60)
    print("             HEALTH SUMMARY REPORT")
    print("=" * 60)

    print(f"Total Patients      : {total_patients}")

    print(f"Average Age         : {average_age:.2f} Years")

    print(f"Average Weight      : {average_weight:.2f} Kg")

    print(f"Average Height      : {average_height:.2f} cm")

    print(f"Average BMI         : {average_bmi:.2f}")

    print(f"Highest BMI         : {highest_bmi:.2f}")

    print(f"Lowest BMI          : {lowest_bmi:.2f}")

    print("\nBMI category Counts")
    print("-" * 25)

    for category, count in bmi_counts.items():

        print(f"{category:<20}: {count}")

    print("=" * 60)


def analytics_menu():

    while True:

        print("\n" + "=" *45)
        print("      PATIENT ANALYTICS MENU")
        print("=" * 45)

        print("1.Search Patient")
        print("2.BMI Category Filter")
        print("3.Age Range Filter")
        print("4.Top 5 Highest BMI")
        print("5.Top 5 Lowest BMI")
        print("6.Healthy Summary Report")
        print("7.Exit")

        choice = input("\Enter your Choice : ")


        if choice == "1":
            search_patient()
        elif choice == "2":
            bmi_category_filter()
        elif choice =="3":
            age_range_filter()
        elif choice == "4":
            top_5_highest_bmi()
        elif choice =="5":
            top_5_lowest_bmi()
        elif choice =="6":
            health_summary()
        elif choice == "7":
            print("\nThank you for using NutriAyurAI!")

            break
        else:
            print("\nInvalid choice! Please try again.")




if __name__ == "__main__":
    analytics_menu()
    search_patient()
    bmi_category_filter()
    age_range_filter()
    top_5_highest_bmi()
    top_5_lowest_bmi()
    health_summary()
