import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Enhanced CSS styling - More compact
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #b11f4a 0%, #e63946 100%);
        padding: 0.8rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        background: linear-gradient(135deg, #f7f7fa 0%, #ffffff 100%);
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .filter-section {
        background: #667eea;
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    .chart-container {
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    html, body, [class*="css"]  {
        font-size: 12px !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 35px;
        padding: 0px 12px;
    }
    h1 { font-size: 1.4rem !important; margin-bottom: 0.2rem !important; }
    h2 { font-size: 1.2rem !important; margin-bottom: 0.2rem !important; }
    h3 { font-size: 1.1rem !important; margin-bottom: 0.2rem !important; }
    h4 { font-size: 1rem !important; margin-bottom: 0.2rem !important; }
    .metric-value { font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)ea;
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
    .correlation-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif'})

# Load data with better error handling
@st.cache_data
def load_data():
    possible_files = [
        "heart_2020_cleaned (1).csv",
        "heart_2020_cleaned.csv", 
        "heart.csv",
        "data.csv"
    ]
    
    for filename in possible_files:
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                if not df.empty and 'HeartDisease' in df.columns:
                    return df
            except Exception as e:
                continue
    
    st.error("❌ CSV file not found or invalid format.")
    st.stop()

df = load_data()

# Main header
st.markdown("""
<div class="main-header">
    <h1>❤️ Heart Disease Analytics Dashboard</h1>
    <p style="margin-bottom: 0;">Comprehensive insights into cardiovascular health patterns</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown('<div class="filter-section"><h3>🔍 Demographic Filters</h3></div>', unsafe_allow_html=True)
    
    st.info("ℹ️ Filters apply to entire population, then heart disease analysis is performed")
    
    age_options = ['All'] + sorted(df['AgeCategory'].unique().tolist())
    selected_age = st.selectbox('👥 Age Category', age_options)
    
    gender_options = ['All'] + df['Sex'].unique().tolist()
    selected_gender = st.selectbox('⚧ Gender', gender_options)
    
    health_options = ['All'] + sorted(df['GenHealth'].unique().tolist())
    selected_health = st.selectbox('🏥 General Health', health_options)
    
    st.markdown("---")
    st.markdown("### 📊 Filter Impact")
    
    # Apply filters
    filtered_df = df.copy()
    if selected_age != 'All':
        filtered_df = filtered_df[filtered_df['AgeCategory'] == selected_age]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]
    if selected_health != 'All':
        filtered_df = filtered_df[filtered_df['GenHealth'] == selected_health]
    
    st.metric("Records", f"{len(filtered_df):,}")
    
    if len(filtered_df) > 0:
        hd_rate = (filtered_df['HeartDisease'] == 'Yes').mean() * 100
        st.metric("HD Rate", f"{hd_rate:.1f}%")

# Calculate datasets
hd_df = filtered_df[filtered_df["HeartDisease"] == "Yes"]
nhd_df = filtered_df[filtered_df["HeartDisease"] == "No"]
all_hd_df = df[df["HeartDisease"] == "Yes"]

if len(filtered_df) == 0:
    st.error("No data matches filters.")
    st.stop()

# Population summary
st.markdown(f"""
<div class="metric-container">
    <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;">
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

# KPI row - ALL heart disease patients (baseline)
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
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Original Dashboard", "📈 Advanced Analytics", "🔗 Correlations", "👥 Demographics", "💡 Insights"])

# TAB 1: Original Dashboard
with tab1:
    row1 = st.columns([1.8, 1.2, 0.7], gap="medium")

    # Risk Factors Bar
    with row1[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Risk Factors Analysis")
        
        risk_factors = ["Smoking", "AlcoholDrinking", "Diabetic", "PhysicalActivity",
                       "Stroke", "DiffWalking", "Asthma", "KidneyDisease", "SkinCancer"]
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
            "Risk Factor": ["Smoking", "Alcohol", "Diabetic", "No Activity",
                           "Stroke", "Diff Walk", "Asthma", "Kidney", "SkinCa"],
            "Heart Disease": hd_risk,
            "No Heart Disease": nhd_risk
        })
        melt_df = risk_df.melt(id_vars="Risk Factor", value_vars=["Heart Disease", "No Heart Disease"],
                            var_name="HD", value_name="Prevalence (%)")
        fig, ax = plt.subplots(figsize=(5, 2.5))
        sns.barplot(data=melt_df, x="Prevalence (%)", y="Risk Factor", hue="HD",
                   palette=["#e63946", "#457b9d"], orient="h")
        ax.set_xlabel("Prevalence (%)", fontsize=11)
        ax.set_ylabel("")
        ax.set_title("Risk Factors Comparison", fontsize=12, pad=10)
        ax.legend(fontsize=10, title='', loc='lower right')
        plt.tight_layout(pad=0.8)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Comorbidities Heatmap
    with row1[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🔥 Comorbidities Heatmap")
        
        condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
        heat_df = filtered_df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
        fig, ax = plt.subplots(figsize=(2.6, 2.3))
        sns.heatmap(heat_df, annot=True, cmap="Reds", fmt=".1f", ax=ax, cbar=True,
                   annot_kws={"size": 11, "weight": "bold"}, cbar_kws={"shrink": 0.8})
        ax.set_title("Comorbidities (%)", fontsize=12, pad=10)
        ax.set_xlabel("")
        ax.set_ylabel("")
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10, rotation=0)
        plt.tight_layout(pad=0.7)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Gender Pie
    with row1[2]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### ⚧ Gender Distribution")
        
        if len(hd_df) > 0:
            gender_counts = hd_df["Sex"].value_counts()
            fig_gender = px.pie(names=gender_counts.index, values=gender_counts.values,
                              hole=0.5, height=200, color_discrete_sequence=['#c92c6d', '#667eea'])
            fig_gender.update_traces(textinfo='label+percent', textposition='inside',
                                   textfont_size=12, textfont_color='white')
            fig_gender.update_layout(margin=dict(t=20, b=0, l=0, r=0), showlegend=False,
                                   font=dict(size=12), title=dict(text="Heart Disease by Gender", x=0.5, font=dict(size=11)))
            st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Row
    row2 = st.columns(2, gap="medium")

    with row2[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 👥 Age Group Distribution")
        
        if len(hd_df) > 0:
            age_counts = hd_df["AgeCategory"].value_counts().sort_index()
            fig_age = px.bar(x=age_counts.index, y=age_counts.values, color=age_counts.values,
                           color_continuous_scale="Viridis", height=250, title="Heart Disease Cases by Age Group")
            fig_age.update_layout(showlegend=False, font=dict(size=11), margin=dict(t=30, b=0, l=0, r=0),
                                xaxis_title='Age Group', yaxis_title='Count', title_x=0.5)
            fig_age.update_traces(hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>')
            st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🏥 General Health Status")
        
        df_summary = filtered_df.groupby(['HeartDisease', 'GenHealth']).size().reset_index(name='count')
        if len(df_summary) > 0:
            df_summary['percent'] = df_summary.groupby('HeartDisease')['count'].transform(lambda x: x / x.sum() * 100)
            fig = px.bar(df_summary, x="GenHealth", y="percent", color="HeartDisease", barmode="group",
                        labels={"GenHealth": "General Health", "percent": "% of Group", "HeartDisease": "Heart Disease"},
                        color_discrete_sequence=['#28a745', '#c92c6d'], height=250, title="Health Status Distribution")
            fig.update_layout(font=dict(size=11), margin=dict(t=30, b=0, l=0, r=0), title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: Advanced Analytics
with tab2:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Interactive Risk Factor Analysis")
        
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
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Heart Disease', x=risk_df_adv['Factor'], y=risk_df_adv['Heart Disease'],
                           marker_color='#e63946', hovertemplate='<b>%{x}</b><br>Heart Disease: %{y:.1f}%<extra></extra>'))
        fig.add_trace(go.Bar(name='No Heart Disease', x=risk_df_adv['Factor'], y=risk_df_adv['No Heart Disease'],
                           marker_color='#457b9d', hovertemplate='<b>%{x}</b><br>No Heart Disease: %{y:.1f}%<extra></extra>'))
        
        fig.update_layout(title='Interactive Risk Factor Prevalence', xaxis_title='Risk Factors',
                         yaxis_title='Prevalence (%)', barmode='group', height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Risk Ratios")
        
        risk_df_sorted = risk_df_adv.sort_values('Risk Ratio', ascending=True)
        
        fig_ratio = go.Figure(go.Bar(x=risk_df_sorted['Risk Ratio'], y=risk_df_sorted['Factor'],
                                   orientation='h', marker_color='#ff6b6b',
                                   hovertemplate='<b>%{y}</b><br>Risk Ratio: %{x:.2f}x<extra></extra>'))
        
        fig_ratio.update_layout(title='Risk Ratios (HD vs No HD)', xaxis_title='Risk Ratio',
                              height=400, yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_ratio, use_container_width=True)
    
    # Advanced Analysis
    st.subheader("📈 Advanced Analysis")
    col3, col4 = st.columns(2)
    
    with col3:
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
        fig_age_adv.add_trace(go.Bar(name='Total Population', x=age_df_adv['Age Category'], y=age_df_adv['Total'],
                                   marker_color='lightblue', yaxis='y'))
        fig_age_adv.add_trace(go.Scatter(name='HD Rate (%)', x=age_df_adv['Age Category'], y=age_df_adv['HD Rate (%)'],
                                       mode='lines+markers', marker=dict(color='red', size=8),
                                       line=dict(width=3, color='red'), yaxis='y2'))
        
        fig_age_adv.update_layout(title='Population & HD Rate by Age', xaxis_title='Age Category',
                                yaxis=dict(title='Population', side='left'),
                                yaxis2=dict(title='HD Rate (%)', side='right', overlaying='y'), height=400)
        
        st.plotly_chart(fig_age_adv, use_container_width=True)
    
    with col4:
        st.markdown("#### ⚖️ BMI vs General Health")
        
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['BMI_Category'] = pd.cut(filtered_df_copy['BMI'], 
                                                bins=[0, 18.5, 25, 30, 100], 
                                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
        
        bmi_health_data = filtered_df_copy.groupby(['BMI_Category', 'GenHealth'])['HeartDisease'].apply(
            lambda x: (x == 'Yes').mean() * 100).reset_index()
        bmi_health_pivot = bmi_health_data.pivot(index='BMI_Category', columns='GenHealth', values='HeartDisease')
        
        fig_bmi_health = go.Figure(data=go.Heatmap(z=bmi_health_pivot.values, x=bmi_health_pivot.columns,
                                                 y=bmi_health_pivot.index, colorscale='Oranges', hoverongaps=False,
                                                 hovertemplate='<b>%{y}</b><br>%{x} Health<br>HD Rate: %{z:.1f}%<extra></extra>'))
        
        fig_bmi_health.update_layout(title='HD Rate: BMI vs General Health', height=400,
                                   xaxis_title='General Health', yaxis_title='BMI Category')
        
        st.plotly_chart(fig_bmi_health, use_container_width=True)

# TAB 3: Correlations
with tab3:
    st.subheader("🔗 Feature Correlation Analysis")
    
    corr_cols = ['BMI', 'MentalHealth', 'PhysicalHealth', 'SleepTime']
    binary_cols = ['Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'Diabetic', 
                   'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer']
    
    corr_df = filtered_df[corr_cols].copy()
    for col in binary_cols:
        corr_df[col] = (filtered_df[col] == 'Yes').astype(int)
    corr_df['HeartDisease'] = (filtered_df['HeartDisease'] == 'Yes').astype(int)
    
    correlation_matrix = corr_df.corr()
    
    fig_corr = go.Figure(data=go.Heatmap(z=correlation_matrix.values, x=correlation_matrix.columns,
                                       y=correlation_matrix.index, colorscale='Blues', hoverongaps=False,
                                       hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlation: %{z:.3f}<extra></extra>'))
    
    fig_corr.update_layout(title='Feature Correlation Matrix', height=600)
    st.plotly_chart(fig_corr, use_container_width=True)
    
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

# TAB 4: Demographics
with tab4:
    st.subheader("👥 Demographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Heart Disease by Gender")
        
        gender_data = filtered_df.groupby(['Sex'])['HeartDisease'].apply(lambda x: (x == 'Yes').mean() * 100).reset_index()
        
        fig_gender_analysis = px.bar(gender_data, x='Sex', y='HeartDisease', title='Heart Disease Rate by Gender',
                                   color='HeartDisease', color_continuous_scale='Reds', height=400)
        fig_gender_analysis.update_layout(xaxis_title='Gender', yaxis_title='Heart Disease Rate (%)', showlegend=False)
        st.plotly_chart(fig_gender_analysis, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Risk by Age Groups")
        
        age_risk_data = []
        for age_cat in sorted(filtered_df['AgeCategory'].unique()):
            age_subset = filtered_df[filtered_df['AgeCategory'] == age_cat]
            total = len(age_subset)
            hd_cases = len(age_subset[age_subset['HeartDisease'] == 'Yes'])
            risk_rate = (hd_cases / total * 100) if total > 0 else 0
            age_risk_data.append({'Age Group': age_cat, 'Risk Rate (%)': risk_rate})
        
        age_risk_df = pd.DataFrame(age_risk_data)
        
        fig_age_risk = px.line(age_risk_df, x='Age Group', y='Risk Rate (%)', markers=True,
                             title='Heart Disease Risk by Age Group', color_discrete_sequence=['#e63946'])
        fig_age_risk.update_traces(line=dict(width=3), marker=dict(size=8))
        fig_age_risk.update_layout(height=400)
        st.plotly_chart(fig_age_risk, use_container_width=True)
    
    # Demographics table
    st.markdown("#### 📋 Detailed Analysis")
    demographic_analysis = []
    
    for age in sorted(filtered_df['AgeCategory'].unique()):
        subset = filtered_df[filtered_df['AgeCategory'] == age]
        if len(subset) > 0:
            hd_rate = (subset['HeartDisease'] == 'Yes').mean() * 100
            demographic_analysis.append({
                'Category': 'Age', 'Group': age, 'Total': len(subset),
                'HD Cases': len(subset[subset['HeartDisease'] == 'Yes']), 'HD Rate (%)': f"{hd_rate:.1f}%"
            })
    
    for gender in filtered_df['Sex'].unique():
        subset = filtered_df[filtered_df['Sex'] == gender]
        if len(subset) > 0:
            hd_rate = (subset['HeartDisease'] == 'Yes').mean() * 100
            demographic_analysis.append({
                'Category': 'Gender', 'Group': gender, 'Total': len(subset),
                'HD Cases': len(subset[subset['HeartDisease'] == 'Yes']), 'HD Rate (%)': f"{hd_rate:.1f}%"
            })
    
    for health in sorted(filtered_df['GenHealth'].unique()):
        subset = filtered_df[filtered_df['GenHealth'] == health]
        if len(subset) > 0:
            hd_rate = (subset['HeartDisease'] == 'Yes').mean() * 100
            demographic_analysis.append({
                'Category': 'Health Status', 'Group': health, 'Total': len(subset),
                'HD Cases': len(subset[subset['HeartDisease'] == 'Yes']), 'HD Rate (%)': f"{hd_rate:.1f}%"
            })
