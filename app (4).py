import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    .tab-content {
        padding: 1rem 0;
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
    .correlation-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
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
    <p style="margin-bottom: 0;">Ultimate insights combining original visualizations with advanced analytics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown('<div class="filter-section"><h3>🔍 Interactive Filters</h3></div>', unsafe_allow_html=True)
    
    # Remove smoking filter, keep only demographic filters
    st.info("ℹ️ Filters apply to the entire population, then heart disease analysis is performed on the filtered subset")
    
    # Age filter
    age_options = ['All'] + sorted(df['AgeCategory'].unique().tolist())
    selected_age = st.selectbox('👥 Age Category', age_options)
    
    # Gender filter
    gender_options = ['All'] + df['Sex'].unique().tolist()
    selected_gender = st.selectbox('⚧ Gender', gender_options)
    
    # General Health filter
    health_options = ['All'] + sorted(df['GenHealth'].unique().tolist())
    selected_health = st.selectbox('🏥 General Health', health_options)
    
    st.markdown("---")
    
    # Show filter impact
    st.markdown("### 📊 Filter Impact")
    original_size = len(df)
    
    # Apply filters to entire population (demographic only)
    filtered_df = df.copy()
    if selected_age != 'All':
        filtered_df = filtered_df[filtered_df['AgeCategory'] == selected_age]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]
    if selected_health != 'All':
        filtered_df = filtered_df[filtered_df['GenHealth'] == selected_health]
    
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

# Enhanced KPI row - ALWAYS shows whole population heart disease stats
all_hd_df = df[df["HeartDisease"] == "Yes"]  # Unfiltered heart disease data
if len(all_hd_df) > 0:
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #f7f7fa 0%, #e9ecef 100%); 
                border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem;
                display: flex; justify-content: center; gap: 2.5rem; flex-wrap: wrap;
                border: 1px solid #dee2e6;'>
        <span style="font-weight: 600; color: #495057;">❤️ <span style="color: #c92c6d;">{len(all_hd_df):,}</span></span>
        <span style="font-weight: 600; color: #495057;">⚖️ Avg BMI: <span style="color: #fd7e14;">{all_hd_df['BMI'].mean():.1f}</span></span>
        <span style="font-weight: 600; color: #495057;">🚬 Smoking: <span style="color: #dc3545;">{(all_hd_df['Smoking'] == 'Yes').mean() * 100:.1f}%</span></span>
        <span style="font-weight: 600; color: #495057;">🍺 Alcohol: <span style="color: #ffc107;">{(all_hd_df['AlcoholDrinking'] == 'Yes').mean() * 100:.1f}%</span></span>
        <span style="font-weight: 600; color: #495057;">🏃 Inactive: <span style="color: #6f42c1;">{(all_hd_df['PhysicalActivity'] == 'No').mean() * 100:.1f}%</span></span>
    </div>
    """)

# Create comprehensive tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Original Dashboard", "📈 Advanced Analytics", "🔗 Correlations", "👥 Demographics", "💡 Insights & Data"])

# TAB 1: Original Dashboard (Your beloved charts!)
with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Your original visualizations with enhanced containers
    row1 = st.columns([1.8, 1.2, 0.7], gap="medium")

    # Chart 1: Risk Factors Bar (your original code enhanced)
    with row1[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Risk Factors Analysis")
        
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
        fig, ax = plt.subplots(figsize=(5, 2.5))
        sns.barplot(
            data=melt_df,
            x="Prevalence (%)",
            y="Risk Factor",
            hue="HD",
            palette=["#e63946", "#457b9d"],
            orient="h"
        )
        ax.set_xlabel("Prevalence (%)", fontsize=11)
        ax.set_ylabel("")
        ax.set_title("Risk Factors Comparison", fontsize=12, pad=10)
        ax.legend(fontsize=10, title='', loc='lower right')
        plt.tight_layout(pad=0.8)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2: Comorbidities Heatmap (enhanced)
    with row1[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🔥 Comorbidities Heatmap")
        
        condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
        heat_df = filtered_df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
        fig, ax = plt.subplots(figsize=(2.6, 2.3))
        sns.heatmap(
            heat_df,
            annot=True,
            cmap="Reds",  # Light to dark red gradient
            fmt=".1f",
            ax=ax,
            cbar=True,
            annot_kws={"size": 11, "weight": "bold"},
            cbar_kws={"shrink": 0.8}
        )
        ax.set_title("Comorbidities (%)", fontsize=12, pad=10)
        ax.set_xlabel("")
        ax.set_ylabel("")
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10, rotation=0)
        plt.tight_layout(pad=0.7)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart 3: Gender Pie (enhanced)
    with row1[2]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### ⚧ Gender Distribution")
        
        if len(hd_df) > 0:
            gender_counts = hd_df["Sex"].value_counts()
            fig_gender = px.pie(
                names=gender_counts.index,
                values=gender_counts.values,
                hole=0.5,
                height=200,
                color_discrete_sequence=['#c92c6d', '#667eea']
            )
            fig_gender.update_traces(
                textinfo='label+percent',
                textposition='inside',
                textfont_size=12,
                textfont_color='white'
            )
            fig_gender.update_layout(
                margin=dict(t=20, b=0, l=0, r=0),
                showlegend=False,
                font=dict(size=12),
                title=dict(text="Heart Disease by Gender", x=0.5, font=dict(size=11))
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Row: Enhanced versions
    row2 = st.columns(2, gap="medium")

    with row2[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 👥 Age Group Distribution")
        
        if len(hd_df) > 0:
            age_counts = hd_df["AgeCategory"].value_counts().sort_index()
            fig_age = px.bar(
                x=age_counts.index,
                y=age_counts.values,
                color=age_counts.values,
                color_continuous_scale="Viridis",
                height=250,
                title="Heart Disease Cases by Age Group"
            )
            fig_age.update_layout(
                showlegend=False, 
                font=dict(size=11),
                margin=dict(t=30, b=0, l=0, r=0),
                xaxis_title='Age Group', 
                yaxis_title='Count',
                title_x=0.5
            )
            fig_age.update_traces(
                hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>'
            )
            st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🏥 General Health Status")
        
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
                color_discrete_sequence=['#28a745', '#c92c6d'],
                height=250,
                title="Health Status Distribution"
            )
            fig.update_layout(
                font=dict(size=11),
                margin=dict(t=30, b=0, l=0, r=0),
                title_x=0.5
            )
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: Advanced Analytics (Interactive Plotly charts)
with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Interactive Risk Factor Analysis")
        
        # Enhanced interactive risk factors chart
        risk_factors = ["Smoking", "AlcoholDrinking", "Diabetic", "PhysicalActivity", 
                       "Stroke", "DiffWalking", "Asthma", "KidneyDisease", "SkinCancer"]
        
        risk_data = []
        for factor in risk_factors:
            if factor == "PhysicalActivity":
                hd_rate_val = (hd_df[factor] == "No").mean() * 100 if len(hd_df) > 0 else 0
                nhd_rate_val = (nhd_df[factor] == "No").mean() * 100 if len(nhd_df) > 0 else 0
                factor_name = "No Activity"
            else:
                hd_rate_val = (hd_df[factor] == "Yes").mean() * 100 if len(hd_df) > 0 else 0
                nhd_rate_val = (nhd_df[factor] == "Yes").mean() * 100 if len(nhd_df) > 0 else 0
                factor_name = factor
                
            risk_data.append({
                'Factor': factor_name,
                'Heart Disease': hd_rate_val,
                'No Heart Disease': nhd_rate_val,
                'Risk Ratio': hd_rate_val / nhd_rate_val if nhd_rate_val > 0 else 0
            })
        
        risk_df_adv = pd.DataFrame(risk_data)
        
        # Create interactive bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Heart Disease',
            x=risk_df_adv['Factor'],
            y=risk_df_adv['Heart Disease'],
            marker_color='#e63946',
            hovertemplate='<b>%{x}</b><br>Heart Disease: %{y:.1f}%<br>Risk Factor Prevalence<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            name='No Heart Disease',
            x=risk_df_adv['Factor'],
            y=risk_df_adv['No Heart Disease'],
            marker_color='#457b9d',
            hovertemplate='<b>%{x}</b><br>No Heart Disease: %{y:.1f}%<br>Risk Factor Prevalence<extra></extra>'
        ))
        
        fig.update_layout(
            title='Interactive Risk Factor Prevalence Comparison',
            xaxis_title='Risk Factors',
            yaxis_title='Prevalence (%)',
            barmode='group',
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Risk Ratios")
        
        # Risk ratio visualization
        risk_df_sorted = risk_df_adv.sort_values('Risk Ratio', ascending=True)
        
        fig_ratio = go.Figure(go.Bar(
            x=risk_df_sorted['Risk Ratio'],
            y=risk_df_sorted['Factor'],
            orientation='h',
            marker_color='#ff6b6b',
            hovertemplate='<b>%{y}</b><br>Risk Ratio: %{x:.2f}x<br>Higher risk for HD patients<extra></extra>'
        ))
        
        fig_ratio.update_layout(
            title='Risk Ratios (HD vs No HD)',
            xaxis_title='Risk Ratio',
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_ratio, use_container_width=True)
    
    # Advanced Age Analysis
    st.subheader("📈 Advanced Age & Health Analysis")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Age distribution with HD rates
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
        
        age_df_adv = pd.DataFrame(age_data)
        
        fig_age_adv = go.Figure()
        fig_age_adv.add_trace(go.Bar(
            name='Total Population',
            x=age_df_adv['Age Category'],
            y=age_df_adv['Total'],
            marker_color='lightblue',
            yaxis='y',
            hovertemplate='<b>%{x}</b><br>Total Population: %{y}<extra></extra>'
        ))
        fig_age_adv.add_trace(go.Scatter(
            name='HD Rate (%)',
            x=age_df_adv['Age Category'],
            y=age_df_adv['HD Rate (%)'],
            mode='lines+markers',
            marker=dict(color='red', size=8),
            line=dict(width=3, color='red'),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>HD Rate: %{y:.1f}%<extra></extra>'
        ))
        
        fig_age_adv.update_layout(
            title='Population & Heart Disease Rate by Age',
            xaxis_title='Age Category',
            yaxis=dict(title='Population Count', side='left'),
            yaxis2=dict(title='Heart Disease Rate (%)', side='right', overlaying='y'),
            height=400
        )
        
        st.plotly_chart(fig_age_adv, use_container_width=True)
    
    with col4:
        # BMI vs General Health Analysis  
        st.markdown("#### ⚖️ BMI vs General Health")
        
        # Create BMI categories
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['BMI_Category'] = pd.cut(
            filtered_df_copy['BMI'], 
            bins=[0, 18.5, 25, 30, 100], 
            labels=['Underweight', 'Normal', 'Overweight', 'Obese']
        )
        
        # Create BMI vs General Health heatmap
        bmi_health_data = filtered_df_copy.groupby(['BMI_Category', 'GenHealth'])['HeartDisease'].apply(
            lambda x: (x == 'Yes').mean() * 100
        ).reset_index()
        bmi_health_pivot = bmi_health_data.pivot(index='BMI_Category', columns='GenHealth', values='HeartDisease')
        
        fig_bmi_health = go.Figure(data=go.Heatmap(
            z=bmi_health_pivot.values,
            x=bmi_health_pivot.columns,
            y=bmi_health_pivot.index,
            colorscale='Oranges',  # Light to dark orange gradient
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>%{x} Health<br>HD Rate: %{z:.1f}%<extra></extra>'
        ))
        
        fig_bmi_health.update_layout(
            title='Heart Disease Rate: BMI vs General Health',
            height=400,
            xaxis_title='General Health Status',
            yaxis_title='BMI Category'
        )
        
        st.plotly_chart(fig_bmi_health, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: Correlations
with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("🔗 Feature Correlation Analysis")
    
    # Create correlation matrix
    corr_cols = ['BMI', 'MentalHealth', 'PhysicalHealth', 'SleepTime']
    binary_cols = ['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'Diabetic', 
                   'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer']
    
    # Convert binary variables to numeric
    corr_df = filtered_df[corr_cols].copy()
    for col in binary_cols:
        corr_df[col] = (filtered_df[col] == 'Yes').astype(int)
    
    corr_df['HeartDisease'] = (filtered_df['HeartDisease'] == 'Yes').astype(int)
    
    correlation_matrix = corr_df.corr()
    
    # Create interactive heatmap
    fig_corr = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='Blues',  # Light to dark blue gradient
        hoverongaps=False,
        hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.3f}<extra></extra>'
    ))
    
    fig_corr.update_layout(
        title='Feature Correlation Matrix',
        height=600,
        width=800
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Top correlations analysis
    hd_correlations = correlation_matrix['HeartDisease'].drop('HeartDisease').sort_values(key=abs, ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="correlation-section">', unsafe_allow_html=True)
        st.subheader("📈 Strongest Positive Correlations")
        positive_corr = hd_correlations[hd_correlations > 0].head(5)
        for feature, corr in positive_corr.items():
            st.write(f"**{feature}**: {corr:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="correlation-section">', unsafe_allow_html=True)
        st.subheader("📉 Strongest Negative Correlations")
        negative_corr = hd_correlations[hd_correlations < 0].head(5)
        for feature, corr in negative_corr.items():
            st.write(f"**{feature}**: {corr:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: Demographics
with tab4:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.subheader("👥 Comprehensive Demographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Heart Disease by Gender")
        
        # Create gender analysis
        gender_data = filtered_df.groupby(['Sex'])['HeartDisease'].apply(
            lambda x: (x == 'Yes').mean() * 100
        ).reset_index()
        
        fig_gender_analysis = px.bar(
            gender_data,
            x='Sex',
            y='HeartDisease',
            title='Heart Disease Rate by Gender',
            color='HeartDisease',
            color_continuous_scale='Reds',
            height=400
        )
        
        fig_gender_analysis.update_layout(
            xaxis_title='Gender',
            yaxis_title='Heart Disease Rate (%)',
            showlegend=False
        )
        
        st.plotly_chart(fig_gender_analysis, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Risk by Age Groups")
        
        # Age group risk analysis
        age_risk_data = []
        for age_cat in sorted(filtered_df['AgeCategory'].unique()):
            age_subset = filtered_df[filtered_df['AgeCategory'] == age_cat]
            total = len(age_subset)
            hd_cases = len(age_subset[age_subset['HeartDisease'] == 'Yes'])
            risk_rate = (hd_cases / total * 100) if total > 0 else 0
            
            age_risk_data.append({
                'Age Group': age_cat,
                'Total Population': total,
                'HD Cases': hd_cases,
                'Risk Rate (%)': risk_rate
            })
        
        age_risk_df = pd.DataFrame(age_risk_data)
        
        fig_age_risk = px.line(
            age_risk_df,
            x='Age Group',
            y='Risk Rate (%)',
            markers=True,
            title='Heart Disease Risk by Age Group',
            color_discrete_sequence=['#e63946']
        )
        
        fig_age_risk.update_traces(
            line=dict(width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Risk Rate: %{y:.1f}%<br>Population: %{customdata[0]}<extra></extra>',
            customdata=age_risk_df[['Total Population']].values
        )
        
        fig_age_risk.update_layout(height=400)
        
        st.plotly_chart(fig_age_risk, use_container_width=True)
    
    # Detailed demographic breakdown table
    st.markdown("#### 📋 Detailed Risk Analysis Table")
    
    # Create comprehensive demographic analysis
    demographic_analysis = []
    
    # By Age Category
    for age in sorted(filtered_df['AgeCategory'].unique()):
        subset = filtered_df[filtered_df['AgeCategory'] == age]
        if len(subset) > 0:
            hd_rate = (subset['HeartDisease'] == 'Yes').mean() * 100
            demographic_analysis.append({
                'Category': 'Age',
                'Group': age,
                'Total': len(subset),
                'HD Cases': len(subset[subset['HeartDisease'] == 'Yes']),
                'HD Rate (%)': f"{hd_rate:.1f}%"
            })
    
    # By Gender
    for gender in filtered_df['Sex'].unique():
        subset = filtered_df[filtered_df['Sex'] == gender]
        if len(subset) > 0:
            hd_rate = (subset['HeartDisease'] == 'Yes').mean() * 100
            demographic_analysis.append({
                'Category': 'Gender',
                'Group': gender,
                'Total': len(subset),
                'HD Cases': len(subset[subset['HeartDisease'] == 'Yes']),
                'HD Rate (%)': f"{hd_rate:.1f}%"
            })
    
    # By General Health Status
    for health in sorted(filtered_df['GenHealth'].unique()):
        subset = filtered_df[filtered_df['GenHealth'] == health]
        if len(subset) > 0:
            hd_rate = (subset['HeartDisease'] == 'Yes').mean() * 100
            demographic_analysis.append({
                'Category': 'Health Status',
                'Group': health,
                'Total': len(subset),
                'HD Cases': len(subset[subset['HeartDisease'] == 'Yes']),
                'HD Rate (%)': f"{hd_rate:.1f}%"
            })
    
    demo_df = pd.DataFrame(demographic_analysis)
    st.dataframe(demo_df, use_container_width=True, height=400)
    
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 5: Insights & Data Explorer
with tab5:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    
    # Insights Section
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
        
        # Gender insights
        if len(filtered_df.groupby('Sex')['HeartDisease'].apply(lambda x: (x == 'Yes').mean() * 100)) > 1:
            gender_rates = filtered_df.groupby('Sex')['HeartDisease'].apply(lambda x: (x == 'Yes').mean() * 100)
            higher_risk_gender = gender_rates.idxmax()
            insights.append(f"⚧ **Gender Risk**: {higher_risk_gender}s show higher heart disease rates ({gender_rates.max():.1f}% vs {gender_rates.min():.1f}%)")
    
    # Display insights in cards
    for i, insight in enumerate(insights):
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
    
    # Health recommendations
    st.markdown("### 🎯 Personalized Health Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏃‍♂️ Lifestyle Modifications")
        lifestyle_recs = [
            "**Exercise Regularly**: Aim for 150+ minutes of moderate exercise per week",
            "**Avoid Smoking**: Smoking dramatically increases cardiovascular risk",
            "**Healthy Diet**: Focus on heart-healthy foods like fruits, vegetables, and whole grains",
            "**Maintain Healthy Weight**: Keep BMI in the normal range (18.5-24.9)"
        ]
        for rec in lifestyle_recs:
            st.markdown(f"- {rec}")
    
    with col2:
        st.markdown("#### 🩺 Medical Care")
        medical_recs = [
            "**Regular Checkups**: Monitor blood pressure, cholesterol, and blood sugar",
            "**Quality Sleep**: Get 7-9 hours of restful sleep nightly",
            "**Manage Stress**: Practice stress-reduction techniques like meditation",
            "**Follow Prescriptions**: Take medications as directed by healthcare providers"
        ]
        for rec in medical_recs:
            st.markdown(f"- {rec}")
    
    # Data Explorer Section
    st.subheader("📋 Data Explorer")
    
    # Data overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
    with col2:
        st.metric("Features", len(filtered_df.columns))
    with col3:
        st.metric("Heart Disease Rate", f"{(len(hd_df)/len(filtered_df)*100):.1f}%")
    with col4:
        avg_age_numeric = filtered_df['AgeCategory'].map({
            '18-24': 21, '25-29': 27, '30-34': 32, '35-39': 37, 
            '40-44': 42, '45-49': 47, '50-54': 52, '55-59': 57,
            '60-64': 62, '65-69': 67, '70-74': 72, '75-79': 77, '80 or older': 85
        }).mean()
        st.metric("Avg Age Group", f"~{avg_age_numeric:.0f} years")
    
    # Data sample viewer
    st.markdown("#### 📊 Data Sample")
    
    # Option to view different data segments
    view_option = st.selectbox(
        "Choose data view:",
        ["All Data", "Heart Disease Cases Only", "Healthy Cases Only", "High Risk Factors"]
    )
    
    if view_option == "Heart Disease Cases Only":
        display_df = hd_df
    elif view_option == "Healthy Cases Only":
        display_df = nhd_df
    elif view_option == "High Risk Factors":
        # Show people with multiple risk factors
        risk_score = (
            (filtered_df['Smoking'] == 'Yes').astype(int) +
            (filtered_df['Diabetic'] == 'Yes').astype(int) +
            (filtered_df['PhysicalActivity'] == 'No').astype(int) +
            (filtered_df['BMI'] > 30).astype(int)
        )
        display_df = filtered_df[risk_score >= 2]  # 2+ risk factors
    else:
        display_df = filtered_df
    
    st.dataframe(
        display_df.head(100),
        use_container_width=True,
        height=400
    )
    
    # Statistical summary
    st.markdown("#### 📈 Statistical Summary")
    st.dataframe(
        display_df.describe(),
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced footer with comprehensive filter status
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
if bmi_range != (bmi_min, bmi_max):
    active_filters.append(f"BMI: {bmi_range[0]:.1f}-{bmi_range[1]:.1f}")

filter_text = " | ".join(active_filters) if active_filters else "No filters applied"

st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem; background: #f8f9fa; border-radius: 10px;'>
    <p><strong>❤️ Ultimate Heart Disease Analytics Dashboard</strong> | Built with Streamlit</p>
    <p>📊 Showing {len(filtered_df):,} records | Active Filters: {filter_text}</p>
    <p>🎯 Heart Disease Rate in Current View: {(len(hd_df)/len(filtered_df)*100):.1f}%</p>
    <p>🔬 Combining original matplotlib/seaborn charts with advanced Plotly analytics</p>
</div>
""", unsafe_allow_html=True)
