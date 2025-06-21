import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Title
st.title("❤️ Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

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

st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")

# Sidebar filters with unique keys
st.sidebar.header("🧮 Filter the Data")
gender = st.sidebar.multiselect("Select Sex", df["Sex"].unique(), default=df["Sex"].unique(), key="gender_filter")
age = st.sidebar.multiselect("Select Age Category", df["AgeCategory"].unique(), default=df["AgeCategory"].unique(), key="age_filter")
hd_status = st.sidebar.selectbox("Filter by Heart Disease Status", options=["All", "Yes", "No"], key="heart_filter")

# Apply filters
filtered_df = df[df["Sex"].isin(gender) & df["AgeCategory"].isin(age)]
if hd_status != "All":
    filtered_df = filtered_df[filtered_df["HeartDisease"] == hd_status]

st.markdown(f"**Filtered dataset size:** `{filtered_df.shape}`")
st.dataframe(filtered_df.head())

# === Key Metrics ===
st.header("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Patients", f"{len(df):,}")
    st.metric("Avg BMI", round(df["BMI"].mean(), 1))
with col2:
    st.metric("Heart Disease %", f"{(df['HeartDisease'] == 'Yes').mean() * 100:.1f}%")
    st.metric("Smoking Rate", f"{(df['Smoking'] == 'Yes').mean() * 100:.1f}%")
with col3:
    st.metric("Avg Sleep Time", f"{df['SleepTime'].mean():.1f} hrs")
    st.metric("Alcohol Use Rate", f"{(df['AlcoholDrinking'] == 'Yes').mean() * 100:.1f}%")

# === Donut Chart ===
st.subheader("❤️ Heart Disease Proportion (Donut Chart)")
fig = px.pie(df, names="HeartDisease", hole=0.4, title="Heart Disease Proportion", color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig)

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

# 1. Stacked Bar: Smoking & Stroke vs Heart Disease by Gender
st.subheader("🚬 Smoking & Stroke Rates by Gender")

heart_df = df[df["HeartDisease"] == "Yes"]

smoke_stroke = heart_df.groupby("Sex")[["Smoking", "Stroke"]].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
smoke_stroke_melted = pd.melt(smoke_stroke, id_vars="Sex", var_name="Condition", value_name="Percentage")

fig_smoke_stroke = px.bar(smoke_stroke_melted, x="Sex", y="Percentage", color="Condition", barmode="stack", title="Smoking & Stroke Among Heart Disease Patients")
st.plotly_chart(fig_smoke_stroke, use_container_width=True)

# 2. Bar: General Health Perception Among Heart Disease Patients
st.subheader("📋 General Health Status")

gen_health = heart_df["GenHealth"].value_counts(normalize=True).sort_index() * 100
fig2 = px.bar(x=gen_health.index, y=gen_health.values, title="Self-Reported General Health (%)", labels={"x": "Health Status", "y": "%"})
st.plotly_chart(fig2, use_container_width=True)

# 3. Line Chart: BMI Trend by Age Group
st.subheader("📈 Average BMI by Age Group")

bmi_age = heart_df.groupby("AgeCategory")["BMI"].mean().reset_index()
fig3 = px.line(bmi_age, x="AgeCategory", y="BMI", markers=True, title="Average BMI Across Age Groups")
st.plotly_chart(fig3, use_container_width=True)

# 4. Donut Chart: Age Distribution
st.subheader("🍩 Age Distribution")

age_counts = heart_df["AgeCategory"].value_counts().sort_index()
fig4 = px.pie(values=age_counts.values, names=age_counts.index, hole=0.5, title="Age Breakdown of Heart Disease Patients")
st.plotly_chart(fig4, use_container_width=True)

# 5. Radar Chart: Chronic Condition Prevalence
st.subheader("🧬 Chronic Conditions Radar")

chronic_columns = ["Diabetic", "Stroke", "Asthma", "KidneyDisease", "SkinCancer"]
radar_data = {col: (heart_df[col] == "Yes").mean() * 100 for col in chronic_columns}
radar_df = pd.DataFrame({"Condition": list(radar_data.keys()), "Percentage": list(radar_data.values())})

fig5 = go.Figure(data=go.Scatterpolar(
    r=radar_df["Percentage"],
    theta=radar_df["Condition"],
    fill='toself',
    name='Chronic Conditions %'
))
fig5.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Chronic Conditions Radar")
st.plotly_chart(fig5, use_container_width=True)

# 6. KPIs: Sleep, BMI, Excellent Health %
st.subheader("🔢 Key Health Indicators (Heart Disease Patients)")
avg_sleep = round(heart_df["SleepTime"].mean(), 1)
avg_bmi = round(heart_df["BMI"].mean(), 1)
excellent_health = round((heart_df["GenHealth"] == "Excellent").mean() * 100, 1)

col1, col2, col3 = st.columns(3)
col1.metric("Avg Sleep Time (hrs)", avg_sleep)
col2.metric("Avg BMI", avg_bmi)
col3.metric("% Reporting Excellent Health", f"{excellent_health}%")

st.subheader("🚬 Heart Disease Rate by Smoking Status")
smoke_hd = df.groupby("Smoking")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0) * 100
fig = px.bar(
    smoke_hd,
    barmode="group",
    labels={"value": "% of Group", "Smoking": "Smoking Status", "variable": "Heart Disease"},
    title="Heart Disease Rate by Smoking Status"
)
st.plotly_chart(fig, use_container_width=True)
