elif ss.current_page == 'graphs':
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    st.markdown("<h2 class='sub-header'>Graphs and Analytics</h2>", unsafe_allow_html=True)
    
    # Check if we have data to work with
    if ('calculation_results' in ss and 'df' in ss.calculation_results) or ('weather_data' in ss):
        
        # Get data - prefer calculation data if available
        if 'calculation_results' in ss and 'df' in ss.calculation_results:
            df = ss.calculation_results['df']
        else:
            df = ss.weather_data
        
        # Speed vs. Wind / Wave Analysis
        st.header("Speed vs. Environmental Conditions")
        
        # Check required columns
        if ('speed' in df.columns or 'actual_speed' in df.columns) and ('wind_speed' in df.columns or 'beaufort_number' in df.columns or 'significant_wave_height' in df.columns):
            
            # Prepare speed column
            speed_col = 'speed' if 'speed' in df.columns else 'actual_speed'
            
            # Speed vs. Wind (Beaufort)
            if 'beaufort_number' in df.columns:
                st.subheader("Speed vs. Beaufort Scale")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='beaufort_number', y=speed_col, data=df, ax=ax)
                
                # Add regression line
                sns.regplot(x='beaufort_number', y=speed_col, data=df, scatter=False, ax=ax, color='red')
                
                ax.set_title('Vessel Speed vs. Beaufort Scale')
                ax.set_xlabel('Beaufort Number')
                ax.set_ylabel('Speed (knots)')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                
                # Correlation coefficient
                corr = df[[speed_col, 'beaufort_number']].corr().iloc[0, 1]
                st.write(f"Correlation coefficient: {corr:.4f}")
                
                if corr < -0.5:
                    st.write("Strong negative correlation: Speed significantly decreases as Beaufort number increases.")
                elif corr < -0.3:
                    st.write("Moderate negative correlation: Speed tends to decrease as Beaufort number increases.")
                elif corr < -0.1:
                    st.write("Weak negative correlation: Speed slightly decreases as Beaufort number increases.")
                elif corr < 0.1:
                    st.write("No significant correlation between speed and Beaufort number.")
                else:
                    st.write("Unexpected positive correlation: Speed increases as Beaufort number increases, which is unusual.")
            
            # Speed vs. Wave Height
            if 'significant_wave_height' in df.columns:
                st.subheader("Speed vs. Significant Wave Height")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='significant_wave_height', y=speed_col, data=df, ax=ax)
                
                # Add regression line
                sns.regplot(x='significant_wave_height', y=speed_col, data=df, scatter=False, ax=ax, color='red')
                
                ax.set_title('Vessel Speed vs. Significant Wave Height')
                ax.set_xlabel('Wave Height (meters)')
                ax.set_ylabel('Speed (knots)')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                
                # Correlation coefficient
                corr = df[[speed_col, 'significant_wave_height']].corr().iloc[0, 1]
                st.write(f"Correlation coefficient: {corr:.4f}")
        else:
            st.warning("Required columns for speed vs. environmental conditions analysis are missing.")
        
        # CP Speed vs Actual Speed
        st.header("CP Speed vs. Actual Speed")
        if 'cp_data' in ss and ('speed' in df.columns or 'actual_speed' in df.columns):
            speed_col = 'speed' if 'speed' in df.columns else 'actual_speed'
            warranted_speed = ss.cp_data.get('warranted_speed', 13.0)
            
            st.subheader("Speed Performance Analysis")
            
            # Create a figure for speed comparison
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Add actual speed from data
            if 'date' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['date']):
                    df['date'] = pd.to_datetime(df['date'])
                
                # Plot actual speed
                plt.plot(df['date'], df[speed_col], marker='o', label='Actual Speed')
                
                # Add horizontal line for warranted speed
                plt.axhline(y=warranted_speed, color='r', linestyle='-', label=f'Warranted Speed ({warranted_speed} knots)')
                
                # Add warranted speed tolerance band
                speed_tolerance = ss.cp_data.get('speed_tolerance_knots', 0.5)
                plt.axhline(y=warranted_speed + speed_tolerance, color='r', linestyle='--', alpha=0.5)
                plt.axhline(y=warranted_speed - speed_tolerance, color='r', linestyle='--', alpha=0.5)
                plt.fill_between(df['date'], warranted_speed - speed_tolerance, warranted_speed + speed_tolerance, 
                                color='r', alpha=0.1, label=f'Speed Tolerance (±{speed_tolerance} knots)')
                
                plt.title('Actual Speed vs. Warranted Speed')
                plt.xlabel('Date')
                plt.ylabel('Speed (knots)')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
            
            # Speed statistics
            st.write("**Speed Statistics:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                speed_stats = df[speed_col].describe().round(2)
                st.write(f"Average Speed: {speed_stats['mean']} knots")
                st.write(f"Min Speed: {speed_stats['min']} knots")
                st.write(f"Max Speed: {speed_stats['max']} knots")
            
            with col2:
                # Calculate percentage of time at or above warranted speed
                pct_at_or_above = (df[df[speed_col] >= warranted_speed].shape[0] / df.shape[0] * 100).round(2)
                st.write(f"% Time at or above warranted speed: {pct_at_or_above}%")
                
                # Within tolerance
                pct_within_tol = (df[
                    (df[speed_col] >= warranted_speed - ss.cp_data.get('speed_tolerance_knots', 0.5)) & 
                    (df[speed_col] <= warranted_speed + ss.cp_data.get('speed_tolerance_knots', 0.5))
                ].shape[0] / df.shape[0] * 100).round(2)
                st.write(f"% Time within speed tolerance: {pct_within_tol}%")
        else:
            st.warning("Required data for CP Speed vs. Actual Speed analysis is missing.")
        
        # Performance Dashboard
        if 'calculation_results' in ss and 'summary' in ss.calculation_results:
            st.header("Performance Dashboard")
            
            summary = ss.calculation_results['summary']
            
            # Extract values for dashboard
            fuel_overconsumption = float(summary.loc[summary['Metric'] == 'Fuel Overconsumption (MT)', 'Value'])
            fuel_saving = float(summary.loc[summary['Metric'] == 'Fuel Saving (MT)', 'Value'])
            time_gained = float(summary.loc[summary['Metric'] == 'Time Gained (hrs)', 'Value'])
            time_lost = float(summary.loc[summary['Metric'] == 'Time Lost (hrs)', 'Value'])
            good_wx_speed = float(summary.loc[summary['Metric'] == 'Good Wx Speed (knots)', 'Value'])
            
            # Create dashboard indicators
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("⏱️ Time Performance")
                if time_gained > 0:
                    st.success(f"Time Gained: {time_gained:.2f} hours")
                    st.write(f"The vessel gained approximately {time_gained/24:.2f} days compared to the minimum time allowed under the charterparty.")
                elif time_lost > 0:
                    st.error(f"Time Lost: {time_lost:.2f} hours")
                    st.write(f"The vessel lost approximately {time_lost/24:.2f} days compared to the maximum time allowed under the charterparty.")
                else:
                    st.info("The vessel's time performance is within the allowed range.")
            
            with col2:
                st.subheader("⛽ Fuel Performance")
                if fuel_saving > 0:
                    st.success(f"Fuel Saved: {fuel_saving:.2f} MT")
                    # Assuming average bunker cost of $500 per MT
                    bunker_cost = 500
                    st.write(f"Estimated savings: ${(fuel_saving * bunker_cost):,.2f}")
                elif fuel_overconsumption > 0:
                    st.error(f"Fuel Overconsumed: {fuel_overconsumption:.2f} MT")
                    # Assuming average bunker cost of $500 per MT
                    bunker_cost = 500
                    st.write(f"Estimated additional cost: ${(fuel_overconsumption * bunker_cost):,.2f}")
                else:
                    st.info("The vessel's fuel consumption is within the allowed range.")
            
            with col3:
                st.subheader("🚢 Speed Performance")
                warranted_speed = ss.cp_data.get('warranted_speed', 13.0)
                speed_diff = good_wx_speed - warranted_speed
                
                if abs(speed_diff) <= ss.cp_data.get('speed_tolerance_knots', 0.5):
                    st.info(f"Good Weather Speed: {good_wx_speed:.2f} knots\n\nWithin tolerance of warranted speed ({warranted_speed} knots)")
                elif speed_diff > 0:
                    st.success(f"Good Weather Speed: {good_wx_speed:.2f} knots\n\n{speed_diff:.2f} knots faster than warranted ({warranted_speed} knots)")
                else:
                    st.error(f"Good Weather Speed: {good_wx_speed:.2f} knots\n\n{abs(speed_diff):.2f} knots slower than warranted ({warranted_speed} knots)")
    else:
        st.info("No data available for analysis. Please complete the calculations first or upload weather data.")
