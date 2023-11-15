import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(
                        host="34.79.134.188",
                        user="postgres",
                        password="piwo2137")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM users")

# Retrieve query results
records = cur.fetchall()

print(records)