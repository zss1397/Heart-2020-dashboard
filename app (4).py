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

# Enhanced CSS styling - Compact design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #b11f4a 0%, #e63946 100%);
        padding: 0.8rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 0.8rem;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
    }
    .single-kpi-container {
        background: linear-gradient(135deg, #f7f7fa 0%, #ffffff 100%);
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.8rem;
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
        padding: 0.6rem;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 0.6rem;
        height: fit-content;
    }
    html, body, [class*="css"]  {
        font-size: 12px !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 100%;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 30px;
        padding: 0px 10px;
    }
    h1 { font-size: 1.3rem !important; margin-bottom: 0.2rem !important; }
    h2 { font-size: 1.0rem !important; margin-bottom: 0.2rem !important; }
    h3 { font-size: 0.95rem !important; margin-bottom: 0.2rem !important; }
    h4 { font-size: 0.9rem !important; margin-bottom: 0.2rem !important; }
    .kpi-item {
        text-align: center;
        min-width: 90px;
        flex: 1;
    }
    .kpi-value {
        font-size: 1.1rem;
        font-weight: bold;
        margin: 0;
        line-height: 1.2;
    }
    .kpi-label {
        font-size: 0.7rem;
        color: #666;
        margin: 0;
        line-height: 1.1;
    }
    .correlation-section {
        background: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.8rem 0;
    }
    .insight-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 0.8rem;
        margin: 0.8rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

plt.rcParams.update({'font.size': 8, 'font.family': 'sans-serif'})

# Load data
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

# Compact header
st.markdown("""
<div class="main-header">
    <h1>❤️ Heart Disease Analytics Dashboard</h1>
    <p style="margin-bottom: 0; font-size: 0.9rem;">Comprehensive insights into cardiovascular health patterns</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown('<div class="filter-section"><h3>🔍 Filters</h3></div>', unsafe_allow_html=True)
    
    age_options = ['All'] + sorted(df['AgeCategory'].unique().tolist())
    selected_age = st.selectbox('👥 Age Category', age_options)
    
    gender_options = ['All'] + df['Sex'].unique().tolist()
    selected_gender = st.selectbox('⚧ Gender', gender_options)
    
    health_options = ['All'] + sorted(df['GenHealth'].unique().tolist())
    selected_health = st.selectbox('🏥 General Health', health_options)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_age != 'All':
        filtered_df = filtered_df[filtered_df['AgeCategory'] == selected_age]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]
    if selected_health != 'All':
        filtered_df = filtered_df[filtered_df['GenHealth'] == selected_health]
    
    st.markdown("---")
    st.markdown("### 📊 Filter Impact")
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

# Calculate all KPI values
total_pop = len(filtered_df)
hd_cases = len(hd_df)
healthy_cases = len(nhd_df)
hd_rate = round((hd_cases / total_pop * 100), 1) if total_pop > 0 else 0

# Additional metrics from heart disease patients
avg_bmi = round(all_hd_df['BMI'].mean(), 1) if len(all_hd_df) > 0 else 0
smoking_rate = round((all_hd_df['Smoking'] == 'Yes').mean() * 100, 1) if len(all_hd_df) > 0 else 0
alcohol_rate = round((all_hd_df['AlcoholDrinking'] == 'Yes').mean() * 100, 1) if len(all_hd_df) > 0 else 0
inactive_rate = round((all_hd_df['PhysicalActivity'] == 'No').mean() * 100, 1) if len(all_hd_df) > 0 else 0

# SINGLE COMPREHENSIVE KPI ROW - ALL 8 METRICS IN ONE ROW
st.markdown(f"""
<div class="single-kpi-container">
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #0a58ca;">👥 {total_pop:,}</h3>
        <p class="kpi-label">Total Population</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #c92c6d;">❤️ {hd_cases:,}</h3>
        <p class="kpi-label">Heart Disease Cases</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #28a745;">💚 {healthy_cases:,}</h3>
        <p class="kpi-label">Healthy Cases</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #fd7e14;">📈 {hd_rate}%</h3>
        <p class="kpi-label">HD Rate</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #6f42c1;">⚖️ {avg_bmi}</h3>
        <p class="kpi-label">Avg BMI (All HD)</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #dc3545;">🚬 {smoking_rate}%</h3>
        <p class="kpi-label">Smoking (All HD)</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #ffc107;">🍺 {alcohol_rate}%</h3>
        <p class="kpi-label">Alcohol (All HD)</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #17a2b8;">🏃 {inactive_rate}%</h3>
        <p class="kpi-label">Inactive (All HD)</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📈 Analytics", "🔗 Correlations", "👥 Demographics", "💡 Insights"])

# TAB 1: Dashboard
with tab1:
    row1 = st.columns([1.8, 1.2, 0.7], gap="small")

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
        fig, ax = plt.subplots(figsize=(4.5, 2.0))
        sns.barplot(data=melt_df, x="Prevalence (%)", y="Risk Factor", hue="HD",
                   palette=["#e63946", "#457b9d"], orient="h")
        ax.set_xlabel("Prevalence (%)", fontsize=9)
        ax.set_ylabel("")
        ax.set_title("Risk Factors Comparison", fontsize=10, pad=5)
        ax.legend(fontsize=8, title='', loc='lower right')
        plt.tight_layout(pad=0.3)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Comorbidities Heatmap
    with row1[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🔥 Comorbidities")
        
        condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
        heat_df = filtered_df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
        fig, ax = plt.subplots(figsize=(2.2, 1.8))
        sns.heatmap(heat_df, annot=True, cmap="Reds", fmt=".1f", ax=ax, cbar=True,
                   annot_kws={"size": 8, "weight": "bold"}, cbar_kws={"shrink": 0.7})
        ax.set_title("Comorbidities (%)", fontsize=9, pad=5)
        ax.set_xlabel("")
        ax.set_ylabel("")
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7, rotation=0)
        plt.tight_layout(pad=0.3)
        st.pyplot(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Gender Pie
    with row1[2]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### ⚧ Gender")
        
        if len(hd_df) > 0:
            gender_counts = hd_df["Sex"].value_counts()
            fig_gender = px.pie(names=gender_counts.index, values=gender_counts.values,
                              hole=0.5, height=150, color_discrete_sequence=['#c92c6d', '#667eea'])
            fig_gender.update_traces(textinfo='label+percent', textposition='inside',
                                   textfont_size=9, textfont_color='white')
            fig_gender.update_layout(margin=dict(t=15, b=0, l=0, r=0), showlegend=False,
                                   font=dict(size=8), title=dict(text="HD by Gender", x=0.5, font=dict(size=9)))
            st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Row
    row2 = st.columns(2, gap="small")

    with row2[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 👥 Age Groups")
        
        if len(hd_df) > 0:
            age_counts = hd_df["AgeCategory"].value_counts().sort_index()
            fig_age = px.bar(x=age_counts.index, y=age_counts.values, color=age_counts.values,
                           color_continuous_scale="Viridis", height=180, title="HD Cases by Age")
            fig_age.update_layout(showlegend=False, font=dict(size=8), margin=dict(t=20, b=5, l=5, r=5),
                                xaxis_title='Age Group', yaxis_title='Count', title_x=0.5, title_font_size=9)
            fig_age.update_traces(hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>')
            st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row2[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### 🏥 Health Status")
        
        df_summary = filtered_df.groupby(['HeartDisease', 'GenHealth']).size().reset_index(name='count')
        if len(df_summary) > 0:
            df_summary['percent'] = df_summary.groupby('HeartDisease')['count'].transform(lambda x: x / x.sum() * 100)
            fig = px.bar(df_summary, x="GenHealth", y="percent", color="HeartDisease", barmode="group",
                        labels={"GenHealth": "General Health", "percent": "% of Group", "HeartDisease": "Heart Disease"},
                        color_discrete_sequence=['#28a745', '#c92c6d'], height=180, title="Health Status")
            fig.update_layout(font=dict(size=8), margin=dict(t=20, b=5, l=5, r=5), title_x=0.5, title_font_size=9)
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
                         yaxis_title='Prevalence (%)', barmode='group', height=350)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Risk Ratios")
        
        risk_df_sorted = risk_df_adv.sort_values('Risk Ratio', ascending=True)
        
        fig_ratio = go.Figure(go.Bar(x=risk_df_sorted['Risk Ratio'], y=risk_df_sorted['Factor'],
                                   orientation='h', marker_color='#ff6b6b',
                                   hovertemplate='<b>%{y}</b><br>Risk Ratio: %{x:.2f}x<extra></extra>'))
        
        fig_ratio.update_layout(title='Risk Ratios (HD vs No HD)', xaxis_title='Risk Ratio',
                              height=350, yaxis={'categoryorder': 'total ascending'})
        
        st.plotly_chart(fig_ratio, use_container_width=True)

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
    
    fig_corr.update_layout(title='Feature Correlation Matrix', height=450)
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
                                   color='HeartDisease', color_continuous_scale='Reds', height=350)
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
        fig_age_risk.update_layout(height=350)
        st.plotly_chart(fig_age_risk, use_container_width=True)

# TAB 5: Insights
with tab5:
    st.subheader("💡 Key Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Key Findings")
        st.write(f"• **Total Population**: {total_pop:,} records analyzed")
        st.write(f"• **Heart Disease Rate**: {hd_rate}% of filtered population")
        st.write(f"• **Average BMI** (All HD patients): {avg_bmi}")
        st.write(f"• **Smoking Rate** (All HD patients): {smoking_rate}%")
        st.write(f"• **Physical Inactivity** (All HD patients): {inactive_rate}%")
        st.write(f"• **Alcohol Consumption** (All HD patients): {alcohol_rate}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Recommendations")
        st.write("• **Smoking cessation programs** - High prevalence in HD patients")
        st.write("• **Physical activity promotion** - Target inactive populations")
        st.write("• **Weight management initiatives** - Address BMI-related risks")
        st.write("• **Regular health screenings** - Focus on high-risk age groups")
        st.write("• **Preventive education** - Heart-healthy lifestyle choices")
        st.write("• **Comorbidity management** - Diabetes, stroke prevention")
        st.markdown('</div>', unsafe_allow_html=True)
