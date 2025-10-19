from db import get_connection
from services.employee_service import adjust_leave_balance, get_employee


#  Apply for a new leave
def apply_leave(employee_id, leave_type, start_date, end_date, days, reason):
    emp = get_employee(employee_id)
    if not emp:
        print(" Employee not found.")
        return

    # Check available leave balance
    balance_field = {
        "Annual": "annual_leave_balance",
        "Sick": "sick_leave_balance",
        "Casual": "casual_leave_balance",
    }.get(leave_type)

    if not balance_field:
        print(" Invalid leave type. Choose from: Annual, Sick, Casual.")
        return

    available_balance = emp[balance_field]
    if available_balance < days:
        print(f" Insufficient {leave_type} leave balance ({available_balance} days left).")
        return

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO leaves
            (employee_id, leave_type, start_date, end_date, days, reason)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (employee_id, leave_type, start_date, end_date, days, reason),
        )
        conn.commit()
    print(f" Leave request submitted for employee ID {employee_id} ({days} day(s), {leave_type}).")


#  List all pending leave requests
def list_pending_leaves():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT l.leave_id, e.name, l.leave_type, l.start_date, l.end_date, l.days, l.reason, l.status
            FROM leaves l
            JOIN employees e ON e.employee_id = l.employee_id
            WHERE l.status = 'Pending'
            ORDER BY l.created_at DESC
            """
        ).fetchall()
    return rows



