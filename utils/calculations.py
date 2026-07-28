def calculate_bmi(weight, height):
    """
    Calculate Body Mass Index.
    """

    return weight / ((height / 100) ** 2)


def average(values):
    """
    Return average value.
    """

    if len(values) == 0:
        return 0

    return sum(values) / len(values)