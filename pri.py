import sqlite3

# Connect to the database
conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# Run the query
query = "SELECT title, availability FROM books"
cursor.execute(query)
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()
