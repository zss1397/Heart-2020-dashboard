import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("heart_2020_cleaned (1).csv")

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

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Summary of heart disease
st.subheader("Heart Disease Prevalence")
hd_count = filtered_df["HeartDisease"].value_counts()
st.write("With Heart Disease:", int(hd_count.get("Yes", 0)))
st.write("Without Heart Disease:", int(hd_count.get("No", 0)))

# Pie chart of heart disease in filtered data
st.subheader("Heart Disease Breakdown (Pie Chart)")
if not hd_count.empty:
    fig, ax = plt.subplots()
    labels = hd_count.index
    sizes = hd_count.values
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures pie is circular.
    st.pyplot(fig)
else:
    st.write("No data available for selected filters.")
if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters. Try broadening your selection.")
else:
    st.dataframe(filtered_df)

    st.subheader("Heart Disease Prevalence")
    hd_count = filtered_df["HeartDisease"].value_counts()
    st.write("With Heart Disease:", int(hd_count.get("Yes", 0)))
    st.write("Without Heart Disease:", int(hd_count.get("No", 0)))

    st.subheader("Heart Disease Breakdown (Pie Chart)")
    fig, ax = plt.subplots()
    ax.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

