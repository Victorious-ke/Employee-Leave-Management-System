from db import get_connection
from services.employee_service import adjust_leave_balance, get_employee


#  Apply for a new leave
def apply_leave(employee_id, leave_type, start_date, end_date, days, reason):
    emp = get_employee(employee_id)
    if not emp:
        print(" Employee not found.")
        return

    # Check leave balance
    available_balance = emp["available_leaves"]
    if available_balance < days:
        print(f"  Insufficient leave balance ({available_balance} days left).")
        return

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO leaves (employee_id, leave_type, start_date, end_date, num_days, reason)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (employee_id, leave_type, start_date, end_date, days, reason),
        )
        conn.commit()

    print(f" Leave request submitted for employee ID {employee_id} ({days} day(s), {leave_type}).")


#  List all pending leave requests
def list_pending_leaves():
    with get_connection() as conn:
        conn.row_factory = dict_factory
        rows = conn.execute(
            """
            SELECT 
                l.id AS leave_id,
                e.name AS employee_name,
                e.department,
                l.leave_type,
                l.start_date,
                l.end_date,
                l.num_days,
                l.reason,
                l.status,
                l.created_at
            FROM leaves l
            JOIN employees e ON e.id = l.employee_id
            WHERE l.status = 'Pending'
            ORDER BY l.created_at DESC
            """
        ).fetchall()
    return rows


#  List all leaves for a specific employee
def list_employee_leaves(employee_id):
    with get_connection() as conn:
        conn.row_factory = dict_factory
        rows = conn.execute(
            """
            SELECT 
                id AS leave_id,
                leave_type,
                start_date,
                end_date,
                num_days,
                reason,
                status,
                manager_remark,
                created_at,
                updated_at
            FROM leaves
            WHERE employee_id = ?
            ORDER BY created_at DESC
            """,
            (employee_id,),
        ).fetchall()
    return rows


#  Approve a leave request
def approve_leave(leave_id, remark=None):
    with get_connection() as conn:
        conn.row_factory = dict_factory
        leave = conn.execute(
            "SELECT * FROM leaves WHERE id = ?", (leave_id,)
        ).fetchone()

        if not leave:
            print(" Leave request not found.")
            return
        if leave["status"] != "Pending":
            print(f" Leave ID {leave_id} is already {leave['status']}.")
            return

        # Update leave status
        conn.execute(
            """
            UPDATE leaves
            SET status = 'Approved',
                manager_remark = ?,
                updated_at = datetime('now')
            WHERE id = ?
            """,
            (remark or "Approved", leave_id),
        )
        conn.commit()

        # Adjust employee leave balance
        adjust_leave_balance(leave["employee_id"], leave["num_days"])

    print(f" Leave ID {leave_id} approved successfully.")


#  Reject a leave request
def reject_leave(leave_id, remark=None):
    with get_connection() as conn:
        conn.row_factory = dict_factory
        leave = conn.execute(
            "SELECT * FROM leaves WHERE id = ?", (leave_id,)
        ).fetchone()

        if not leave:
            print(" Leave request not found.")
            return
        if leave["status"] != "Pending":
            print(f" Leave ID {leave_id} is already {leave['status']}.")
            return

        conn.execute(
            """
            UPDATE leaves
            SET status = 'Rejected',
                manager_remark = ?,
                updated_at = datetime('now')
            WHERE id = ?
            """,
            (remark or "Rejected", leave_id),
        )
        conn.commit()

    print(f" Leave ID {leave_id} rejected successfully.")


#  Summary report for departments
def leave_summary():
    with get_connection() as conn:
        conn.row_factory = dict_factory
        rows = conn.execute(
            """
            SELECT 
                e.department,
                COUNT(l.id) AS total_leaves,
                SUM(CASE WHEN l.status = 'Approved' THEN 1 ELSE 0 END) AS approved,
                SUM(CASE WHEN l.status = 'Rejected' THEN 1 ELSE 0 END) AS rejected,
                SUM(CASE WHEN l.status = 'Pending' THEN 1 ELSE 0 END) AS pending
            FROM employees e
            LEFT JOIN leaves l ON e.id = l.employee_id
            GROUP BY e.department
            """
        ).fetchall()
    return rows


# Helper: return rows as dicts
def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
