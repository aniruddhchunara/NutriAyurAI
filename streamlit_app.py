import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NutriAyurAI",
    page_icon="🌿",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🌿 NutriAyurAI")

st.subheader(
    "Professional Health Analytics & Machine Learning Platform"
)

st.write(
    """
    NutriAyurAI is an integrated health and nutrition management
    platform that combines health data analysis, machine learning,
    nutrition planning and Ayurvedic principles in one application.
    """
)

st.markdown("---")


# ============================================================
# ABOUT THE PROJECT
# ============================================================

st.header("🌱 About NutriAyurAI")

st.write(
    """
    NutriAyurAI is designed to help manage and analyze health and
    nutrition information in a structured way.

    The platform provides tools for patient management, appointments,
    health analysis, AI-based predictions, diet planning, analytics
    and reporting.

    It brings these functions together into a single application so
    that health and nutrition information can be managed more
    efficiently.
    """
)

st.info(
    """
    💡 **Project Goal**

    To create a centralized health and nutrition management system
    that uses data analysis, machine learning and Ayurvedic nutrition
    concepts to support personalized wellness management.
    """
)


# ============================================================
# WHAT THE APPLICATION PROVIDES
# ============================================================

st.header("✨ What NutriAyurAI Provides")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Patient Management")
    st.write(
        """
        Create, search, update and manage patient records including
        age, weight, height and activity information.
        """
    )

with col2:
    st.subheader("📅 Appointment Management")
    st.write(
        """
        Manage patient appointments including doctor, date, time
        and appointment reason.
        """
    )

with col3:
    st.subheader("🤖 AI Health Analysis")
    st.write(
        """
        Analyze health information and generate BMI, BMR, calorie,
        protein, water and health-status insights.
        """
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("🥗 Diet Plans")
    st.write(
        """
        Create and manage personalized diet plans with meals,
        nutrition information and Ayurvedic considerations.
        """
    )

with col5:
    st.subheader("📊 Analytics")
    st.write(
        """
        Analyze patient and health-related information through
        dashboards and analytical views.
        """
    )

with col6:
    st.subheader("📄 Reports")
    st.write(
        """
        Generate useful health and nutrition reports from the
        information managed within the application.
        """
    )


# ============================================================
# KEY HEALTH ANALYSIS
# ============================================================

st.markdown("---")

st.header("🧠 Health & Nutrition Analysis")

st.write(
    """
    NutriAyurAI uses important health parameters to provide
    structured nutritional and wellness insights.
    """
)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric("BMI", "Health Indicator")

with metric2:
    st.metric("BMR", "Energy Requirement")

with metric3:
    st.metric("Calories", "Daily Requirement")

with metric4:
    st.metric("Health Score", "Overall Indicator")


metric5, metric6, metric7, metric8 = st.columns(4)

with metric5:
    st.metric("Protein", "Daily Requirement")

with metric6:
    st.metric("Water", "Daily Requirement")

with metric7:
    st.metric("Ideal Weight", "Weight Range")

with metric8:
    st.metric("Health Status", "Personalized")


# ============================================================
# HOW THE SYSTEM WORKS
# ============================================================

st.markdown("---")

st.header("🔄 How NutriAyurAI Works")

step1, step2, step3, step4, step5 = st.columns(5)

with step1:
    st.subheader("1️⃣")
    st.write("Patient Data")
    st.caption("Collect health and personal information.")

with step2:
    st.subheader("2️⃣")
    st.write("Health Analysis")
    st.caption("Analyze important health parameters.")

with step3:
    st.subheader("3️⃣")
    st.write("AI Prediction")
    st.caption("Generate health and nutrition insights.")

with step4:
    st.subheader("4️⃣")
    st.write("Diet Planning")
    st.caption("Create personalized nutrition plans.")

with step5:
    st.subheader("5️⃣")
    st.write("Monitoring")
    st.caption("Review analytics and generate reports.")


# ============================================================
# AYURVEDIC APPROACH
# ============================================================

st.markdown("---")

st.header("🌿 Ayurvedic Nutrition Approach")

st.write(
    """
    NutriAyurAI also incorporates Ayurvedic dietary concepts into
    the nutrition-management workflow.

    The purpose is to combine traditional Ayurvedic principles with
    modern nutrition and data-driven analysis to support a more
    holistic approach to wellness.
    """
)

with st.expander("🌱 Learn about the Ayurvedic concept"):
    st.write(
        """
        Ayurveda emphasizes balance, appropriate food choices and
        lifestyle practices according to individual needs.

        NutriAyurAI provides a platform where these concepts can be
        considered alongside modern health and nutrition information.
        """
    )


# ============================================================
# APPLICATION MODULES
# ============================================================

st.markdown("---")

st.header("🧩 Application Modules")

st.write(
    """
    The application is organized into different modules so that
    each major part of the health-management workflow can be
    accessed separately.
    """
)

module1, module2 = st.columns(2)

with module1:
    st.write("🏠 **Dashboard**")
    st.write("Overview of the application and important information.")

    st.write("👤 **Patients**")
    st.write("Manage patient records and patient information.")

    st.write("📅 **Appointments**")
    st.write("Create and manage patient appointments.")

    st.write("📊 **Analytics**")
    st.write("Analyze available health and application data.")

with module2:
    st.write("🤖 **AI Prediction**")
    st.write("Perform health and nutrition analysis.")

    st.write("📄 **Reports**")
    st.write("Generate health and nutrition reports.")

    st.write("⚙️ **Settings**")
    st.write("Manage application-related settings.")

    st.write("🥗 **Diet Plans**")
    st.write("Create, manage and review personalized diet plans.")


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.markdown("---")

st.header("💻 Technology Behind NutriAyurAI")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.subheader("🐍 Python")
    st.write("Core programming language")

with tech2:
    st.subheader("🎈 Streamlit")
    st.write("Application interface")

with tech3:
    st.subheader("🗄️ SQLite")
    st.write("Application database")

with tech4:
    st.subheader("🤖 Machine Learning")
    st.write("Health prediction and analysis")


# ============================================================
# PROJECT HIGHLIGHT
# ============================================================

st.markdown("---")

st.success(
    """
    🌿 **NutriAyurAI**

    Bringing together patient management, nutrition,
    Ayurvedic concepts, health analytics and AI-powered
    insights in one platform.
    """
)


# ============================================================
# GET STARTED
# ============================================================

st.markdown("---")

st.header("🚀 Get Started")

st.write(
    """
    Use the navigation menu on the left to explore the different
    modules of NutriAyurAI.
    """
)

if st.button("Open Application →", type="primary"):
    st.info(
        "Select a module from the navigation menu to begin."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🌿 NutriAyurAI — Ancient Wisdom • Modern Nutrition • Intelligent Analysis"
)