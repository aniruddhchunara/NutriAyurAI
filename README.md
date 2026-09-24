# NutriAyurAI

### Practice Management & Nutrient Analysis Software for Ayurvedic Dietitians

NutriAyurAI is a Python-based healthcare analytics and practice management web application designed around patient management, appointments, Ayurvedic diet planning, health analysis, analytics, and report generation.

The project combines **Python, Object-Oriented Programming, SQLite, Streamlit, Data Analytics, and basic AI/health prediction logic** into one integrated application.

---

## ðŸ“Œ Project Overview

NutriAyurAI provides a centralized platform for managing patient information and supporting nutrition-focused healthcare workflows.

The application includes:

- Patient Management
- Appointment Management
- AI Health & Nutrition Analysis
- Ayurvedic Diet Plan Management
- Diet Plan Templates
- Analytics Dashboard
- Health Reports
- PDF Generation
- Patient Diet History
- Application Settings
- Patient Authentication

---

# âœ¨ Main Features

## ðŸ‘¤ Patient Management

Complete patient CRUD functionality:

- Add patients
- Search patients
- View patient details
- Update patient information
- Delete patients
- Patient ID-based operations
- Activity-level tracking

Patient information includes:

- Name
- Age
- Weight
- Height
- Activity Factor

---

## ðŸ“… Appointment Management

Manage patient appointments with:

- Patient name
- Doctor name
- Appointment date
- Appointment time
- Appointment reason
- Appointment search
- Appointment update
- Appointment deletion

---

## ðŸ¤– AI Health & Nutrition Analysis

The prediction module analyzes basic health and nutrition parameters.

It calculates:

- BMI
- BMI health status
- BMR
- Daily calorie requirement
- Protein requirement
- Water requirement
- Ideal weight range
- Health score
- Weight-management goal
- Health recommendations

The module also includes input validation for health-related values.

---

## ðŸ¥— Ayurvedic Diet Plans

Dietitians can create and manage personalized diet plans.

Features include:

- Create diet plans
- Update diet plans
- Delete diet plans
- Plan status management
- Meal management
- Calories
- Protein
- Food items
- Meal timing
- Rasa
- Virya
- Digestion information
- Notes

Supported plan statuses:

- Active
- Paused
- Completed
- Archived

---

## ðŸ“‹ Diet Plan Templates

The application includes reusable diet-plan templates that can be applied to existing plans.

Templates can automatically create multiple meals with predefined nutritional and Ayurvedic information.

---

## ðŸ“Š Analytics Dashboard

The analytics module provides visual insights into patient data.

Available analysis includes:

- Patient statistics
- BMI analysis
- Age analysis
- Health status information
- Patient distributions
- Dashboard KPIs
- Search and filtering

---

## ðŸ“„ Reports

NutriAyurAI supports health and nutrition report generation.

Reports can include:

- Patient information
- BMI
- Health status
- Health score
- Ideal weight range
- Activity factor
- Dietitian notes
- Follow-up information
- Review information

PDF reports are generated using the application's report-generation utilities.

---

## ðŸ” Authentication

The project includes an authentication service supporting:

- Patient account creation
- Patient login
- Password hashing
- Password verification
- User roles
- Patient-account linking

Password hashing uses PBKDF2-HMAC-SHA256 with a random salt.

---

# ðŸ—ï¸ Project Architecture

The application follows a layered Python architecture:

```text
NutriAyurAI/
â”‚
â”œâ”€â”€ database/
â”‚   â”œâ”€â”€ database.py
â”‚   â”œâ”€â”€ nutriayurai.db
â”‚   â””â”€â”€ __init__.py
â”‚
â”œâ”€â”€ models/
â”‚   â”œâ”€â”€ patient.py
â”‚   â”œâ”€â”€ appointment.py
â”‚   â””â”€â”€ __init__.py
â”‚
â”œâ”€â”€ repository/
â”‚   â”œâ”€â”€ patient_repository.py
â”‚   â”œâ”€â”€ appointment_repository.py
â”‚   â”œâ”€â”€ diet_plan_repository.py
â”‚   â””â”€â”€ __init__.py
â”‚
â”œâ”€â”€ services/
â”‚   â”œâ”€â”€ analytics_service.py
â”‚   â”œâ”€â”€ appointment_service.py
â”‚   â”œâ”€â”€ auth_service.py
â”‚   â”œâ”€â”€ dashboard_service.py
â”‚   â”œâ”€â”€ diet_history_service.py
â”‚   â”œâ”€â”€ diet_plan_service.py
â”‚   â”œâ”€â”€ diet_plan_template_service.py
â”‚   â”œâ”€â”€ excel_report.py
â”‚   â”œâ”€â”€ patient_service.py
â”‚   â”œâ”€â”€ prediction_service.py
â”‚   â”œâ”€â”€ report.py
â”‚   â”œâ”€â”€ report_service.py
â”‚   â”œâ”€â”€ settings_service.py
â”‚   â””â”€â”€ view_patients.py
â”‚
â”œâ”€â”€ pages/
â”‚   â”œâ”€â”€ 1_Dashboard.py
â”‚   â”œâ”€â”€ 2_Patients.py
â”‚   â”œâ”€â”€ 3_Appointments.py
â”‚   â”œâ”€â”€ 4_Analytics.py
â”‚   â”œâ”€â”€ 5_AI_predicition.py
â”‚   â”œâ”€â”€ 6_Diet_Plans.py
â”‚   â”œâ”€â”€ 7_Reports.py
â”‚   â””â”€â”€ 8_Settings.py
â”‚
â”œâ”€â”€ utils/
â”‚   â”œâ”€â”€ pdf_generator.py
â”‚   â”œâ”€â”€ diet_plan_pdf_generator.py
â”‚   â””â”€â”€ menu.py
â”‚
â”œâ”€â”€ components/
â”‚
â”œâ”€â”€ main.py
â”œâ”€â”€ migrate_database.py
â”œâ”€â”€ streamlit_app.py
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
