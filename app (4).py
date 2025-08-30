import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Heart Disease Analytics Dashboard", 
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #b11f4a 0%, #e63946 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        background: linear-gradient(135deg, #f7f7fa 0%, #ffffff 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .filter-section {
        background: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .insight-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    html, body, [class*="css"]  {
        font-size: 13px !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    .stSlider > div > div > div {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Set matplotlib style
plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif'})

# Load and cache data with better error handling
@st.cache_data
def load_data():
    """Load and preprocess the heart disease data with improved error handling"""
    possible_filenames = [
        "heart_2020_cleaned (1).csv",
        "heart_2020_cleaned.csv", 
        "heart_disease_data.csv",
        "data.csv"
    ]
    
    for filename in possible_filenames:
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                if not df.empty:
                    return df, filename
            except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
                continue
    
    return None, None

# Load data
data_result = load_data()
if data_result[0] is None:
    st.error("❌ CSV file not found. Please ensure one of these files exists in your directory:")
    st.write("- heart_2020_cleaned (1).csv")
    st.write("- heart_2020_cleaned.csv")
    st.write("- heart_disease_data.csv") 
    st.write("- data.csv")
    
    # File uploader as backup
    uploaded_file = st.file_uploader("Or upload a CSV file:", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        filename = "uploaded_file.csv"
    else:
        st.stop()
else:
    df, filename = data_result

# Validate required columns
required_columns = ['HeartDisease']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"❌ Missing required columns: {missing_columns}")
    st.write("Available columns:", list(df.columns))
    st.stop()

# Main header
st.markdown("""
<div class="main-header">
    <h1>❤️ Heart Disease Analytics Dashboard</h1>
    <p style="margin-bottom: 0;">Comprehensive insights into cardiovascular health patterns and risk factors</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown('<div class="filter-section"><h3>🔍 Interactive Filters</h3></div>', unsafe_allow_html=True)
    
    st.info(f"📁 Using: {filename}\n📊 Total Records: {len(df):,}")
    
    # Age filter
    if 'AgeCategory' in df.columns:
        age_options = ['All'] + sorted(df['AgeCategory'].unique().tolist())
        selected_age = st.selectbox('👥 Age Category', age_options)
    else:
        selected_age = 'All'
    
    # Gender filter
    if 'Sex' in df.columns:
        gender_options = ['All'] + df['Sex'].unique().tolist()
        selected_gender = st.selectbox('⚧ Gender', gender_options)
    else:
        selected_gender = 'All'
    
    # Race filter  
    if 'Race' in df.columns:
        race_options = ['All'] + sorted(df['Race'].unique().tolist())
        selected_race = st.selectbox('🌍 Race/Ethnicity', race_options)
    else:
        selected_race = 'All'
    
    # BMI range filter
    if 'BMI' in df.columns:
        bmi_min, bmi_max = float(df['BMI'].min()), float(df['BMI'].max())
        bmi_range = st.slider('⚖️ BMI Range', bmi_min, bmi_max, (bmi_min, bmi_max), step=0.1)
    else:
        bmi_range = (18.0, 40.0)
    
    # General Health filter
    if 'GenHealth' in df.columns:
        health_options = ['All'] + sorted(df['GenHealth'].unique().tolist())
        selected_health = st.selectbox('
