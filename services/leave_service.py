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

# Remove an employee
def delete_employee(employee_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
        conn.commit()
    print(f" Employee ID {employee_id} deleted successfully.")

#  Adjust leave balance (used after approvals)
def adjust_leave_balance(employee_id, leave_type, days):
    field_map = {
        "Annual": "annual_leave_balance",
        "Sick": "sick_leave_balance",
        "Casual": "casual_leave_balance",
    }
    if leave_type not in field_map:
        raise ValueError("Invalid leave type. Must be Annual, Sick, or Casual.")

    with get_connection() as conn:
        conn.execute(
            f"""
            UPDATE employees
            SET {field_map[leave_type]} = {field_map[leave_type]} - ?
            WHERE employee_id = ?
            """,
            (days, employee_id),
        )
        conn.commit()
    print(f"Updated {leave_type} leave balance for employee ID {employee_id}.")

#  Get employee leave balances
def get_leave_balances(employee_id):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT annual_leave_balance, sick_leave_balance, casual_leave_balance
            FROM employees WHERE employee_id = ?
            """,
            (employee_id,),
        ).fetchone()
    return row



