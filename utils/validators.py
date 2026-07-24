def get_age():

    while True:

        try:
            age = int(input("Enter age: "))
            return age
        except ValueError:
           print("please enter number only.")


def get_weight():

    while True:
        try:
            weight = float(input("Enter Weight: "))
            return weight
        except ValueError:
            print("please enter a valid weight.")


def get_height():

    while True:
        try:
            height = float(input("Enter height: "))

            if height > 10:
                height = height/100

            return height

        except ValueError:

            print("please eenter a valid height. ")


def pause():

    input ("\npress Enter to return to the Main Menu....")

def get_activity_factor():

        print("===== Activity Level =====")
        print("1. sedentary")
        print("2. Lightly Active")
        print("3. Moderately Active")
        print("4. Very Active")
        print("5. Athlete")

        while True:

            choice = input("Choose activitynlevel (1-5): ")

            activity_levels ={
                "1": 1.20,
                "2": 1.375,
                "3": 1.55,
                "4": 1.725,
                "5": 1.90,
            }
            if choice in activity_levels:
                return activity_levels[choice]

            print("Invalid choice.please enter 1-5.")




