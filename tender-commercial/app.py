import streamlit as st
import pdfkit
from jinja2 import Environment, FileSystemLoader
import datetime

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="Vendor Assessment Portal", layout="wide")

# Initialize Session State for saving data and tracking segments
if 'segment' not in st.session_state:
    st.session_state.segment = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# --- SEGMENT NAVIGATION ---
def save_and_forward():
    st.session_state.segment += 1

def go_back():
    st.session_state.segment -= 1

st.title("🏛️ Official Vendor Assessment & Registration")
st.write(f"**Segment {st.session_state.segment} of 4**")
st.progress(st.session_state.segment / 4)

# --- SEGMENT 1: GENERAL & SAVING ---
if st.session_state.segment == 1:
    st.subheader("General Identification")
    with st.container():
        st.session_state.form_data['comp_name'] = st.text_input("Full Name of Company", st.session_state.form_data.get('comp_name', ''))
        st.session_state.form_data['pan'] = st.text_input("Income Tax PAN", st.session_state.form_data.get('pan', ''))
        st.button("Save & Forward ➡️", on_click=save_and_forward)

# --- SEGMENT 2: TECHNICAL ---
elif st.session_state.segment == 2:
    st.subheader("Technical & Manufacturing")
    st.session_state.form_data['testing'] = st.radio("In-house Testing available?", ["Yes", "No"], 
        index=0 if st.session_state.form_data.get('testing') == "Yes" else 1)
    st.session_state.form_data['iso'] = st.selectbox("ISO 9001:2015 Certified?", ["Yes", "No"],
        index=0 if st.session_state.form_data.get('iso') == "Yes" else 1)
    
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=go_back)
    col2.button("Save & Forward ➡️", on_click=save_and_forward)

# --- SEGMENT 3: FINANCIAL ---
elif st.session_state.segment == 3:
    st.subheader("Financial Soundness")
    st.session_state.form_data['turnover'] = st.number_input("Last Year Turnover (in Cr)", value=st.session_state.form_data.get('turnover', 0.0))
    
    col1, col2 = st.columns(2)
    col1.button("⬅️ Back", on_click=go_back)
    col2.button("Save & Forward ➡️", on_click=save_and_forward)

# --- SEGMENT 4: REVIEW & PRINT REPORT ---
elif st.session_state.segment == 4:
    st.subheader("Complete Report Summary")
    st.info("Please review the details below. Once confirmed, click 'Generate Report' to print/download.")
    
    # Show summary table
    st.table(st.session_state.form_data)
    
    col1, col2 = st.columns(2)
    col1.button("⬅️ Edit Details", on_click=go_back)
    
    if col2.button("📝 Generate & Print Final Report"):
        # Compile Report Data
        st.session_state.form_data['date'] = datetime.date.today().strftime("%d/%m/%Y")
        
        # Logic for PDF Generation
        try:
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('full_report.html')
            html_out = template.render(d=st.session_state.form_data)
            
            # This generates the PDF for the user to download/print
            pdf = pdfkit.from_string(html_out, False)
            st.download_button(
                label="📥 Download & Print Assessment",
                data=pdf,
                file_name=f"Report_{st.session_state.form_data['comp_name']}.pdf",
                mime="application/pdf"
            )
            st.success("Report Generated Successfully! You can now print the downloaded PDF.")
        except Exception as e:
            st.error(f"Configuration Error: {e}")
