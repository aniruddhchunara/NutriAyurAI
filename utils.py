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

