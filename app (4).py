import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import plotly.graph_objects as go

st.set_page_config(page_title="Heart Disease Insights Dashboard", layout="wide")

st.title("🫀 Heart Disease Insights Dashboard")
st.markdown("""
Welcome!  
This dashboard explores the profile and key risk factors of heart disease patients using CDC BRFSS 2020 data.
""")
st.markdown("---")

with st.sidebar:
    st.header("About")
    st.markdown("""
    **Heart Disease Dashboard**  
    Built using CDC 2020 BRFSS Data.
    - [Dataset info](https://www.cdc.gov/brfss/annual_data/annual_2020.html)
    - Built by [Your Name], 2025
    """)
    st.markdown("---")

# Load CSV
csv_filename = "heart_2020_cleaned (1).csv"
if not os.path.exists(csv_filename):
    st.error("❌ CSV file not found.")
    st.stop()
try:
    df = pd.read_csv(csv_filename)
except Exception as e:
    st.error(f"❌ Failed to load CSV: {e}")
    st.stop()

# Focus only on people with heart disease
hd_df = df[df["HeartDisease"] == "Yes"]

# ==== Metrics ====
col1, col2, col3 = st.columns(3)
col1.metric("❤️ Heart Disease Patients", f"{len(hd_df):,}")
col2.metric("⚖️ Avg BMI", round(hd_df["BMI"].mean(), 1))
col3.metric("🚬 Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean() * 100:.1f}%")

# ==== Show Full Data ====
st.markdown("### 👁️ Full Data: Heart Disease Patients")
st.dataframe(hd_df, height=210)

st.markdown("---")

# ==== Patient Profile: Age and Sex (side by side) ====
colA, colB = st.columns(2)
with colA:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index, y=age_counts.values,
        labels={"x": "Age Category", "y": "Patients"},
        title="Age Distribution",
        color_discrete_sequence=["#ef476f"]
    )
    fig_age.update_layout(height=180, width=320)
    st.plotly_chart(fig_age, use_container_width=False)
with colB:
    sex_counts = hd_df["Sex"].value_counts()
    fig_sex = px.pie(
        names=sex_counts.index, values=sex_counts.values, hole=0.45,
        title="Sex Distribution",
        color_discrete_sequence=["#ffd166", "#118ab2"]
    )
    fig_sex.update_layout(height=180, width=320)
    st.plotly_chart(fig_sex, use_container_width=False)

# ==== Grouped Bar: Main Risk Factors in One Chart ====
st.markdown("### ⚡ Main Risk Factors (Grouped Bar)")

risk_factors = ["Smoking", "Diabetic", "AlcoholDrinking", "Stroke"]
factor_map = {"Smoking": "Smoker", "Diabetic": "Diabetic", "AlcoholDrinking": "Alcohol Use", "Stroke": "Stroke"}
bar_data = []
for factor in risk_factors:
    percent = (hd_df[factor] == "Yes").mean() * 100
    bar_data.append({"Risk Factor": factor_map[factor], "Percent": percent})

bar_df = pd.DataFrame(bar_data)
fig_risk = px.bar(
    bar_df, x="Risk Factor", y="Percent",
    color="Risk Factor",
    color_discrete_sequence=px.colors.qualitative.Plotly,
    title="Prevalence of Risk Factors Among Heart Disease Patients",
    text="Percent"
)
fig_risk.update_layout(height=210, width=660, showlegend=False)
fig_risk.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig_risk, use_container_width=False)

# ==== Chronic Conditions Radar Chart ====
colC, colD = st.columns(2)
with colC:
    st.markdown("### 🧬 Chronic Conditions Radar")
    chronic_columns = ["Diabetic", "Stroke", "Asthma", "KidneyDisease", "SkinCancer"]
    radar_data = {col: (hd_df[col] == "Yes").mean() * 100 for col in chronic_columns}
    radar_df = pd.DataFrame({"Condition": list(radar_data.keys()), "Percentage": list(radar_data.values())})
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=radar_df["Percentage"],
        theta=radar_df["Condition"],
        fill='toself',
        name='Chronic Conditions %',
        line=dict(color="#06d6a0")
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        height=210, width=330,
        title="Chronic Conditions (%)"
    )
    st.plotly_chart(fig_radar, use_container_width=False)

# ==== Correlation Heatmap ====
with colD:
    st.markdown("### 📈 Correlation Heatmap")
    num_cols = ["BMI", "PhysicalHealth", "MentalHealth", "SleepTime", "AgeCategory"]
    # Encode AgeCategory for numeric correlation
    temp_df = hd_df.copy()
    age_order = {cat: i for i, cat in enumerate(sorted(hd_df["AgeCategory"].unique()))}
    temp_df["AgeCategory"] = temp_df["AgeCategory"].map(age_order)
    corr = temp_df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(3.5,2.6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="viridis", ax=ax, cbar=False)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)

st.markdown("---")


