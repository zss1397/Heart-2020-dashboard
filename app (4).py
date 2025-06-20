import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
try:
    df = pd.read_csv("heart_2020_cleaned (1).csv")
    st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")
    st.markdown("### Columns:")
    st.write(list(df.columns))
except Exception as e:
    st.error(f"❌ Error loading CSV: {e}")
    st.stop()

# App Title
st.title("Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

# Sidebar Filters
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

st.markdown(f"**Filtered dataset size:** `{filtered_df.shape}`")
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# If empty, stop everything else
if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters. Try broadening your selection.")
    st.stop()

# Heart Disease Prevalence (Pie Chart)
st.subheader("Heart Disease Breakdown (Pie Chart)")
hd_count = filtered_df["HeartDisease"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

# Bar Chart: Heart Disease by Sex
st.subheader("Heart Disease by Sex")
sex_counts = filtered_df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)
fig2, ax2 = plt.subplots()
sex_counts.plot(kind="bar", stacked=True, ax=ax2, color=["#1f77b4", "#ff7f0e"])
ax2.set_ylabel("Number of People")
ax2.set_title("Heart Disease Prevalence by Sex")
st.pyplot(fig2)

# Bar Chart: Heart Disease by Age
st.subheader("Heart Disease by Age Group")
age_counts = filtered_df.groupby(["AgeCategory", "HeartDisease"]).size().unstack().fillna(0)

# Logical sorting
age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
             '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
age_counts = age_counts.reindex(age_order).dropna(how="all")

fig3, ax3 = plt.subplots(figsize=(10, 5))
age_counts.plot(kind="bar", stacked=True, ax=ax3, color=["#1f77b4", "#ff7f0e"])
ax3.set_ylabel("Number of People")
ax3.set_title("Heart Disease Prevalence by Age Group")
plt.xticks(rotation=45)
st.pyplot(fig3)
