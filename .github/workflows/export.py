"""
=========================================================
DailyExpense Manager

export.py

Export Manager

Supports:
- CSV
- Excel
- PDF

Python 3.11
Pydroid 3 Compatible
=========================================================
"""


import os
import csv
import sqlite3
from datetime import datetime


DB_NAME = "database/expenses.db"


EXPORT_FOLDER = "exports"



class ExportManager:


    def __init__(self):

        self.create_folder()



    # -------------------------------------------------

    def create_folder(self):

        if not os.path.exists(EXPORT_FOLDER):

            os.makedirs(EXPORT_FOLDER)



    # -------------------------------------------------

    def get_expenses(self):

        conn = sqlite3.connect(DB_NAME)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT *
            FROM expenses
            ORDER BY id DESC
            """
        )


        rows = cursor.fetchall()


        conn.close()


        return rows



    # -------------------------------------------------

    # CSV Export

    def export_csv(self):

        rows = self.get_expenses()


        filename = (
            EXPORT_FOLDER +
            "/expenses_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
            +
            ".csv"
        )


        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:


            writer = csv.writer(file)


            writer.writerow(
                [
                    "ID",
                    "Date",
                    "Category",
                    "Description",
                    "Amount",
                    "Payment Method"
                ]
            )


            for row in rows:

                writer.writerow(
                    [
                        row["id"],
                        row["date"],
                        row["category"],
                        row["description"],
                        row["amount"],
                        row["payment_method"]
                    ]
                )



        return filename



    # -------------------------------------------------

    # Excel Export

    def export_excel(self):

        from openpyxl import Workbook


        rows = self.get_expenses()


        filename = (
            EXPORT_FOLDER +
            "/expenses_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
            +
            ".xlsx"
        )


        wb = Workbook()


        ws = wb.active


        ws.title = "Expenses"


        ws.append(
            [
                "ID",
                "Date",
                "Category",
                "Description",
                "Amount",
                "Payment Method"
            ]
        )


        for row in rows:

            ws.append(
                [
                    row["id"],
                    row["date"],
                    row["category"],
                    row["description"],
                    row["amount"],
                    row["payment_method"]
                ]
            )


        wb.save(filename)


        return filename



    # -------------------------------------------------

    # PDF Export

    def export_pdf(self):

        from reportlab.platypus import (
            SimpleDocTemplate,
            Table,
            TableStyle,
            Paragraph
        )

        from reportlab.lib.styles import getSampleStyleSheet



        rows = self.get_expenses()


        filename = (
            EXPORT_FOLDER +
            "/expenses_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
            +
            ".pdf"
        )


        doc = SimpleDocTemplate(
            filename
        )


        data = [

            [
                "ID",
                "Date",
                "Category",
                "Amount",
                "Payment"
            ]

        ]



        for row in rows:

            data.append(
                [
                    str(row["id"]),
                    row["date"],
                    row["category"],
                    str(row["amount"]),
                    row["payment_method"]
                ]
            )



        table = Table(data)


        table.setStyle(
            TableStyle(
                [
                    ("GRID",
                     (0,0),
                     (-1,-1),
                     1,
                     None)
                ]
            )
        )


        elements = []


        styles = getSampleStyleSheet()


        elements.append(
            Paragraph(
                "Daily Expense Report",
                styles["Title"]
            )
        )


        elements.append(table)


        doc.build(elements)



        return filename



    # -------------------------------------------------

    def export_all(self):

        return {

            "CSV":
            self.export_csv(),

            "Excel":
            self.export_excel(),

            "PDF":
            self.export_pdf()

        }