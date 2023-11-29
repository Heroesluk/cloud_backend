from typing import Optional
import psycopg2
from Exceptions import UserTableDuplicateUsername
from models import User, Image

# Connect to your postgres DB
conn = psycopg2.connect(
    host="34.79.134.188",
    user="postgres",
    password="piwo2137")


# TODO: Write tests 1. User object is correctly returned, 2 exception is raise if duplicate, 3 None is returned
# SEE https://pypi.org/project/pytest-postgresql/
def get_user_by_username_query(username: str) -> Optional[User]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))

    records: list = cur.fetchall()
    if len(records) > 1:
        raise UserTableDuplicateUsername("There's duplicate")
    if len(records) == 0:
        return None
    return User(records[0][0], records[0][1], records[0][2], records[0][3])


# This will probably be changed a lot, temporary solution, don't create tests
def match_credentials_query(username, password) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = %s AND password_hash = %s)", (username, password))

    return cur.fetchone()[0]


def getAllUsers():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    print(cur.fetchall())


getAllUsers()


def get_user_id_query(username):
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))

    return cur.fetchone()[0]


def get_user_files_query(id: int):
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE folder_id = %s", (id,))

    records = cur.fetchall()
    if len(records) == 0:
        return []

    return [Image(r[0], r[1], r[2], r[3], r[4]) for r in records]



