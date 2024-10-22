import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('providers_data.db')

# Create a cursor object
cur = conn.cursor()

# Example query: Fetch all records from the 'providers' table
cur.execute("SELECT * FROM providers limit 10")

# Fetch all results from the query
rows = cur.fetchall()

# Loop through the results and print each row
for row in rows:
    print(row)

# Close the connection
conn.close()
