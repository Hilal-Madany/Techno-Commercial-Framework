import streamlit as st
import pdfkit
from jinja2 import Environment, FileSystemLoader
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="National Vendor Assessment Portal", layout="wide")

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #003366; color: white; }
    .section-box { padding: 20px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 20px; background: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ National Vendor Assessment System")
st.info("Authorized Standard Format for PSU, Railways, and Govt. Departments")

# --- SIDEBAR NAVIGATION ---
menu = ["1. General Info", "2. Technical & Manufacturing", "3. Quality System", "4. Financial Soundness", "5. Final Review & PDF"]
choice = st.sidebar.radio("Assessment Sections", menu)

# Initialize Session State to store data across tabs
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# --- SECTION 1: GENERAL INFO ---
if choice == "1. General Info":
    with st.container():
        st.header("General & Statutory Identification")
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.form_data['comp_name'] = st.text_input("Name of Supplier in Full")
            st.session_state.form_data['reg_office'] = st.text_area("Registered Office Address")
            st.session_state.form_data['pan'] = st.text_input("PAN / TAN Number")
        with col2:
            st.session_state.form_data['factory_addr'] = st.text_area("Factory / Works Address")
            st.session_state.form_data['gst'] = st.text_input("GST / TIN Number")
            st.session_state.form_data['msme'] = st.text_input("MSME Registration No.")

# --- SECTION 2: TECHNICAL ---
elif choice == "2. Technical & Manufacturing":
    st.header("Manufacturing & Process Capability")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.form_data['nature'] = st.multiselect("Nature of Business", ["Manufacturing", "EPC", "Dealer", "Service Provider"])
        st.session_state.form_data['area'] = st.number_input("Total Covered Area (Sq. m.)", min_value=0)
    with col2:
        st.session_state.form_data['testing_inhouse'] = st.radio("In-house Testing Facility available?", ["Yes", "No"])
        st.session_state.form_data['power_load'] = st.text_input("Electric Power Connected Load (kVA)")

# --- SECTION 3: QUALITY ---
elif choice == "3. Quality System":
    st.header("Quality Control & Compliance")
    q1, q2 = st.columns(2)
    with q1:
        st.session_state.form_data['iso_9001'] = st.selectbox("Is company ISO 9001 Certified?", ["Yes", "No"])
        st.session_state.form_data['iso_14001'] = st.selectbox("Is company ISO 14001 Certified?", ["Yes", "No"])
    with q2:
        st.session_state.form_data['q_manual'] = st.selectbox("Written Quality Manual available?", ["Yes", "No"])
        st.session_state.form_data['traceability'] = st.selectbox("System for Identification & Traceability?", ["Yes", "No"])

# --- SECTION 4: FINANCIAL ---
elif choice == "4. Financial Soundness":
    st.header("Financial Data (Last 3 Years)")
    f1, f2, f3 = st.columns(3)
    with f1: st.session_state.form_data['turnover_1'] = st.number_input("Turnover Year 1 (in Cr)", format="%.2f")
    with f2: st.session_state.form_data['turnover_2'] = st.number_input("Turnover Year 2 (in Cr)", format="%.2f")
    with f3: st.session_state.form_data['turnover_3'] = st.number_input("Turnover Year 3 (in Cr)", format="%.2f")

# --- SECTION 5: FINAL REVIEW & PDF ---
elif choice == "5. Final Review & PDF":
    st.header("Final Submission & Scoring")
    
    # Calculate Score
    score = 0
    if st.session_state.form_data.get('iso_9001') == "Yes": score += 25
    if st.session_state.form_data.get('testing_inhouse') == "Yes": score += 25
    if st.session_state.form_data.get('q_manual') == "Yes": score += 25
    if st.session_state.form_data.get('turnover_3', 0) > 0: score += 25
    
    st.metric("Total Compliance Score", f"{score}%")
    
    if st.button("Generate & Download Official PDF Report"):
        # Compile final data for jinja template
        final_data = st.session_state.form_data
        final_data['score'] = score
        final_data['date'] = datetime.date.today().strftime("%d/%m/%Y")
        
        # HTML Template Render (Assuming template exists in /templates)
        try:
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('full_report.html')
            html_content = template.render(d=final_data)
            
            # PDF Generation
            pdf = pdfkit.from_string(html_content, False)
            st.download_button("Download Final Report", data=pdf, file_name="Vendor_Assessment_Final.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error: Ensure 'templates/full_report.html' exists in GitHub. {e}")
