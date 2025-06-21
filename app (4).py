import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import seaborn as sns
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# Title
st.title("❤️ Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

# Load CSV safely
csv_filename = "heart_2020_cleaned (1).csv"
if not os.path.exists(csv_filename):
    st.error("❌ CSV file not found. Please ensure it's uploaded correctly with the exact name.")
    st.stop()

# Load data
try:
    df = pd.read_csv(csv_filename)
    st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")
except Exception as e:
    st.error(f"❌ Failed to load CSV: {e}")
    st.stop()
st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")

# Display column names for reference
with st.expander("🧾 Columns"):
    st.json({i: col for i, col in enumerate(df.columns)})

# ====================
# SIDEBAR FILTERS
# ====================
st.sidebar.header("🧮 Filter the Data")
gender = st.sidebar.multiselect("Select Sex", df["Sex"].unique(), default=df["Sex"].unique())
age = st.sidebar.multiselect("Select Age Category", df["AgeCategory"].unique(), default=df["AgeCategory"].unique())

# Apply Filters
filtered_df = df[(df["Sex"].isin(gender)) & (df["AgeCategory"].isin(age))]

st.markdown(f"**Filtered dataset size:** `{filtered_df.shape}`")

# Show filtered data
st.subheader("🔍 Filtered Data")
st.dataframe(filtered_df)

if filtered_df.empty:
    st.warning("⚠️ Filtered dataset is empty. Try adjusting your sidebar filters.")


# ====================
# Filtered Visuals
# ====================
st.header("📊 Visualizations (Filtered Data)")

# 1. Pie Chart (Heart Disease)
st.subheader("Heart Disease Distribution (Pie Chart)")
hd_count = df["HeartDisease"].value_counts()  # For testing on full data
if not hd_count.empty:
    fig1, ax1 = plt.subplots()
    ax1.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

# 2. Bar Chart by Sex
st.subheader("Heart Disease by Sex")
sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)
if not sex_counts.empty:
    fig2, ax2 = plt.subplots()
    sex_counts.plot(kind="bar", stacked=True, ax=ax2)
    ax2.set_ylabel("Number of People")
    ax2.set_title("Heart Disease Prevalence by Sex")
    st.pyplot(fig2)

# 3. Bar Chart by Age Category
st.subheader("Heart Disease by Age Category")
age_counts = filtered_df.groupby(["AgeCategory", "HeartDisease"]).size().unstack().fillna(0)
if not age_counts.empty:
    age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
                 '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
    age_counts = age_counts.reindex(age_order).dropna(how='all')
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    age_counts.plot(kind="bar", stacked=True, ax=ax3)
    ax3.set_ylabel("Number of People")
    ax3.set_title("Heart Disease Prevalence by Age Group")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# ====================
# Key Indicators (All Data)
# ====================
st.header("🗂️ Key Indicators (All Data)")

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

# ====================
# Visuals (All Data)
# ====================
st.header("📊 Additional Insights (All Data, Not Filtered)")

# Correlation heatmap
st.subheader("Correlation Heatmap (BMI, Physical & Mental Health, SleepTime)")
fig4, ax4 = plt.subplots()
sns.heatmap(df[["BMI", "PhysicalHealth", "MentalHealth", "SleepTime"]].corr(), annot=True, cmap="coolwarm", ax=ax4)
st.pyplot(fig4)

# Average Sleep Time by General Health
st.subheader("Average Sleep Time by General Health")
avg_sleep = df.groupby("GenHealth")["SleepTime"].mean().sort_values()
fig5, ax5 = plt.subplots()
avg_sleep.plot(kind="bar", ax=ax5, color="green")
ax5.set_ylabel("Average Sleep Time")
ax5.set_title("Sleep Time by General Health")
st.pyplot(fig5)

# Heart Disease by Smoking
st.subheader("Heart Disease vs Smoking")
smoke_counts = df.groupby(["Smoking", "HeartDisease"]).size().unstack().fillna(0)
fig6, ax6 = plt.subplots()
smoke_counts.plot(kind="bar", stacked=True, ax=ax6)
ax6.set_ylabel("Count")
ax6.set_title("Heart Disease Prevalence by Smoking Status")
st.pyplot(fig6)

# Heart Disease by Diabetes
st.subheader("Heart Disease by Diabetes Status")
diabetes_counts = df.groupby(["Diabetic", "HeartDisease"]).size().unstack().fillna(0)
fig7, ax7 = plt.subplots()
diabetes_counts.plot(kind="bar", stacked=True, ax=ax7)
ax7.set_ylabel("Number of People")
ax7.set_title("Heart Disease Prevalence by Diabetes Status")
st.pyplot(fig7)

# Heart Disease by General Health
st.subheader("Heart Disease by General Health (All Data)")
gen_health_counts = df.groupby(["GenHealth", "HeartDisease"]).size().unstack().fillna(0)
fig8, ax8 = plt.subplots()
gen_health_counts.plot(kind="bar", stacked=True, ax=ax8)
ax8.set_ylabel("Number of People")
ax8.set_title("Heart Disease by General Health")
st.pyplot(fig8)

# ====================
# Radar Chart: Heart Disease Prevalence by General Health
# ====================
st.subheader("🕸️ Heart Disease Prevalence by General Health (Radar Chart)")

# Prepare data
radar_data = df.groupby("GenHealth")["HeartDisease"].value_counts(normalize=True).unstack().fillna(0)
if "Yes" in radar_data.columns:
    radar_yes = radar_data["Yes"]
    categories = list(radar_yes.index)
    values = radar_yes.values.tolist()
    values += values[:1]  # repeat first value to close the circle

    # Radar chart setup
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='orange', linewidth=2)
    ax.fill(angles, values, color='orange', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title("Heart Disease % by General Health", size=14, weight='bold')

    st.pyplot(fig)
else:
    st.info("No heart disease data found for radar chart.")

# Radar Chart: Chronic Conditions Prevalence by Heart Disease Status
st.subheader("🕸️ Chronic Conditions Radar Chart (Heart Disease vs No Heart Disease)")

# List of chronic conditions in dataset
chronic_columns = ["Stroke", "Diabetic", "KidneyDisease", "Asthma"]

# Calculate proportions for each condition
radar_data = {}
for condition in chronic_columns:
    counts = df.groupby("HeartDisease")[condition].value_counts(normalize=True).unstack().fillna(0)
    radar_data[condition] = [counts.loc["Yes", "Yes"] * 100, counts.loc["No", "Yes"] * 100]

labels = list(radar_data.keys())
HD_Yes = [radar_data[cond][0] for cond in labels]
HD_No = [radar_data[cond][1] for cond in labels]

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
HD_Yes += HD_Yes[:1]
HD_No += HD_No[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, HD_Yes, color="red", linewidth=2, label="Heart Disease: Yes")
ax.fill(angles, HD_Yes, color="red", alpha=0.25)

ax.plot(angles, HD_No, color="blue", linewidth=2, label="Heart Disease: No")
ax.fill(angles, HD_No, color="blue", alpha=0.25)

ax.set_thetagrids(np.degrees(angles[:-1]), labels)
ax.set_title("Chronic Conditions Comparison")
ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
st.pyplot(fig)

# Diverging Bar Chart: General Health vs Heart Disease
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
st.pyplot(fig)

st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")

st.write(df.head())
st.write(df.columns)

st.header("🧮 Dataset Overview")

# Show a few rows
st.subheader("🔍 Preview of Dataset")
st.dataframe(df.head())

# Show basic statistics
st.subheader("📈 Statistical Summary")
st.write(df.describe())

# Show column names and types
st.subheader("🧾 Column Info")
st.write(df.dtypes)

# Heart Disease Pie Chart
st.header("❤️ Heart Disease Distribution")

hd_counts = df["HeartDisease"].value_counts()

if not hd_counts.empty:
    fig, ax = plt.subplots()
    ax.pie(hd_counts.values, labels=hd_counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Proportion of Heart Disease Cases")
    ax.axis('equal')  # Equal aspect ratio ensures pie chart is a circle
    st.pyplot(fig)
else:
    st.warning("No heart disease data available.")

# Pie Chart: Heart Disease Distribution (Filtered)
st.subheader("🧠 Heart Disease Distribution (Pie Chart)")

hd_count = filtered_df["HeartDisease"].value_counts()

if not hd_count.empty:
    fig, ax = plt.subplots()
    ax.pie(hd_count, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures a perfect circle
    st.pyplot(fig)
else:
    st.warning("⚠️ No data available for selected filters to display the pie chart.")

# Heart Disease Distribution - Full Dataset
st.subheader("Heart Disease Distribution (All Data)")
full_hd_count = df["HeartDisease"].value_counts()

if not full_hd_count.empty:
    fig_full, ax_full = plt.subplots()
    ax_full.pie(full_hd_count.values, labels=full_hd_count.index, autopct='%1.1f%%', startangle=90)
    ax_full.axis('equal')
    st.pyplot(fig_full)
else:
    st.warning("No data available to show.")

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

st.subheader("🎛️ Interactive Health Insights")

# Interactive dropdowns
selected_sex = st.selectbox("Select Gender", df["Sex"].unique())
selected_age = st.selectbox("Select Age Group", df["AgeCategory"].unique())

# Filter
subset = df[(df["Sex"] == selected_sex) & (df["AgeCategory"] == selected_age)]

# Bar chart
gh_counts = subset.groupby(["GenHealth", "HeartDisease"]).size().unstack().fillna(0)
gh_counts = gh_counts[["No", "Yes"]] if "No" in gh_counts.columns and "Yes" in gh_counts.columns else gh_counts

fig_int = px.bar(
    gh_counts,
    barmode='stack',
    title=f"Heart Disease by General Health ({selected_sex}, Age {selected_age})",
    labels={"value": "Number of People", "GenHealth": "General Health"},
)
st.plotly_chart(fig_int)

# Horizontal Bar Chart: Heart Disease Rate by Age Group
st.subheader("Heart Disease Rate by Age Group (All Data)")
age_heart_rate = df.groupby("AgeCategory")["HeartDisease"].apply(lambda x: (x == "Yes").mean() * 100)
age_heart_rate = age_heart_rate.reindex(['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
                                         '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older'])
fig, ax = plt.subplots(figsize=(8, 5))
age_heart_rate.plot(kind="barh", ax=ax, color="steelblue")
ax.set_xlabel("Percentage with Heart Disease")
ax.set_ylabel("Age Group")
ax.set_title("Heart Disease Prevalence by Age")
st.pyplot(fig)

# === DEBUG BLOCK ===
st.subheader("✅ Debugging Visual Display")

# Check filtered data
st.write("Filtered Data Size:", filtered_df.shape)

# Check HeartDisease column presence
if "HeartDisease" in filtered_df.columns:
    st.success("✅ 'HeartDisease' column exists in filtered data.")
    st.write("HeartDisease value counts (filtered):")
    st.write(filtered_df["HeartDisease"].value_counts())
else:
    st.error("❌ 'HeartDisease' column missing!")

# Check full data too
st.write("HeartDisease value counts (full dataset):")
st.write(df["HeartDisease"].value_counts())

# Show head of filtered data
st.write("🔍 Sample filtered data:")
st.write(filtered_df.head())

if filtered_df.empty:
    st.warning("⚠️ Filtered dataset is empty. Try adjusting your sidebar filters.")
else:
    # All the visuals go here (pie chart, bar charts, etc.)

