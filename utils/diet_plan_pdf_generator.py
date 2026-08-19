from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# ==========================================================
# GENERATE DIET PLAN PDF
# ==========================================================

def generate_diet_plan_pdf(
    plan,
    meals,
    filename
):
    """
    Generate a professional Diet Plan PDF.

    plan structure:
        0 = id
        1 = patient_name
        2 = plan_name
        3 = created_at
        4 = status
        5 = updated_at
        6 = start_date
        7 = end_date
        8 = duration_days

    meal structure:
        0 = meal_id
        1 = meal_type
        2 = meal_time
        3 = calories
        4 = protein
        5 = food_items
        6 = rasa
        7 = virya
        8 = digestion
        9 = notes
    """

    # ======================================================
    # DOCUMENT
    # ======================================================

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    # ======================================================
    # STYLES
    # ======================================================

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#0B6E4F")

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#0B6E4F")

    normal_style = styles["BodyText"]

    center_style = styles["BodyText"]
    center_style.alignment = TA_CENTER

    # ======================================================
    # STORY
    # ======================================================

    story = []

    # ======================================================
    # HEADER
    # ======================================================

    story.append(
        Paragraph(
            "<b>NutriAyurAI</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Personalized Diet Plan",
            center_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ======================================================
    # PLAN INFORMATION
    # ======================================================

    plan_id = plan[0]
    patient_name = plan[1]
    plan_name = plan[2]
    created_at = plan[3]
    status = plan[4] or "Active"
    updated_at = plan[5] or "Not updated"
    start_date = plan[6] if len(plan)  > 6 else None
    end_date = plan[7] if len(plan) > 7 else None
    duration_days = plan[8] if len(plan) > 8 else None

    story.append(
        Paragraph(
            "📋 Diet Plan Information",
            heading_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    plan_table = Table(
        [
            ["Plan ID", str(plan_id)],
            ["Patient", str(patient_name)],
            ["Plan Name", str(plan_name)],
            ["Status", str(status)],
            ["Created On", str(created_at)],
            ["Last Updated", str(updated_at)]
        ],
        colWidths=[
            45 * mm,
            125 * mm
        ]
    )

    plan_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#E8F5E9")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    story.append(
        plan_table
    )

    story.append(
        Spacer(1, 20)
    )
    
    # ======================================================
    # DIET PLAN SCHEDULE
    # ======================================================

    story.append(
        Paragraph(
            "📅 Diet Plan Schedule",
            heading_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    schedule_table = Table(
        [
            [
                "Start Date",
                str(start_date or "Not set")
            ],
            [
                "End Date",
                str(end_date or "Not set")
            ],
            [
                "Duration",
                (
                    f"{duration_days} days"
                    if duration_days
                    else "Not set"
                )
            ]
        ],
        colWidths=[
            45 * mm,
            125 * mm
        ]
    )

    schedule_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#E8F5E9")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    story.append(
        schedule_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ======================================================
    # NUTRITION TOTALS
    # ======================================================

    total_calories = sum(
        float(meal[3] or 0)
        for meal in meals
    )

    total_protein = sum(
        float(meal[4] or 0)
        for meal in meals
    )

    total_meals = len(meals)

    story.append(
        Paragraph(
            "📊 Nutrition Summary",
            heading_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    summary_table = Table(
        [
            [
                "Total Meals",
                "Total Calories",
                "Total Protein"
            ],
            [
                str(total_meals),
                f"{total_calories:.0f} kcal",
                f"{total_protein:.1f} g"
            ]
        ],
        colWidths=[
            55 * mm,
            55 * mm,
            55 * mm
        ]
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0B6E4F")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    story.append(
        summary_table
    )

    story.append(
        Spacer(1, 20)
    )

    # ======================================================
    # MEALS
    # ======================================================

    story.append(
        Paragraph(
            "🍽️ Meal Plan",
            heading_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    meal_rows = [
        [
            "Meal",
            "Time",
            "Calories",
            "Protein",
            "Food Items"
        ]
    ]

    for meal in meals:

        meal_type = meal[1]
        meal_time = meal[2]
        calories = meal[3]
        protein = meal[4]
        food_items = meal[5] or ""

        meal_rows.append(
            [
                str(meal_type),
                str(meal_time),
                f"{float(calories or 0):.0f}",
                f"{float(protein or 0):.1f} g",
                str(food_items)
            ]
        )

    meal_table = Table(
        meal_rows,
        colWidths=[
            30 * mm,
            22 * mm,
            25 * mm,
            25 * mm,
            68 * mm
        ],
        repeatRows=1
    )

    meal_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0B6E4F")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story.append(
        meal_table
    )

    story.append(
        Spacer(1, 20)
    )

    # ======================================================
    # AYURVEDIC DETAILS
    # ======================================================

    story.append(
        Paragraph(
            "🌿 Ayurvedic Meal Details",
            heading_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    ayurvedic_rows = [
        [
            "Meal",
            "Rasa",
            "Virya",
            "Digestion"
        ]
    ]

    for meal in meals:

        ayurvedic_rows.append(
            [
                str(meal[1]),
                str(meal[6] or "Not specified"),
                str(meal[7] or "Not specified"),
                str(meal[8] or "Not specified")
            ]
        )

    ayurvedic_table = Table(
        ayurvedic_rows,
        colWidths=[
            45 * mm,
            40 * mm,
            40 * mm,
            45 * mm
        ],
        repeatRows=1
    )

    ayurvedic_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0B6E4F")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ]
        )
    )

    story.append(
        ayurvedic_table
    )

    story.append(
        Spacer(1, 20)
    )

    # ======================================================
    # NOTES
    # ======================================================

    story.append(
        Paragraph(
            "📝 Meal Notes",
            heading_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    has_notes = False

    for meal in meals:

        if meal[9]:

            has_notes = True

            story.append(
                Paragraph(
                    f"<b>{meal[1]}:</b> "
                    f"{meal[9]}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 5)
            )

    if not has_notes:

        story.append(
            Paragraph(
                "No meal-specific notes were provided.",
                normal_style
            )
        )

    story.append(
        Spacer(1, 20)
    )

    # ======================================================
    # DISCLAIMER
    # ======================================================

    story.append(
        Paragraph(
            "⚠️ Disclaimer",
            heading_style
        )
    )

    story.append(
        Spacer(1, 8)
    )

    story.append(
        Paragraph(
            "This diet plan is intended for nutritional "
            "guidance and should be reviewed by a qualified "
            "dietitian or healthcare professional. "
            "It does not replace professional medical "
            "diagnosis or treatment.",
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ======================================================
    # FOOTER
    # ======================================================

    story.append(
        Paragraph(
            "NutriAyurAI — AI Health & Nutrition "
            "Assessment System",
            center_style
        )
    )

    story.append(
        Paragraph(
            "Diet Plan Report | Version 1.0",
            center_style
        )
    )

    # ======================================================
    # BUILD PDF
    # ======================================================

    doc.build(
        story
    )