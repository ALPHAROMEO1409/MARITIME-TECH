import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import base64
import io
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Charterparty Performance Analysis",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# Custom Styling
# =========================
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #0078D7; text-align: center; margin-bottom: 1rem;}
    .sub-header {font-size: 1.5rem; color: #0078D7; margin-bottom: 1rem;}
    .stButton>button {background-color: #0078D7; color: white;}
    .stButton>button:hover {background-color: #005a9e;}
    .highlight {background-color: #f0f7ff; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #0078D7;}
    @media print {
        div.page-break {page-break-after: always; page-break-inside: avoid;}
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Session State Initialization
# =========================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'vessel_input'

if 'vessel_data' not in st.session_state:
    st.session_state.vessel_data = {}

if 'voyage_data' not in st.session_state:
    st.session_state.voyage_data = {}

if 'cp_data' not in st.session_state:
    st.session_state.cp_data = {}

if 'exclusion_periods' not in st.session_state:
    st.session_state.exclusion_periods = []

if 'weather_definitions' not in st.session_state:
    st.session_state.weather_definitions = {}

# =========================
# Navigation Functions
# =========================
def nav_buttons():
    cols = st.columns(4)
    pages = {
        '📄 Vessel Input': 'vessel_input',
        '🧮 Calculations': 'calculations',
        '🌊 Weather Analysis': 'weather_analysis',
        '📊 Graphs & Analytics': 'graphs'
    }
    
    for col, (label, page) in zip(cols, pages.items()):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

# =========================
# Main Page Content
# =========================
st.markdown("<h1 class='main-header'>Charterparty Performance Analysis</h1>", unsafe_allow_html=True)
nav_buttons()

# =========================
# Page 1: Vessel Input
# =========================
if st.session_state.current_page == 'vessel_input':
    st.markdown("<h2 class='sub-header'>Vessel and Voyage Details</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Vessel Details", "Voyage Details", "CP Details", "Exclusion Periods", "Weather Definitions"])
    
    with tabs[0]:
        st.header("Vessel Details")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.vessel_data['name'] = st.text_input("Vessel Name", st.session_state.vessel_data.get('name', ''))
            st.session_state.vessel_data['imo'] = st.text_input("IMO Number", st.session_state.vessel_data.get('imo', ''))
        with col2:
            st.session_state.vessel_data['dwt'] = st.number_input("Deadweight (MT)", min_value=0, value=st.session_state.vessel_data.get('dwt', 0))
            st.session_state.vessel_data['grt'] = st.number_input("Gross Tonnage", min_value=0, value=st.session_state.vessel_data.get('grt', 0))

    with tabs[1]:
        st.header("Voyage Details")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.voyage_data['voyage_no'] = st.text_input("Voyage Number", st.session_state.voyage_data.get('voyage_no', ''))
            st.session_state.voyage_data['from_port'] = st.text_input("From Port", st.session_state.voyage_data.get('from_port', ''))
        with col2:
            st.session_state.voyage_data['to_port'] = st.text_input("To Port", st.session_state.voyage_data.get('to_port', ''))
            st.session_state.voyage_data['cosp_date'] = st.date_input("COSP Date", st.session_state.voyage_data.get('cosp_date', datetime.date.today()))

    with tabs[2]:
        st.header("Charterparty Details")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.cp_data['warranted_speed'] = st.number_input("Warranted Speed (knots)", value=st.session_state.cp_data.get('warranted_speed', 13.0))
            st.session_state.cp_data['warranted_consumption'] = st.number_input("Warranted Consumption (MT/day)", value=st.session_state.cp_data.get('warranted_consumption', 19.9))
        with col2:
            st.session_state.cp_data['fuel_tolerance_percent'] = st.number_input("Fuel Tolerance (%)", value=st.session_state.cp_data.get('fuel_tolerance_percent', 5.0))
            st.session_state.cp_data['speed_tolerance_knots'] = st.number_input("Speed Tolerance (knots)", value=st.session_state.cp_data.get('speed_tolerance_knots', 0.5))

    # ... (similar sections for other tabs)

# =========================
# Page 2: Calculations
# =========================
elif st.session_state.current_page == 'calculations':
    st.markdown("<h2 class='sub-header'>Performance Calculations</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Voyage Data", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Data processing logic here...
            # (Include the calculation logic from your original code)
            
            st.success("Data processed successfully!")
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# =========================
# Page 3: Weather Analysis
# =========================
elif st.session_state.current_page == 'weather_analysis':
    st.markdown("<h2 class='sub-header'>Weather Analysis</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Weather Data", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Weather analysis logic here...
            # (Include visualization code from your original script)
            
            st.success("Weather data analyzed!")
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# =========================
# Page 4: Graphs & Analytics
# =========================
elif st.session_state.current_page == 'graphs':
    st.markdown("<h2 class='sub-header'>Graphs & Analytics</h2>", unsafe_allow_html=True)
    
    if 'calculation_results' in st.session_state:
        # Visualization logic here...
        # (Include graph plotting code from your original script)
        
        fig, ax = plt.subplots()
        sns.lineplot(data=st.session_state.calculation_results['df'], x='date', y='speed')
        st.pyplot(fig)
    else:
        st.warning("No calculation results available. Perform calculations first.")

# =========================
# PDF Report Generation
# =========================
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add content to PDF
    pdf.cell(200, 10, txt="Charterparty Performance Report", ln=1, align='C')
    
    # Add vessel details
    pdf.cell(200, 10, txt=f"Vessel Name: {st.session_state.vessel_data.get('name', '')}", ln=1)
    
    # Add more sections as needed...
    
    return pdf.output(dest="S").encode("latin-1")

if st.sidebar.button("Generate PDF Report"):
    pdf_data = create_pdf()
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="report.pdf">Download PDF Report</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

# =========================
# Helper Functions
# =========================
def create_download_link(val, filename):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download PDF</a>'
