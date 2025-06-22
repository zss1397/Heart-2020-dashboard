import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- GLOBAL FONT AND PADDING FIX ---
plt.rcParams.update({'font.size': 8, 'font.family': 'sans-serif'})

st.set_page_config(page_title="Heart Disease Dashboard", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 12px !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 0.3rem;
        padding-bottom: 0.3rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }
    .st-emotion-cache-10trblm {margin-bottom: 0.15rem;}
    h1, h2, h3, h4, h5, h6 {
        font-size: 1rem !important;
        margin-bottom: 0.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

# --- Ultra-compact header ---
st.markdown(
    "<div style='text-align:center; font-size:0.95rem; font-weight:600; margin-bottom:0.12em;'>💖 Heart Disease Insights</div>",
    unsafe_allow_html=True
)

# --- KPI Bar with colored background ---
st.markdown(
    """
    <div style='background-color:#f5f6fa; border-radius:8px; padding:0.28em 0.09em 0.28em 0.09em; margin-bottom:0.15em;'>
    <div style='display:flex; justify-content:space-around;'>
    <span style='font-size:0.85rem;'>❤️ {}</span>
    <span style='font-size:0.85rem;'>⚖️ Avg BMI: {:.1f}</span>
    <span style='font-size:0.85rem;'>🚬 Smoking: {:.1f}%</span>
    <span style='font-size:0.85rem;'>🍺 Alcohol: {:.1f}%</span>
    <span style='font-size:0.85rem;'>🏃 Activity: {:.1f}%</span>
    </div>
    </div>
    """.format(
        f"{len(hd_df):,}",
        hd_df['BMI'].mean(),
        (hd_df['Smoking'] == 'Yes').mean()*100,
        (hd_df['AlcoholDrinking'] == 'Yes').mean()*100,
        (hd_df['PhysicalActivity'] == 'Yes').mean()*100,
    ),
    unsafe_allow_html=True
)

# --- 2 rows, 3 columns grid for charts ---
row1 = st.columns(3, gap="small")
row2 = st.columns(3, gap="small")

# --- Chart 1: Gender Pie ---
with row1[0]:
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.65,
        height=120,
        width=120,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_gender.update_traces(textinfo="percent+label", textfont_size=8)
    fig_gender.update_layout(
        margin=dict(t=0, b=0, l=0, r=0), showlegend=False, 
        font=dict(size=8, family="Segoe UI, Roboto, Arial, sans-serif")
    )
    st.plotly_chart(fig_gender, use_container_width=True)

# --- Chart 2: Risk Factors Bar ---
with row1[1]:
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
    fig, ax = plt.subplots(figsize=(1.1, 1))
    sns.barplot(
        data=melt_df,
        x="Risk Factor", y="Prevalence (%)",
        hue="HD",
        palette=["#e63946", "#457b9d"]
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("%", fontsize=7)
    ax.set_xlabel("")
    ax.set_title("", fontsize=8)
    plt.tight_layout(pad=0.4)
    ax.legend(fontsize=6)
    st.pyplot(fig)

# --- Chart 3: Heatmap ---
with row1[2]:
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(0.95, 1))
    sns.heatmap(
        heat_df,
        annot=True,
        cmap="RdBu",
        fmt=".1f",
        ax=ax,
        cbar=False,
        annot_kws={"size": 7}
    )
    ax.set_title("", fontsize=8)
    ax.set_xlabel("", fontsize=7)
    ax.set_ylabel("", fontsize=7)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.tight_layout(pad=0.4)
    st.pyplot(fig)

# --- Chart 4: Age Distribution ---
with row2[0]:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=120,
        width=120
    )
    fig_age.update_layout(
        showlegend=False, font=dict(size=8, family="Segoe UI, Roboto, Arial, sans-serif"),
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_age, use_container_width=True)

# --- Chart 5: GenHealth ---
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
        height=120,
        width=120
    )
    fig.update_layout(
        font=dict(size=8, family="Segoe UI, Roboto, Arial, sans-serif"),
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Last slot: Leave blank or place your logo, or a short insight ---
with row2[2]:
    st.markdown(
        "<div style='height:140px; display:flex; align-items:center; justify-content:center; color:#aaa;'>"
        "Powered by Streamlit</div>",
        unsafe_allow_html=True
    )
