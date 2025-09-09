import streamlit as st
import requests
import json
import pandas as pd
from typing import List, Dict
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Drug Interaction Detection System",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 1rem 0;
    }
    .drug-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .interaction-high {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .interaction-medium {
        background: #fff8e1;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .interaction-low {
        background: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Backend API Configuration
API_BASE_URL = "http://localhost:5000/api"

class DrugSystemAPI:
    @staticmethod
    def extract_drugs(text: str) -> List[Dict]:
        """Extract drugs from medical text"""
        try:
            response = requests.post(f"{API_BASE_URL}/extract-drugs",
                                   json={"text": text},
                                   timeout=30)
            if response.status_code == 200:
                return response.json().get('drugs', [])
            else:
                st.error(f"API Error: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {e}")
            return []

    @staticmethod
    def check_interactions(drugs: List[Dict]) -> List[Dict]:
        """Check drug interactions"""
        try:
            response = requests.post(f"{API_BASE_URL}/check-interactions",
                                   json={"drugs": drugs},
                                   timeout=30)
            if response.status_code == 200:
                return response.json().get('interactions', [])
            else:
                st.error(f"API Error: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {e}")
            return []

    @staticmethod
    def get_comprehensive_analysis(drugs: List[Dict], patient: Dict) -> Dict:
        """Get comprehensive analysis"""
        try:
            response = requests.post(f"{API_BASE_URL}/comprehensive-analysis",
                                   json={"drugs": drugs, "patient": patient},
                                   timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code}")
                return {}
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: {e}")
            return {}

def initialize_session_state():
    """Initialize session state variables"""
    if 'drugs' not in st.session_state:
        st.session_state.drugs = []
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = {
            'age': 30,
            'weight': 70.0,
            'conditions': [],
            'allergies': []
        }
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}

def render_header():
    """Render the main header"""
    st.markdown('<div class="main-header">💊 Drug Interaction Detection System</div>',
                unsafe_allow_html=True)
    st.markdown("---")

    # System overview
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🔍 NLP Extraction", "Active", help="Extract drug info from text")
    with col2:
        st.metric("⚠️ Interaction Check", "Real-time", help="Detect drug interactions")
    with col3:
        st.metric("👶 Age Dosage", "Adaptive", help="Age-specific recommendations")
    with col4:
        st.metric("🔄 Alternatives", "Smart", help="Alternative drug suggestions")
    with col5:
        st.metric("🧠 IBM Granite", "Powered", help="AI-powered analysis")

def render_sidebar():
    """Render the sidebar with patient information"""
    st.sidebar.header("👤 Patient Information")

    # Patient demographics
    age = st.sidebar.number_input("Age", min_value=0, max_value=120,
                                  value=st.session_state.patient_data['age'])
    weight = st.sidebar.number_input("Weight (kg)", min_value=0.0, max_value=300.0,
                                     value=st.session_state.patient_data['weight'], step=0.1)

    # Medical conditions
    st.sidebar.subheader("Medical Conditions")
    conditions_input = st.sidebar.text_area("Enter conditions (one per line)",
                                            value='\n'.join(st.session_state.patient_data['conditions']))
    conditions = [c.strip() for c in conditions_input.split('\n') if c.strip()]

    # Allergies
    st.sidebar.subheader("Known Allergies")
    allergies_input = st.sidebar.text_area("Enter allergies (one per line)",
                                           value='\n'.join(st.session_state.patient_data['allergies']))
    allergies = [a.strip() for a in allergies_input.split('\n') if a.strip()]

    # Update session state
    st.session_state.patient_data = {
        'age': age,
        'weight': weight,
        'conditions': conditions,
        'allergies': allergies
    }

    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip**: Update patient information for personalized recommendations")

def render_nlp_extraction():
    """Render NLP drug extraction interface"""
    st.markdown('<div class="section-header">🔍 NLP-Based Drug Information Extraction</div>',
                unsafe_allow_html=True)

    # Text input for medical text
    sample_text = """Patient prescribed Aspirin 325mg twice daily and Warfarin 5mg once daily for atrial fibrillation. Also taking Metformin 500mg twice daily for diabetes."""

    medical_text = st.text_area("Enter Medical Text or Prescription",
                                placeholder="Enter medical text, prescription, or clinical notes...",
                                height=100,
                                value=sample_text if st.button("Load Sample Text") else "")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Extract Drug Information", type="primary"):
            if medical_text:
                with st.spinner("Processing text with IBM Granite..."):
                    extracted_drugs = DrugSystemAPI.extract_drugs(medical_text)

                if extracted_drugs:
                    st.success(f"✅ Extracted {len(extracted_drugs)} drug(s)")

                    # Add to current drugs list
                    for drug in extracted_drugs:
                        if drug not in st.session_state.drugs:
                            st.session_state.drugs.append(drug)
                else:
                    st.warning("No drugs could be extracted from the text")

    with col2:
        if st.button("🧹 Clear Extracted Drugs"):
            st.session_state.drugs = []
            st.success("Cleared all drugs")

def render_drug_input():
    """Render manual drug input interface"""
    st.markdown('<div class="section-header">💊 Manual Drug Entry</div>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        drug_name = st.text_input("Drug Name", placeholder="e.g., Aspirin")
    with col2:
        dosage = st.text_input("Dosage", placeholder="e.g., 325mg")
    with col3:
        frequency = st.text_input("Frequency", placeholder="e.g., twice daily")
    with col4:
        route = st.selectbox("Route", ["oral", "IV", "IM", "topical", "sublingual"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add Drug", type="primary"):
            if drug_name:
                new_drug = {
                    'name': drug_name,
                    'dosage': dosage,
                    'frequency': frequency,
                    'route': route
                }
                if new_drug not in st.session_state.drugs:
                    st.session_state.drugs.append(new_drug)
                    st.success(f"Added {drug_name} to the list.")
