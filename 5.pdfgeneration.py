# Add PDF generation capability
import base64
from fpdf import FPDF
import io
import matplotlib.pyplot as plt

# Create a button for PDF generation in sidebar
st.sidebar.markdown("---")
if st.sidebar.button("Generate PDF Report"):
    try:
        # Create PDF instance
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add title page
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Get vessel and voyage details from session state
        vessel_name = ss.vessel_data.get('name', 'Unknown Vessel')
        voyage_no = ss.voyage_data.get('voyage_no', 'Unknown Voyage')
        from_port = ss.voyage_data.get('from_port', 'Unknown')
        to_port = ss.voyage_data.get('to_port', 'Unknown')
        
        # Title
        pdf.cell(0, 10, f"Charterparty Performance Report", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"{vessel_name}", ln=True, align='C')
        pdf.cell(0, 10, f"Voyage: {voyage_no}", ln=True, align='C')
        pdf.cell(0, 10, f"Route: {from_port} to {to_port}", ln=True, align='C')
        pdf.ln(10)
        
        # Date of report
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Report generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        
        # Section 1: Vessel Details
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "1. Vessel Details", ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        for key, value in ss.vessel_data.items():
            pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
        
        # Section 2: Voyage Details
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "2. Voyage Details", ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        for key, value in ss.voyage_data.items():
            pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
        
        # Section 3: CP Details
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "3. Charterparty Details", ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        for key, value in ss.cp_data.items():
            pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
        
        # Section 4: Weather Definitions
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "4. Weather Definitions", ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        for key, value in ss.weather_definitions.items():
            pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
        
        # Section 5: Calculation Results
        if 'calculation_results' in ss and 'summary' in ss.calculation_results:
            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, "5. Performance Calculations", ln=True)
            pdf.ln(5)
            
            # Convert summary to table
            pdf.set_font('Arial', '', 10)
            summary = ss.calculation_results['summary']
            
            # Draw table header
            pdf.set_fill_color(200, 220, 255)
            pdf.cell(100, 10, "Metric", 1, 0, 'C', 1)
            pdf.cell(80, 10, "Value", 1, 1, 'C', 1)
            
            # Draw table rows
            for index, row in summary.iterrows():
                pdf.cell(100, 10, str(row['Metric']), 1, 0)
                pdf.cell(80, 10, str(round(row['Value'], 2) if isinstance(row['Value'], (int, float)) else row['Value']), 1, 1)
                
        # Create download link for PDF
        html = create_download_link(pdf.output(dest="S").encode("latin-1"), f"{vessel_name}_Voyage_{voyage_no}_Report")
        st.sidebar.markdown(html, unsafe_allow_html=True)
        
        st.sidebar.success("PDF generated successfully!")
        
    except Exception as e:
        st.sidebar.error(f"Error generating PDF: {str(e)}")

# Helper function for PDF download link
def create_download_link(val, filename):
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download PDF Report</a>'

# Add page break CSS for printing from browser
st.markdown(
    """
    <style type="text/css" media="print">
    div.page-break {
        page-break-after: always;
        page-break-inside: avoid;
    }
    </style>
    <div class="page-break"></div>
    """,
    unsafe_allow_html=True,
)

