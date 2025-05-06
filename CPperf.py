import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
from io import BytesIO
import pdfkit

# Configure page settings
st.set_page_config(
    page_title="Charterparty Performance Analyzer PRO",
    page_icon="⛴️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Session State Management
if 'vessel_details' not in st.session_state:
    st.session_state.vessel_details = {}
if 'voyage_data' not in st.session_state:
    st.session_state.voyage_data = {}
if 'cp_params' not in st.session_state:
    st.session_state.cp_params = {}
if 'weather_def' not in st.session_state:
    st.session_state.weather_def = {}

# Page 1: Vessel and Voyage Details
def vessel_details_page():
    st.header("🚢 Vessel & Voyage Configuration")
    
    # Initialize voyage_data with default values
    if 'voyage_data' not in st.session_state:
        st.session_state.voyage_data = {
            'cosp': datetime(2024, 3, 1, 8, 0),
            'eosp': datetime(2024, 3, 10, 18, 0)
        }

    with st.container():
        cols = st.columns([1,1,1])
        with cols[0]:
            st.subheader("Vessel Particulars")
            st.session_state.vessel_details['name'] = st.text_input("Vessel Name", value="MV Ocean Carrier")
            st.session_state.vessel_details['imo'] = st.text_input("IMO Number", value="IMO1234567")
            st.session_state.vessel_details['type'] = st.selectbox("Vessel Type", 
                ["Tanker", "Bulk Carrier", "Container Ship", "LNG Carrier"])
        
        with cols[1]:
            st.subheader("Voyage Parameters")
            st.session_state.voyage_data['voyage_no'] = st.text_input("Voyage Number", value="V2024-01")
            st.session_state.voyage_data['load_port'] = st.text_input("Loading Port", value="Rotterdam")
            st.session_state.voyage_data['discharge_port'] = st.text_input("Discharge Port", value="Singapore")
            
            # Correct datetime input using date and time pickers
            cosp_date = st.date_input("COSP Date", value=st.session_state.voyage_data['cosp'].date(), key="cosp_date_input")
            cosp_time = st.time_input("COSP Time", value=st.session_state.voyage_data['cosp'].time(), key="cosp_time_input")
            st.session_state.voyage_data['cosp'] = datetime.combine(cosp_date, cosp_time)

            eosp_date = st.date_input("EOSP Date", value=st.session_state.voyage_data['eosp'].date(), key="eosp_date_input")
            eosp_time = st.time_input("EOSP Time", value=st.session_state.voyage_data['eosp'].time(), key="eosp_time_input")
            st.session_state.voyage_data['eosp'] = datetime.combine(eosp_date, eosp_time)
        
        with cols[2]:
            st.subheader("CP Parameters")
            st.session_state.cp_params['warranted_speed'] = st.number_input("Warranted Speed (knots)", 
                value=13.0, min_value=0.0, step=0.1)
            st.session_state.cp_params['warranted_consumption'] = st.number_input("Warranted Consumption (MT/day)", 
                value=19.9, min_value=0.0, step=0.1)
            st.session_state.cp_params['fuel_tolerance'] = st.number_input("Fuel Tolerance (%)", 
                value=5.0, min_value=0.0, max_value=100.0)
            st.session_state.cp_params['speed_tolerance'] = st.number_input("Speed Tolerance (knots)", 
                value=0.5, min_value=0.0, step=0.1)

    st.divider()
    
    # Weather Definition
    st.subheader("🌦️ Weather Criteria Configuration")
    cols = st.columns(2)
    with cols[0]:
        st.session_state.weather_def['beaufort'] = st.selectbox("Max Beaufort Scale for Good Weather",
            options=[(n, f"Beaufort {n}") for n in range(0, 13)], format_func=lambda x: x[1])
        
    with cols[1]:
        wave_heights = [round(i*0.25, 2) for i in range(0, 21)]
        st.session_state.weather_def['wave_height'] = st.selectbox("Max Significant Wave Height (m)",
            options=wave_heights, index=8)  # Default 2.0m

    # Exclusion Periods
    st.subheader("⏳ Exclusion Periods Management")
    if 'exclusions' not in st.session_state:
        st.session_state.exclusions = []

    cols = st.columns([2,2,1])
    with cols[0]:
        start = st.date_input("Start Date", value=datetime(2024, 3, 3))
    with cols[1]:
        end = st.date_input("End Date", value=datetime(2024, 3, 5))
    with cols[2]:
        st.write("")
        if st.button("➕ Add Exclusion Period", use_container_width=True):
            st.session_state.exclusions.append((start, end))

    # Display current exclusions
    if st.session_state.exclusions:
        st.write("**Active Exclusion Periods:**")
        for idx, (s, e) in enumerate(st.session_state.exclusions):
            st.write(f"{idx+1}. {s.strftime('%d %b %Y')} - {e.strftime('%d %b %Y')}")


    st.divider()
    
    # Weather Definition
    st.subheader("🌦️ Weather Criteria Configuration")
    cols = st.columns(2)
    with cols[0]:
        st.session_state.weather_def['beaufort'] = st.selectbox("Max Beaufort Scale for Good Weather",
            options=[(n, f"Beaufort {n}") for n in range(0, 13)], format_func=lambda x: x[1])
        
    with cols[1]:
        wave_heights = [round(i*0.25, 2) for i in range(0, 21)]
        st.session_state.weather_def['wave_height'] = st.selectbox("Max Significant Wave Height (m)",
            options=wave_heights, index=8)  # Default 2.0m

    # Exclusion Periods
    st.subheader("⏳ Exclusion Periods Management")
    if 'exclusions' not in st.session_state:
        st.session_state.exclusions = []

    cols = st.columns([2,2,1])
    with cols[0]:
        start = st.date_input("Start Date", value=datetime(2024, 3, 3))
    with cols[1]:
        end = st.date_input("End Date", value=datetime(2024, 3, 5))
    with cols[2]:
        st.write("")
        if st.button("➕ Add Exclusion Period", use_container_width=True):
            st.session_state.exclusions.append((start, end))

    # Display current exclusions
    if st.session_state.exclusions:
        st.write("**Active Exclusion Periods:**")
        for idx, (s, e) in enumerate(st.session_state.exclusions):
            st.write(f"{idx+1}. {s.strftime('%d %b %Y')} - {e.strftime('%d %b %Y')}")

# Page 2: Performance Calculations
def calculations_page():
    st.header("📈 Performance Analytics Engine")
    
    uploaded_file = st.file_uploader("Upload Voyage Data (CSV/Excel)", type=['csv', 'xlsx'])
    
    if uploaded_file:
        if 'csv' in uploaded_file.name.lower():
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Apply weather classification
        df['day_status'] = df.apply(classify_weather_day, axis=1)
        
        # Perform calculations using the provided code
        results = perform_calculations(df)
        
        # Display results
        st.subheader("Performance Summary")
        cols = st.columns(4)
        cols[0].metric("Total Distance", f"{results['total_distance']:,.1f} nm")
        cols[1].metric("Avg Speed", f"{results['voyage_avg_speed']:,.1f} knots")
        cols[2].metric("Fuel Consumption", f"{results['total_fuel']:,.1f} MT")
        cols[3].metric("CP Compliance", f"{results['cp_compliance']:,.1%}")

        # Detailed metrics
        st.subheader("Detailed Analysis")
        with st.expander("Weather Impact Analysis"):
            cols = st.columns(2)
            cols[0].metric("Good Weather Days", f"{len(results['good_days'])}")
            cols[1].metric("Bad Weather Days", f"{len(results['bad_days'])}")
            
        with st.expander("Fuel Efficiency Analysis"):
            cols = st.columns(3)
            cols[0].metric("Overconsumption", f"{results['fuel_overconsumption']:,.1f} MT")
            cols[1].metric("Potential Savings", f"{results['fuel_saving']:,.1f} MT")
            cols[2].metric("Time Difference", f"{results['time_lost']:,.1f} hrs")

        # Raw data preview
        st.subheader("Processed Data Preview")
        st.dataframe(df.style.background_gradient(cmap='viridis'), use_container_width=True)

def classify_weather_day(row):
    # Implement your weather classification logic here
    if row['wind_force'] <= st.session_state.weather_def['beaufort'][0] and \
       row['wave_height'] <= st.session_state.weather_def['wave_height']:
        return 'GOOD WEATHER DAY'
    return 'BAD WEATHER DAY'

def perform_calculations(df):
    # Implement your provided calculation logic here
    # Return results as dictionary
    return {
        'total_distance': 1500,
        'voyage_avg_speed': 12.8,
        'total_fuel': 245.6,
        'cp_compliance': 0.92,
        'good_days': [],
        'bad_days': [],
        'fuel_overconsumption': 15.2,
        'fuel_saving': 8.4,
        'time_lost': 4.5
    }

# Page 3: Weather Analysis
def weather_analysis_page():
    st.header("🌪️ Weather Impact Analytics")
    
    uploaded_file = st.file_uploader("Upload Weather Data (CSV/Excel)", type=['csv', 'xlsx'])
    
    if uploaded_file:
        if 'csv' in uploaded_file.name.lower():
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.session_state.weather_data = df
        
        # Show basic statistics
        st.subheader("Weather Data Overview")
        cols = st.columns(3)
        cols[0].metric("Max Wind Speed", f"{df['wind_speed'].max():.1f} m/s")
        cols[1].metric("Max Wave Height", f"{df['wave_height'].max():.1f} m")
        cols[2].metric("Avg Temperature", f"{df['temperature'].mean():.1f}°C")
        
        # Raw data display
        st.subheader("Weather Data Preview")
        st.dataframe(df.style.background_gradient(cmap='plasma'), use_container_width=True)

# Page 4: Dashboard & Analytics
def dashboard_page():
    st.header("📊 Advanced Performance Analytics")
    
    if 'performance_data' in st.session_state and 'weather_data' in st.session_state:
        df = pd.merge(st.session_state.performance_data, 
                     st.session_state.weather_data,
                     on='timestamp')
        
        # Create visualizations
        st.subheader("Speed Analysis")
        fig1 = px.scatter(df, x='wind_speed', y='speed', 
                         color='wave_height', trendline="lowess")
        st.plotly_chart(fig1, use_container_width=True)
        
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Speed Distribution")
            fig2 = px.histogram(df, x='speed', nbins=20)
            st.plotly_chart(fig2)
        
        with cols[1]:
            st.subheader("Fuel Efficiency")
            fig3 = px.line(df, x='timestamp', y=['fuel_consumption', 'warranted_consumption'])
            st.plotly_chart(fig3)

# Generate PDF Report
def generate_pdf():
    # PDF generation logic using reportlab or similar
    pass

# Main App Controller
pages = {
    "Vessel & Voyage Setup": vessel_details_page,
    "Performance Analysis": calculations_page,
    "Weather Analytics": weather_analysis_page,
    "Advanced Dashboard": dashboard_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))
pages[selection]()

# Report Generation
st.sidebar.divider()
if st.sidebar.button("📄 Generate Full Report"):
    generate_pdf()
