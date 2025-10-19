# Employee-Leave-Management-System

Employee Leave Management System is a small Python-based application to manage employee leave requests. It provides a simple CLI-driven workflow for employees to apply for leave and for managers/administrators to review, approve, or reject requests. The system persists data in SQLite (or optionally uses SQLAlchemy) and supports reporting and balance tracking.


## Features
Employee management: add, view, update, remove employees.
Leave application: employees can apply for Casual, Sick, Annual, etc.
Balance checks: system validates available leave balance before accepting requests.
Approval workflow: managers can view pending requests, approve/reject with remarks.
Automatic balance updates when leave is approved.
Reporting: individual leave history, remaining leave balance, department summaries.
Data persistence via SQLite (or SQLAlchemy for ORM).
Extensible for email notifications, Flask web UI, CSV/PDF export, authentication, dashboards.

## Tech Stack
Language: Python 3.8+
Database: SQLite (file-based); optionally SQLAlchemy for ORM
CLI: Python argparse / simple interactive menu (or click)
Optional: Flask for web UI, smtplib or transactional email provider for notifications, pandas for CSV export

## Quick Start

1. Clone the repo

git clone <https://github.com/Victorious-ke/Employee-Leave-Management-System>
cd Employee-Leave-Management


2. Create & activate Python virtual environment

python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate       # Windows (PowerShell)


3. Install dependencies

pip install -r requirements.txt

If you are using only SQLite + stdlib, requirements.txt can be empty or minimal. Add SQLAlchemy, Flask, etc. only if you plan to use them.

4. Create the database
You can use the provided SQL schema (see below) and run it with the SQLite CLI:

sqlite3 employee_leave.db < schema.sql

5. Run the CLI app

python cli_app.py

## Database Schema

1. Open database

sqlite3 employee_leave.db


2. Add an employee

INSERT INTO employees (name, username, department, position, annual_leave_balance, sick_leave_balance, casual_leave_balance)
VALUES ('Alice Johnson', 'alice.j', 'HR', 'Manager', 20, 10, 5);


3. Apply for leave (employee)

INSERT INTO leaves (employee_id, leave_type, start_date, end_date, days, reason)
VALUES (1, 'Annual', '2025-10-25', '2025-10-28', 4, 'Family vacation');


4. View pending leaves

SELECT l.leave_id, e.name, l.leave_type, l.start_date, l.end_date, l.days, l.status
FROM leaves l
JOIN employees e ON e.employee_id = l.employee_id
WHERE l.status = 'Pending';


5. Approve a leave and update balance

-- Example: approve leave_id = 1
UPDATE leaves SET status = 'Approved', manager_remark = 'Enjoy your vacation', updated_at = datetime('now') WHERE leave_id = 1;

-- Subtract days from employee's annual balance (example)
UPDATE employees
SET annual_leave_balance = annual_leave_balance - (
    SELECT days FROM leaves WHERE leave_id = 1
)
WHERE employee_id = (SELECT employee_id FROM leaves WHERE leave_id = 1);


6. View leave history for an employee

SELECT * FROM leaves WHERE employee_id = 1 ORDER BY created_at DESC;

## Commands & Workflows (suggested CLI commands)
add-employee — create employee record
list-employees — show employees (filter by department)
update-employee / remove-employee
apply-leave — employee creates leave request; system validates balance
list-leaves --status PENDING — managers list pending requests
approve-leave <leave_id> [--remark "OK"] — approve & adjust balance
reject-leave <leave_id> [--remark "Reason"]
report-employee <employee_id> — detailed leave history + balances
report-dept <department> — department-level summary
export --format csv --out path — exports selected report

## Business Rules & Validation (recommendations)
Validate date formats (ISO YYYY-MM-DD) and that end_date >= start_date.
Calculate days considering working days vs calendar days (configurable).
Prevent overlapping approved leaves for the same employee if business rules forbid it.
Prevent negative leave balances — either block application or allow negative with admin approval.
Role separation: employees (apply, view their records), managers (approve/reject), admins (manage employees & balances).


## Development & Contribution
Fork the repository.
Create a feature branch: git checkout -b feat/cli-menu.
Run tests and linting locally.
Open a PR with a clear description and related issue number.


## File Layout
employee-leave-management/
├── README.md
├── schema.sql
├── requirements.txt
├── cli_app.py            
├── db.py                 
├── models.py             
├── services/             
│   ├── leave_service.py
│   └── employee_service.py
└── docs/
    └── design.md

## License

This project is licensed under the MIT License — feel free to reuse and modify.
