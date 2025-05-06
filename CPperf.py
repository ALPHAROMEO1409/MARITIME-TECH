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
