import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("heart_2020_cleaned.csv")

# Title
st.title("Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

# Sidebar filters
st.sidebar.header("Filter the Data")

sex_filter = st.sidebar.multiselect("Select Sex", options=df["Sex"].unique(), default=df["Sex"].unique())
age_filter = st.sidebar.multiselect("Select Age Category", options=df["AgeCategory"].unique(), default=df["AgeCategory"].unique())
race_filter = st.sidebar.multiselect("Select Race", options=df["Race"].unique(), default=df["Race"].unique())

# Apply filters
filtered_df = df[
    (df["Sex"].isin(sex_filter)) &
    (df["AgeCategory"].isin(age_filter)) &
    (df["Race"].isin(race_filter))
]

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Heart disease summary
st.subheader("Heart Disease Prevalence in Filtered Data")
heart_counts = filtered_df["HeartDisease"].value_counts()
st.write("Total Records:", len(filtered_df))
st.write("With Heart Disease:", int(heart_counts.get("Yes", 0)))
st.write("Without Heart Disease:", int(heart_counts.get("No", 0)))
