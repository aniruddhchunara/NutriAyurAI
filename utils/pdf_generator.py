from datetime import datetime
from uuid import uuid4

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors


def generate_health_report(data, filename):
    """
    Generate a professional NutriAyurAI Health Report PDF.
    """

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    story = []

    current_date = datetime.now().strftime(
        "%d %B %Y %I:%M %p"
    )

    report_id = str(uuid4())[:8].upper()
    normal_center = styles["BodyText"]
    normal_center.alignment = TA_CENTER


    story.append(
        Paragraph(
            f"<b>Report ID:</b> NTAI-{report_id}",
            normal_center
        )
    )

    # ==========================================================
    # HEADER
    # ==========================================================

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.darkblue

    sub_title = styles["Heading2"]
    sub_title.alignment = TA_CENTER
    sub_title.textColor = colors.HexColor("#0B6E4F")

    normal_center = styles["BodyText"]
    normal_center.alignment = TA_CENTER

    story.append(
        Paragraph(
            "<b>NutriAyurAI</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI Health & Nutrition Assessment Report",
            sub_title
        )
    )

    story.append(
        Paragraph(
            "Healthy Life • Smart Nutrition • AI Powered",
            normal_center
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"<b>Generated On :</b> {current_date}",
            normal_center
        )
    )

    story.append(
        Paragraph(
            f"<b>Report ID :</b> {report_id}",
            normal_center
        )
    )

    story.append(Spacer(1, 25))

    # ==========================================================
    # PATIENT INFORMATION
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Patient Information</b>",
                heading_style
        )
    )

    patient_table = Table(
        [
            ["Name",data["Name"]],
            ["Age", f"{data['Age']} Years"],
            ["Weight", f"{data['Weight']} kg"],
            ["Height", f"{data['Height']} cm"],
            ["Activity Level", data["Activity Level"]]
        ],
        colWidths=[140,250]
    )

    patient_table.setStyle(
    TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ])
    )

    story.append(patient_table)

    story.append(Spacer(1, 20))

    # ==========================================================
    # HEALTH ANALYSIS
    # ==========================================================

    story.append(
        Paragraph(
            "<b>Health Analysis</b>",
            heading_style
        )
    )

    health_table = Table([
        ["BMI", data["BMI"]],
        ["Health Status", data["Status"]],
        ["Health Score", data["Health Score"]],
        ["Ideal Weight", f"{data['Ideal Min']} - {data['Ideal Max']} kg"]
    ])

    health_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.beige),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(health_table)

    story.append(Spacer(1, 20))

    # ==========================================================
    # DIETITIAN NOTES
    # ==========================================================

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
                "<b>📝 DIETITIAN NOTES</b>",
                styles["Heading2"]
            )
    )

    story.append(Spacer(1, 10))

    for _ in range(5):

        story.append(
            Paragraph(
                "______________________________________________",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 8))



    # ==========================================================
    # FOLLOW-UP INFORMATION
    # ==========================================================

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>📅 FOLLOW-UP INFORMATION</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Next Follow-up:</b> ____________________________",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "<b>Reviewed By (Dietitian):</b> ____________________",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))


    # ==========================================================
    # DISCLAIMER
    # ==========================================================

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>⚠ DISCLAIMER</b>",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
            Paragraph(
            "This report is generated by NutriAyurAI using "
            "AI-assisted health calculations. It is intended "
            "for nutritional guidance only and should not "
            "replace professional medical advice, diagnosis, "
            "or treatment.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))



    # ==========================================================
    # FOOTER
    # ==========================================================

    story.append(
            Paragraph(
            "<hr/>",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 8))

    story.append(
            Paragraph(
            "<b>Generated by NutriAyurAI</b>",
            styles["Normal"]
        )
    )

    story.append(
            Paragraph(
            "AI Health & Nutrition Assessment System",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "Version 1.0",
            styles["Normal"]
        )
    )

    doc.build(story)

