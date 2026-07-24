from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def generate_report(patient):

    filename = f"{patient.name}_Report.pdf"

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph("<b>NutriAyurAI Health Report</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"Name : {patient.name}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Age : {patient.age}", styles["Normal"])
    )

    story.append(
        Paragraph(f"BMI : {round(patient.calculate_bmi(),2)}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Health Status : {patient.health_status()}", styles["Normal"])
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
        Paragraph("<b>Recommendations</b>", styles["Heading2"])
    )

    for item in patient.get_recommendation():

        story.append(
            Paragraph(f"• {item}", styles["Normal"])
        )

    doc.build(story)

    print(f"\nReport Saved Successfully: {filename}")