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

# Load and cache data
@st.cache_data
def load_data():
    csv_filename = "heart_2020_cleaned (1).csv"
    if not os.path.exists(csv_filename):
        st.error("❌ CSV file not found.")
        return None
    return pd.read_csv(csv_filename)

# Load data
df = load_data()
if df is None:
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
    
    # Age filter
    age_options = ['All'] + sorted(df['AgeCategory'].unique().tolist())
    selected_age = st.selectbox('👥 Age Category', age_options)
    
    # Gender filter
    gender_options = ['All'] + df['Sex'].unique().tolist()
    selected_gender = st.selectbox('⚧ Gender', gender_options)
    
    # Race filter  
    race_options = ['All'] + sorted(df['Race'].unique().tolist())
    selected_race = st.selectbox('🌍 Race/Ethnicity', race_options)
    
    # BMI range filter
    bmi_min, bmi_max = float(df['BMI'].min()), float(df['BMI'].max())
    bmi_range = st.slider('⚖️ BMI Range', bmi_min, bmi_max, (bmi_min, bmi_max), step=0.1)
    
    # General Health filter
    health_options = ['All'] + sorted(df['GenHealth'].unique().tolist())
    selected_health = st.selectbox('🏥 General Health', health_options)
    
    st.markdown("---")
    
    # Show filter impact
    st.markdown("### 📊 Filter Impact")
    original_size = len(df)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_age != 'All':
        filtered_df = filtered_df[filtered_df['AgeCategory'] == selected_age]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]
    if selected_race != 'All':
        filtered_df = filtered_df[filtered_df['Race'] == selected_race]
    if selected_health != 'All':
        filtered_df = filtered_df[filtered_df['GenHealth'] == selected_health]
    
    filtered_df = filtered_df[(filtered_df['BMI'] >= bmi_range[0]) & (filtered_df['BMI'] <= bmi_range[1])]
    
    filtered_size = len(filtered_df)
    st.metric("Records Showing", f"{filtered_size:,}", f"{filtered_size - original_size:,}")
    
    if filtered_size > 0:
        hd_rate = (filtered_df['HeartDisease'] == 'Yes').mean() * 100
        st.metric("Heart Disease Rate", f"{hd_rate:.1f}%")

# Calculate filtered datasets
hd_df = filtered_df[filtered_df["HeartDisease"] == "Yes"]
nhd_df = filtered_df[filtered_df["HeartDisease"] == "No"]

if len(filtered_df) == 0:
    st.error("No data matches the selected filters. Please adjust your filter criteria.")
    st.stop()

# Enhanced population summary
st.markdown(f"""
<div class="metric-container">
    <div style="display: flex; justify-content: center; align-items: center; gap: 3rem; flex-wrap: wrap;">
        <div style="text-align: center;">
            <h3 style="margin: 0; color: #0a58ca;">👥 Total Population</h3>
            <h2 style="margin: 0; color: #0a58ca;">{len(filtered_df):,}</h2>
        </div>
        <div style="text-align: center;">
            <h3 style="margin: 0; color: #c92c6d;">❤️ Heart Disease Cases</h3>
            <h2 style="margin: 0; color: #c92c6d;">{len(hd_df):,}</h2>
        </div>
        <div style="text-align: center;">
            <h3 style="margin: 0; color: #28a745;">💚 Healthy Cases</h3>
            <h2 style="margin: 0; color: #28a745;">{len(nhd_df):,}</h2>
        </div>
        <div style="text-align: center;">
            <h3 style="margin: 0; color: #fd7e14;">📈 HD Rate</h3>
            <h2 style="margin: 0; color: #fd7e14;">{(len(hd_df)/len(filtered_df)*100):.1f}%</h2>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced KPI row with better styling
if len(hd_df) > 0:
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #f7f7fa 0%, #e9ecef 100%); 
                border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem;
                display: flex; justify-content: center; gap: 2.5rem; flex-wrap: wrap;
                border: 1px solid #dee2e6;'>
        <span style="font-weight: 600; color: #495057;">❤️ <span style="color: #c92c6d;">{len(hd_df):,}</span></span>
        <span style="font-weight: 600; color: #495057;">⚖️ Avg BMI: <span style="color: #fd7e14;">{hd_df['BMI'].mean():.1f}</span></span>
        <span style="font-weight: 600; color: #495057;">🚬 Smoking: <span style="color: #dc3545;">{(hd_df['Smoking'] == 'Yes').mean() * 100:.1f}%</span></span>
        <span style="font-weight: 600; color: #495057;">🍺 Alcohol: <span style="color: #ffc107;">{(hd_df['AlcoholDrinking'] == 'Yes').mean() * 100:.1f}%</span></span>
        <span style="font-weight: 600; color: #495057;">🏃 Inactive: <span style="color: #6f42c1;">{(hd_df['PhysicalActivity'] == 'No').mean() * 100:.1f}%</span></span>
    </div>
    """, unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["📊 Main Dashboard", "🔍 Detailed Analysis", "💡 Insights & Recommendations"])

with tab1:
    # Your original visualizations with enhanced containers
    row1 = st.columns([1.8, 1.2, 0.7], gap="medium")

    # Chart 1: Risk Factors Bar (your original code with container)
    with row1[0]:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            risk_factors = [
                "Smoking", "AlcoholDrinking", "Diabetic", "PhysicalActivity",
                "Stroke", "DiffWalking", "Asthma", "KidneyDisease", "SkinCancer"
            ]
            hd_risk = []
            nhd_risk = []
            for col in risk_factors:
                if col == "PhysicalActivity":
                    hd_risk.append((hd_df[col] == "No").mean() * 100 if len(hd_df) > 0 else 0)
                    nhd_risk.append((nhd_df[col] == "No").mean() * 100 if len(nhd_df) > 0 else 0)
                else:
                    hd_risk.append((hd_df[col] == "Yes").mean() * 100 if len(hd_df) > 0 else 0)
                    nhd_risk.append((nhd_df[col] == "Yes").mean() * 100 if len(nhd_df) > 0 else 0)
            
            risk_df = pd.DataFrame({
                "Risk Factor": [
                    "Smoking", "Alcohol", "Diabetic", "No Activity",
                    "Stroke", "Diff Walk", "Asthma", "Kidney", "SkinCa"
                ],
                "Heart Disease": hd_risk,
                "No Heart Disease": nhd_risk
            })
            melt_df = risk_df.melt(id_vars="Risk Factor", value_vars=["Heart Disease", "No Heart Disease"],
                                var_name="HD", value_name="Prevalence (%)")
            fig, ax = plt.subplots(figsize=(5, 2.3))
            sns.barplot(
                data=melt_df,
                x="Prevalence (%)",
                y="Risk Factor",
                hue="HD",
                palette=["#e63946", "#457b9d"],
                orient="h"
            )
            ax.set_xlabel("%", fontsize=10)
            ax.set_ylabel("")
            ax.set_title("Risk Factors", fontsize=11, pad=8)
            ax.legend(fontsize=9, title='', loc='lower right')
            plt.tight_layout(pad=0.6)
            st.pyplot(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2: Comorbidities Heatmap (your original code with container)
    with row1[1]:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
            heat_df = filtered_df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
            fig, ax = plt.subplots(figsize=(2.4, 2.1))
            sns.heatmap(
                heat_df,
                annot=True,
                cmap="RdBu",
                fmt=".1f",
                ax=ax,
                cbar=False,
                annot_kws={"size": 10}
            )
            ax.set_title("Comorbidities (%)", fontsize=11, pad=8)
            ax.set_xlabel("")
            ax.set_ylabel("")
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            plt.tight_layout(pad=0.5)
            st.pyplot(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Chart 3: Gender Pie (your original code with container)
    with row1[2]:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            if len(hd_df) > 0:
                gender_counts = hd_df["Sex"].value_counts()
                fig_gender = px.pie(
                    names=gender_counts.index,
                    values=gender_counts.values,
                    hole=0.45,
                    height=170,
                    width=170,
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                fig_gender.update_traces(
                    textinfo='label+percent',
                    textposition='inside',
                    insidetextorientation='horizontal',
                    textfont_size=14
                )
                fig_gender.update_layout(
                    margin=dict(t=0, b=0, l=0, r=0),
                    showlegend=False,
                    font=dict(size=13),
                    title_text="By Gender",
                    title_font=dict(size=12),
                    title_x=0.5
                )
                st.plotly_chart(fig_gender, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Row: Age Group | General Health (your original code with containers)
    row2 = st.columns(2, gap="medium")

    with row2[0]:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            if len(hd_df) > 0:
                age_counts = hd_df["AgeCategory"].value_counts().sort_index()
                fig_age = px.bar(
                    x=age_counts.index,
                    y=age_counts.values,
                    color=age_counts.index,
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    height=200
                )
                fig_age.update_layout(
                    showlegend=False, font=dict(size=11),
                    margin=dict(t=12, b=0, l=0, r=0),
                    xaxis_title='Age Group', yaxis_title='Count',
                    title=dict(text="By Age Group", x=0.5, font=dict(size=11))
                )
                st.plotly_chart(fig_age, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            df_summary = (
                filtered_df.groupby(['HeartDisease', 'GenHealth'])
                .size()
                .reset_index(name='count')
            )
            if len(df_summary) > 0:
                df_summary['percent'] = df_summary.groupby('HeartDisease')['count'].transform(lambda x: x / x.sum() * 100)
                fig = px.bar(
                    df_summary, 
                    x="GenHealth", 
                    y="percent", 
                    color="HeartDisease",
                    barmode="group",
                    labels={"GenHealth": "General Health", "percent": "% of Group", "HeartDisease": "Heart Disease"},
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    height=200
                )
                fig.update_layout(
                    font=dict(size=11),
                    margin=dict(t=12, b=0, l=0, r=0),
                    title=dict(text="By General Health", x=0.5, font=dict(size=11))
                )
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("📈 Detailed Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Risk Factor Impact")
        if len(hd_df) > 0 and len(nhd_df) > 0:
            # Calculate risk ratios
            risk_analysis = []
            for factor in ["Smoking", "AlcoholDrinking", "Diabetic", "Stroke", "DiffWalking"]:
                hd_rate = (hd_df[factor] == 'Yes').mean() * 100
                nhd_rate = (nhd_df[factor] == 'Yes').mean() * 100
                ratio = hd_rate / nhd_rate if nhd_rate > 0 else float('inf')
                risk_analysis.append({
                    'Factor': factor,
                    'HD Rate': f"{hd_rate:.1f}%",
                    'No HD Rate': f"{nhd_rate:.1f}%",
                    'Risk Ratio': f"{ratio:.2f}x"
                })
            
            risk_df = pd.DataFrame(risk_analysis)
            st.dataframe(risk_df, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Demographics Breakdown")
        if len(filtered_df) > 0:
            # Demographics summary
            demo_summary = []
            for category in ['AgeCategory', 'Sex', 'Race']:
                if category in filtered_df.columns:
                    breakdown = filtered_df.groupby(category)['HeartDisease'].apply(
                        lambda x: f"{(x == 'Yes').mean() * 100:.1f}%"
                    ).to_dict()
                    demo_summary.append({'Category': category, 'Breakdown': str(breakdown)})
            
            for item in demo_summary:
                st.write(f"**{item['Category']}**: {item['Breakdown']}")

with tab3:
    st.subheader("💡 Key Insights & Recommendations")
    
    # Generate dynamic insights based on filtered data
    insights = []
    
    if len(hd_df) > 0:
        # Age insights
        age_rates = filtered_df.groupby('AgeCategory')['HeartDisease'].apply(lambda x: (x == 'Yes').mean() * 100)
        if len(age_rates) > 0:
            highest_risk_age = age_rates.idxmax()
            insights.append(f"🔍 **Age Analysis**: The {highest_risk_age} group shows the highest heart disease rate at {age_rates.max():.1f}%")
        
        # BMI insights  
        avg_bmi_hd = hd_df['BMI'].mean()
        avg_bmi_no_hd = nhd_df['BMI'].mean() if len(nhd_df) > 0 else 0
        bmi_diff = avg_bmi_hd - avg_bmi_no_hd
        insights.append(f"⚖️ **BMI Impact**: Heart disease patients have an average BMI {bmi_diff:.1f} points higher ({avg_bmi_hd:.1f} vs {avg_bmi_no_hd:.1f})")
        
        # Lifestyle insights
        smoking_hd = (hd_df['Smoking'] == 'Yes').mean() * 100
        smoking_no_hd = (nhd_df['Smoking'] == 'Yes').mean() * 100 if len(nhd_df) > 0 else 0
        insights.append(f"🚬 **Smoking Impact**: {smoking_hd:.1f}% of HD patients smoke vs {smoking_no_hd:.1f}% of healthy individuals")
        
        # Activity insights
        inactive_hd = (hd_df['PhysicalActivity'] == 'No').mean() * 100
        inactive_no_hd = (nhd_df['PhysicalActivity'] == 'No').mean() * 100 if len(nhd_df) > 0 else 0
        insights.append(f"🏃 **Activity Impact**: {inactive_hd:.1f}% of HD patients are physically inactive vs {inactive_no_hd:.1f}% of healthy individuals")
    
    # Display insights
    for insight in insights:
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
    
    # Health recommendations
    st.markdown("### 🎯 Personalized Health Recommendations")
    
    recommendations = [
        "🏃‍♂️ **Exercise Regularly**: Aim for 150+ minutes of moderate exercise per week",
        "🚭 **Avoid Smoking**: Smoking dramatically increases cardiovascular risk",
        "🍎 **Healthy Diet**: Focus on heart-healthy foods like fruits, vegetables, and whole grains", 
        "⚖️ **Maintain Healthy Weight**: Keep BMI in the normal range (18.5-24.9)",
        "🩺 **Regular Checkups**: Monitor blood pressure, cholesterol, and blood sugar",
        "😴 **Quality Sleep**: Get 7-9 hours of restful sleep nightly",
        "🧘‍♀️ **Manage Stress**: Practice stress-reduction techniques"
    ]
    
    for rec in recommendations:
        st.markdown(f"- {rec}")

# Enhanced footer with filter status
st.markdown("---")
active_filters = []
if selected_age != 'All':
    active_filters.append(f"Age: {selected_age}")
if selected_gender != 'All':
    active_filters.append(f"Gender: {selected_gender}")  
if selected_race != 'All':
    active_filters.append(f"Race: {selected_race}")
if selected_health != 'All':
    active_filters.append(f"Health: {selected_health}")

filter_text = " | ".join(active_filters) if active_filters else "No filters applied"

st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem; background: #f8f9fa; border-radius: 10px;'>
    <p><strong>❤️ Heart Disease Analytics Dashboard</strong> | Built with Streamlit</p>
    <p>📊 Showing {len(filtered_df):,} records | Active Filters: {filter_text}</p>
    <p>🎯 Heart Disease Rate in Current View: {(len(hd_df)/len(filtered_df)*100):.1f}%</p>
</div>
""", unsafe_allow_html=True)
