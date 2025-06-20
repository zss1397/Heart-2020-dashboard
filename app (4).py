import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("heart_2020_cleaned (1).csv")  # change if you rename the file

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

# Handle empty result
if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters.")
else:
    st.write("Filtered dataset size:", filtered_df.shape)

    # Display table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Heart disease summary
    st.subheader("Heart Disease Prevalence")
    hd_count = filtered_df["HeartDisease"].value_counts()
    st.write("With Heart Disease:", int(hd_count.get("Yes", 0)))
    st.write("Without Heart Disease:", int(hd_count.get("No", 0)))

    # Pie chart
    st.subheader("Heart Disease Breakdown (Pie Chart)")
    fig, ax = plt.subplots()
    ax.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Bar chart by sex
    st.subheader("Heart Disease by Sex")
    sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)
    fig, ax = plt.subplots()
    sex_counts.plot(kind="bar", stacked=True, ax=ax, color=["#1f77b4", "#ff7f0e"])
    ax.set_ylabel("Number of People")
    ax.set_title("Heart Disease Prevalence by Sex")
    st.pyplot(fig)

    # Bar chart by age category
    st.subheader("Heart Disease by Age Category")
    age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
                 '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
    age_counts = (
        filtered_df.groupby(["AgeCategory", "HeartDisease"])
        .size()
        .unstack()
        .fillna(0)
        .reindex(age_order)
        .dropna(how='all')
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    age_counts.plot(kind="bar", stacked=True, ax=ax, color=["#1f77b4", "#ff7f0e"])
    ax.set_ylabel("Number of People")
    ax.set_title("Heart Disease Prevalence by Age Group")
    plt.xticks(rotation=45)
    st.pyplot(fig)


