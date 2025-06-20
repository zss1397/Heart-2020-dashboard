import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")

# Title
st.title("Heart Disease Indicators Dashboard (2020)")
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




