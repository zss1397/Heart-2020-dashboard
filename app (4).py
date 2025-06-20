import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import seaborn as sns
import numpy as np

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
df = pd.read_csv(csv_filename)
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

# ====================
# Filtered Visuals
# ====================
st.header("📊 Visualizations (Filtered Data)")

# 1. Pie Chart (Heart Disease)
st.subheader("Heart Disease Distribution (Pie Chart)")
hd_count = filtered_df["HeartDisease"].value_counts()
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

# ===========================
# Advanced Visualizations (All Data)
# ===========================

import seaborn as sns
import numpy as np

st.markdown("---")
st.subheader("📊 Advanced Visualizations (Entire Dataset)")

# 1. Health Conditions vs Heart Disease (Stacked Bar)
st.markdown("### 1️⃣ Health Conditions vs Heart Disease (Stacked Bar)")
conditions = ["Smoking", "AlcoholDrinking", "Stroke", "DiffWalking", "Diabetic", "Asthma", "KidneyDisease", "SkinCancer"]
condition_data = []

for cond in conditions:
    counts = df.groupby([cond, "HeartDisease"]).size().unstack().fillna(0)
    if "Yes" in counts.columns:
        percent = (counts["Yes"] / counts.sum(axis=1)) * 100
        condition_data.append(percent)

bar_df = pd.DataFrame(condition_data, index=conditions).T.fillna(0)

fig1, ax1 = plt.subplots(figsize=(10, 5))
bar_df.plot(kind="bar", stacked=True, ax=ax1)
ax1.set_title("Proportion with Heart Disease by Health Condition")
ax1.set_ylabel("Percentage")
plt.xticks(rotation=45)
st.pyplot(fig1)

# 2. General Health vs Heart Disease (Diverging Bar)
st.markdown("### 2️⃣ General Health vs Heart Disease (Diverging Bar)")
gen_health = df.groupby(["GenHealth", "HeartDisease"]).size().unstack().fillna(0)
gen_health = gen_health.reindex(["Poor", "Fair", "Good", "Very good", "Excellent"])

fig2, ax2 = plt.subplots(figsize=(8, 5))
gen_health.plot(kind='bar', ax=ax2, color=["#ff9999", "#66b3ff"])
ax2.set_title("Heart Disease by General Health")
ax2.set_ylabel("Count")
plt.xticks(rotation=30)
st.pyplot(fig2)

# 3. Sleep Time Distribution
st.markdown("### 3️⃣ Sleep Time Distribution")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.histplot(data=df, x="SleepTime", hue="HeartDisease", kde=True, bins=30, ax=ax3)
ax3.set_title("Distribution of Sleep Time by Heart Disease")
st.pyplot(fig3)

# 4. BMI Distribution by Heart Disease
st.markdown("### 4️⃣ BMI Distribution by Heart Disease")
fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.kdeplot(data=df, x="BMI", hue="HeartDisease", fill=True, common_norm=False, alpha=0.5, ax=ax4)
ax4.set_title("BMI Distribution by Heart Disease Status")
st.pyplot(fig4)

# 5. Radar Chart: Chronic Conditions
st.markdown("### 5️⃣ Chronic Conditions Radar Chart (Proportions)")

radar_labels = ['Asthma', 'KidneyDisease', 'SkinCancer', 'Stroke', 'Diabetic']
yes_props = [df[df[c]=="Yes"]["HeartDisease"].value_counts(normalize=True).get("Yes", 0) for c in radar_labels]

angles = np.linspace(0, 2 * np.pi, len(radar_labels), endpoint=False).tolist()
yes_props += yes_props[:1]
angles += angles[:1]

fig5 = plt.figure(figsize=(6, 6))
ax5 = fig5.add_subplot(111, polar=True)
ax5.plot(angles, yes_props, 'o-', linewidth=2)
ax5.fill(angles, yes_props, alpha=0.25)
ax5.set_thetagrids(np.degrees(angles[:-1]), radar_labels)
ax5.set_title("Proportion with Heart Disease among Chronic Conditions")
st.pyplot(fig5)

# 6. Simulated Trend (Age vs Heart Disease %)
st.markdown("### 6️⃣ Simulated Age Trend of Heart Disease Prevalence")
age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
             '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
age_trend = df.groupby("AgeCategory")["HeartDisease"].apply(lambda x: (x=="Yes").mean()).reindex(age_order)

fig6, ax6 = plt.subplots(figsize=(10, 4))
age_trend.plot(marker='o', ax=ax6)
ax6.set_ylabel("Proportion with Heart Disease")
ax6.set_title("Heart Disease Prevalence by Age Category")
plt.xticks(rotation=45)
st.pyplot(fig6)

