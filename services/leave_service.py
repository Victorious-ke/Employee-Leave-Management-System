from db import get_connection


# Add a new employee
def add_employee(name, department, position, annual=20, sick=10, casual=5):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO employees
            (name, department, position, annual_leave_balance, sick_leave_balance, casual_leave_balance)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, department, position, annual, sick, casual),
        )
        conn.commit()
    print(f" Employee '{name}' added successfully.")


#  List all employees
def list_employees():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT employee_id, name, department, position,
                   annual_leave_balance, sick_leave_balance, casual_leave_balance
            FROM employees
            ORDER BY employee_id
            """
        ).fetchall()
    return rows


#  Get employee by ID
def get_employee(employee_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM employees WHERE employee_id = ?",
            (employee_id,),
        ).fetchone()
    return row

#  Update an employee’s details
def update_employee(employee_id, name=None, department=None, position=None):
    with get_connection() as conn:
        current = get_employee(employee_id)
        if not current:
            print("Employee not found.")
            return

        # Default to existing values if not provided
        name = name or current["name"]
        department = department or current["department"]
        position = position or current["position"]

        conn.execute(
            """
            UPDATE employees
            SET name = ?, department = ?, position = ?
            WHERE employee_id = ?
            """,
            (name, department, position, employee_id),
        )
        conn.commit()
    print(f" Employee ID {employee_id} updated successfully.")




