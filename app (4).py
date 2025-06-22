import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Heart Disease Dashboard", layout="wide")

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

st.markdown(
    """
    <div style='text-align:center; margin-bottom:-1em; margin-top:-2em;'>
        <span style='font-size:1.2rem; font-weight:600;'>💖 Heart Disease Insights</span><br>
        <span style='font-size:0.95rem; color:#666;'>CDC BRFSS 2020 - Main Risk Factors & Patient Profiles</span>
    </div>
    """,
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5, gap="small")
kpi1.metric("❤️ Heart Disease Patients", f"{len(hd_df):,}")
kpi2.metric("⚖️ Avg BMI", f"{hd_df['BMI'].mean():.1f}")
kpi3.metric("🚬 Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean()*100:.1f}%")
kpi4.metric("🍺 Alcohol Use Rate", f"{(hd_df['AlcoholDrinking'] == 'Yes').mean()*100:.1f}%")
kpi5.metric("🏃 Physical Activity", f"{(hd_df['PhysicalActivity'] == 'Yes').mean()*100:.1f}%")
col1, col2, col3, col4 = st.columns(4)

with col1:
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.65,
        height=100,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_gender.update_traces(textinfo="percent+label", textfont_size=6)
    fig_gender.update_layout(margin=dict(t=2, b=2, l=2, r=2), showlegend=False, font=dict(size=6))
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
            "Smoking", "Alcohol", "Diabetic", "No Activity",
            "Stroke", "Diff Walk", "Asthma", "Kidney", "SkinCa"
        ],
        "Heart Disease": hd_risk,
        "No Heart Disease": nhd_risk
    })
    melt_df = risk_df.melt(id_vars="Risk Factor", value_vars=["Heart Disease", "No Heart Disease"],
                        var_name="HD", value_name="Prevalence (%)")
    fig, ax = plt.subplots(figsize=(1.1, 0.7))
    sns.barplot(
        data=melt_df,
        x="Risk Factor", y="Prevalence (%)",
        hue="HD",
        palette=["#e63946", "#457b9d"]
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=5)
    ax.set_ylabel("%", fontsize=5)
    ax.set_xlabel("")
    ax.set_title("", fontsize=6)
    plt.tight_layout()
    st.pyplot(fig)

with col3:
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(0.8, 0.7))
    sns.heatmap(
        heat_df,
        annot=True,
        cmap="RdBu",
        fmt=".1f",
        ax=ax,
        cbar=False,
        annot_kws={"size": 5}
    )
    ax.set_title("", fontsize=6)
    ax.set_xlabel("", fontsize=5)
    ax.set_ylabel("", fontsize=5)
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    plt.tight_layout()
    st.pyplot(fig)

with col4:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=100
    )
    fig_age.update_layout(showlegend=False, font=dict(size=6), margin=dict(t=2, b=2, l=2, r=2))
    st.plotly_chart(fig_age, use_container_width=True)
