elif ss.current_page == 'weather_analysis':
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    st.markdown("<h2 class='sub-header'>Weather Analysis</h2>", unsafe_allow_html=True)
    
    # Upload weather data file
    st.header("Upload Weather Data")
    uploaded_file = st.file_uploader("Upload XLS or CSV file with weather data", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Display the uploaded data
            st.subheader("Uploaded Weather Data")
            st.dataframe(df)
            
            # Check if required columns exist
            required_columns = ['date', 'beaufort_number', 'significant_wave_height', 'wind_speed']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"The following required columns are missing: {', '.join(missing_columns)}. Some analysis may not be available.")
            
            # Weather statistics
            st.subheader("Weather Statistics")
            col1, col2 = st.columns(2)
            
            with col1:
                if 'beaufort_number' in df.columns:
                    st.write("**Beaufort Scale Statistics:**")
                    beaufort_stats = df['beaufort_number'].describe().round(2)
                    st.write(f"Average: {beaufort_stats['mean']}")
                    st.write(f"Min: {beaufort_stats['min']}")
                    st.write(f"Max: {beaufort_stats['max']}")
                    
                    # Create a histogram of Beaufort numbers
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.histplot(df['beaufort_number'], bins=13, kde=True, ax=ax)
                    ax.set_title('Distribution of Beaufort Scale Numbers')
                    ax.set_xlabel('Beaufort Number')
                    ax.set_ylabel('Frequency')
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
            
            with col2:
                if 'significant_wave_height' in df.columns:
                    st.write("**Wave Height Statistics:**")
                    wave_stats = df['significant_wave_height'].describe().round(2)
                    st.write(f"Average: {wave_stats['mean']} meters")
                    st.write(f"Min: {wave_stats['min']} meters")
                    st.write(f"Max: {wave_stats['max']} meters")
                    
                    # Create a histogram of wave heights
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.histplot(df['significant_wave_height'], kde=True, ax=ax)
                    ax.set_title('Distribution of Significant Wave Heights')
                    ax.set_xlabel('Wave Height (meters)')
                    ax.set_ylabel('Frequency')
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
            
            # Good/Bad Weather Analysis
            if 'beaufort_number' in df.columns and 'significant_wave_height' in df.columns and 'weather_definitions' in ss:
                st.subheader("Good/Bad Weather Analysis")
                
                # Apply weather definitions
                df['weather_status'] = df.apply(
                    lambda row: 'GOOD WEATHER DAY' 
                    if (row['beaufort_number'] <= ss.weather_definitions.get('max_beaufort', 5) and 
                        row['significant_wave_height'] <= ss.weather_definitions.get('max_wave_height', 2.0))
                    else 'BAD WEATHER DAY', 
                    axis=1
                )
                
                # Count good vs. bad weather days
                weather_counts = df['weather_status'].value_counts()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Weather Day Counts:**")
                    st.write(f"Good Weather Days: {weather_counts.get('GOOD WEATHER DAY', 0)}")
                    st.write(f"Bad Weather Days: {weather_counts.get('BAD WEATHER DAY', 0)}")
                    
                    # Create a pie chart
                    fig, ax = plt.subplots(figsize=(8, 8))
                    ax.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#F44336'])
                    ax.axis('equal')
                    st.pyplot(fig)
                
                with col2:
                    if 'date' in df.columns:
                        # Convert date column to datetime if it's not already
                        if not pd.api.types.is_datetime64_any_dtype(df['date']):
                            df['date'] = pd.to_datetime(df['date'])
                        
                        # Create a time series of weather status
                        fig, ax = plt.subplots(figsize=(10, 6))
                        df['weather_numeric'] = df['weather_status'].apply(lambda x: 1 if x == 'GOOD WEATHER DAY' else 0)
                        plt.plot(df['date'], df['weather_numeric'], marker='o')
                        plt.yticks([0, 1], ['Bad', 'Good'])
                        plt.title('Weather Status Over Time')
                        plt.xlabel('Date')
                        plt.ylabel('Weather Status')
                        plt.grid(True, alpha=0.3)
                        plt.tight_layout()
                        st.pyplot(fig)
            
            # Store weather data in session state
            ss.weather_data = df
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        # Check if we have data from calculations
        if 'calculation_results' in ss and 'df' in ss.calculation_results:
            df = ss.calculation_results['df']
            
            # Display the data
            st.subheader("Data from Calculations")
            st.dataframe(df)
            
            # Weather analysis based on calculation data
            if 'beaufort_number' in df.columns and 'significant_wave_height' in df.columns:
                st.subheader("Weather Analysis from Calculation Data")
                
                # Beaufort Scale and Wave Height statistics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Beaufort Scale Statistics:**")
                    beaufort_stats = df['beaufort_number'].describe().round(2)
                    st.write(f"Average: {beaufort_stats['mean']}")
                    st.write(f"Min: {beaufort_stats['min']}")
                    st.write(f"Max: {beaufort_stats['max']}")
                
                with col2:
                    st.write("**Wave Height Statistics:**")
                    wave_stats = df['significant_wave_height'].describe().round(2)
                    st.write(f"Average: {wave_stats['mean']} meters")
                    st.write(f"Min: {wave_stats['min']} meters")
                    st.write(f"Max: {wave_stats['max']} meters")
                
                # Good/Bad Weather Day counts
                st.write("**Weather Day Counts:**")
                weather_counts = df['day_status'].value_counts()
                st.write(f"Good Weather Days: {weather_counts.get('GOOD WEATHER DAY', 0)}")
                st.write(f"Bad Weather Days: {weather_counts.get('BAD WEATHER DAY', 0)}")
            
            # Store weather data from calculations
            ss.weather_data = df
        else:
            st.info("Please upload a file with weather data or perform calculations first.")
