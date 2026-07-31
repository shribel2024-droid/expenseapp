"""
=========================================================
DailyExpense Manager

export_module.py

Combined:
- Export Manager
- Export Screen UI

Supports:
- CSV
- Excel
- PDF

Python 3.11
Pydroid 3
Kivy 2.3
=========================================================
"""


import os
import csv
import sqlite3

from datetime import datetime


DB_NAME = "database/expenses.db"

EXPORT_FOLDER = "exports"



# =========================================================
# EXPORT MANAGER
# =========================================================

class ExportManager:


    def __init__(self):

        self.create_folder()



    def create_folder(self):

        if not os.path.exists(EXPORT_FOLDER):

            os.makedirs(EXPORT_FOLDER)



    # -----------------------------------------------------

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


        data = cursor.fetchall()


        conn.close()


        return data



    # -----------------------------------------------------
    # CSV
    # -----------------------------------------------------

    def export_csv(self):

        rows = self.get_expenses()


        filename = (
            EXPORT_FOLDER +
            "/Expense_Report_" +
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



    # -----------------------------------------------------
    # EXCEL
    # -----------------------------------------------------

    def export_excel(self):

        from openpyxl import Workbook


        rows = self.get_expenses()


        filename = (
            EXPORT_FOLDER +
            "/Expense_Report_" +
            datetime.now().strftime("%Y%m%d_%H%M%S")
            +
            ".xlsx"
        )


        workbook = Workbook()


        sheet = workbook.active


        sheet.title="Expenses"


        sheet.append(
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


            sheet.append(
                [
                    row["id"],
                    row["date"],
                    row["category"],
                    row["description"],
                    row["amount"],
                    row["payment_method"]
                ]
            )



        workbook.save(filename)


        return filename




    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    def export_pdf(self):

        from reportlab.platypus import (
            SimpleDocTemplate,
            Table,
            TableStyle,
            Paragraph
        )

        from reportlab.lib.styles import getSampleStyleSheet



        rows=self.get_expenses()



        filename=(

            EXPORT_FOLDER +

            "/Expense_Report_" +

            datetime.now().strftime("%Y%m%d_%H%M%S")

            +

            ".pdf"

        )



        doc=SimpleDocTemplate(
            filename
        )



        table_data=[

            [
                "ID",
                "Date",
                "Category",
                "Amount",
                "Payment"
            ]

        ]



        for row in rows:


            table_data.append(

                [

                    str(row["id"]),

                    row["date"],

                    row["category"],

                    str(row["amount"]),

                    row["payment_method"]

                ]

            )



        table=Table(table_data)



        table.setStyle(

            TableStyle(

                [

                    (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    1,
                    None
                    )

                ]

            )

        )



        elements=[]


        styles=getSampleStyleSheet()



        elements.append(

            Paragraph(

                "Daily Expense Report",

                styles["Title"]

            )

        )


        elements.append(table)



        doc.build(elements)



        return filename



    # -----------------------------------------------------

    def export_all(self):


        return {


            "CSV":
            self.export_csv(),


            "Excel":
            self.export_excel(),


            "PDF":
            self.export_pdf()


        }





# =========================================================
# EXPORT SCREEN
# =========================================================


from kivy.uix.screenmanager import Screen

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button

from kivy.uix.label import Label

from kivy.uix.scrollview import ScrollView





class ExportScreen(Screen):


    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.export=ExportManager()



        root=BoxLayout(

            orientation="vertical",

            spacing=10,

            padding=10

        )



        root.add_widget(

            Label(

                text="Export Data",

                font_size=24,

                size_hint=(1,.1)

            )

        )




        for name in [

            "Export CSV",

            "Export Excel",

            "Export PDF",

            "Export All"

        ]:


            btn=Button(

                text=name,

                size_hint=(1,.1)

            )


            btn.bind(

                on_release=self.export_data

            )


            root.add_widget(btn)



        scroll=ScrollView()



        self.output=Label(

            text="Ready",

            halign="left",

            valign="top",

            text_size=(380,None)

        )



        scroll.add_widget(self.output)



        root.add_widget(scroll)




        back=Button(

            text="Back Dashboard",

            size_hint=(1,.1)

        )


        back.bind(

            on_release=self.go_home

        )


        root.add_widget(back)



        self.add_widget(root)





    def export_data(self,button):


        try:


            if button.text=="Export CSV":

                result=self.export.export_csv()



            elif button.text=="Export Excel":

                result=self.export.export_excel()



            elif button.text=="Export PDF":

                result=self.export.export_pdf()



            else:

                result=self.export.export_all()



            self.output.text=str(result)



        except Exception as e:


            self.output.text=str(e)





    def go_home(self,instance):

        self.manager.current="dashboard"