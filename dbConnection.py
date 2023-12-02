import datetime
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


def get_user_id_query(username):
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))

    return cur.fetchone()[0]


def get_new_user_id():
    cur = conn.cursor()
    cur.execute("SELECT nextval('users_user_id_seq')")

    return cur.fetchone()


def get_new_img_id() -> int:
    cur = conn.cursor()
    cur.execute("SELECT nextval('images_image_id_seq')")

    return cur.fetchone()[0]


def get_user_files_query(id: int) -> list[Image]:
    cur = conn.cursor()
    cur.execute("SELECT * FROM images WHERE folder_id = %s", (id,))

    records = cur.fetchall()
    if len(records) == 0:
        return []

    return [Image(r[0], r[1], r[2], r[3], r[4]) for r in records]


def add_user_to_db(user):
    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING id",
                    (user.username, user.password, user.email))

        new_user_id = cur.fetchone()[0]

        conn.commit()
        cur.close()

        user.id = new_user_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()


def add_image_data_to_db(image: Image) -> str:
    try:
        cur = conn.cursor()
        print()
        cur.execute(
            "INSERT INTO images (image_id,image_name, folder_id, image_size, image_add_date) VALUES (%s,%s, %s, %s, %s)",
            (get_new_img_id(), image.name, image.folder_id, image.image_size,
             image.image_add_date.strftime("%m/%d/%Y, %H:%M:%S")))

        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        print(e)

    finally:
        conn.close()
        return str(image.folder_id) + "/" + image.name


# test = Image(0, "newimg", 1, 1000, datetime.datetime.now())
#
# add_image_data_to_db(test)
