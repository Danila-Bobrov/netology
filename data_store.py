import psycopg2 as pg2
from config import host, user, password, db_name

with pg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name,
                ) as conn:
    conn.autocommit = True


def create_db_users_base():
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_base(
            id serial,
            users_list varchar(50) PRIMARY KEY);"""
        )


def insert_data_users_base(user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO users_base (users_list) 
           VALUES (%s)""",
            (user_id,)
        )


def delete_users_base():
    with conn.cursor() as cursor:
        cursor.execute(
            """DROP TABLE  IF EXISTS users_base CASCADE;"""
        )


print("users_base was created!")
