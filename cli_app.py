from tabulate import tabulate
from db import init_db
from services.employee_service import add_employee, list_employees
from services.leave_service import apply_leave, list_pending_leaves

def show_menu():
    print("""
=== Employee Leave Management System ===
1. Initialize Database
2. Add Employee
3. List Employees
4. Apply for Leave
5. List Pending Leaves
0. Exit
""")

def main():
    while True:
        show_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            init_db()

        elif choice == "2":
            name = input("Name: ")
            dept = input("Department: ")
            position = input("Position: ")
            add_employee(name, dept, position)

        elif choice == "3":
            employees = list_employees()
            print(tabulate(employees, headers="keys", tablefmt="grid"))

        elif choice == "4":
            emp_id = int(input("Employee ID: "))
            leave_type = input("Leave Type (Annual/Sick/Casual): ")
            start_date = input("Start Date (YYYY-MM-DD): ")
            end_date = input("End Date (YYYY-MM-DD): ")
            days = int(input("Number of Days: "))
            reason = input("Reason: ")
            apply_leave(emp_id, leave_type, start_date, end_date, days, reason)

        elif choice == "5":
            leaves = list_pending_leaves()
            print(tabulate(leaves, headers="keys", tablefmt="grid"))

        elif choice == "0":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
