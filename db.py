import sqlite3

DB_NAME = "employee_leave.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn, open("schema.sql", "r") as f:
        conn.executescript(f.read())
    print("Database initialized successfully.")
