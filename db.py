import sqlite3

DB_NAME = "employee_leave.db"

def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Initialize the database tables for employees and leaves."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create employees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        position TEXT NOT NULL,
        available_leaves INTEGER DEFAULT 30,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create leaves table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        leave_type TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        num_days INTEGER NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        manager_remark TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    );
    """)

    conn.commit()
    conn.close()
    print(" Database initialized successfully.")