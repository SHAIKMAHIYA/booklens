import requests
from bs4 import BeautifulSoup
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Connect to SQLite
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Create table with additional columns (e.g., description, image_url)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        title TEXT UNIQUE,
        price TEXT,
        availability TEXT,
        rating TEXT,
        description TEXT,
        image_url TEXT
    )
""")

# Scrape data
url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all("article", class_="product_pod")

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    availability = book.find("p", class_="instock availability").text.strip()
    rating = book.find("p")["class"][1]  # Rating class contains the star rating
    description = book.find("h3").a["title"]  # Placeholder (use actual description scraper)
    image_url = url + book.img["src"]

    # Log the scraped details
    logging.info(f"Scraped: {title} | Price: {price} | Rating: {rating}")

    # Use INSERT OR REPLACE to avoid duplicates and update existing records
    cursor.execute("""
        INSERT OR REPLACE INTO books (title, price, availability, rating, description, image_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, price, availability, rating, description, image_url))

# Save and close
conn.commit()
conn.close()
logging.info("Scraping complete. Data saved to books.db.")
