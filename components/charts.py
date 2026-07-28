import streamlit as st
import plotly.express as px


# -----------------------------------------
# BMI DONUT CHART
# -----------------------------------------

def bmi_distribution_chart(df):

    fig = px.pie(
        df,
        names="BMI Category",
        hole=0.45,
        title="BMI Category Distribution",
        color="BMI Category",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        title_x=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------------------
# AGE HISTOGRAM
# -----------------------------------------

def age_distribution_chart(df):

    fig = px.histogram(
        df,
        x="age",
        nbins=10,
        title="Age Distribution",
        color_discrete_sequence=["#3B82F6"]
    )

    fig.update_layout(
        title_x=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------------------
# WEIGHT BAR CHART
# -----------------------------------------

def weight_chart(df):

    fig = px.bar(
        df,
        x="name",
        y="weight",
        title="Patient Weight",
        color="weight",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        title_x=0.5,
        xaxis_title="Patient",
        yaxis_title="Weight (kg)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------------------
# HEIGHT BAR CHART
# -----------------------------------------

def height_chart(df):

    fig = px.bar(
        df,
        x="name",
        y="height",
        title="Patient Height",
        color="height",
        color_continuous_scale="Greens"
    )

    fig.update_layout(
        title_x=0.5,
        xaxis_title="Patient",
        yaxis_title="Height (cm)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )