from db import get_connection


#  Add a new employee
def add_employee(name, department, position):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO employees (name, department, position, available_leaves)
            VALUES (?, ?, ?, ?)
            """,
            (name, department, position, 30),  # default 30 leave days
        )
        conn.commit()
    print(f" Employee '{name}' added successfully.")


#  List all employees
def list_employees():
    with get_connection() as conn:
        conn.row_factory = dict_factory
        rows = conn.execute(
            """
            SELECT id, name, department, position, available_leaves, created_at
            FROM employees
            ORDER BY id ASC
            """
        ).fetchall()
    return rows


#  Get a single employee by ID
def get_employee(employee_id):
    with get_connection() as conn:
        conn.row_factory = dict_factory
        emp = conn.execute(
            "SELECT * FROM employees WHERE id = ?", (employee_id,)
        ).fetchone()
    return emp


#  Adjust leave balance after approval
def adjust_leave_balance(employee_id, days_used):
    with get_connection() as conn:
        emp = conn.execute(
            "SELECT available_leaves FROM employees WHERE id = ?", (employee_id,)
        ).fetchone()

        if not emp:
            print(" Employee not found for balance update.")
            return

        new_balance = max(emp[0] - days_used, 0)

        conn.execute(
            "UPDATE employees SET available_leaves = ? WHERE id = ?",
            (new_balance, employee_id),
        )
        conn.commit()

    print(f" Updated leave balance: Employee {employee_id} now has {new_balance} days remaining.")


# Helper: return rows as dictionaries
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
