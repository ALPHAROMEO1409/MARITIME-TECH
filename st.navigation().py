import streamlit as st

pages = [
    st.Page("pages/vessel_input.py", title="Vessel Input", icon="🚢"),
    st.Page("pages/calculations.py", title="Calculations", icon="🧮"),
    st.Page("pages/weather_analysis.py", title="Weather Analysis", icon="🌊"),
    st.Page("pages/graphs.py", title="Graphs & Analytics", icon="📊"),
]

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
