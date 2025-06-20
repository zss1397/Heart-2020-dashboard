import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(layout="wide")
st.title("🫀 Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

# Load CSV safely
csv_filename = "heart_2020_cleaned (1).csv"
if not os.path.exists(csv_filename):
    st.error("❌ CSV file not found. Please ensure it's uploaded correctly with the exact name.")
    st.stop()

# Load data
df = pd.read_csv(csv_filename)
st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")

# Display column names
with st.expander("🧾 Columns:"):
    st.json({i: col for i, col in enumerate(df.columns)})

# ===============================
# 📊 Key Indicators (All Data)
# ===============================
st.markdown("### 🗂️ Key Indicators (All Data)")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric("Total Patients", f"{len(df):,}")
with col2:
    heart_disease_pct = (df["HeartDisease"] == "Yes").mean() * 100
    st.metric("Heart Disease %", f"{heart_disease_pct:.1f}%")
with col3:
    avg_sleep = df["SleepTime"].mean()
    st.metric("Avg Sleep Time", f"{avg_sleep:.1f} hrs")
with col4:
    avg_bmi = df["BMI"].mean()
    st.metric("Avg BMI", f"{avg_bmi:.1f}")
with col5:
    smoking_pct = (df["Smoking"] == "Yes").mean() * 100
    st.metric("Smoking Rate", f"{smoking_pct:.1f}%")
with col6:
    alcohol_pct = (df["AlcoholDrinking"] == "Yes").mean() * 100
    st.metric("Alcohol Use Rate", f"{alcohol_pct:.1f}%")

# ===============================
# Sidebar Filters
# ===============================
st.sidebar.header("🧪 Filter the Data")
gender = st.sidebar.multiselect("Select Sex", df["Sex"].unique(), default=df["Sex"].unique())
age = st.sidebar.multiselect("Select Age Category", df["AgeCategory"].unique(), default=df["AgeCategory"].unique())

# Apply Filters
filtered_df = df[
    (df["Sex"].isin(gender)) &
    (df["AgeCategory"].isin(age))
]
st.write("Filtered dataset size:", filtered_df.shape)

# ===============================
# 📊 Filtered Data Display
# ===============================
st.subheader("🔍 Filtered Data")
st.dataframe(filtered_df)

# ===============================
# 📊 Heart Disease Pie Chart
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
# 📊 Bar Chart by Sex
# ===============================
st.subheader("Heart Disease by Sex")
sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)
if not sex_counts.empty:
    fig2, ax2 = plt.subplots()
    sex_counts.plot(kind="bar", stacked=True, ax=ax2)
    ax2.set_ylabel("Number of People")
    ax2.set_title("Heart Disease Prevalence by Sex")
    st.pyplot(fig2)

# ===============================
# 📊 Bar Chart by Age Category
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

# ===============================
# 📊 Heart Disease by General Health (All Data)
# ===============================
st.subheader("Heart Disease by General Health (All Data)")
genhealth_counts = df.groupby(["GenHealth", "HeartDisease"]).size().unstack().fillna(0)
if not genhealth_counts.empty:
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    genhealth_counts.plot(kind="bar", stacked=True, ax=ax4)
    ax4.set_ylabel("Number of People")
    ax4.set_title("Heart Disease Prevalence by General Health")
    st.pyplot(fig4)

# ===============================
# 🔥 Correlation Heatmap (All Data)
# ===============================
st.markdown("### 📉 Correlation Heatmap (BMI, Physical & Mental Health, SleepTime)")
corr_df = df[["BMI", "PhysicalHealth", "MentalHealth", "SleepTime"]]
fig5, ax5 = plt.subplots()
sns.heatmap(corr_df.corr(), annot=True, cmap="coolwarm", ax=ax5)
st.pyplot(fig5)
