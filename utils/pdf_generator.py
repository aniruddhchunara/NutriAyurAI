from datetime import datetime
from uuid import uuid4
from services.settings_service import get_settings
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.pdfgen import canvas

from services.report_service import (
    generate_dietitian_notes,
    get_follow_up_period
)

from reportlab.lib import colors


class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)

        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):

        page_count = len(self.pages)

        for page in self.pages:

            self.__dict__.update(page)

            self.draw_page_number(page_count)

            canvas.Canvas.showPage(self)

        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):

        page_number = self._pageNumber

        self.setFont("Helvetica", 8)

        self.setFillColor(
            colors.HexColor("#64748B")
        )

        self.drawCentredString(
            297,
            20,
            f"Page {page_number} of {page_count}"
        )


def generate_health_report(data, filename):
    """
    Generate a professional NutriAyurAI Health Report PDF.
    """

    doc = SimpleDocTemplate(
        filename,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=45
        )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    story = []

# ==========================================================
# LOAD CLINIC SETTINGS
# ==========================================================

    settings = get_settings()

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
    # PROFESSIONAL HEADER
    # ==========================================================

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#0B6E4F")
    title_style.fontSize = 24
    title_style.leading = 28

    sub_title = styles["Heading2"]
    sub_title.alignment = TA_CENTER
    sub_title.textColor = colors.HexColor("#1E3A5F")
    sub_title.fontSize = 13
    sub_title.leading = 17

    normal_center = styles["BodyText"]
    normal_center.alignment = TA_CENTER
    normal_center.fontSize = 9
    normal_center.leading = 13


    # ----------------------------------------------------------
    # CLINIC NAME
    # ----------------------------------------------------------

    story.append(
        Paragraph(
            f"<b>{settings['clinic_name']}</b>",
            title_style
        )
    )

    story.append(Spacer(1, 4))


    # ----------------------------------------------------------
    # DIETITIAN
    # ----------------------------------------------------------

    dietitian_name = settings.get(
        "dietitian_name",
        ""
    ).strip()

    if dietitian_name:

        story.append(
            Paragraph(
                f"<b>{dietitian_name}</b>",
                sub_title
            )
        )

    story.append(Spacer(1, 8))


    # ----------------------------------------------------------
    # CONTACT INFORMATION
    # ----------------------------------------------------------

    contact_lines = []

    if settings.get("phone"):
        contact_lines.append(
            f"Phone: {settings['phone']}"
        )

    if settings.get("email"):
        contact_lines.append(
            f"Email: {settings['email']}"
        )

    if settings.get("address"):
        contact_lines.append(
            f"Address: {settings['address']}"
        )

    for contact in contact_lines:

        story.append(
            Paragraph(
                contact,
                normal_center
            )
        )


    story.append(Spacer(1, 12))


    # ----------------------------------------------------------
    # REPORT TITLE
    # ----------------------------------------------------------

    story.append(
        Paragraph(
            f"<b>{settings['report_title']}</b>",
                sub_title
        )
    )

    story.append(Spacer(1, 10))


    # ----------------------------------------------------------
    # REPORT META INFORMATION
    # ----------------------------------------------------------

    meta_table = Table(
        [
            [
                Paragraph(
                    f"<b>Generated:</b> {current_date}",
                    normal_center
                ),
                Paragraph(
                    f"<b>Report ID:</b> NTAI-{report_id}",
                    normal_center
                )
            ]
        ],
        colWidths=[250, 140]
    )

    meta_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#F1F5F9")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#CBD5E1")
            ),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.HexColor("#E2E8F0")
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    story.append(meta_table)

    story.append(Spacer(1, 22))

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

    story.append(Spacer(1, 8))

    health_table = Table([
        ["BMI", data["BMI"]],
        ["Health Status", data["Status"]],
        ["Health Score", data["Health Score"]],
        ["Ideal Weight", f"{data['Ideal Min']} - {data['Ideal Max']} kg"]
    ],
    colWidths=[180,210]
    )

    story.append(Spacer(1, 8))


    # ==========================================================
    # DYNAMIC HEALTH STATUS STYLE
    # ==========================================================

    status = str(data["Status"]).lower()

    if status == "healthy":
        status_background = colors.HexColor("#DCFCE7")
        status_text = colors.HexColor("#166534")


    elif status == "underweight":
        status_background = colors.HexColor("#FEF3C7")
        status_text = colors.HexColor("#92400E")

    elif status == "overweight":
        status_background = colors.HexColor("#FFEDD5")
        status_text = colors.HexColor("#9A3412")

    else:
        status_background = colors.HexColor("#FEE2E2")
        status_text = colors.HexColor("#991B1B")


    health_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#CBD5E1")
            ),

        # Left labels
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#E2E8F0")
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

        # Default value column
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                colors.white
            ),

        # Dynamic Health Status
            (
                "BACKGROUND",
                (1, 1),
                (1, 1),
                status_background
            ),

            (
                "TEXTCOLOR",
                (1, 1),
                (1, 1),
                status_text
            ),

            (
                "FONTNAME",
                (1, 1),
                (1, 1),
                "Helvetica-Bold"
            ),

        # Health Score
            (
                "FONTNAME",
                (1, 2),
                (1, 2),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                10
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
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
                heading_style
            )
    )

    story.append(Spacer(1, 10))

    notes = generate_dietitian_notes(data)

    notes_data = []

    for note in notes:

        notes_data.append(
            [
                "•",
                Paragraph(
                    note,
                    styles["BodyText"]
                )
            ]
        )
        notes_table = Table(
            notes_data,
            colWidths=[25,365]
        )
        notes_table.setStyle(
            TableStyle([
                (
                    "BACKGROUNG",
                    (0 ,0),
                    (-1 ,-1),
                    colors.HexColor("#F8FAFC")
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.HexColor("#CBD5E1")
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#E2E8F0")
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#0B6E4F")
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

    story.append(notes_table)
    story.append(Spacer(1, 20))

    # ==========================================================
    # FOLLOW-UP INFORMATION
    # ==========================================================

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>FOLLOW-UP INFORMATION</b>",
            heading_style
        )
    )

    story.append(Spacer(1, 8))

    follow_up = get_follow_up_period(data)

    dietitian_name = settings.get(
            "dietitian_name",
            ""
    ).strip()

    if not dietitian_name:
        dietitian_name = "Not specified"


    followup_table = Table(
        [
            [
                Paragraph(
                    "<b>Next Follow-up</b>",
                    styles["BodyText"]
                ),
                Paragraph(
                    f"<b>{follow_up}</b>",
                    styles["BodyText"]
                )
            ],
            [
                Paragraph(
                    "<b>Reviewed By</b>",
                    styles["BodyText"]
                ),
                Paragraph(
                    dietitian_name,
                    styles["BodyText"]
                )
            ]
        ],
        colWidths=[180, 210]
    )

    followup_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#CBD5E1")
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#E2E8F0")
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
        ])
    )

    story.append(followup_table)

    story.append(Spacer(1, 20))


    # ==========================================================
    # DISCLAIMER
    # ==========================================================

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>DISCLAIMER</b>",
            heading_style
        )
    )

    story.append(Spacer(1, 8))

    disclaimer_text = (
        "This report is generated by NutriAyurAI using "
        "AI-assisted health calculations. It is intended "
        "for nutritional guidance only and should not "
        "replace professional medical advice, diagnosis, "
        "or treatment."
    )

    disclaimer_table = Table(
        [
            [
                Paragraph(
                    disclaimer_text,
                    styles["BodyText"]
                )
            ]
        ],
        colWidths=[390]
    )

    disclaimer_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#F8FAFC")
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                0.8,
                colors.HexColor("#CBD5E1")
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                12
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10
            ),
        ])
    )

    story.append(disclaimer_table)

    story.append(Spacer(1, 15))



    # ==========================================================
    # FOOTER
    # ==========================================================

    footer_text = settings.get(
        "report_footer",
        "Generated by NutriAyurAI"
    ).strip()

    footer_style = styles["BodyText"]
    footer_style.alignment = TA_CENTER
    footer_style.fontSize = 8
    footer_style.textColor = colors.HexColor("#64748B")

    story.append(
        Paragraph(
            "____________________________________________",
            footer_style
        )
    )

    story.append(Spacer(1, 6))

    story.append(
        Paragraph(
            f"<b>{footer_text}</b>",
            footer_style
        )
    )

    story.append(
        Paragraph(
            "AI Health & Nutrition Assessment System",
            footer_style
        )
    )

    story.append(
        Paragraph(
            "Version 1.0",
            footer_style
        )
    )

    doc.build(
    story,
    canvasmaker=NumberedCanvas
    )