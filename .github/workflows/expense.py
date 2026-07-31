"""
=========================================================
DailyExpense Manager
expense.py
Expense Management Module
Compatible with Python 3.11 & Pydroid 3
=========================================================
"""

from database import execute, fetch_all, fetch_one
from datetime import datetime


class ExpenseManager:

    # -----------------------------------------
    # Add Expense
    # -----------------------------------------
    def add_expense(
        self,
        category,
        description,
        amount,
        payment_method="Cash",
        notes=""
    ):

        now = datetime.now()

        expense_date = now.strftime("%d-%m-%Y")
        expense_time = now.strftime("%H:%M:%S")
        created_on = now.strftime("%Y-%m-%d %H:%M:%S")

        execute("""
        INSERT INTO expenses
        (
            expense_date,
            expense_time,
            category,
            description,
            amount,
            payment_method,
            notes,
            created_on
        )
        VALUES (?,?,?,?,?,?,?,?)
        """,
        (
            expense_date,
            expense_time,
            category,
            description,
            float(amount),
            payment_method,
            notes,
            created_on
        ))

        return True

    # -----------------------------------------
    # Update Expense
    # -----------------------------------------
    def update_expense(
        self,
        expense_id,
        category,
        description,
        amount,
        payment_method,
        notes
    ):

        execute("""
        UPDATE expenses
        SET
            category=?,
            description=?,
            amount=?,
            payment_method=?,
            notes=?
        WHERE id=?
        """,
        (
            category,
            description,
            float(amount),
            payment_method,
            notes,
            expense_id
        ))

    # -----------------------------------------
    # Delete Expense
    # -----------------------------------------
    def delete_expense(self, expense_id):

        execute(
            "DELETE FROM expenses WHERE id=?",
            (expense_id,)
        )

    # -----------------------------------------
    # Get All Expenses
    # -----------------------------------------
    def get_all_expenses(self):

        return fetch_all("""
        SELECT
            id,
            expense_date,
            expense_time,
            category,
            description,
            amount,
            payment_method,
            notes
        FROM expenses
        ORDER BY id DESC
        """)

    # -----------------------------------------
    # Get Single Expense
    # -----------------------------------------
    def get_expense(self, expense_id):

        return fetch_one("""
        SELECT *
        FROM expenses
        WHERE id=?
        """, (expense_id,))

    # -----------------------------------------
    # Search by Category
    # -----------------------------------------
    def search_category(self, category):

        return fetch_all("""
        SELECT *
        FROM expenses
        WHERE category LIKE ?
        ORDER BY expense_date DESC
        """,
        ("%" + category + "%",))

    # -----------------------------------------
    # Search by Date
    # -----------------------------------------
    def search_date(self, expense_date):

        return fetch_all("""
        SELECT *
        FROM expenses
        WHERE expense_date=?
        """,
        (expense_date,))

    # -----------------------------------------
    # Search by Keyword
    # -----------------------------------------
    def search_keyword(self, keyword):

        return fetch_all("""
        SELECT *
        FROM expenses
        WHERE
            description LIKE ?
            OR notes LIKE ?
        """,
        (
            "%" + keyword + "%",
            "%" + keyword + "%"
        ))

    # -----------------------------------------
    # Total Expense
    # -----------------------------------------
    def total_expense(self):

        row = fetch_one("""
        SELECT SUM(amount)
        FROM expenses
        """)

        if row[0] is None:
            return 0

        return row[0]

    # -----------------------------------------
    # Expense Count
    # -----------------------------------------
    def total_transactions(self):

        row = fetch_one("""
        SELECT COUNT(*)
        FROM expenses
        """)

        return row[0]


# ---------------------------------------------------
# Testing
# ---------------------------------------------------

if __name__ == "__main__":

    manager = ExpenseManager()

    print("=" * 50)
    print("DailyExpense Manager")
    print("=" * 50)

    print("\nAdding Sample Expense...")

    manager.add_expense(
        category="Food",
        description="Lunch",
        amount=250,
        payment_method="UPI",
        notes="Office canteen"
    )

    print("Expense Added Successfully.")

    print("\nAll Expenses\n")

    data = manager.get_all_expenses()

    for row in data:
        print(row)

    print("\nTotal Expense :", manager.total_expense())

    print("Transactions :", manager.total_transactions())