"""Module to keep all database functionality in one place."""
import sqlalchemy
import sqlite3

DATABASE_NAME = "app/weights.db"
conn = sqlite3.connect(DATABASE_NAME)
c = conn.cursor()


def create_database():
    try:
        table_sql = """CREATE TABLE weight (
            date datetime,
            weight char(10),
            clothing_code char(2))"""
        c.execute(table_sql)
    except sqlite3.OperationalError as e:
        print(f"Could not create table. Following error was raised {e}")


def add_weight_measurement(weight):
    conn = connect_to_database()


if __name__ == "__main__":
    create_database()
