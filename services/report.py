from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


styles = getSampleStyleSheet()


# ==========================================================
# CLI HEALTH REPORT
# ==========================================================

def generate_report(patient):

    filename = f"{patient.name}_Report.pdf"

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<b>NutriAyurAI Health Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Name : {patient.name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Age : {patient.age}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"BMI : {round(patient.calculate_bmi(), 2)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Health Status : {patient.health_status()}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Water Intake : {patient.calculate_water_intake()} Litres",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"BMR : {patient.calculate_bmr()} kcal/day",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Risk Level : {patient.risk_level()}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "<b>Recommendations</b>",
            styles["Heading2"]
        )
    )

    for item in patient.get_recommendation():

        story.append(
            Paragraph(
                f"• {item}",
                styles["Normal"]
            )
        )

    doc.build(story)

    print(
        f"\nReport Saved Successfully: {filename}"
    )


# ==========================================================
# VALIDATE ASSESSMENT RESULT
# ==========================================================

def _get_status(result):

    if not isinstance(result, dict):
        raise ValueError(
            "Assessment result must be a dictionary."
        )

    status = result.get("Status")

    if not status:
        raise ValueError(
            "Assessment status is required."
        )

    return status


# ==========================================================
# DIETITIAN NOTES
# ==========================================================

def generate_dietitian_notes(result):

    status = _get_status(result)

    if status == "Underweight":

        return [
            "Increase calorie intake with nutrient-dense foods.",
            "Consume protein-rich meals 5–6 times a day.",
            "Monitor weight weekly.",
            "Schedule follow-up after 4 weeks."
        ]

    elif status == "Healthy":

        return [
            "Maintain a balanced diet.",
            "Continue regular exercise.",
            "Drink adequate water daily.",
            "Schedule routine review after 3 months."
        ]

    elif status == "Overweight":

        return [
            "Reduce sugar and processed foods.",
            "Exercise for at least 30 minutes daily.",
            "Increase vegetables and fiber intake.",
            "Schedule follow-up after 6 weeks."
        ]

    else:

        return [
            "Consult a clinical dietitian.",
            "Follow a structured nutrition plan.",
            "Increase physical activity gradually.",
            "Monitor BMI regularly.",
            "Schedule follow-up after 4 weeks."
        ]


# ==========================================================
# FOLLOW-UP PERIOD
# ==========================================================

def get_follow_up_period(result):

    status = _get_status(result)

    if status == "Underweight":
        return "4 weeks"

    elif status == "Healthy":
        return "3 months"

    elif status == "Overweight":
        return "6 weeks"

    else:
        return "4 weeks"