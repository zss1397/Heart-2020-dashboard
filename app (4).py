import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns

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

# --- Compact Intro ---
st.markdown(
    """
    <div style='text-align:center; margin-bottom: 0.1em;'>
        <span style='font-size:1.7rem; font-weight:700;'>💖 Heart Disease Insights</span>
        <br>
        <span style='font-size:0.92rem; color:#555;'>CDC BRFSS 2020 - Main Risk Factors & Patient Profiles</span>
    </div>
    """,
    unsafe_allow_html=True
)

# --- KPIs ---
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("❤️ Patients", f"{len(hd_df):,}")
kpi2.metric("⚖️ Avg BMI", f"{hd_df['BMI'].mean():.1f}")
kpi3.metric("🚬 Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean()*100:.1f}%")
kpi4.metric("🍺 Alcohol Use", f"{(hd_df['AlcoholDrinking'] == 'Yes').mean()*100:.1f}%")
kpi5.metric("🏃 Physical Active", f"{(hd_df['PhysicalActivity'] == 'Yes').mean()*100:.1f}%")

# --- Ultra-Compact Row 1: 3 Charts Side by Side ---
col1, col2, col3 = st.columns(3)

with col1:
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.6,
        height=140,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_gender.update_traces(textinfo="percent+label", textfont_size=8)
    fig_gender.update_layout(margin=dict(t=5, b=5, l=0, r=0), showlegend=False, font=dict(size=8))
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
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
    fig, ax = plt.subplots(figsize=(2.2, 1.0))
    sns.barplot(
        data=melt_df,
        x="Risk Factor", y="Prevalence (%)",
        hue="Heart Disease Status",
        palette=["#e63946", "#457b9d"]
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=7)
    ax.set_ylabel("%", fontsize=7)
    ax.set_xlabel("")
    ax.set_title("", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)

with col3:
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(1.25, 0.95))
    sns.heatmap(
        heat_df,
        annot=True,
        cmap="RdBu",
        fmt=".1f",
        ax=ax,
        cbar=False,
        annot_kws={"size": 7}
    )
    ax.set_title("", fontsize=7)
    ax.set_xlabel("", fontsize=7)
    ax.set_ylabel("", fontsize=7)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.tight_layout()
    st.pyplot(fig)

# --- Ultra-Compact Row 2: 2 Charts Side by Side ---
col4, col5 = st.columns(2)

with col4:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=140
    )
    fig_age.update_layout(showlegend=False, font=dict(size=8), margin=dict(t=5, b=5, l=0, r=0))
    st.plotly_chart(fig_age, use_container_width=True)

with col5:
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
        height=140
    )
    fig.update_layout(font=dict(size=8), margin=dict(t=5, b=5, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
