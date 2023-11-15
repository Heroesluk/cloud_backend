import psycopg2
from Exceptions import UserTableDuplicateUsername

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


# TODO: Write tests 1. user row is correctly returned, 2 exception is raise if duplicate
# SEE https://pypi.org/project/pytest-postgresql/
def get_user_by_username(username: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))

    records: list = cur.fetchall()
    if len(records) > 1:
        raise UserTableDuplicateUsername("There's duplicate")

    return records


print(get_user_by_username("user2"))
