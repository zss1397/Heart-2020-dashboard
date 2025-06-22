import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Heart Disease Dashboard", layout="wide")

# --- Load Data ---
csv_filename = "heart_2020_cleaned (1).csv"
if not os.path.exists(csv_filename):
    st.error("❌ CSV file not found.")
    st.stop()
try:
    df = pd.read_csv(csv_filename)
except Exception as e:
    st.error(f"❌ Failed to load CSV: {e}")
    st.stop()

# Focus only on heart disease patients for visuals
hd_df = df[df["HeartDisease"] == "Yes"]
nhd_df = df[df["HeartDisease"] == "No"]

# --- KPIs ---
st.title("💖 Heart Disease Insights Dashboard")
st.markdown(
    "Explore the main risk factors, trends, and correlations among heart disease patients (CDC BRFSS 2020)."
)
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("❤️ Heart Disease Patients", f"{len(hd_df):,}")
col2.metric("⚖️ Avg BMI", f"{hd_df['BMI'].mean():.1f}")
col3.metric("🚬 Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean()*100:.1f}%")
col4.metric("🍺 Alcohol Use Rate", f"{(hd_df['AlcoholDrinking'] == 'Yes').mean()*100:.1f}%")
col5.metric("🏃 Physical Activity", f"{(hd_df['PhysicalActivity'] == 'Yes').mean()*100:.1f}%")

st.markdown("---")

# --- Main Visuals: Risk Factors & Gender Distribution ---
colA, colB = st.columns(2)

# Pie/Donut Chart for Gender
with colA:
    st.subheader("🧑‍🤝‍🧑 Gender Distribution (Heart Disease)")
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.5,
        title="Gender Split",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_gender, use_container_width=True)

# Main Risk Factors Bar Chart
with colB:
    st.subheader("🌡️ Key Risk Factors Among Heart Disease Patients")
    # List of main risk factors to display
    risk_factors = {
        "Smoking": (hd_df["Smoking"] == "Yes").mean() * 100,
        "Alcohol Drinking": (hd_df["AlcoholDrinking"] == "Yes").mean() * 100,
        "Diabetic": (hd_df["Diabetic"] == "Yes").mean() * 100,
        "Physical Activity": (hd_df["PhysicalActivity"] == "Yes").mean() * 100,
        "Stroke": (hd_df["Stroke"] == "Yes").mean() * 100,
        "Difficulty Walking": (hd_df["DiffWalking"] == "Yes").mean() * 100,
        "Asthma": (hd_df["Asthma"] == "Yes").mean() * 100,
        "Kidney Disease": (hd_df["KidneyDisease"] == "Yes").mean() * 100,
        "Skin Cancer": (hd_df["SkinCancer"] == "Yes").mean() * 100,
    }
    fig_risk = px.bar(
        x=list(risk_factors.keys()),
        y=list(risk_factors.values()),
        labels={"x": "Risk Factor", "y": "% of Patients"},
        title="Prevalence of Risk Factors",
        color=list(risk_factors.keys()),
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=350
    )
    fig_risk.update_layout(showlegend=False, yaxis=dict(range=[0,100]))
    st.plotly_chart(fig_risk, use_container_width=True)

st.markdown("---")

st.subheader("🔥 Heatmap: Conditions by Heart Disease Status")
condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
fig, ax = plt.subplots(figsize=(3.5, 2.2))  # or whatever size you want
sns.heatmap(
    heat_df,
    annot=True,
    cmap="RdBu",    # or "YlOrRd", "coolwarm", etc.
    fmt=".1f",
    ax=ax,
    cbar=False,
    annot_kws={"size": 8}
)
ax.set_title("Percentage with Each Condition by Heart Disease Status", fontsize=10)
ax.set_xlabel("Condition", fontsize=8)
ax.set_ylabel("Heart Disease", fontsize=8)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.tight_layout()
st.pyplot(fig)


# --- More compact layout (Optional: Add more summary plots as needed) ---

# Feel free to add a small summary bar for Age Category, e.g.:
colE, colF = st.columns(2)
with colE:
    st.subheader("📊 Age Distribution (Heart Disease Patients)")
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        labels={"x": "Age Category", "y": "Count"},
        title="Age Groups",
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=300
    )
    fig_age.update_layout(showlegend=False)
    st.plotly_chart(fig_age, use_container_width=True)

with colF:
    st.subheader("🩺 General Health (Heart Disease Patients)")
    gh_counts = hd_df["GenHealth"].value_counts()
    fig_gh = px.bar(
        x=gh_counts.index,
        y=gh_counts.values,
        labels={"x": "General Health", "y": "Count"},
        title="General Health Status",
        color=gh_counts.index,
        color_discrete_sequence=px.colors.sequential.Plasma,
        height=300
    )
    fig_gh.update_layout(showlegend=False)
    st.plotly_chart(fig_gh, use_container_width=True)

# Remove footer, table, and summary; dashboard ends here.

