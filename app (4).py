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

hd_df = df[df["HeartDisease"] == "Yes"]
nhd_df = df[df["HeartDisease"] == "No"]

# --- KPIs ---
st.markdown(
    """
    <div style='text-align:center; margin-bottom: 0.3em;'>
        <span style='font-size:2rem; font-weight:700;'>💖 Heart Disease Insights</span>
        <br>
        <span style='font-size:1rem; color:#555;'>CDC BRFSS 2020 - Main Risk Factors & Patient Profiles</span>
    </div>
    """,
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("❤️ Heart Disease Patients", f"{len(hd_df):,}")
kpi2.metric("⚖️ Avg BMI", f"{hd_df['BMI'].mean():.1f}")
kpi3.metric("🚬 Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean()*100:.1f}%")
kpi4.metric("🍺 Alcohol Use Rate", f"{(hd_df['AlcoholDrinking'] == 'Yes').mean()*100:.1f}%")
kpi5.metric("🏃 Physical Activity", f"{(hd_df['PhysicalActivity'] == 'Yes').mean()*100:.1f}%")

st.markdown("---", unsafe_allow_html=True)

# --- Row 1: 3 main charts side by side ---
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown("##### 🧑‍🤝‍🧑 Gender Distribution")
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.5,
        height=250,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_gender.update_traces(textinfo="percent+label", textfont_size=12)
    fig_gender.update_layout(margin=dict(t=30, b=20, l=0, r=0), showlegend=False)
    st.plotly_chart(fig_gender, use_container_width=True)

with row1_col2:
    st.markdown("##### 🌡️ Key Risk Factors")
    risk_factors = [
        "Smoking", "AlcoholDrinking", "Diabetic", "PhysicalActivity",
        "Stroke", "DiffWalking", "Asthma", "KidneyDisease", "SkinCancer"
    ]
    hd_risk = []
    nhd_risk = []
    for col in risk_factors:
        if col == "PhysicalActivity":
            hd_risk.append((hd_df[col] == "No").mean() * 100)
            nhd_risk.append((nhd_df[col] == "No").mean() * 100)
        else:
            hd_risk.append((hd_df[col] == "Yes").mean() * 100)
            nhd_risk.append((nhd_df[col] == "Yes").mean() * 100)
    risk_df = pd.DataFrame({
        "Risk Factor": [
            "Smoking", "Alcohol Drinking", "Diabetic", "Not Physically Active",
            "Stroke", "Difficulty Walking", "Asthma", "Kidney Disease", "Skin Cancer"
        ],
        "Heart Disease": hd_risk,
        "No Heart Disease": nhd_risk
    })
    melt_df = risk_df.melt(id_vars="Risk Factor", value_vars=["Heart Disease", "No Heart Disease"],
                        var_name="Heart Disease Status", value_name="Prevalence (%)")
    fig, ax = plt.subplots(figsize=(4, 2.5))
    sns.barplot(
        data=melt_df,
        x="Risk Factor", y="Prevalence (%)",
        hue="Heart Disease Status",
        palette=["#e63946", "#457b9d"]
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("%")
    ax.set_xlabel("")
    ax.set_title("", fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)

with row1_col3:
    st.markdown("##### 🔥 Chronic Conditions Heatmap")
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(2.5, 2.2))
    sns.heatmap(
        heat_df,
        annot=True,
        cmap="RdBu",
        fmt=".1f",
        ax=ax,
        cbar=False,
        annot_kws={"size": 8}
    )
    ax.set_title("", fontsize=10)
    ax.set_xlabel("", fontsize=8)
    ax.set_ylabel("", fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)

# --- Row 2: 2 charts side by side ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("##### 📊 Age Distribution")
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        labels={"x": "Age Category", "y": "Count"},
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=240
    )
    fig_age.update_layout(showlegend=False, margin=dict(t=20, b=20, l=0, r=0))
    st.plotly_chart(fig_age, use_container_width=True)

with row2_col2:
    st.markdown("##### 💡 General Health Status")
    df_summary = (
        df.groupby(['HeartDisease', 'GenHealth'])
        .size()
        .reset_index(name='count')
    )
    df_summary['percent'] = df_summary.groupby('HeartDisease')['count'].transform(lambda x: x / x.sum() * 100)
    fig = px.bar(
        df_summary, 
        x="GenHealth", 
        y="percent", 
        color="HeartDisease",
        barmode="group",
        labels={"GenHealth": "General Health", "percent": "% of Group", "HeartDisease": "Heart Disease"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=240
    )
    fig.update_layout(margin=dict(t=20, b=20, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

# Optionally, you can further shrink padding or font size in some charts for ultra-compact look.

# ---- End of compact dashboard ----
