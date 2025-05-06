import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Charter Party Performance", layout="wide", page_icon="🚢")

# =========================
# Sidebar Navigation
# =========================
page = st.sidebar.radio("Navigation", [
    "1. Voyage Details Input",
    "2. CP Performance Calculation",
    "3. Weather Data Upload & View",
    "4. Analysis & Report Generation"
])

st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8;
    }
    .stApp {
        background-image: linear-gradient(to right, #74ebd5, #ACB6E5);
        color: #1f2937;
    }
    .css-1v3fvcr {
        background-color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Global storage
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None
if "weather_definition" not in st.session_state:
    st.session_state.weather_definition = {}

# =========================
# Page 1: Voyage Details Input
# =========================
if page == "1. Voyage Details Input":
    st.header("🛳️ Voyage, Vessel, CP, and Weather Details")

    with st.form("voyage_form"):
        st.subheader("Vessel and Voyage Details")
        col1, col2 = st.columns(2)
        with col1:
            vessel_name = st.text_input("Vessel Name")
            from_port = st.text_input("From Port")
            voyage_no = st.text_input("Voyage No")
        with col2:
            to_port = st.text_input("To Port")
            cosp_date = st.date_input("COSP Date")
            eosp_date = st.date_input("EOSP Date")

        st.subheader("Charter Party Details")
        warranted_speed = st.number_input("Warranted Speed (knots)", value=13.0)
        warranted_consumption = st.number_input("Warranted Consumption (MT/day)", value=19.9)
        fuel_tolerance_percent = st.number_input("Fuel Tolerance (%)", value=5.0)
        speed_tolerance_knots = st.number_input("Speed Tolerance (knots)", value=0.5)

        st.subheader("Weather Exclusion Periods")
        exclusion_notes = st.text_area("Mention any weather exclusion period or notes")

        st.subheader("Weather Definition Settings")
        wind_force = st.slider("Max Wind Force (Beaufort Scale)", 0, 12, 4)
        wave_height = st.selectbox("Max Significant Wave Height (m)", [round(x * 0.25, 2) for x in range(0, 21)])

        submitted = st.form_submit_button("Save Details")
        if submitted:
            st.session_state.weather_definition = {
                'wind_force': wind_force,
                'wave_height': wave_height
            }
            st.success("Details Saved Successfully!")

# =========================
# Page 2: Calculation
# =========================
elif page == "2. CP Performance Calculation":
    st.header("⚙️ Performance Calculation")
    uploaded_file = st.file_uploader("Upload Noon Report Excel/CSV File", type=['xlsx', 'csv'])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state.uploaded_data = df
        st.success("File uploaded and processed successfully.")

        # TODO: Plug in the detailed calculation logic here (from your code)
        st.write("Calculation logic will be integrated here (as provided in your script).")

# =========================
# Page 3: Weather Upload & View
# =========================
elif page == "3. Weather Data Upload & View":
    st.header("🌦️ Upload & View Weather Data")
    weather_file = st.file_uploader("Upload Weather Data File (XLS/CSV)", type=['xlsx', 'csv'], key="weather")
    if weather_file:
        if weather_file.name.endswith(".csv"):
            df_weather = pd.read_csv(weather_file)
        else:
            df_weather = pd.read_excel(weather_file)

        st.dataframe(df_weather)

# =========================
# Page 4: Graphs & Reports
# =========================
elif page == "4. Analysis & Report Generation":
    st.header("📊 Performance Analytics & Reports")
    if st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data

        fig1, ax1 = plt.subplots()
        sns.scatterplot(data=df, x="wind_force", y="speed", ax=ax1)
        ax1.set_title("Speed vs Wind Force")
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=df, x="significant_wave_height", y="speed", ax=ax2)
        ax2.set_title("Speed vs Wave Height")
        st.pyplot(fig2)

        # Generate PDF
        if st.button("Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Charter Party Performance Report", ln=True, align='C')
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt="Summary and graphs will be printed here.")

            # Save PDF
            buffer = BytesIO()
            pdf.output(buffer)
            st.download_button("Download Report", data=buffer.getvalue(), file_name="performance_report.pdf", mime="application/pdf")
    else:
        st.warning("No performance data found. Please upload in Page 2.")
