import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
try:
    df = pd.read_csv("heart_2020_cleaned (1).csv")
    st.success("✅ CSV loaded successfully. Shape: {}".format(df.shape))
    st.markdown("**Columns:**")
    st.write(list(df.columns))
except Exception as e:
    st.error(f"Failed to load data: {e}")
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

st.write("Filtered dataset size:", filtered_df.shape)
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Show warning if data is empty
if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters. Try broadening your selection.")
    st.stop()

# Pie chart of Heart Disease distribution
st.subheader("Heart Disease Breakdown (Pie Chart)")
hd_count = filtered_df["HeartDisease"].value_counts()
if not hd_count.empty:
    fig, ax = plt.subplots()
    ax.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.info("No data to display.")

# Bar chart: Heart Disease by Sex
st.subheader("Heart Disease by Sex")
sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)
if not sex_counts.empty:
    fig, ax = plt.subplots()
    sex_counts.plot(kind="bar", stacked=True, ax=ax, color=["#1f77b4", "#ff7f0e"])
    ax.set_ylabel("Number of People")
    ax.set_title("Heart Disease Prevalence by Sex")
    st.pyplot(fig)
else:
    st.info("No data to display.")

# Bar chart: Heart Disease by Age Category
st.subheader("Heart Disease by Age Group")
age_counts = filtered_df.groupby(["AgeCategory", "HeartDisease"]).size().unstack().fillna(0)

# Reorder age categories for logic
age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
             '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
age_counts = age_counts.reindex(age_order).dropna(how='all')

if not age_counts.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    age_counts.plot(kind="bar", stacked=True, ax=ax, color=["#1f77b4", "#ff7f0e"])
    ax.set_ylabel("Number of People")
    ax.set_title("Heart Disease Prevalence by Age Group")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("No data to display.")
