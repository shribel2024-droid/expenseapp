"""
=========================================================
DailyExpense Manager
database.py
SQLite Database Manager
Compatible with:
- Python 3.11
- Pydroid 3
=========================================================
"""

import sqlite3
import os
from datetime import datetime

# ---------------------------------------------------------
# Database Location
# ---------------------------------------------------------

DB_FOLDER = "database"
DB_NAME = "expenses.db"

os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, DB_NAME)


# ---------------------------------------------------------
# Database Manager
# ---------------------------------------------------------

class DatabaseManager:

    def __init__(self):
        self.db_path = DB_PATH
        self.create_database()

    def connect(self):
        return sqlite3.connect(self.db_path)

    # -----------------------------------------------------
    # Create Database
    # -----------------------------------------------------

    def create_database(self):

        conn = self.connect()
        cur = conn.cursor()

        # ---------------- Expenses ----------------

        cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            expense_date TEXT,

            expense_time TEXT,

            category TEXT,

            description TEXT,

            amount REAL,

            payment_method TEXT,

            notes TEXT,

            created_on TEXT
        )
        """)

        # ---------------- Categories ----------------

        cur.execute("""
        CREATE TABLE IF NOT EXISTS categories(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category_name TEXT UNIQUE
        )
        """)

        # ---------------- Budget ----------------

        cur.execute("""
        CREATE TABLE IF NOT EXISTS budget(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            month INTEGER,

            year INTEGER,

            budget_amount REAL
        )
        """)

        # ---------------- Settings ----------------

        cur.execute("""
        CREATE TABLE IF NOT EXISTS settings(

            id INTEGER PRIMARY KEY,

            currency TEXT,

            theme TEXT,

            date_format TEXT,

            backup_path TEXT
        )
        """)

        conn.commit()

        self.insert_default_categories(cur)
        self.insert_default_settings(cur)

        conn.commit()
        conn.close()

    # -----------------------------------------------------
    # Default Categories
    # -----------------------------------------------------

    def insert_default_categories(self, cur):

        categories = [

            "Food",
            "Grocery",
            "Fuel",
            "Medical",
            "Electricity",
            "Mobile Recharge",
            "Internet",
            "Entertainment",
            "Shopping",
            "Education",
            "Travel",
            "Rent",
            "Salary",
            "Investment",
            "Miscellaneous"

        ]

        for item in categories:

            cur.execute("""

            INSERT OR IGNORE INTO categories(category_name)

            VALUES(?)

            """, (item,))

    # -----------------------------------------------------
    # Default Settings
    # -----------------------------------------------------

    def insert_default_settings(self, cur):

        cur.execute("""

        INSERT OR IGNORE INTO settings

        (id,currency,theme,date_format,backup_path)

        VALUES(1,'INR','Light','DD-MM-YYYY','backup')

        """)


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

db = DatabaseManager()


def execute(query, values=()):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(query, values)

    conn.commit()

    conn.close()


def fetch_all(query, values=()):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(query, values)

    rows = cur.fetchall()

    conn.close()

    return rows


def fetch_one(query, values=()):

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute(query, values)

    row = cur.fetchone()

    conn.close()

    return row


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 45)

    print("DailyExpense Database")

    print("=" * 45)

    print("Database Created Successfully")

    print("Location :", DB_PATH)

    print()

    print("Categories:")

    data = fetch_all("SELECT category_name FROM categories")

    for i in data:

        print("-", i[0])

    print()

    print("Settings")

    print(fetch_one("SELECT * FROM settings"))

    print()

    print("Ready.")