import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def display_dashboard():
    # Set page configuration
    st.set_page_config(page_title="📚 Book Price Dashboard", page_icon="📚", layout="wide")

    # Add custom styling
    st.markdown("""
        <style>
            .main {
                background-color: #f8f9fc;
            }
            h1, h2, h3 {
                color: #4a69bd;
            }
            .sidebar .sidebar-content {
                background-color: #dfe6e9;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("📚 Book Price Dashboard")

    # Load dataset from SQLite database
    conn = sqlite3.connect("books.db")
    df = pd.read_sql_query("SELECT * FROM books", conn)

    # Clean and preprocess data
    df["price"] = df["price"].str.replace("£", "").str.replace("Â", "").astype(float)

    # Sidebar filters
    st.sidebar.title("Filter Options")

    price_min, price_max = st.sidebar.slider(
        "Select Price Range (£)", 
        min_value=float(df["price"].min()), 
        max_value=float(df["price"].max()), 
        value=(float(df["price"].min()), float(df["price"].max()))
    )

    rating_options = df["rating"].unique()
    selected_ratings = st.sidebar.multiselect(
        "Select Ratings",
        options=rating_options,
        default=rating_options
    )

    availability_options = ["In stock", "Out of stock"]
    selected_availability = st.sidebar.multiselect(
        "Select Availability",
        options=availability_options,
        default=availability_options
    )

    # Apply filters to the dataset
    filtered_df = df[
        (df["price"] >= price_min) &
        (df["price"] <= price_max) &
        (df["rating"].isin(selected_ratings)) &
        (df["availability"].isin(selected_availability))
    ]

    st.subheader("📊 Filtered Data")
    st.dataframe(filtered_df)

    # Search Bar for Book Titles
    st.subheader("🔍 Search for a Book")
    query = st.text_input("Enter book title:")
    if query:
        search_results = filtered_df[filtered_df["title"].str.contains(query, case=False, na=False)]
        if not search_results.empty:
            st.write("Search Results:")
            st.dataframe(search_results)
        else:
            st.write("No matching books found.")

    # Visualizations
    st.subheader("📈 Price Distribution")
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        filtered_df["price"].plot(kind="hist", bins=20, color="#FF5733", edgecolor="black", alpha=0.9, ax=ax)
        ax.set_title("Filtered Book Price Distribution", fontsize=14)
        ax.set_xlabel("Price (£)")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.warning("No data available for price distribution.")

    st.subheader("📦 Book Availability")
    availability_counts = filtered_df["availability"].value_counts()
    if not availability_counts.empty:
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(availability_counts, labels=availability_counts.index, autopct="%1.1f%%", colors=["#6a89cc", "#82ccdd"])
        ax_pie.set_title("Availability Distribution")
        st.pyplot(fig_pie)
    else:
        st.warning("No data available for availability distribution.")

    st.subheader("⭐ Book Ratings")
    rating_counts = filtered_df["rating"].value_counts()
    if not rating_counts.empty:
        fig_ratings, ax_ratings = plt.subplots(figsize=(7, 4))
        rating_counts.plot(kind="bar", color="#1F77B4", ax=ax_ratings)
        ax_ratings.set_title("Book Rating Distribution", fontsize=14)
        ax_ratings.set_xlabel("Rating")
        ax_ratings.set_ylabel("Count")
        st.pyplot(fig_ratings)
    else:
        st.warning("No data available for rating distribution.")

    # Top 5 Expensive Books
    st.subheader("💸 Top 5 Expensive Books")
    if not filtered_df.empty:
        st.table(filtered_df.nlargest(5, "price"))
    else:
        st.warning("No data available for top expensive books.")

    # Download filtered data
    st.sidebar.download_button(
        label="Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_books.csv",
        mime="text/csv"
    )

# ✅ Call the function to display the dashboard
if __name__ == "__main__":
    display_dashboard()
