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

# --- Ultra-compact header ---
st.markdown(
    "<div style='text-align:center; font-size:1.1rem; font-weight:600; margin-bottom:0.3em;'>💖 Heart Disease Insights</div>",
    unsafe_allow_html=True
)

# --- KPI Bar with colored background ---
st.markdown(
    """
    <div style='background-color:#f5f6fa; border-radius:8px; padding:0.6em 0.2em 0.6em 0.2em; margin-bottom:0.8em;'>
    <div style='display:flex; justify-content:space-around;'>
    <span style='font-size:1rem;'>❤️ {}</span>
    <span style='font-size:1rem;'>⚖️ Avg BMI: {:.1f}</span>
    <span style='font-size:1rem;'>🚬 Smoking: {:.1f}%</span>
    <span style='font-size:1rem;'>🍺 Alcohol: {:.1f}%</span>
    <span style='font-size:1rem;'>🏃 Activity: {:.1f}%</span>
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

# --- 2 rows, 3 columns grid for charts (leave last cell blank or use for logo) ---
row1 = st.columns(3)
row2 = st.columns(3)

# --- Chart 1: Gender Pie ---
with row1[0]:
    gender_counts = hd_df["Sex"].value_counts()
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        hole=0.65,
        height=200,
        width=200,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_gender.update_traces(textinfo="percent+label", textfont_size=10)
    fig_gender.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=False, font=dict(size=10))
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
    fig, ax = plt.subplots(figsize=(2.5, 1.4))
    sns.barplot(
        data=melt_df,
        x="Risk Factor", y="Prevalence (%)",
        hue="HD",
        palette=["#e63946", "#457b9d"]
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("%", fontsize=8)
    ax.set_xlabel("")
    ax.set_title("", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

# --- Chart 3: Heatmap ---
with row1[2]:
    condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
    heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
    fig, ax = plt.subplots(figsize=(1.6, 1.4))
    sns.heatmap(
        heat_df,
        annot=True,
        cmap="RdBu",
        fmt=".1f",
        ax=ax,
        cbar=False,
        annot_kws={"size": 8}
    )
    ax.set_title("", fontsize=9)
    ax.set_xlabel("", fontsize=8)
    ax.set_ylabel("", fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)

# --- Chart 4: Age Distribution ---
with row2[0]:
    age_counts = hd_df["AgeCategory"].value_counts().sort_index()
    fig_age = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        color=age_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis,
        height=200,
        width=200
    )
    fig_age.update_layout(showlegend=False, font=dict(size=10), margin=dict(t=10, b=10, l=10, r=10))
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
        height=200,
        width=200
    )
    fig.update_layout(font=dict(size=10), margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

# --- Last slot: Leave blank or place your logo, or a short insight ---
with row2[2]:
    st.markdown(
        "<div style='height:210px; display:flex; align-items:center; justify-content:center; color:#aaa;'>"
        "Powered by Streamlit</div>",
        unsafe_allow_html=True
    )
