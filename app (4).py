import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

# Title
st.title("Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

csv_filename = "heart_2020_cleaned (1).csv"

# Check if file exists
if not os.path.exists(csv_filename):
    st.error("❌ CSV file not found.")
    st.stop()
else:
    st.success("✅ CSV file found. Now loading...")

try:
    df = pd.read_csv(csv_filename)
    st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")
except pd.errors.EmptyDataError:
    st.error("❌ CSV is empty or unreadable.")
    st.stop()

# Display column names for reference
st.write("Columns:")
st.json({i: col for i, col in enumerate(df.columns)})

# Sidebar Filters
st.sidebar.header("Filter the Data")
gender = st.sidebar.multiselect("Select Sex", df["Sex"].unique(), default=df["Sex"].unique())
age = st.sidebar.multiselect("Select Age Category", df["AgeCategory"].unique(), default=df["AgeCategory"].unique())
race = st.sidebar.multiselect("Select Race", df["Race"].unique(), default=df["Race"].unique())

# Apply Filters
filtered_df = df[
    (df["Sex"].isin(gender)) &
    (df["AgeCategory"].isin(age)) &
    (df["Race"].isin(race))
]

st.write("Filtered dataset size:", filtered_df.shape)

# Show filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# ===============================
# Visual 1: Pie Chart (HeartDisease)
# ===============================
st.subheader("Heart Disease Distribution (Pie Chart)")
hd_count = filtered_df["HeartDisease"].value_counts()

if not hd_count.empty:
    fig1, ax1 = plt.subplots()
    ax1.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
else:
    st.warning("⚠️ No data available for the selected filters.")

# ===============================
# Visual 2: Bar Chart by Sex
# ===============================
st.subheader("Heart Disease by Sex")
sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)

if not sex_counts.empty:
    fig2, ax2 = plt.subplots()
    sex_counts.plot(kind="bar", stacked=True, ax=ax2)
    ax2.set_ylabel("Number of People")
    ax2.set_title("Heart Disease Prevalence by Sex")
    st.pyplot(fig2)
else:
    st.info("No data to display by Sex.")

# ===============================
# Visual 3: Bar Chart by Age Category
# ===============================
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
else:
    st.info("No data to display by Age Group.")

st.markdown("---")
st.header("📊 Additional Insights (All Data, Not Filtered)")

# Heatmap of correlations
st.subheader("Correlation Heatmap (BMI, Physical & Mental Health, SleepTime)")
import seaborn as sns
import numpy as np

corr_features = ["BMI", "PhysicalHealth", "MentalHealth", "SleepTime"]
corr_matrix = df[corr_features].corr()

fig4, ax4 = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax4)
st.pyplot(fig4)

# Histogram of BMI
st.subheader("BMI Distribution")
fig5, ax5 = plt.subplots()
ax5.hist(df["BMI"], bins=30, color='skyblue', edgecolor='black')
ax5.set_xlabel("BMI")
ax5.set_ylabel("Count")
st.pyplot(fig5)

# Average SleepTime by General Health
st.subheader("Average Sleep Time by General Health")
sleep_by_health = df.groupby("GenHealth")["SleepTime"].mean().sort_values()

fig6, ax6 = plt.subplots()
sleep_by_health.plot(kind="bar", ax=ax6, color='green')
ax6.set_ylabel("Average Sleep Time (hours)")
ax6.set_title("Sleep Time by General Health")
st.pyplot(fig6)

# Stacked Bar: Heart Disease vs Smoking
st.subheader("Heart Disease vs Smoking")
smoke_counts = df.groupby(["Smoking", "HeartDisease"]).size().unstack().fillna(0)
fig7, ax7 = plt.subplots()
smoke_counts.plot(kind="bar", stacked=True, ax=ax7, color=["#1f77b4", "#ff7f0e"])
ax7.set_ylabel("Count")
ax7.set_title("Heart Disease Prevalence by Smoking Status")
st.pyplot(fig7)

# ===============================
# 📊 Additional Insights (All Data, Not Filtered)
# ===============================
st.markdown("## 📊 Additional Insights (All Data, Not Filtered)")

# 1. Correlation Heatmap
st.subheader("Correlation Heatmap (BMI, Physical & Mental Health, SleepTime)")
import seaborn as sns

numeric_cols = ["BMI", "PhysicalHealth", "MentalHealth", "SleepTime"]
corr_matrix = df[numeric_cols].corr()

fig_corr, ax_corr = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax_corr)
st.pyplot(fig_corr)

# 2. General Health Distribution
st.subheader("General Health Distribution")
genhealth_counts = df["GenHealth"].value_counts()

fig_gen, ax_gen = plt.subplots()
genhealth_counts.plot(kind="bar", color="skyblue", ax=ax_gen)
ax_gen.set_ylabel("Count")
ax_gen.set_title("General Health Ratings")
st.pyplot(fig_gen)

# 3. Diabetes vs Heart Disease
st.subheader("Heart Disease by Diabetes Status")
diabetes_hd = df.groupby(["Diabetic", "HeartDisease"]).size().unstack().fillna(0)

fig_dia, ax_dia = plt.subplots()
diabetes_hd.plot(kind="bar", stacked=True, ax=ax_dia)
ax_dia.set_ylabel("Number of People")
ax_dia.set_title("Heart Disease Prevalence by Diabetes Status")
st.pyplot(fig_dia)


