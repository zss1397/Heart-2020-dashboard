import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
csv_path = "heart_2020_cleaned (1).csv"
try:
    df = pd.read_csv(csv_path)
    st.success(f"✅ CSV loaded successfully. Shape: {df.shape}")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Show column names to confirm file loaded
st.subheader("Columns:")
st.write(list(df.columns))

# Show title
st.title("Heart Disease Indicators Dashboard (2020)")
st.markdown("Analyze risk factors for heart disease using CDC BRFSS 2020 data.")

# Confirm dataset loaded
st.write("Filtered dataset size:", df.shape)

# DEBUG: Check for actual data
st.write("Sample data:", df.head())

# ✅ Try rendering a basic pie chart (no filters)
st.subheader("Heart Disease Pie Chart")
if "HeartDisease" in df.columns:
    hd_count = df["HeartDisease"].value_counts()
    st.write("HeartDisease count:", hd_count)

    fig, ax = plt.subplots()
    ax.pie(hd_count.values, labels=hd_count.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
else:
    st.error("HeartDisease column not found in the dataset.")
