import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os
import plotly.graph_objects as go

st.set_page_config(page_title="Heart Disease Insights Dashboard", layout="wide")

st.title("🫀 Heart Disease Insights Dashboard")
st.markdown("""
Welcome!  
This dashboard helps you explore the profile of heart disease patients and key risk factors using the CDC BRFSS 2020 data.

- **Profile & Distribution**: See who is affected and how
- **Risk Factors**: Explore what increases the risk
- **Summary**: Key findings and recommendations

Use the sidebar filters to dive deeper!
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
    st.info("Select filters (coming soon) to personalize your view.")

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

# Filter for heart disease patients
hd_df = df[df["HeartDisease"] == "Yes"]
    
# Sidebar filters with unique keys
st.sidebar.header("🧮 Filter the Data")
gender = st.sidebar.multiselect("Select Sex", df["Sex"].unique(), default=df["Sex"].unique(), key="gender_filter")
age = st.sidebar.multiselect("Select Age Category", df["AgeCategory"].unique(), default=df["AgeCategory"].unique(), key="age_filter")
hd_status = st.sidebar.selectbox("Filter by Heart Disease Status", options=["All", "Yes", "No"], key="heart_filter")

# Apply filters
filtered_df = df[df["Sex"].isin(gender) & df["AgeCategory"].isin(age)]
if hd_status != "All":
    filtered_df = filtered_df[filtered_df["HeartDisease"] == hd_status]

# === Key Metrics ===
st.header("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Heart Disease Patients", f"{len(hd_df):,}")
    st.metric("Avg BMI", round(hd_df["BMI"].mean(), 1))
with col2:
    st.metric("Avg Sleep Time", f"{hd_df['SleepTime'].mean():.1f} hrs")
    st.metric("Smoking Rate", f"{(hd_df['Smoking'] == 'Yes').mean() * 100:.1f}%")
with col3:
    st.metric("Alcohol Use Rate", f"{(hd_df['AlcoholDrinking'] == 'Yes').mean() * 100:.1f}%")
    st.metric("Diabetes Rate", f"{(hd_df['Diabetic'] == 'Yes').mean() * 100:.1f}%")

# === Section 1: Profile & Distribution ===
st.header("🧑‍🤝‍🧑 Patient Profile & Distribution")
st.markdown("### Heart Disease Prevalence")

# Heart Disease Prevalence Pie (Filtered)
hd_counts = filtered_df["HeartDisease"].value_counts()
fig_pie = px.pie(
    names=hd_counts.index, 
    values=hd_counts.values, 
    hole=0.45, 
    title="Heart Disease Prevalence (Filtered)"
)
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("### Age Distribution")
age_counts = filtered_df["AgeCategory"].value_counts().sort_index()
fig_age = px.bar(
    x=age_counts.index, 
    y=age_counts.values, 
    labels={"x": "Age Category", "y": "Count"}, 
    title="Age Distribution"
)
st.plotly_chart(fig_age, use_container_width=True)

st.markdown("### BMI Distribution by Heart Disease Status")
fig_bmi, ax = plt.subplots()
sns.kdeplot(data=filtered_df, x="BMI", hue="HeartDisease", fill=True, common_norm=False, alpha=0.4, ax=ax)
ax.set_title("BMI Distribution by Heart Disease Status")
ax.set_xlabel("BMI")
st.pyplot(fig_bmi)

st.markdown("### General Health Distribution")
genhealth_counts = filtered_df["GenHealth"].value_counts().sort_index()
fig_gen = px.bar(
    x=genhealth_counts.index, 
    y=genhealth_counts.values, 
    labels={"x": "General Health", "y": "Count"}, 
    title="General Health (Filtered)"
)
st.plotly_chart(fig_gen, use_container_width=True)


# === Horizontal Bar Chart (Age vs Heart Disease %) ===
st.subheader("📈 Heart Disease Rate by Age Group (All Data)")
age_hd_percent = df.groupby("AgeCategory")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0)
age_hd_percent = (age_hd_percent["Yes"] * 100).sort_values()

fig_age_bar = px.bar(
    age_hd_percent,
    x=age_hd_percent.values,
    y=age_hd_percent.index,
    orientation='h',
    labels={"x": "Heart Disease Rate (%)", "y": "Age Group"},
    title="Heart Disease Rate by Age Group",
    text=age_hd_percent.round(1).astype(str) + '%'
)
st.plotly_chart(fig_age_bar)

# === Interactive Health Visualization ===
st.subheader("🎛️ Interactive Health Insights")

selected_sex = st.selectbox("Select Gender", df["Sex"].unique(), key="select_sex")
selected_age = st.selectbox("Select Age Group", df["AgeCategory"].unique(), key="select_age")

subset = df[(df["Sex"] == selected_sex) & (df["AgeCategory"] == selected_age)]

if not subset.empty:
    gh_counts = subset.groupby(["GenHealth", "HeartDisease"]).size().unstack().fillna(0)
    if "No" in gh_counts.columns and "Yes" in gh_counts.columns:
        gh_counts = gh_counts[["No", "Yes"]]

    fig_int = px.bar(
        gh_counts,
        barmode='stack',
        title=f"Heart Disease by General Health ({selected_sex}, Age {selected_age})",
        labels={"value": "Number of People", "GenHealth": "General Health"},
    )
    st.plotly_chart(fig_int)
else:
    st.warning("No data for selected filter combination.")
st.subheader("🌞 Sunburst Chart: Heart Disease Breakdown by Sex and Age")
sunburst_df = df.copy()
sunburst_fig = px.sunburst(
    sunburst_df,
    path=["Sex", "AgeCategory", "HeartDisease"],
    values=None,
    title="Nested Distribution of Heart Disease by Sex and Age",
    color="HeartDisease",
    color_discrete_map={"Yes": "crimson", "No": "lightblue"}
)
st.plotly_chart(sunburst_fig)

st.subheader("🔗 Parallel Categories: Lifestyle vs Heart Disease")
parallel_df = df[["Smoking", "AlcoholDrinking", "HeartDisease"]]
fig_parallel = px.parallel_categories(
    parallel_df,
    dimensions=["Smoking", "AlcoholDrinking", "HeartDisease"],
    color_continuous_scale=px.colors.sequential.Inferno,
    title="Lifestyle Habits and Heart Disease Relationship"
)
st.plotly_chart(fig_parallel)

st.subheader("🔗 Lifestyle vs Heart Disease (Parallel Categories)")
fig_parallel_2 = px.parallel_categories(
    df[["Smoking", "AlcoholDrinking", "HeartDisease"]],
    dimensions=["Smoking", "AlcoholDrinking", "HeartDisease"],
    color_continuous_scale=px.colors.sequential.Viridis,
    title="Variant View: Lifestyle and Heart Disease"
)
st.plotly_chart(fig_parallel_2)

st.subheader("🔥 Heatmap: Conditions by Heart Disease Status")
condition_cols = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]
heat_df = df.groupby("HeartDisease")[condition_cols].apply(lambda x: (x == "Yes").mean() * 100)
fig, ax = plt.subplots()
sns.heatmap(heat_df, annot=True, cmap="YlOrRd", fmt=".1f", ax=ax)
ax.set_title("Percentage with Each Condition by Heart Disease Status")
st.pyplot(fig)

st.subheader("📦 BMI Distribution by General Health")
fig = px.box(df, x="GenHealth", y="BMI", color="GenHealth",
             title="BMI Boxplot by General Health", points="all")
st.plotly_chart(fig)

# Diverging Bar Chart: General Health vs Heart Disease Status
st.subheader("🟦🟥 General Health Perception by Heart Disease Status")

gen_health = df.groupby(["GenHealth", "HeartDisease"]).size().unstack().fillna(0)
gen_health = gen_health.loc[["Excellent", "Very good", "Good", "Fair", "Poor"]]  # ordered

fig, ax = plt.subplots()
ax.barh(gen_health.index, -gen_health["No"], label="No Heart Disease", color="skyblue")
ax.barh(gen_health.index, gen_health["Yes"], label="With Heart Disease", color="salmon")
ax.set_title("General Health Perception by Heart Disease Status")
ax.set_xlabel("Number of People")
ax.legend(loc="lower right")
st.pyplot(fig)

# Histogram of Sleep Time
st.subheader("🛌 Sleep Time Distribution")

fig, ax = plt.subplots()
sns.histplot(df["SleepTime"], bins=20, kde=True, color="purple", ax=ax)
ax.set_title("Distribution of Sleep Time")
ax.set_xlabel("Hours of Sleep")
st.pyplot(fig)

# BMI Distribution by Heart Disease
st.subheader("⚖️ BMI Distribution by Heart Disease Status")

fig, ax = plt.subplots()
sns.kdeplot(data=df, x="BMI", hue="HeartDisease", fill=True, common_norm=False, alpha=0.4, ax=ax)
ax.set_title("BMI Distribution by Heart Disease Status")
ax.set_xlabel("BMI")
st.pyplot(fig)

# Correlation heatmap
st.subheader("📉 Correlation Heatmap (BMI, Physical & Mental Health, SleepTime)")
fig, ax = plt.subplots()
sns.heatmap(df[["BMI", "PhysicalHealth", "MentalHealth", "SleepTime"]].corr(), annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Matrix of Health Metrics")
st.pyplot(fig)

# BMI Distribution by Heart Disease
st.subheader("⚖️ BMI Distribution by Heart Disease Status")

fig, ax = plt.subplots()
sns.kdeplot(data=df, x="BMI", hue="HeartDisease", fill=True, common_norm=False, alpha=0.4, ax=ax)
ax.set_title("BMI Distribution by Heart Disease Status")
ax.set_xlabel("BMI")
st.pyplot(fig)

# BMI Distribution by Heart Disease
st.subheader("⚖️ BMI Distribution by Heart Disease Status")

fig, ax = plt.subplots()
sns.kdeplot(data=df, x="BMI", hue="HeartDisease", fill=True, common_norm=False, alpha=0.4, ax=ax)
ax.set_title("BMI Distribution by Heart Disease Status")
ax.set_xlabel("BMI")
st.pyplot(fig)

# === Section 2: Advanced Profile of Heart Disease Patients ===
st.header("🫀 Advanced Profile: Heart Disease Patients")
heart_df = filtered_df[filtered_df["HeartDisease"] == "Yes"]
st.markdown(f"**Subset size:** `{heart_df.shape}`")

# 1. Smoking & Stroke by Gender (stacked bar)
st.subheader("🚬 Smoking & Stroke by Gender")
smoke_stroke = heart_df.groupby("Sex")[["Smoking", "Stroke"]].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
smoke_stroke_melted = pd.melt(smoke_stroke, id_vars="Sex", var_name="Condition", value_name="Percentage")
fig_smoke_stroke = px.bar(
    smoke_stroke_melted,
    x="Sex",
    y="Percentage",
    color="Condition",
    barmode="stack",
    title="Smoking & Stroke Rates by Gender (Heart Disease Patients)"
)
st.plotly_chart(fig_smoke_stroke, use_container_width=True)

# 2. General Health Status
st.subheader("📋 General Health Status (Heart Disease Patients)")
gen_health = heart_df["GenHealth"].value_counts(normalize=True).sort_index() * 100
fig_genhealth = px.bar(
    x=gen_health.index,
    y=gen_health.values,
    labels={"x": "General Health", "y": "%"},
    title="Self-Reported General Health (%)"
)
st.plotly_chart(fig_genhealth, use_container_width=True)

# 3. Average BMI by Age Group (line)
st.subheader("📈 Average BMI by Age Group (Heart Disease Patients)")
bmi_age = heart_df.groupby("AgeCategory")["BMI"].mean().reset_index()
fig_bmi_age = px.line(
    bmi_age,
    x="AgeCategory",
    y="BMI",
    markers=True,
    title="Average BMI Across Age Groups"
)
st.plotly_chart(fig_bmi_age, use_container_width=True)

# 4. Age Distribution (donut)
st.subheader("🍩 Age Distribution (Heart Disease Patients)")
age_counts_hd = heart_df["AgeCategory"].value_counts().sort_index()
fig_age_hd = px.pie(
    values=age_counts_hd.values,
    names=age_counts_hd.index,
    hole=0.5,
    title="Age Breakdown of Heart Disease Patients"
)
st.plotly_chart(fig_age_hd, use_container_width=True)

# 5. Chronic Conditions Radar Chart
st.subheader("🧬 Chronic Conditions Radar (Heart Disease Patients)")
chronic_columns = ["Diabetic", "Stroke", "Asthma", "KidneyDisease", "SkinCancer"]
radar_data = {col: (heart_df[col] == "Yes").mean() * 100 for col in chronic_columns}
radar_df = pd.DataFrame({"Condition": list(radar_data.keys()), "Percentage": list(radar_data.values())})
fig_radar = go.Figure(data=go.Scatterpolar(
    r=radar_df["Percentage"],
    theta=radar_df["Condition"],
    fill='toself',
    name='Chronic Conditions %'
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    title="Chronic Conditions Radar"
)
st.plotly_chart(fig_radar, use_container_width=True)

# 6. KPIs for Heart Disease Patients
st.subheader("🔢 Key Health Indicators (Heart Disease Patients)")
avg_sleep = round(heart_df["SleepTime"].mean(), 1)
avg_bmi = round(heart_df["BMI"].mean(), 1)
excellent_health = round((heart_df["GenHealth"] == "Excellent").mean() * 100, 1)
col1, col2, col3 = st.columns(3)
col1.metric("Avg Sleep Time (hrs)", avg_sleep)
col2.metric("Avg BMI", avg_bmi)
col3.metric("% Excellent Health", f"{excellent_health}%")


import plotly.express as px
import pandas as pd

st.markdown("## 🔥 Key Heart Disease Risk Factors")

# === Section 3: Key Risk Factor Visuals ===
st.header("⚠️ Key Heart Disease Risk Factors (All Patients)")

# Smoking Status
st.subheader("🚬 Heart Disease Rate by Smoking Status")
smoke_hd = filtered_df.groupby("Smoking")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig_smoke = px.bar(
    smoke_hd,
    barmode="group",
    labels={"value": "% of Group", "Smoking": "Smoking Status", "variable": "Heart Disease"},
    title="Heart Disease Rate by Smoking Status"
)
st.plotly_chart(fig_smoke, use_container_width=True)

# Diabetic Status
st.subheader("🩸 Heart Disease Rate by Diabetic Status")
diab_hd = filtered_df.groupby("Diabetic")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig_diab = px.bar(
    diab_hd,
    barmode="group",
    labels={"value": "% of Group", "Diabetic": "Diabetic Status", "variable": "Heart Disease"},
    title="Heart Disease Rate by Diabetic Status"
)
st.plotly_chart(fig_diab, use_container_width=True)

# Alcohol Drinking
st.subheader("🍺 Heart Disease Rate by Alcohol Drinking")
alc_hd = filtered_df.groupby("AlcoholDrinking")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig_alc = px.bar(
    alc_hd,
    barmode="group",
    labels={"value": "% of Group", "AlcoholDrinking": "Alcohol Drinking", "variable": "Heart Disease"},
    title="Heart Disease Rate by Alcohol Drinking"
)
st.plotly_chart(fig_alc, use_container_width=True)

# Stroke History
st.subheader("🧠 Heart Disease Rate by Stroke History")
stroke_hd = filtered_df.groupby("Stroke")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig_stroke = px.bar(
    stroke_hd,
    barmode="group",
    labels={"value": "% of Group", "Stroke": "Stroke History", "variable": "Heart Disease"},
    title="Heart Disease Rate by Stroke History"
)
st.plotly_chart(fig_stroke, use_container_width=True)

# Physical Activity
st.subheader("🏃‍♂️ Heart Disease Rate by Physical Activity")
physact_hd = filtered_df.groupby("PhysicalActivity")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig_phys = px.bar(
    physact_hd,
    barmode="group",
    labels={"value": "% of Group", "PhysicalActivity": "Physical Activity", "variable": "Heart Disease"},
    title="Heart Disease Rate by Physical Activity"
)
st.plotly_chart(fig_phys, use_container_width=True)

# BMI Grouping
st.subheader("⚖️ Heart Disease Rate by BMI Group")
bmi_bins = [0, 18.5, 25, 30, 100]
bmi_labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
filtered_df['BMI_Group'] = pd.cut(filtered_df['BMI'], bins=bmi_bins, labels=bmi_labels)
bmi_hd = filtered_df.groupby("BMI_Group")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig_bmi = px.bar(
    bmi_hd,
    barmode="group",
    labels={"value": "% of Group", "BMI_Group": "BMI Group", "variable": "Heart Disease"},
    title="Heart Disease Rate by BMI Group"
)
st.plotly_chart(fig_bmi, use_container_width=True)

# General Health
st.subheader("🩺 Heart Disease Rate by General Health")
gen_hd = filtered_df.groupby("GenHealth")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig_gen = px.bar(
    gen_hd,
    barmode="group",
    labels={"value": "% of Group", "GenHealth": "General Health", "variable": "Heart Disease"},
    title="Heart Disease Rate by General Health"
)
st.plotly_chart(fig_gen, use_container_width=True)
