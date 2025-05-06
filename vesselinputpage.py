import streamlit as st
import datetime
import pandas as pd
from streamlit import session_state as ss

# Set page config
st.set_page_config(
    page_title="Charterparty Performance Analysis",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #0078D7; text-align: center; margin-bottom: 1rem;}
    .sub-header {font-size: 1.5rem; color: #0078D7; margin-bottom: 1rem;}
    .stButton>button {background-color: #0078D7; color: white;}
    .stButton>button:hover {background-color: #005a9e;}
    .highlight {background-color: #f0f7ff; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #0078D7;}
    
    /* Print page break settings */
    @media print {
        div.page-break {
            page-break-after: always;
            page-break-inside: avoid;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if not already present
if 'vessel_data' not in ss:
    ss.vessel_data = {}
if 'voyage_data' not in ss:
    ss.voyage_data = {}
if 'cp_data' not in ss:
    ss.cp_data = {}
if 'exclusion_periods' not in ss:
    ss.exclusion_periods = []
if 'weather_definitions' not in ss:
    ss.weather_definitions = {}
if 'current_page' not in ss:
    ss.current_page = 'vessel_input'

# Custom navigation buttons
def nav_buttons():
    cols = st.columns(4)
    with cols[0]:
        if st.button("📄 Vessel Input", use_container_width=True):
            ss.current_page = 'vessel_input'
            st.experimental_rerun()
    with cols[1]:
        if st.button("🧮 Calculations", use_container_width=True):
            ss.current_page = 'calculations'
            st.experimental_rerun()
    with cols[2]:
        if st.button("🌊 Weather Analysis", use_container_width=True):
            ss.current_page = 'weather_analysis'
            st.experimental_rerun()
    with cols[3]:
        if st.button("📊 Graphs & Analytics", use_container_width=True):
            ss.current_page = 'graphs'
            st.experimental_rerun()
    st.markdown("---")

# Main app header
st.markdown("<h1 class='main-header'>Charterparty Performance Analysis</h1>", unsafe_allow_html=True)
nav_buttons()

# Page content based on current page
if ss.current_page == 'vessel_input':
    st.markdown("<h2 class='sub-header'>Vessel and Voyage Details</h2>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    tabs = st.tabs(["Vessel Details", "Voyage Details", "CP Details", "Exclusion Periods", "Weather Definitions"])
    
    # Tab 1: Vessel Details
    with tabs[0]:
        st.header("Vessel Details")
        col1, col2 = st.columns(2)
        
        with col1:
            ss.vessel_data['name'] = st.text_input("Vessel Name", ss.vessel_data.get('name', ''))
            ss.vessel_data['imo'] = st.text_input("IMO Number", ss.vessel_data.get('imo', ''))
            ss.vessel_data['type'] = st.selectbox("Vessel Type", 
                                               ["Bulk Carrier", "Oil Tanker", "Container Ship", "Gas Carrier", "Chemical Tanker", "Other"],
                                               index=0 if 'type' not in ss.vessel_data else 
                                               ["Bulk Carrier", "Oil Tanker", "Container Ship", "Gas Carrier", "Chemical Tanker", "Other"].index(ss.vessel_data['type']))
        
        with col2:
            ss.vessel_data['dwt'] = st.number_input("Deadweight (MT)", min_value=0, value=ss.vessel_data.get('dwt', 0))
            ss.vessel_data['grt'] = st.number_input("Gross Tonnage", min_value=0, value=ss.vessel_data.get('grt', 0))
            ss.vessel_data['built'] = st.number_input("Year Built", min_value=1900, max_value=datetime.datetime.now().year, 
                                                 value=ss.vessel_data.get('built', 2000))
    
    # Tab 2: Voyage Details
    with tabs[1]:
        st.header("Voyage Details")
        col1, col2 = st.columns(2)
        
        with col1:
            ss.voyage_data['voyage_no'] = st.text_input("Voyage Number", ss.voyage_data.get('voyage_no', ''))
            ss.voyage_data['from_port'] = st.text_input("From Port", ss.voyage_data.get('from_port', ''))
            ss.voyage_data['to_port'] = st.text_input("To Port", ss.voyage_data.get('to_port', ''))
        
        with col2:
            cosp_date = ss.voyage_data.get('cosp_date', datetime.datetime.now().date())
            if isinstance(cosp_date, str):
                cosp_date = datetime.datetime.strptime(cosp_date, "%Y-%m-%d").date()
            ss.voyage_data['cosp_date'] = st.date_input("COSP Date", cosp_date)
            
            ss.voyage_data['cosp_time'] = st.time_input("COSP Time", 
                                                   datetime.time(0, 0) if 'cosp_time' not in ss.voyage_data else ss.voyage_data['cosp_time'])
            
            eosp_date = ss.voyage_data.get('eosp_date', datetime.datetime.now().date())
            if isinstance(eosp_date, str):
                eosp_date = datetime.datetime.strptime(eosp_date, "%Y-%m-%d").date()
            ss.voyage_data['eosp_date'] = st.date_input("EOSP Date", eosp_date)
            
            ss.voyage_data['eosp_time'] = st.time_input("EOSP Time", 
                                                   datetime.time(0, 0) if 'eosp_time' not in ss.voyage_data else ss.voyage_data['eosp_time'])
    
    # Tab 3: CP Details
    with tabs[2]:
        st.header("Charterparty Details")
        col1, col2 = st.columns(2)
        
        with col1:
            ss.cp_data['charterer'] = st.text_input("Charterer", ss.cp_data.get('charterer', ''))
            ss.cp_data['cp_date'] = st.date_input("CP Date", 
                                             datetime.datetime.now().date() if 'cp_date' not in ss.cp_data else ss.cp_data['cp_date'])
            
        with col2:
            ss.cp_data['warranted_speed'] = st.number_input("Warranted Speed (knots)", 
                                                      min_value=0.0, value=ss.cp_data.get('warranted_speed', 13.0), step=0.1)
            ss.cp_data['warranted_consumption'] = st.number_input("Warranted Consumption (MT/day)", 
                                                            min_value=0.0, value=ss.cp_data.get('warranted_consumption', 19.9), step=0.1)
            ss.cp_data['fuel_tolerance_percent'] = st.number_input("Fuel Tolerance (%)", 
                                                             min_value=0.0, value=ss.cp_data.get('fuel_tolerance_percent', 5.0), step=0.1)
            ss.cp_data['speed_tolerance_knots'] = st.number_input("Speed Tolerance (knots)", 
                                                            min_value=0.0, value=ss.cp_data.get('speed_tolerance_knots', 0.5), step=0.1)
    
    # Tab 4: Exclusion Periods
    with tabs[3]:
        st.header("Exclusion Periods")
        st.write("Add periods to exclude from performance calculations:")
        
        # Add new exclusion period
        st.subheader("Add New Exclusion Period")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_start_date = st.date_input("Start Date", datetime.datetime.now().date())
            new_start_time = st.time_input("Start Time", datetime.time(0, 0))
        
        with col2:
            new_end_date = st.date_input("End Date", datetime.datetime.now().date())
            new_end_time = st.time_input("End Time", datetime.time(0, 0))
        
        with col3:
            new_reason = st.text_input("Reason for Exclusion")
            if st.button("Add Exclusion Period"):
                new_period = {
                    'start_date': new_start_date.strftime("%Y-%m-%d"),
                    'start_time': new_start_time.strftime("%H:%M:%S"),
                    'end_date': new_end_date.strftime("%Y-%m-%d"),
                    'end_time': new_end_time.strftime("%H:%M:%S"),
                    'reason': new_reason
                }
                ss.exclusion_periods.append(new_period)
                st.success("Exclusion period added successfully!")
        
        # Display existing exclusion periods
        if ss.exclusion_periods:
            st.subheader("Existing Exclusion Periods")
            for i, period in enumerate(ss.exclusion_periods):
                expander = st.expander(f"Period {i+1}: {period['start_date']} to {period['end_date']}")
                with expander:
                    st.write(f"**Start:** {period['start_date']} {period['start_time']}")
                    st.write(f"**End:** {period['end_date']} {period['end_time']}")
                    st.write(f"**Reason:** {period['reason']}")
                    if st.button(f"Remove Period {i+1}"):
                        ss.exclusion_periods.pop(i)
                        st.experimental_rerun()
    
    # Tab 5: Weather Definitions
    with tabs[4]:
        st.header("Weather Definitions")
        st.write("Define weather parameters for good and bad weather days:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Wind Force (Beaufort Scale)")
            ss.weather_definitions['max_beaufort'] = st.selectbox(
                "Maximum Beaufort Scale for Good Weather", 
                list(range(13)),  # Beaufort scale goes from 0 to 12
                index=ss.weather_definitions.get('max_beaufort', 5) if 'max_beaufort' in ss.weather_definitions else 5
            )
            
            # Display Beaufort scale description
            st.info("Beaufort Scale Reference: The Beaufort scale is an empirical measure that relates wind speed to observed conditions at sea or on land.[16]")
        
        with col2:
            st.subheader("Significant Wave Height")
            wave_height_options = [round(i * 0.25, 2) for i in range(1, 21)]  # 0.25 to 5.00 in 0.25 increments
            ss.weather_definitions['max_wave_height'] = st.selectbox(
                "Maximum Wave Height (m) for Good Weather",
                wave_height_options,
                index=wave_height_options.index(ss.weather_definitions.get('max_wave_height', 2.0)) if 'max_wave_height' in ss.weather_definitions and ss.weather_definitions['max_wave_height'] in wave_height_options else 8  # Default to 2.0m
            )
        
        # Additional weather parameters
        st.subheader("Additional Weather Parameters")
        col1, col2 = st.columns(2)
        
        with col1:
            ss.weather_definitions['max_wind_speed'] = st.number_input(
                "Maximum Wind Speed (knots) for Good Weather",
                min_value=0.0,
                value=ss.weather_definitions.get('max_wind_speed', 20.0),
                step=0.5
            )
        
        with col2:
            ss.weather_definitions['max_swell_height'] = st.number_input(
                "Maximum Swell Height (m) for Good Weather",
                min_value=0.0,
                value=ss.weather_definitions.get('max_swell_height', 2.0),
                step=0.25
            )
        
        # Save weather definitions
        if st.button("Save Weather Definitions"):
            st.success("Weather definitions saved successfully!")
