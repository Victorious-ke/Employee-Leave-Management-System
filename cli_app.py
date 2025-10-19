from tabulate import tabulate
from db import init_db
from services.employee_service import add_employee, list_employees, get_employee
from services.leave_service import (
    apply_leave,
    list_pending_leaves,
    list_employee_leaves,
    approve_leave,
    reject_leave,
    leave_summary,
)


def show_menu():
    print("""
===============================
 Employee Leave Management System
===============================
1. Initialize Database
2. Add Employee
3. List Employees
4. Apply for Leave
5. List Pending Leaves (Manager)
6. Approve Leave (Manager)
7. Reject Leave (Manager)
8. View Employee Leave History
9. Department Leave Summary
0. Exit
""")


def main():
    while True:
        show_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            init_db()

        elif choice == "2":
            name = input("Employee Name: ")
            dept = input("Department: ")
            position = input("Position: ")
            add_employee(name, dept, position)

        elif choice == "3":
            employees = list_employees()
            if employees:
                print(tabulate(employees, headers="keys", tablefmt="grid"))
            else:
                print("No employees found.")

        elif choice == "4":
            emp_id = int(input("Employee ID: "))
            emp = get_employee(emp_id)
            if not emp:
                print(" Invalid employee ID.")
                continue

            leave_type = input("Leave Type (Annual/Sick/Casual): ")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            days = int(input("Number of Days: "))
            reason = input("Reason: ")
            apply_leave(emp_id, leave_type, start_date, end_date, days, reason)

        elif choice == "5":
            leaves = list_pending_leaves()
            if leaves:
                print(tabulate(leaves, headers="keys", tablefmt="grid"))
            else:
                print(" No pending leave requests.")

        elif choice == "6":
            leave_id = int(input("Leave ID to approve: "))
            remark = input("Manager Remark (optional): ")
            approve_leave(leave_id, remark)

        elif choice == "7":
            leave_id = int(input("Leave ID to reject: "))
            remark = input("Manager Remark (optional): ")
            reject_leave(leave_id, remark)

        elif choice == "8":
            emp_id = int(input("Employee ID: "))
            leaves = list_employee_leaves(emp_id)
            if leaves:
                print(tabulate(leaves, headers="keys", tablefmt="grid"))
            else:
                print("No leave history found for this employee.")

        elif choice == "9":
            summary = leave_summary()
            if summary:
                print(tabulate(summary, headers="keys", tablefmt="grid"))
            else:
                print("No data available.")

        elif choice == "0":
            print(" Exiting the system. Goodbye!")
            break

        else:
            print(" Invalid option, please try again.")


if __name__ == "__main__":
    main()
