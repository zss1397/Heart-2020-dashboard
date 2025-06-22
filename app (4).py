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
This dashboard helps you explore the profile of heart disease patients and key risk factors using the CDC BRFSS 2020 data.
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

hd_df = df[df["HeartDisease"] == "Yes"]

# Sidebar filters (you can uncomment when needed)
# gender = st.sidebar.multiselect("Select Sex", df["Sex"].unique(), default=df["Sex"].unique(), key="gender_filter")
# age = st.sidebar.multiselect("Select Age Category", df["AgeCategory"].unique(), default=df["AgeCategory"].unique(), key="age_filter")

# ==== Metrics ====
col1, col2, col3 = st.columns(3)
col1.metric("Total Heart Disease Patients", f"{len(hd_df):,}")
col2.metric("Avg BMI", round(hd_df["BMI"].mean(), 1))
col3.metric("Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean() * 100:.1f}%")

st.markdown("---")

# ==== Patient Profile ====
st.header("👥 Patient Profile")

# Age and Sex Distribution side-by-side
col1, col2 = st.columns(2)
with col1:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        labels={"x": "Age Category", "y": "Patients"},
        title="Age Distribution"
    )
    fig_age.update_layout(height=220, width=330)
    st.plotly_chart(fig_age, use_container_width=False)
with col2:
    sex_counts = hd_df["Sex"].value_counts()
    fig_sex = px.pie(
        names=sex_counts.index,
        values=sex_counts.values,
        title="Sex Distribution"
    )
    fig_sex.update_layout(height=220, width=330)
    st.plotly_chart(fig_sex, use_container_width=False)

st.markdown("---")

# ==== Main Risk Factors ====
st.header("⚠️ Main Risk Factors")

col3, col4 = st.columns(2)
with col3:
    smoke_hd = df.groupby("Smoking")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
    fig_smoke = px.bar(
        smoke_hd,
        barmode="group",
        labels={"value": "% with/without Heart Disease", "Smoking": "Smoking Status", "variable": "Heart Disease"},
        title="Heart Disease Rate by Smoking Status"
    )
    fig_smoke.update_layout(height=220, width=330)
    st.plotly_chart(fig_smoke, use_container_width=False)
with col4:
    diab_hd = df.groupby("Diabetic")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
    fig_diab = px.bar(
        diab_hd,
        barmode="group",
        labels={"value": "% with/without Heart Disease", "Diabetic": "Diabetic Status", "variable": "Heart Disease"},
        title="Heart Disease Rate by Diabetes Status"
    )
    fig_diab.update_layout(height=220, width=330)
    st.plotly_chart(fig_diab, use_container_width=False)

col5, col6 = st.columns(2)
with col5:
    alc_hd = df.groupby("AlcoholDrinking")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
    fig_alc = px.bar(
        alc_hd,
        barmode="group",
        labels={"value": "% with/without Heart Disease", "AlcoholDrinking": "Alcohol Drinking", "variable": "Heart Disease"},
        title="Heart Disease Rate by Alcohol Drinking"
    )
    fig_alc.update_layout(height=220, width=330)
    st.plotly_chart(fig_alc, use_container_width=False)
with col6:
    stroke_hd = df.groupby("Stroke")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
    fig_stroke = px.bar(
        stroke_hd,
        barmode="group",
        labels={"value": "% with/without Heart Disease", "Stroke": "Stroke History", "variable": "Heart Disease"},
        title="Heart Disease Rate by Stroke History"
    )
    fig_stroke.update_layout(height=220, width=330)
    st.plotly_chart(fig_stroke, use_container_width=False)

st.markdown("---")

# ==== Chronic Conditions Radar Chart ====
st.header("🧬 Chronic Conditions in Heart Disease Patients")
chronic_columns = ["Diabetic", "Stroke", "Asthma", "KidneyDisease", "SkinCancer"]
radar_data = {col: (hd_df[col] == "Yes").mean() * 100 for col in chronic_columns}
radar_df = pd.DataFrame({"Condition": list(radar_data.keys()), "Percentage": list(radar_data.values())})
fig_radar = go.Figure(data=go.Scatterpolar(
    r=radar_df["Percentage"],
    theta=radar_df["Condition"],
    fill='toself',
    name='Chronic Conditions %'
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    height=320, width=380,
    title="Chronic Conditions (%)"
)
st.plotly_chart(fig_radar, use_container_width=False)

st.markdown("---")

# ==== Executive Summary ====
st.header("📝 Executive Summary")
st.info("""
- **Heart disease is more common in older adults and males.**
- **Smoking and diabetes are strong risk factors for heart disease.**
- **Chronic conditions are more frequent among heart disease patients.**
""")

# ==== Optional: Data Table Expander at Bottom ====
with st.expander("Show Data Table"):
    st.dataframe(hd_df.head())

import streamlit as st
import plotly.express as px

# KPIs
k1, k2, k3 = st.columns(3)
k1.metric("❤️ Patients", f"{len(hd_df):,}")
k2.metric("⚖️ Avg BMI", round(hd_df["BMI"].mean(), 1))
k3.metric("🚬 Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean() * 100:.1f}%")

st.markdown("---")

# Profile Section
st.header("🧑‍🤝‍🧑 Patient Profile")
col1, col2 = st.columns(2)
with col1:
    fig_age = px.bar(..., color_discrete_sequence=["#e63946"])
    fig_age.update_layout(height=200, width=320, plot_bgcolor="#F7F7F7", paper_bgcolor="#F7F7F7")
    st.plotly_chart(fig_age, use_container_width=False)
    st.info("Most patients are age 60+.")
with col2:
    fig_sex = px.pie(..., hole=0.45, color_discrete_sequence=["#f1faee", "#457b9d"])
    fig_sex.update_layout(height=200, width=320)
    st.plotly_chart(fig_sex, use_container_width=False)
    st.info("More than half are male.")

# Main Risk
st.header("⚠️ Main Risk Factors")
col3, col4 = st.columns(2)
with col3:
    fig_smoke = px.bar(..., orientation="h", color_discrete_sequence=["#e76f51", "#2a9d8f"])
    fig_smoke.update_layout(height=200, width=320)
    st.plotly_chart(fig_smoke, use_container_width=False)
    st.success("Smokers have higher heart disease rates.")
with col4:
    fig_diab = px.bar(..., orientation="h", color_discrete_sequence=["#a8dadc", "#457b9d"])
    fig_diab.update_layout(height=200, width=320)
    st.plotly_chart(fig_diab, use_container_width=False)
    st.warning("Diabetes is a strong risk factor.")

import matplotlib.pyplot as plt

st.header("📈 Correlation Heatmap")
corr = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(6, 4))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, cbar=False)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)


