import streamlit as st


def kpi_card(title, value, icon, help_text=""):

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg,#1e293b,#0f172a);
            border-radius:20px;
            padding:20px;
            border:1px solid #334155;
            box-shadow:0px 8px 20px rgba(0,0,0,0.25);
            transition:0.3s;
            height:170px;
        ">

            <div style="
                font-size:20px;
            ">
                {icon}
            </div>

            <div style="
                color:#94A3B8;
                font-size:15px;
                margin-top:10px;
            ">
                {title}
            </div>

            <div style="
                color:white;
                font-size:34px;
                font-weight:bold;
                margin-top:10px;
            ">
                {value}
            </div>

            <div style="
                color:#64748B;
                font-size:12px;
                margin-top:12px;
            ">
                {help_text}
            </div>

        </div>

        <br>
        """,
        unsafe_allow_html=True
    )