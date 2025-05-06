elif ss.current_page == 'calculations':
    st.markdown("<h2 class='sub-header'>Performance Calculations</h2>", unsafe_allow_html=True)
    
    # Upload data file
    st.header("Upload Voyage Data")
    uploaded_file = st.file_uploader("Upload XLS or CSV file with voyage data", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Display the uploaded data
            st.subheader("Uploaded Data")
            st.dataframe(df)
            
            # Filter relevant rows based on the uploaded data
            if 'event_type' in df.columns:
                df = df[df['event_type'].isin(['NOON AT SEA', 'COSP', 'EOSP'])]
                
                # Process data
                # Ensure numeric types for calculations
                df['distance_travelled_actual'] = pd.to_numeric(df['distance_travelled_actual'], errors='coerce')
                df['steaming_time_hrs'] = pd.to_numeric(df['steaming_time_hrs'], errors='coerce')
                df['me_fuel_consumed'] = pd.to_numeric(df['me_fuel_consumed'], errors='coerce')
                
                # Apply weather definitions to categorize days
                if 'weather_definitions' in ss and 'beaufort_number' in df.columns and 'significant_wave_height' in df.columns:
                    df['day_status'] = df.apply(
                        lambda row: 'GOOD WEATHER DAY' 
                        if (row['beaufort_number'] <= ss.weather_definitions.get('max_beaufort', 5) and 
                            row['significant_wave_height'] <= ss.weather_definitions.get('max_wave_height', 2.0))
                        else 'BAD WEATHER DAY', 
                        axis=1
                    )
                
                # =========================
                # Total Metrics
                # =========================
                total_distance = df['distance_travelled_actual'].sum()
                total_time = df['steaming_time_hrs'].sum()
                total_fuel = df['me_fuel_consumed'].sum()
                voyage_avg_speed = total_distance / total_time if total_time else 0
                
                # =========================
                # Good and Bad Weather Segmentation
                # =========================
                good_days = df[df['day_status'] == 'GOOD WEATHER DAY']
                bad_days = df[df['day_status'] == 'BAD WEATHER DAY']
                
                # Good Weather Metrics
                good_distance = good_days['distance_travelled_actual'].sum()
                good_time = good_days['steaming_time_hrs'].sum()
                good_fuel = good_days['me_fuel_consumed'].sum()
                good_speed = good_distance / good_time if good_time else 0
                good_fo_hr = good_fuel / good_time if good_time else 0
                good_fo_day = good_fo_hr * 24
                
                # Bad Weather Metrics
                bad_distance = bad_days['distance_travelled_actual'].sum()
                bad_time = bad_days['steaming_time_hrs'].sum()
                bad_fuel = bad_days['me_fuel_consumed'].sum()
                bad_speed = bad_distance / bad_time if bad_time else 0
                
                # Get CP parameters from session state
                warranted_speed = ss.cp_data.get('warranted_speed', 13.0)
                warranted_consumption = ss.cp_data.get('warranted_consumption', 19.9)
                fuel_tolerance_percent = ss.cp_data.get('fuel_tolerance_percent', 5.0)
                speed_tolerance_knots = ss.cp_data.get('speed_tolerance_knots', 0.5)
                
                # =========================
                # Warranted Calculations
                # =========================
                fuel_tolerance_mt = warranted_consumption * (fuel_tolerance_percent / 100)
                warranted_plus_tol = warranted_consumption + fuel_tolerance_mt
                warranted_minus_tol = warranted_consumption - fuel_tolerance_mt
                
                # Entire Voyage Consumption Using Good Weather Consumption
                entire_voyage_good_weather_based = (total_distance / good_speed) * (good_fo_day / 24) if good_speed else 0
                
                # Maximum and Minimum Warranted Fuel
                adjusted_speed = good_speed
                if good_speed > warranted_speed + speed_tolerance_knots:
                    adjusted_speed = warranted_speed + speed_tolerance_knots
                elif good_speed < warranted_speed - speed_tolerance_knots:
                    adjusted_speed = warranted_speed - speed_tolerance_knots
                
                max_warranted_cons = (total_distance / adjusted_speed) * (warranted_plus_tol / 24)
                min_warranted_cons = (total_distance / adjusted_speed) * (warranted_minus_tol / 24)
                
                # Overconsumption and Saving
                fuel_overconsumption = (entire_voyage_good_weather_based - max_warranted_cons) if entire_voyage_good_weather_based > max_warranted_cons else 0
                fuel_saving = (min_warranted_cons - entire_voyage_good_weather_based) if entire_voyage_good_weather_based < min_warranted_cons else 0
                
                # Time Estimates
                time_at_good_spd = total_distance / adjusted_speed
                max_time = total_distance / (warranted_speed - speed_tolerance_knots)
                min_time = total_distance / (warranted_speed + speed_tolerance_knots)
                time_gained = (max_time - time_at_good_spd) if time_at_good_spd < max_time else 0
                time_lost = (time_at_good_spd - min_time) if time_at_good_spd > min_time else 0
                
                # Create summary dataframe
                summary = pd.DataFrame({
                    "Metric": [
                        "Total Distance (nm)",
                        "Total Steaming Time (hrs)",
                        "Voyage Avg Speed (knots)",
                        "Good Wx Distance (nm)",
                        "Good Wx Time (hrs)",
                        "Good Wx Speed (knots)",
                        "Good Wx FO Cons (MT)",
                        "Good Wx FO Rate (MT/hr)",
                        "Good Wx FO Rate (MT/day)",
                        "Bad Wx Distance (nm)",
                        "Bad Wx Time (hrs)",
                        "Bad Wx FO Cons (MT)",
                        "Bad Wx Speed (knots)",
                        "Total ME Fuel (MT)",
                        "Entire Voyage Cons (MT) via Good Wx Perf",
                        "Max Warranted FO (MT)",
                        "Min Warranted FO (MT)",
                        "Fuel Overconsumption (MT)",
                        "Fuel Saving (MT)",
                        "Time @ Good Wx Speed (hrs)",
                        "Max Time @ Warranted Spd (hrs)",
                        "Min Time @ Warranted Spd (hrs)",
                        "Time Gained (hrs)",
                        "Time Lost (hrs)"
                    ],
                    "Value": [
                        total_distance,
                        total_time,
                        round(voyage_avg_speed, 2),
                        good_distance,
                        good_time,
                        round(good_speed, 2),
                        round(good_fuel, 2),
                        round(good_fo_hr, 3),
                        round(good_fo_day, 3),
                        bad_distance,
                        bad_time,
                        round(bad_fuel, 2),
                        round(bad_speed, 2),
                        round(total_fuel, 2),
                        round(entire_voyage_good_weather_based, 2),
                        round(max_warranted_cons, 2),
                        round(min_warranted_cons, 2),
                        round(fuel_overconsumption, 2),
                        round(fuel_saving, 2),
                        round(time_at_good_spd, 2),
                        round(max_time, 2),
                        round(min_time, 2),
                        round(time_gained, 2),
                        round(time_lost, 2)
                    ]
                })
                
                # Store results in session state
                ss.calculation_results = {
                    'df': df,
                    'summary': summary,
                    'total_distance': total_distance,
                    'total_time': total_time,
                    'voyage_avg_speed': voyage_avg_speed,
                    'good_distance': good_distance,
                    'good_time': good_time,
                    'good_speed': good_speed,
                    'good_fuel': good_fuel,
                    'good_fo_hr': good_fo_hr,
                    'good_fo_day': good_fo_day,
                    'bad_distance': bad_distance,
                    'bad_time': bad_time,
                    'bad_fuel': bad_fuel,
                    'bad_speed': bad_speed,
                    'total_fuel': total_fuel,
                    'entire_voyage_good_weather_based': entire_voyage_good_weather_based,
                    'max_warranted_cons': max_warranted_cons,
                    'min_warranted_cons': min_warranted_cons,
                    'fuel_overconsumption': fuel_overconsumption,
                    'fuel_saving': fuel_saving,
                    'time_at_good_spd': time_at_good_spd,
                    'max_time': max_time,
                    'min_time': min_time,
                    'time_gained': time_gained,
                    'time_lost': time_lost
                }
                
                # Display results
                st.subheader("Calculation Results")
                st.dataframe(summary.set_index("Metric"))
                
                # Export options
                import io
                buffer = io.BytesIO()
                summary.to_excel(buffer, index=False, engine='xlsxwriter')
                buffer.seek(0)
                st.download_button(
                    label="Download Results as Excel",
                    data=buffer,
                    file_name="voyage_performance_report.xlsx",
                    mime="application/vnd.ms-excel"
                )
                
            else:
                st.error("The uploaded file does not contain the required columns. Please check your data format.")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        st.info("Please upload a file to perform calculations.")

