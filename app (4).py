import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
try:
    df = pd.read_csv("heart_2020_cleaned.csv")
    st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")
    st.write("Columns:", df.columns.to_list())
except FileNotFoundError:
    st.error("❌ CSV file not found. Please check the file name and make sure it’s uploaded to GitHub correctly.")
    st.stop()

# App title
st.title("Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

# Sidebar filters
st.sidebar.header("Filter the Data")
gender = st.sidebar.multiselect("Select Sex", df["Sex"].unique(), default=df["Sex"].unique())
age = st.sidebar.multiselect("Select Age Category", df["AgeCategory"].unique(), default=df["AgeCategory"].unique())
race = st.sidebar.multiselect("Select Race", df["Race"].unique(), default=df["Race"].unique())

# Apply filters
filtered_df = df[
    (df["Sex"].isin(gender)) &
    (df["AgeCategory"].isin(age)) &
    (df["Race"].isin(race))
]

# Show filtered dataset size
st.write("Filtered dataset size:", filtered_df.shape)

# Filtered data preview
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Heart disease summary
st.subheader("Heart Disease Summary")
hd_count = filtered_df["HeartDisease"].value_counts()
st.dataframe(hd_count.reset_index().rename(columns={'index': 'HeartDisease', 'HeartDisease': 'count'}))

# Pie chart
st.subheader("Heart Disease Breakdown (Pie Chart)")
if not hd_count.empty:
    fig1, ax1 = plt.subplots()
    ax1.pie(hd_count, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
else:
    st.warning("No data available for selected filters.")

# Bar chart by Sex
st.subheader("Heart Disease by Sex")
sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)
if not sex_counts.empty:
    fig2, ax2 = plt.subplots()
    sex_counts.plot(kind="bar", stacked=True, ax=ax2, color=["#1f77b4", "#ff7f0e"])
    ax2.set_ylabel("Number of People")
    ax2.set_title("Heart Disease Prevalence by Sex")
    st.pyplot(fig2)
else:
    st.info("No data to display for selected filters.")

# Bar chart by Age Category
st.subheader("Heart Disease by Age Category")
age_counts = filtered_df.groupby(["AgeCategory", "HeartDisease"]).size().unstack().fillna(0)

# Ensure logical age order
age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
             '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
age_counts = age_counts.reindex(age_order).dropna(how='all')

if not age_counts.empty:
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    age_counts.plot(kind="bar", stacked=True, ax=ax3, color=["#1f77b4", "#ff7f0e"])
    ax3.set_ylabel("Number of People")
    ax3.set_title("Heart Disease Prevalence by Age Group")
    plt.xticks(rotation=45)
    st.pyplot(fig3)
else:
    st.info("No age-related data to display.")
