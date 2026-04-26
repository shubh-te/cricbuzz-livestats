import sqlite3

def connect_db():
    conn = sqlite3.connect("cricket.db", check_same_thread=False)
    return conn