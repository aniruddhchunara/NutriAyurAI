import streamlit as st
from streamlit_option_menu import option_menu

from database.database import (
    create_table,
    create_appointment_table,
    create_diet_plan_tables
)


st.set_page_config(
    page_title="NutriAyurAI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)


create_table()
create_appointment_table()
create_diet_plan_tables()



st.title("🥗 NutriAyurAI")

st.markdown(
    """
    ## Welcome to NutriAyurAI
    
    Professional Health Anlytics &
    Machine Learning Dashboard
    """
)

st.info("Use the sidebar to navigate through the application.")



st.write("Welcome to NutriAyurAI!")

st.success("Streamlit is working successfully.")
