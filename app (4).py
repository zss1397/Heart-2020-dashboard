import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif'})
st.set_page_config(page_title="Heart Disease Dashboard", layout="wide")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 13px !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 0.6rem;
        padding-bottom: 0.6rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .st-emotion-cache-10trblm {margin-bottom: 0.15rem;}
    h1, h2, h3, h4, h5, h6 {
        font-size: 1.1rem !important;
        margin-bottom: 0.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

csv_filename = "heart_2020_cleaned (1).csv"
if not os.path.exists(csv_filename):
    st.error("❌ CSV file not found.")
    st.stop()
df = pd.read_csv(csv_filename)
hd_df = df[df["HeartDisease"] == "Yes"]
nhd_df = df[df["HeartDisease"] == "No"]

# --- Header & KPIs (thin) ---
st.markdown(
    """
    <div style='text-align:center; font-size:1.15rem; font-weight:600; margin-bottom:0.4em; color:#b11f4a;'>
        💖 Heart Disease Insights
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style='background-color:#f7f7fa; border-radius:9px; padding:0.4em 0.4em 0.4em 0.4em; margin-bottom:1.1em;
        display: flex; justify-content: center; gap: 3em;'>
        <span>❤️ {:,}</span>
        <span>⚖️ Avg BMI: {:.1f}</span>
        <span>🚬 Smoking: {:.1f}%</span>
        <span>🍺 Alcohol: {:.1f}%</span>
        <span>🏃 Activity: {:.1f}%</span>
    </div>
    """.format(
        len(hd_df),
        hd_df['BMI'].mean(),
        (hd_df['Smoking'] == 'Yes').mean() * 100,
        (hd_df['AlcoholDrinking'] == 'Yes').mean() * 100,
        (hd_df['PhysicalActivity'] == 'No').mean() * 100,
    ),
    unsafe_allow_html=True
)

# --- Top Row: Risk Factors | Heatmap | Gender Pie ---
row1 = st.columns([1.8, 1.2, 0.7], gap="small")

# --- Chart 1: Risk Factors Bar (horizontal, wide, clear) ---
with row1[0]:
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
    fig, ax = plt.subplots(figsize=(5, 2.3))
    sns.barplot(
        data=melt_df,
        x="Prevalence (%)",
        y="Risk Factor",
        hue="HD",
        palette=["#e63946", "#457b9d"],
        orient="h"
    )
    ax.set_xlabel("%", fontsize=10)
    ax.set_ylabel("")
    ax.set_title("Risk Factors", fontsize=11, pad=8)
    ax.legend(fontsize=9, title='', loc='lower right')
    plt.tight_layout(pad=0.6)
    st.pyplot(fig, use_container_width=True)

# --- Chart 2: Comorbidities Heatmap (clear, neat) ---
with row1[1]:
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(2.4, 2.1))
    sns.heatmap(
        heat_df,
        annot=True,
        cmap="RdBu",
        fmt=".1f",
        ax=ax,
        cbar=False,
        annot_kws={"size": 10}
    )
    ax.set_title("Comorbidities (%)", fontsize=11, pad=8)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)

# --- Chart 3: Gender Pie (small, clear, legend vertical right) ---
with row1[2]:
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.45,  # Slightly thicker donut
        height=170,
        width=170,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_gender.update_traces(
        textinfo='label+percent',
        textposition='inside',
        insidetextorientation='horizontal',
        textfont_size=14
    )
    fig_gender.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        showlegend=False,
        font=dict(size=13),
        title_text="By Gender",
        title_font=dict(size=12),
        title_x=0.5
    )
    st.plotly_chart(fig_gender, use_container_width=True)

# --- Bottom Row: Age Group | General Health ---
row2 = st.columns(2, gap="small")

with row2[0]:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=200
    )
    fig_age.update_layout(
        showlegend=False, font=dict(size=11),
        margin=dict(t=12, b=0, l=0, r=0),
        xaxis_title='Age Group', yaxis_title='Count',
        title=dict(text="By Age Group", x=0.5, font=dict(size=11))
    )
    st.plotly_chart(fig_age, use_container_width=True)

with row2[1]:
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
        height=200
    )
    fig.update_layout(
        font=dict(size=11),
        margin=dict(t=12, b=0, l=0, r=0),
        title=dict(text="By General Health", x=0.5, font=dict(size=11))
    )
    st.plotly_chart(fig, use_container_width=True)
