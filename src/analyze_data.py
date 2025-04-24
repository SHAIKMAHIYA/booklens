import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_prices():
    # Load data
    conn = sqlite3.connect("books.db")
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()

    df["price"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)

    # Check for empty data
    if df.empty:
        raise ValueError("No data available in the database.")

    # Display stats in a structured format
    price_stats = df["price"].describe()
    availability_stats = df["availability"].str.lower().str.strip().value_counts()
    rating_stats = df["rating"].value_counts()

    print("Price Statistics:\n", price_stats)
    print("\nAvailability Statistics:\n", availability_stats)
    print("\nRating Statistics:\n", rating_stats)

    # Enhanced visualization with Seaborn
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.histplot(df["price"], bins=20, kde=True, color="skyblue")
    plt.title("Book Price Distribution")
    plt.xlabel("Price (£)")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("price_distribution_enhanced.png")
    plt.close()

    # Additional insights
    top_5_expensive_books = df.sort_values(by="price", ascending=False).head()
    print("\nTop 5 Expensive Books:\n", top_5_expensive_books)
