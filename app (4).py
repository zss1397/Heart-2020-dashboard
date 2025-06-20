import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(r"heart_2020_cleaned (1).csv")

st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")

# Show column names to confirm
st.markdown("### Columns:")
st.write(list(df.columns))

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

# Sample data
st.markdown("#### Sample data:")
st.dataframe(filtered_df.head())

# Pie chart: Heart Disease count
st.markdown("## Heart Disease Pie Chart")
hd_count = filtered_df["HeartDisease"].value_counts()
st.write("HeartDisease count:")
st.dataframe(hd_count.reset_index(names=["HeartDisease", "Count"]))


if not hd_count.empty:
    fig, ax = plt.subplots()
    ax.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.warning("No data to show pie chart.")

# Bar chart: Heart Disease by Sex
st.markdown("## Heart Disease by Sex")
sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)
if not sex_counts.empty:
    fig, ax = plt.subplots()
    sex_counts.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel("Count")
    ax.set_title("Heart Disease Prevalence by Sex")
    st.pyplot(fig)
else:
    st.warning("No data to show bar chart by sex.")

# Bar chart: Heart Disease by Age
st.markdown("## Heart Disease by Age Category")
age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
             '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
age_counts = filtered_df.groupby(["AgeCategory", "HeartDisease"]).size().unstack().fillna(0)
age_counts = age_counts.reindex(age_order).dropna(how='all')

if not age_counts.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    age_counts.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel("Count")
    ax.set_title("Heart Disease Prevalence by Age Group")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("No data to show bar chart by age.")
