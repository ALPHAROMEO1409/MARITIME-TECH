import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime
from io import BytesIO
import pdfkit

# Set page config
st.set_page_config(
    page_title="CharterParty Performance Suite",
    page_icon="⛴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(315deg, #0cbaba 0%, #380036 74%);
    color: #ffffff;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0.5);
}

[data-testid="stSidebar"] {
    background: rgba(18, 18, 18, 0.8) !important;
}

.metric-box {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 25px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Session State Management
if 'vessel_details' not in st.session_state:
    st.session_state.vessel_details = {}
if 'cp_params' not in st.session_state:
    st.session_state.cp_params = {}
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None

# Page 1: Vessel & CP Details
def input_page():
    st.header("📝 Voyage Configuration")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Vessel Particulars")
            st.session_state.vessel_details['name'] = st.text_input("Vessel Name", value="MV Ocean Explorer")
            st.session_state.vessel_details['imo'] = st.text_input("IMO Number", value="IMO9876543")
            st.session_state.vessel_details['type'] = st.selectbox("Vessel Type", ["VLCC", "Suezmax", "Aframax", "Panamax"])
        
        with col2:
            st.subheader("CP Parameters")
            st.session_state.cp_params['warranted_speed'] = st.number_input("Warranted Speed (knots)", value=13.0)
            st.session_state.cp_params['warranted_cons'] = st.number_input("Warranted Consumption (MT/day)", value=19.9)
            st.session_state.cp_params['speed_tol'] = st.number_input("Speed Tolerance (knots)", value=0.5)
            st.session_state.cp_params['fuel_tol'] = st.number_input("Fuel Tolerance (%)", value=5.0)

# Page 2: Performance Calculations
def calculations_page():
    st.header("⚡ Performance Analytics")
    
    uploaded_file = st.file_uploader("Upload Voyage Data (Excel/CSV)", type=['xlsx', 'csv'])
    
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Perform calculations from provided script
        df = df[df['event_type'].isin(['NOON AT SEA', 'COSP', 'EOSP'])]
        numeric_cols = ['distance_travelled_actual', 'steaming_time_hrs', 'me_fuel_consumed']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Calculate metrics
        total_distance = df['distance_travelled_actual'].sum()
        total_time = df['steaming_time_hrs'].sum()
        total_fuel = df['me_fuel_consumed'].sum()
        
        # Display KPIs
        cols = st.columns(3)
        cols[0].metric("Total Distance", f"{total_distance:.2f} nm")
        cols[1].metric("Total Fuel Used", f"{total_fuel:.2f} MT")
        cols[2].metric("Avg Speed", f"{(total_distance / total_time * 24):.2f} knots")
        
        # Show interactive data table
        st.subheader("Voyage Data Analysis")
        st.dataframe(df.style.background_gradient(cmap='viridis'), use_container_width=True)

# Page 3: Weather Analysis
def weather_analysis():
    st.header("🌪️ Weather Impact Analysis")
    
    uploaded_file = st.file_uploader("Upload Weather Data", type=['csv', 'xlsx'])
    
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            weather_df = pd.read_csv(uploaded_file)
        else:
            weather_df = pd.read_excel(uploaded_file)
        
        st.session_state.weather_data = weather_df
        
        # Create visualizations
        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(weather_df, x='wind_speed', y='speed', 
                           title="Speed vs Wind Speed")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(weather_df, x='wave_height', y='speed',
                           title="Speed vs Wave Height")
            st.plotly_chart(fig, use_container_width=True)

# Page 4: Analytics Dashboard
def analytics_dashboard():
    st.header("📈 Advanced Analytics")
    
    # Performance Comparison
    fig = px.line(title="Speed Performance Comparison")
    if 'performance_data' in st.session_state:
        df = st.session_state.performance_data
        fig.add_scatter(x=df['timestamp'], y=df['speed'], name="Actual Speed")
        fig.add_hline(y=st.session_state.cp_params['warranted_speed'], 
                     line_dash="dot", name="Warranted Speed")
    st.plotly_chart(fig, use_container_width=True)
    
    # Fuel Analysis
    if 'performance_data' in st.session_state:
        df = st.session_state.performance_data
        fig = px.bar(df, x='timestamp', y='me_fuel_consumed',
                    title="Fuel Consumption Pattern")
        st.plotly_chart(fig, use_container_width=True)

# Report Generation
def generate_report():
    # PDF generation logic here
    pass

# Main App Logic
pages = {
    "Voyage Setup": input_page,
    "Performance Analysis": calculations_page,
    "Weather Impact": weather_analysis,
    "Advanced Analytics": analytics_dashboard
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))
pages[selection]()

st.sidebar.divider()
if st.sidebar.button("📄 Generate Full Report"):
    generate_report()
