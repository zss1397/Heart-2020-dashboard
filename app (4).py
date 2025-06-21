import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import os

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

st.subheader("🔗 Parallel Categories: Lifestyle vs Heart Disease")
parallel_df = df[["Smoking", "AlcoholDrinking", "HeartDisease"]]
fig_parallel = px.parallel_categories(
    parallel_df,
    dimensions=["Smoking", "AlcoholDrinking", "HeartDisease"],
    color_continuous_scale=px.colors.sequential.Inferno,
    title="Lifestyle Habits and Heart Disease Relationship"
)
st.plotly_chart(fig_parallel)

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


