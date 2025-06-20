import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file with exact filename
try:
    df = pd.read_csv("heart_2020_cleaned (1).csv")
    st.success("✅ CSV loaded successfully. Shape: {}".format(df.shape))
    st.write("**Columns:**")
    st.write(list(df.columns))
except FileNotFoundError:
    st.error("❌ CSV file not found. Please check the file name and make sure it’s uploaded to GitHub correctly.")
    st.stop()

# Title and description
st.title("Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

# Display sample data
st.write("**Sample data:**")
st.dataframe(df.head())

# Pie chart for Heart Disease
st.subheader("Heart Disease Pie Chart")
hd_count = df["HeartDisease"].value_counts()
st.write("**HeartDisease count:**")
hd_df = hd_count.reset_index()
hd_df.columns = ["HeartDisease", "Count"]
st.dataframe(hd_df)

fig1, ax1 = plt.subplots()
ax1.pie(hd_count.values, labels=hd_count.index, autopct='%1.1f%%', startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

# Bar chart by Sex
st.subheader("Heart Disease by Sex")
sex_counts = df.groupby(["Sex", "HeartDisease"]).size().unstack().fillna(0)

fig2, ax2 = plt.subplots()
sex_counts.plot(kind="bar", stacked=True, ax=ax2, color=["#1f77b4", "#ff7f0e"])
ax2.set_ylabel("Count")
ax2.set_title("Heart Disease Distribution by Sex")
st.pyplot(fig2)

# Bar chart by Age Category
st.subheader("Heart Disease by Age Category")
age_order = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
             '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
age_counts = df.groupby(["AgeCategory", "HeartDisease"]).size().unstack().fillna(0)
age_counts = age_counts.reindex(age_order).dropna(how='all')

fig3, ax3 = plt.subplots(figsize=(10, 5))
age_counts.plot(kind="bar", stacked=True, ax=ax3, color=["#1f77b4", "#ff7f0e"])
ax3.set_ylabel("Count")
ax3.set_title("Heart Disease Distribution by Age Group")
plt.xticks(rotation=45)
st.pyplot(fig3)


