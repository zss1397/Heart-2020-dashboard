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

st.subheader("🌡️ Key Risk Factors: With vs Without Heart Disease")

risk_factors = [
    "Smoking", "AlcoholDrinking", "Diabetic", "PhysicalActivity",
    "Stroke", "DiffWalking", "Asthma", "KidneyDisease", "SkinCancer"
]

# Calculate prevalence for each group
hd_risk = []
nhd_risk = []

for col in risk_factors:
    # For PhysicalActivity, we flip "Yes" to "No" to indicate inactivity as risk
    if col == "PhysicalActivity":
        hd_risk.append((hd_df[col] == "No").mean() * 100)
        nhd_risk.append((nhd_df[col] == "No").mean() * 100)
    else:
        hd_risk.append((hd_df[col] == "Yes").mean() * 100)
        nhd_risk.append((nhd_df[col] == "Yes").mean() * 100)

# Prepare DataFrame for plotting
risk_df = pd.DataFrame({
    "Risk Factor": [
        "Smoking", "Alcohol Drinking", "Diabetic", "Not Physically Active",
        "Stroke", "Difficulty Walking", "Asthma", "Kidney Disease", "Skin Cancer"
    ],
    "Heart Disease": hd_risk,
    "No Heart Disease": nhd_risk
})

# Melt for seaborn
melt_df = risk_df.melt(id_vars="Risk Factor", value_vars=["Heart Disease", "No Heart Disease"],
                       var_name="Heart Disease Status", value_name="Prevalence (%)")

fig, ax = plt.subplots(figsize=(7, 2.8))
sns.barplot(
    data=melt_df,
    x="Risk Factor", y="Prevalence (%)",
    hue="Heart Disease Status",
    palette=["#e63946", "#457b9d"]
)
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
ax.set_ylabel("% of Patients")
ax.set_xlabel("")
ax.set_title("Risk Factor Prevalence by Heart Disease Status", fontsize=14, fontweight="bold", loc="left")
plt.tight_layout()
st.pyplot(fig)

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

import pandas as pd
import plotly.express as px

# Assuming df has "HeartDisease" and "GenHealth"
df_summary = (
    df.groupby(['HeartDisease', 'GenHealth'])
    .size()
    .reset_index(name='count')
)

# Calculate percentage within each group
df_summary['percent'] = df_summary.groupby('HeartDisease')['count'].transform(lambda x: x / x.sum() * 100)

fig = px.bar(
    df_summary, 
    x="GenHealth", 
    y="percent", 
    color="HeartDisease",
    barmode="group",
    labels={"GenHealth": "General Health", "percent": "% of Group", "HeartDisease": "Heart Disease"},
    title="General Health Distribution by Heart Disease Status",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig, use_container_width=True)


