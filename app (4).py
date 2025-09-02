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

# Enhanced CSS styling - Compact single screen design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #b11f4a 0%, #e63946 100%);
        padding: 0.8rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .kpi-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
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
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
        height: fit-content;
    }
    html, body, [class*="css"]  {
        font-size: 12px !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    h1 { font-size: 1.3rem !important; margin-bottom: 0.2rem !important; }
    h2 { font-size: 1.1rem !important; margin-bottom: 0.2rem !important; }
    h3 { font-size: 1rem !important; margin-bottom: 0.2rem !important; }
    h4 { font-size: 0.95rem !important; margin-bottom: 0.2rem !important; }
    .kpi-item {
        text-align: center;
        min-width: 120px;
    }
    .kpi-value {
        font-size: 1.4rem;
        font-weight: bold;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #666;
        margin: 0;
    }
    /* Remove scrollbar */
    .main .block-container {
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

plt.rcParams.update({'font.size': 8, 'font.family': 'sans-serif'})

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

# Compact header
st.markdown("""
<div class="main-header">
    <h1>❤️ Heart Disease Analytics Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar filters - more compact
with st.sidebar:
    st.markdown('<div class="filter-section"><h3>🔍 Filters</h3></div>', unsafe_allow_html=True)
    
    age_options = ['All'] + sorted(df['AgeCategory'].unique().tolist())
    selected_age = st.selectbox('Age Category', age_options)
    
    gender_options = ['All'] + df['Sex'].unique().tolist()
    selected_gender = st.selectbox('Gender', gender_options)
    
    health_options = ['All'] + sorted(df['GenHealth'].unique().tolist())
    selected_health = st.selectbox('General Health', health_options)

# Apply filters
filtered_df = df.copy()
if selected_age != 'All':
    filtered_df = filtered_df[filtered_df['AgeCategory'] == selected_age]
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]
if selected_health != 'All':
    filtered_df = filtered_df[filtered_df['GenHealth'] == selected_health]

# Calculate datasets
hd_df = filtered_df[filtered_df["HeartDisease"] == "Yes"]
nhd_df = filtered_df[filtered_df["HeartDisease"] == "No"]

if len(filtered_df) == 0:
    st.error("No data matches filters.")
    st.stop()

# Calculate KPI values safely
total_pop = len(filtered_df)
hd_cases = len(hd_df)
healthy_cases = len(nhd_df)
hd_rate = (hd_cases / total_pop * 100) if total_pop > 0 else 0

# Heart disease specific metrics
avg_bmi_hd = hd_df['BMI'].mean() if len(hd_df) > 0 else 0
smoking_rate_hd = (hd_df['Smoking'] == 'Yes').mean() * 100 if len(hd_df) > 0 else 0
alcohol_rate_hd = (hd_df['AlcoholDrinking'] == 'Yes').mean() * 100 if len(hd_df) > 0 else 0
inactive_rate_hd = (hd_df['PhysicalActivity'] == 'No').mean() * 100 if len(hd_df) > 0 else 0

# Single comprehensive KPI row
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #0a58ca;">{total_pop:,}</h3>
        <p class="kpi-label">👥 Total Population</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #c92c6d;">{hd_cases:,}</h3>
        <p class="kpi-label">❤️ Heart Disease</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #28a745;">{healthy_cases:,}</h3>
        <p class="kpi-label">💚 Healthy</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #fd7e14;">{hd_rate:.1f}%</h3>
        <p class="kpi-label">📈 HD Rate</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #6f42c1;">{avg_bmi_hd:.1f}</h3>
        <p class="kpi-label">⚖️ Avg BMI (HD)</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #dc3545;">{smoking_rate_hd:.1f}%</h3>
        <p class="kpi-label">🚬 Smoking (HD)</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #ffc107;">{alcohol_rate_hd:.1f}%</h3>
        <p class="kpi-label">🍺 Alcohol (HD)</p>
    </div>
    <div class="kpi-item">
        <h3 class="kpi-value" style="color: #17a2b8;">{inactive_rate_hd:.1f}%</h3>
        <p class="kpi-label">🏃 Inactive (HD)</p>
    </div>

# Main dashboard in a single row - compact layout
col1, col2, col3, col4 = st.columns([2.2, 1.3, 1, 1.5], gap="small")

# Risk Factors Bar Chart - Compact
with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Risk Factors Comparison")
    
    risk_factors = ["Smoking", "AlcoholDrinking", "Diabetic", "PhysicalActivity",
                   "Stroke", "DiffWalking", "Asthma", "KidneyDisease", "SkinCancer"]
    hd_risk = []
    nhd_risk = []
    for col_name in risk_factors:
        if col_name == "PhysicalActivity":
            hd_risk.append((hd_df[col_name] == "No").mean() * 100 if len(hd_df) > 0 else 0)
            nhd_risk.append((nhd_df[col_name] == "No").mean() * 100 if len(nhd_df) > 0 else 0)
        else:
            hd_risk.append((hd_df[col_name] == "Yes").mean() * 100 if len(hd_df) > 0 else 0)
            nhd_risk.append((nhd_df[col_name] == "Yes").mean() * 100 if len(nhd_df) > 0 else 0)
    
    risk_df = pd.DataFrame({
        "Risk Factor": ["Smoking", "Alcohol", "Diabetic", "No Activity",
                       "Stroke", "Diff Walk", "Asthma", "Kidney", "SkinCa"],
        "Heart Disease": hd_risk,
        "No Heart Disease": nhd_risk
    })
    melt_df = risk_df.melt(id_vars="Risk Factor", value_vars=["Heart Disease", "No Heart Disease"],
                        var_name="HD", value_name="Prevalence (%)")
    fig, ax = plt.subplots(figsize=(5.5, 3))
    sns.barplot(data=melt_df, x="Prevalence (%)", y="Risk Factor", hue="HD",
               palette=["#e63946", "#457b9d"], orient="h")
    ax.set_xlabel("Prevalence (%)", fontsize=9)
    ax.set_ylabel("")
    ax.set_title("Risk Factors by Heart Disease Status", fontsize=10, pad=5)
    ax.legend(fontsize=8, title='', loc='lower right')
    plt.tight_layout(pad=0.3)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Comorbidities Heatmap - Compact
with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 🔥 Comorbidities")
    
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = filtered_df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(2.5, 2.2))
    sns.heatmap(heat_df, annot=True, cmap="Reds", fmt=".1f", ax=ax, cbar=True,
               annot_kws={"size": 8, "weight": "bold"}, cbar_kws={"shrink": 0.8})
    ax.set_title("Comorbidities (%)", fontsize=9, pad=5)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7, rotation=0)
    plt.tight_layout(pad=0.3)
    st.pyplot(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Gender Distribution - Compact
with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### ⚧ Gender Split")
    
    if len(hd_df) > 0:
        gender_counts = hd_df["Sex"].value_counts()
        fig_gender = px.pie(names=gender_counts.index, values=gender_counts.values,
                          hole=0.5, height=200, color_discrete_sequence=['#c92c6d', '#667eea'])
        fig_gender.update_traces(textinfo='label+percent', textposition='inside',
                               textfont_size=10, textfont_color='white')
        fig_gender.update_layout(margin=dict(t=15, b=0, l=0, r=0), showlegend=False,
                               font=dict(size=9), title=dict(text="HD by Gender", x=0.5, font=dict(size=9)))
        st.plotly_chart(fig_gender, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Age Distribution - Compact
with col4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 👥 Age Distribution")
    
    if len(hd_df) > 0:
        age_counts = hd_df["AgeCategory"].value_counts().sort_index()
        fig_age = px.bar(x=age_counts.index, y=age_counts.values, color=age_counts.values,
                       color_continuous_scale="Viridis", height=200, title="HD Cases by Age")
        fig_age.update_layout(showlegend=False, font=dict(size=8), margin=dict(t=20, b=5, l=5, r=5),
                            xaxis_title='', yaxis_title='Cases', title_x=0.5, title_font_size=9)
        fig_age.update_traces(hovertemplate='<b>%{x}</b><br>Cases: %{y}<extra></extra>')
        fig_age.update_xaxes(tickangle=45, tickfont=dict(size=7))
        st.plotly_chart(fig_age, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Bottom row - Health Status and additional insights
col5, col6 = st.columns(2, gap="small")

with col5:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 🏥 Health Status Distribution")
    
    df_summary = filtered_df.groupby(['HeartDisease', 'GenHealth']).size().reset_index(name='count')
    if len(df_summary) > 0:
        df_summary['percent'] = df_summary.groupby('HeartDisease')['count'].transform(lambda x: x / x.sum() * 100)
        fig = px.bar(df_summary, x="GenHealth", y="percent", color="HeartDisease", barmode="group",
                    labels={"GenHealth": "General Health", "percent": "% of Group", "HeartDisease": "Heart Disease"},
                    color_discrete_sequence=['#28a745', '#c92c6d'], height=220, title="Health Status by HD")
        fig.update_layout(font=dict(size=8), margin=dict(t=20, b=5, l=5, r=5), title_x=0.5, title_font_size=9)
        fig.update_xaxes(tickfont=dict(size=7))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 📊 BMI vs Sleep Analysis")
    
    if len(hd_df) > 0 and len(nhd_df) > 0:
        # Create scatter plot of BMI vs Sleep Time
        fig_scatter = go.Figure()
        
        # Add heart disease cases
        fig_scatter.add_trace(go.Scatter(
            x=hd_df['BMI'], y=hd_df['SleepTime'],
            mode='markers', name='Heart Disease',
            marker=dict(color='#e63946', size=4, opacity=0.6),
            hovertemplate='BMI: %{x}<br>Sleep: %{y}h<extra></extra>'
        ))
        
        # Add healthy cases (sample to avoid overcrowding)
        nhd_sample = nhd_df.sample(min(1000, len(nhd_df))) if len(nhd_df) > 1000 else nhd_df
        fig_scatter.add_trace(go.Scatter(
            x=nhd_sample['BMI'], y=nhd_sample['SleepTime'],
            mode='markers', name='No Heart Disease',
            marker=dict(color='#457b9d', size=3, opacity=0.4),
            hovertemplate='BMI: %{x}<br>Sleep: %{y}h<extra></extra>'
        ))
        
        fig_scatter.update_layout(
            title='BMI vs Sleep Time',
            xaxis_title='BMI', yaxis_title='Sleep Time (hours)',
            height=220, font=dict(size=8),
            margin=dict(t=20, b=5, l=5, r=5),
            title_x=0.5, title_font_size=9,
            legend=dict(font=dict(size=7))
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
