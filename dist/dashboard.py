import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Streamlit configuration
st.set_page_config(page_title="📚 Book Price Dashboard", page_icon="📚", layout="wide")

# Title and description
st.title("📚 Book Monitoring Dashboard")
st.markdown("This dashboard allows you to explore and filter book metadata, including pricing, ratings, and availability.")

# Connect to the database and load metadata
conn = sqlite3.connect("books.db")
df = pd.read_sql_query("SELECT * FROM books", conn)
df["price"] = df["price"].str.replace("£", "").str.replace("Â", "").astype(float)
conn.close()

# Sidebar filters
st.sidebar.subheader("Filter Options")

# Price range slider
price_min, price_max = st.sidebar.slider(
    "Select Price Range (£)", 
    min_value=float(df["price"].min()), 
    max_value=float(df["price"].max()), 
    value=(float(df["price"].min()), float(df["price"].max()))
)

# Rating filter
rating_options = df["rating"].unique()
selected_ratings = st.sidebar.multiselect(
    "Select Ratings", 
    options=rating_options, 
    default=rating_options
)

# Availability filter
availability_options = ["In stock", "Out of stock"]
selected_availability = st.sidebar.multiselect(
    "Select Availability", 
    options=availability_options, 
    default=availability_options
)

# Apply filters
filtered_df = df[
    (df["price"] >= price_min) & 
    (df["price"] <= price_max) & 
    (df["rating"].isin(selected_ratings)) & 
    (df["availability"].isin(selected_availability))
]

# Display filtered data
st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# Visualization: Price distribution
st.subheader("📈 Filtered Price Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
filtered_df["price"].plot(kind="hist", bins=20, color="#FF5733", edgecolor="black", alpha=0.9, ax=ax)
ax.set_title("Filtered Price Distribution", fontsize=16)
ax.set_xlabel("Price (£)")
ax.set_ylabel("Count")
st.pyplot(fig)

# Visualization: Ratings bar chart
st.subheader("⭐ Ratings Distribution")
rating_counts = filtered_df["rating"].value_counts()
if rating_counts.empty:
    st.warning("No data available for ratings.")
else:
    fig, ax = plt.subplots()
    rating_counts.plot(kind="bar", color="#1F77B4", ax=ax)
    ax.set_title("Ratings Distribution", fontsize=16)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Download filtered data
st.sidebar.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_books.csv",
    mime="text/csv"
)
