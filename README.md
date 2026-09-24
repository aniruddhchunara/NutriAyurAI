# NutriAyurAI

### Practice Management & Nutrient Analysis Software for Ayurvedic Dietitians

NutriAyurAI is a Python-based healthcare analytics and practice management web application designed around patient management, appointments, Ayurvedic diet planning, health analysis, analytics, and report generation.

The project combines Python, Object-Oriented Programming, SQLite, Streamlit, Data Analytics, and basic AI/health prediction logic into one integrated application.

---

## Project Overview

NutriAyurAI provides a centralized platform for managing patient information and supporting nutrition-focused healthcare workflows.

The application includes:

- Patient Management
- Appointment Management
- AI Health and Nutrition Analysis
- Ayurvedic Diet Plan Management
- Diet Plan Templates
- Analytics Dashboard
- Health Reports
- PDF Generation
- Patient Diet History
- Application Settings
- Patient Authentication

---

## Main Features

### Patient Management

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

### Appointment Management

Manage patient appointments with:

- Patient name
- Doctor name
- Appointment date
- Appointment time
- Appointment reason
- Appointment search
- Appointment update
- Appointment deletion

### AI Health and Nutrition Analysis

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

### Ayurvedic Diet Plans

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

### Diet Plan Templates

The application includes reusable diet-plan templates that can be applied to existing plans.

Templates can automatically create multiple meals with predefined nutritional and Ayurvedic information.

### Analytics Dashboard

The analytics module provides visual insights into patient data.

Available analysis includes:

- Patient statistics
- BMI analysis
- Age analysis
- Health status information
- Patient distributions
- Dashboard KPIs
- Search and filtering

### Reports

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

### Authentication

The project includes an authentication service supporting:

- Patient account creation
- Patient login
- Password hashing
- Password verification
- User roles
- Patient-account linking

Password hashing uses PBKDF2-HMAC-SHA256 with a random salt.

---

## Project Architecture

The application follows a layered Python architecture:

```text
NutriAyurAI/
|
+-- database/
|   +-- database.py
|   +-- nutriayurai.db
|   +-- __init__.py
|
+-- models/
|   +-- patient.py
|   +-- appointment.py
|   +-- __init__.py
|
+-- repository/
|   +-- patient_repository.py
|   +-- appointment_repository.py
|   +-- diet_plan_repository.py
|   +-- __init__.py
|
+-- services/
|   +-- analytics_service.py
|   +-- appointment_service.py
|   +-- auth_service.py
|   +-- dashboard_service.py
|   +-- diet_history_service.py
|   +-- diet_plan_service.py
|   +-- diet_plan_template_service.py
|   +-- excel_report.py
|   +-- patient_service.py
|   +-- prediction_service.py
|   +-- report.py
|   +-- report_service.py
|   +-- settings_service.py
|   +-- view_patients.py
|
+-- pages/
|   +-- 1_Dashboard.py
|   +-- 2_Patients.py
|   +-- 3_Appointments.py
|   +-- 4_Analytics.py
|   +-- 5_AI_predicition.py
|   +-- 6_Diet_Plans.py
|   +-- 7_Reports.py
|   +-- 8_Settings.py
|
+-- utils/
|   +-- pdf_generator.py
|   +-- diet_plan_pdf_generator.py
|   +-- menu.py
|
+-- components/
|
+-- main.py
+-- migrate_database.py
+-- streamlit_app.py
+-- requirements.txt
+-- README.md