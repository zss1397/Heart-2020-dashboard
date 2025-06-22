import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size': 8, 'font.family': 'sans-serif'})
st.set_page_config(page_title="Heart Disease Dashboard", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 11px !important;
        font-family: 'Segoe UI', 'Roboto', Arial, sans-serif !important;
    }
    .block-container {
        padding-top: 0.3rem;
        padding-bottom: 0.3rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .st-emotion-cache-10trblm {margin-bottom: 0.12rem;}
    h1, h2, h3, h4, h5, h6 {
        font-size: 1rem !important;
        margin-bottom: 0.05rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
    <div style='text-align:center; font-size:1.12rem; font-weight:600; margin-bottom:0.45em; color:#b11f4a;'>
        💖 Heart Disease Insights
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style='background-color:#f7f7fa; border-radius:8px; padding:0.4em 0.2em 0.4em 0.2em; margin-bottom:0.7em;
        display: flex; justify-content: center; gap: 2em;'>
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
        (hd_df['PhysicalActivity'] == 'Yes').mean() * 100,
    ),
    unsafe_allow_html=True
)

row1 = st.columns([1, 1.3, 1.2], gap="small")
row2 = st.columns(2, gap="small")

with row1[0]:
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.62,
        height=150,
        width=150,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_gender.update_traces(textinfo="percent+label", textfont_size=10)
    fig_gender.update_layout(
        margin=dict(t=0, b=0, l=0, r=0), showlegend=False, 
        font=dict(size=10)
    )
    st.markdown("<div style='text-align:center; font-size:0.88rem; margin-bottom:0.1em;'>By Gender</div>", unsafe_allow_html=True)
    st.plotly_chart(fig_gender, use_container_width=True)

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
    fig, ax = plt.subplots(figsize=(2.2, 1.3))
    sns.barplot(
        data=melt_df,
        x="Risk Factor", y="Prevalence (%)",
        hue="HD",
        palette=["#e63946", "#457b9d"]
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("%", fontsize=8)
    ax.set_xlabel("")
    ax.set_title("")
    ax.legend(fontsize=7, title='')
    plt.tight_layout(pad=0.2)
    st.markdown("<div style='text-align:center; font-size:0.88rem; margin-bottom:0.1em;'>Risk Factors</div>", unsafe_allow_html=True)
    st.pyplot(fig)

with row1[2]:
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(1.2, 1.2))
    sns.heatmap(
        heat_df,
        annot=True,
        cmap="RdBu",
        fmt=".1f",
        ax=ax,
        cbar=False,
        annot_kws={"size": 8}
    )
    ax.set_title("")
    ax.set_xlabel("", fontsize=8)
    ax.set_ylabel("", fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout(pad=0.2)
    st.markdown("<div style='text-align:center; font-size:0.88rem; margin-bottom:0.1em;'>Comorbidities</div>", unsafe_allow_html=True)
    st.pyplot(fig)

with row2[0]:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=180
    )
    fig_age.update_layout(
        showlegend=False, font=dict(size=9),
        margin=dict(t=10, b=0, l=0, r=0),
        xaxis_title='Age', yaxis_title='Count'
    )
    st.markdown("<div style='text-align:center; font-size:0.88rem; margin-bottom:0.1em;'>By Age Group</div>", unsafe_allow_html=True)
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
        height=180
    )
    fig.update_layout(
        font=dict(size=9),
        margin=dict(t=10, b=0, l=0, r=0)
    )
    st.markdown("<div style='text-align:center; font-size:0.88rem; margin-bottom:0.1em;'>By General Health</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
