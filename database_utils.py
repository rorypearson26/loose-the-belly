"""Module to keep all database functionality in one place."""
import sqlalchemy
import sqlite3

DATABASE_NAME = "weights.db"


def connect_to_database():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def add_weight_measurement(weight):
    conn = connect_to_database()
