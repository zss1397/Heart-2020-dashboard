import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Heart Disease Analytics Dashboard",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    .insight-box {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .filter-header {
        background: #667eea;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Load and cache data with better error handling
@st.cache_data
def load_data():
    """Load and preprocess the heart disease data with error handling"""
    possible_filenames = [
        "heart_2020_cleaned (1).csv",
        "heart_2020_cleaned.csv",
        "heart_disease_data.csv",
        "data.csv"
    ]
    
    for filename in possible_filenames:
        try:
            df = pd.read_csv(filename)
            if not df.empty:
                st.success(f"✅ Successfully loaded data from: {filename}")
                return df, filename
        except (FileNotFoundError, pd.errors.EmptyDataError):
            continue
    
    # If no file found, show file uploader
    st.error("❌ No CSV file found. Please upload your heart disease dataset.")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df, "uploaded_file.csv"
    
    return None, None

# Load data
data_result = load_data()
if data_result[0] is None:
    st.stop()

df, filename = data_result

# Display data info
st.sidebar.info(f"📁 Using: {filename}\n📊 Records: {len(df):,}\n📋 Columns: {len(df.columns)}")

# Sidebar filters
st.sidebar.markdown('<div class="filter-header"><h3>🔍 Data Filters</h3></div>', unsafe_allow_html=True)

# Check required columns exist
required_columns = ['HeartDisease', 'AgeCategory', 'Sex', 'BMI']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.write("Available columns:", list(df.columns))
    st.stop()

# Filter options
age_categories = ['All'] + sorted(df['AgeCategory'].unique().tolist()) if 'AgeCategory' in df.columns else ['All']
selected_age = st.sidebar.selectbox('👥 Age Category', age_categories)

sex_options = ['All'] + df['Sex'].unique().tolist() if 'Sex' in df.columns else ['All']
selected_sex = st.sidebar.selectbox('⚧ Gender', sex_options)

if 'Race' in df.columns:
    race_options = ['All'] + sorted(df['Race'].unique().tolist())
    selected_race = st.sidebar.selectbox('🌍 Race/Ethnicity', race_options)
else:
    selected_race = 'All'

bmi_range = st.sidebar.slider(
    '⚖️ BMI Range',
    float(df['BMI'].min()),
    float(df['BMI'].max()),
    (float(df['BMI'].min()), float(df['BMI'].max()))
) if 'BMI' in df.columns else (18, 40)

# Apply filters
filtered_df = df.copy()
if selected_age != 'All':
    filtered_df = filtered_df[filtered_df['AgeCategory'] == selected_age]
if selected_sex != 'All':
    filtered_df = filtered_df[filtered_df['Sex'] == selected_sex]
if selected_race != 'All' and 'Race' in df.columns:
    filtered_df = filtered_df[filtered_df['Race'] == selected_race]

if 'BMI' in df.columns:
    filtered_df = filtered_df[(filtered_df['BMI'] >= bmi_range[0]) & (filtered_df['BMI'] <= bmi_range[1])]

# Calculate filtered data
hd_filtered = filtered_df[filtered_df["HeartDisease"] == "Yes"] if "HeartDisease" in filtered_df.columns else pd.DataFrame()
nhd_filtered = filtered_df[filtered_df["HeartDisease"] == "No"] if "HeartDisease" in filtered_df.columns else pd.DataFrame()
hd_rate = len(hd_filtered) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0

# Main header
st.markdown("""
<div class="main-header">
    <h1>❤️ Heart Disease Analytics Dashboard</h1>
    <p>Comprehensive insights into cardiovascular health risk factors and patterns</p>
</div>
""", unsafe_allow_html=True)

# Key metrics row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="📊 Total Records",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df):,}" if len(filtered_df) != len(df) else None
    )

with col2:
    st.metric(
        label="❤️ Heart Disease Cases",
        value=f"{len(hd_filtered):,}",
        delta=f"{hd_rate:.1f}%"
    )

with col3:
    avg_bmi = hd_filtered['BMI'].mean() if len(hd_filtered) > 0 and 'BMI' in hd_filtered.columns else 0
    st.metric(
        label="⚖️ Avg BMI (HD)",
        value=f"{avg_bmi:.1f}",
        delta=f"{avg_bmi - df[df['HeartDisease']=='Yes']['BMI'].mean():.1f}" if 'BMI' in df.columns and len(df[df['HeartDisease']=='Yes']) > 0 else None
    )

with col4:
    smoking_rate = (hd_filtered['Smoking'] == 'Yes').mean() * 100 if len(hd_filtered) > 0 and 'Smoking' in hd_filtered.columns else 0
    st.metric(
        label="🚬 Smoking Rate (HD)",
        value=f"{smoking_rate:.1f}%"
    )

with col5:
    activity_rate = (hd_filtered['PhysicalActivity'] == 'No').mean() * 100 if len(hd_filtered) > 0 and 'PhysicalActivity' in hd_filtered.columns else 0
    st.metric(
        label="🏃 Inactive Rate (HD)",
        value=f"{activity_rate:.1f}%"
    )

# Analysis tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Risk Analysis", "📈 Demographics", "🔗 Correlations", "🎯 Insights", "📋 Data Explorer"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Risk Factor Analysis")
        
        # Enhanced risk factors chart
        risk_factors = ["Smoking", "AlcoholDrinking", "Diabetic", "PhysicalActivity", 
                       "Stroke", "DiffWalking", "Asthma", "KidneyDisease", "SkinCancer"]
        
        # Filter to only existing columns
        available_risk_factors = [rf for rf in risk_factors if rf in filtered_df.columns]
        
        if available_risk_factors:
            risk_data = []
            for factor in available_risk_factors:
                if factor == "PhysicalActivity":
                    hd_rate_val = (hd_filtered[factor] == "No").mean() * 100 if len(hd_filtered) > 0 else 0
                    nhd_rate_val = (nhd_filtered[factor] == "No").mean() * 100 if len(nhd_filtered) > 0 else 0
                    factor_name = "No Activity"
                else:
                    hd_rate_val = (hd_filtered[factor] == "Yes").mean() * 100 if len(hd_filtered) > 0 else 0
                    nhd_rate_val = (nhd_filtered[factor] == "Yes").mean() * 100 if len(nhd_filtered) > 0 else 0
                    factor_name = factor
                    
                risk_data.append({
                    'Factor': factor_name,
                    'Heart Disease': hd_rate_val,
                    'No Heart Disease': nhd_rate_val,
                    'Risk Ratio': hd_rate_val / nhd_rate_val if nhd_rate_val > 0 else 0
                })
            
            risk_df = pd.DataFrame(risk_data)
            
            # Create interactive bar chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Heart Disease',
                x=risk_df['Factor'],
                y=risk_df['Heart Disease'],
                marker_color='#e63946',
                hovertemplate='<b>%{x}</b><br>Heart Disease: %{y:.1f}%<extra></extra>'
            ))
            fig.add_trace(go.Bar(
                name='No Heart Disease',
                x=risk_df['Factor'],
                y=risk_df['No Heart Disease'],
                marker_color='#457b9d',
                hovertemplate='<b>%{x}</b><br>No Heart Disease: %{y:.1f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title='Risk Factor Prevalence Comparison',
                xaxis_title='Risk Factors',
                yaxis_title='Prevalence (%)',
                barmode='group',
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No risk factor columns found in the dataset")
    
    with col2:
        st.subheader("Risk Ratios")
        
        if 'risk_df' in locals() and not risk_df.empty:
            # Risk ratio visualization
            risk_df_sorted = risk_df.sort_values('Risk Ratio', ascending=True)
            
            fig_ratio = go.Figure(go.Bar(
                x=risk_df_sorted['Risk Ratio'],
                y=risk_df_sorted['Factor'],
                orientation='h',
                marker_color='#ff6b6b',
                hovertemplate='<b>%{y}</b><br>Risk Ratio: %{x:.2f}<extra></extra>'
            ))
            
            fig_ratio.update_layout(
                title='Risk Ratios (HD vs No HD)',
                xaxis_title='Risk Ratio',
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            st.plotly_chart(fig_ratio, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Age Distribution")
        
        if 'AgeCategory' in filtered_df.columns:
            # Age distribution comparison
            age_data = []
            for age_cat in sorted(filtered_df['AgeCategory'].unique()):
                total_age = len(filtered_df[filtered_df['AgeCategory'] == age_cat])
                hd_age = len(filtered_df[(filtered_df['AgeCategory'] == age_cat) & (filtered_df['HeartDisease'] == 'Yes')])
                
                age_data.append({
                    'Age Category': age_cat,
                    'Total': total_age,
                    'Heart Disease': hd_age,
                    'HD Rate (%)': (hd_age / total_age * 100) if total_age > 0 else 0
                })
            
            age_df = pd.DataFrame(age_data)
            
            fig_age = go.Figure()
            fig_age.add_trace(go.Bar(
                name='Total Population',
                x=age_df['Age Category'],
                y=age_df['Total'],
                marker_color='lightblue',
                yaxis='y'
            ))
            fig_age.add_trace(go.Scatter(
                name='HD Rate (%)',
                x=age_df['Age Category'],
                y=age_df['HD Rate (%)'],
                mode='lines+markers',
                marker_color='red',
                line=dict(width=3),
                yaxis='y2'
            ))
            
            fig_age.update_layout(
                title='Heart Disease by Age Group',
                xaxis_title='Age Category',
                yaxis=dict(title='Population Count', side='left'),
                yaxis2=dict(title='Heart Disease Rate (%)', side='right', overlaying='y'),
                height=400
            )
            
            st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        st.subheader("Gender & Race Analysis")
        
        if 'Sex' in filtered_df.columns and 'Race' in filtered_df.columns:
            # Create demographic heatmap
            demo_data = filtered_df.groupby(['Sex', 'Race'])['HeartDisease'].apply(
                lambda x: (x == 'Yes').mean() * 100
            ).reset_index()
            demo_pivot = demo_data.pivot(index='Race', columns='Sex', values='HeartDisease')
            
            fig_demo = go.Figure(data=go.Heatmap(
                z=demo_pivot.values,
                x=demo_pivot.columns,
                y=demo_pivot.index,
                colorscale='Reds',
                hoverongaps=False,
                hovertemplate='<b>%{y}</b><br>%{x}<br>HD Rate: %{z:.1f}%<extra></extra>'
            ))
            
            fig_demo.update_layout(
                title='Heart Disease Rate by Demographics',
                height=400
            )
            
            st.plotly_chart(fig_demo, use_container_width=True)
        else:
            st.info("Gender and/or Race columns not available for analysis")

with tab3:
    st.subheader("Correlation Analysis")
    
    # Create correlation matrix for numerical and binary variables
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        # Add binary columns if they exist
        binary_cols = ['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'Diabetic', 
                       'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer']
        available_binary_cols = [col for col in binary_cols if col in filtered_df.columns]
        
        # Convert binary variables to numeric
        corr_df = filtered_df[numeric_cols].copy()
        for col in available_binary_cols:
            corr_df[col] = (filtered_df[col] == 'Yes').astype(int)
        
        if 'HeartDisease' in filtered_df.columns:
            corr_df['HeartDisease'] = (filtered_df['HeartDisease'] == 'Yes').astype(int)
        
        correlation_matrix = corr_df.corr()
        
        fig_corr = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu',
            zmid=0,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
        ))
        
        fig_corr.update_layout(
            title='Feature Correlation Matrix',
            height=600,
            width=800
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Top correlations with heart disease
        if 'HeartDisease' in correlation_matrix.columns:
            hd_correlations = correlation_matrix['HeartDisease'].drop('HeartDisease').sort_values(key=abs, ascending=False)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Strongest Positive Correlations")
                positive_corr = hd_correlations[hd_correlations > 0].head(5)
                for feature, corr in positive_corr.items():
                    st.write(f"**{feature}**: {corr:.3f}")
            
            with col2:
                st.subheader("Strongest Negative Correlations")
                negative_corr = hd_correlations[hd_correlations < 0].head(5)
                for feature, corr in negative_corr.items():
                    st.write(f"**{feature}**: {corr:.3f}")
    else:
        st.warning("No numeric columns found for correlation analysis")

with tab4:
    st.subheader("Key Insights & Recommendations")
    
    # Calculate insights based on filtered data
    insights = []
    
    if len(hd_filtered) > 0:
        # Age insight
        if 'AgeCategory' in filtered_df.columns:
            age_hd_rates = filtered_df.groupby('AgeCategory')['HeartDisease'].apply(lambda x: (x == 'Yes').mean() * 100)
            if not age_hd_rates.empty:
                highest_risk_age = age_hd_rates.idxmax()
                insights.append(f"🔍 **Age Risk**: {highest_risk_age} age group shows the highest heart disease rate at {age_hd_rates.max():.1f}%")
        
        # Gender insight
        if 'Sex' in filtered_df.columns:
            gender_rates = filtered_df.groupby('Sex')['HeartDisease'].apply(lambda x: (x == 'Yes').mean() * 100)
            if len(gender_rates) > 1:
                higher_risk_gender = gender_rates.idxmax()
                insights.append(f"⚧ **Gender Risk**: {higher_risk_gender}s have a higher heart disease rate ({gender_rates.max():.1f}% vs {gender_rates.min():.1f}%)")
        
        # BMI insight
        if 'BMI' in hd_filtered.columns and 'BMI' in nhd_filtered.columns:
            avg_bmi_hd = hd_filtered['BMI'].mean()
            avg_bmi_no_hd = nhd_filtered['BMI'].mean() if len(nhd_filtered) > 0 else 0
            if avg_bmi_hd > avg_bmi_no_hd:
                insights.append(f"⚖️ **BMI Impact**: People with heart disease have an average BMI of {avg_bmi_hd:.1f}, compared to {avg_bmi_no_hd:.1f} for those without")
        
        # Lifestyle factors
        if 'Smoking' in hd_filtered.columns and 'Smoking' in nhd_filtered.columns:
            smoking_hd = (hd_filtered['Smoking'] == 'Yes').mean() * 100
            smoking_no_hd = (nhd_filtered['Smoking'] == 'Yes').mean() * 100 if len(nhd_filtered) > 0 else 0
            if smoking_hd > smoking_no_hd:
                insights.append(f"🚬 **Smoking Risk**: {smoking_hd:.1f}% of heart disease patients smoke vs {smoking_no_hd:.1f}% of healthy individuals")
    
    for i, insight in enumerate(insights):
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("🎯 Health Recommendations")
    recommendations = [
        "🏃‍♂️ **Exercise Regularly**: Engage in at least 150 minutes of moderate aerobic activity weekly",
        "🚭 **Quit Smoking**: Smoking significantly increases heart disease risk",
        "🍎 **Healthy Diet**: Focus on fruits, vegetables, whole grains, and lean proteins",
        "⚖️ **Maintain Healthy Weight**: Keep BMI within the normal range (18.5-24.9)",
        "🩺 **Regular Checkups**: Monitor blood pressure, cholesterol, and blood sugar regularly",
        "😴 **Quality Sleep**: Aim for 7-9 hours of quality sleep per night",
        "🧘‍♀️ **Stress Management**: Practice stress reduction techniques like meditation or yoga"
    ]
    
    for rec in recommendations:
        st.markdown(f"- {rec}")

with tab5:
    st.subheader("Data Explorer")
    
    # Data overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(filtered_df))
    with col2:
        st.metric("Features", len(filtered_df.columns))
    with col3:
        st.metric("Heart Disease Rate", f"{hd_rate:.1f}%")
    
    # Show data sample
    st.subheader("Data Sample")
    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        height=400
    )
    
    # Data summary
    st.subheader("Statistical Summary")
    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>❤️ Heart Disease Analytics Dashboard | Built with Streamlit & Plotly</p>
        <p>📁 Data: {filename} | 📊 Records: {len(filtered_df):,}</p>
    </div>
    """,
    unsafe_allow_html=True
)
