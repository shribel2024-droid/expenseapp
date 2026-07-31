"""
=========================================================
DailyExpense Manager
charts.py

Charts & Graphs Module

Compatible with:
- Python 3.11
- Pydroid 3
=========================================================
"""

import os
import matplotlib.pyplot as plt

from report import ReportManager


class ChartManager:

    def __init__(self):

        self.report = ReportManager()

        self.chart_folder = "charts"

        os.makedirs(self.chart_folder, exist_ok=True)

    # -------------------------------------------------
    # Save Chart
    # -------------------------------------------------

    def save_chart(self, filename):

        path = os.path.join(
            self.chart_folder,
            filename
        )

        plt.tight_layout()

        plt.savefig(path, dpi=300)

        return path

    # -------------------------------------------------
    # Category Expense Bar Chart
    # -------------------------------------------------

    def category_bar_chart(
        self,
        start_date=None,
        end_date=None,
        save=True,
        show=True
    ):

        data = self.report.category_summary(
            start_date,
            end_date
        )

        if len(data) == 0:

            print("No expense data available.")

            return

        categories = []

        totals = []

        for item in data:

            categories.append(
                item["category"]
            )

            totals.append(
                item["total"]
            )

        plt.figure(figsize=(10, 6))

        plt.bar(
            categories,
            totals
        )

        plt.title("Category-wise Expense")

        plt.xlabel("Category")

        plt.ylabel("Amount")

        plt.xticks(rotation=30)

        if save:

            file = self.save_chart(
                "category_bar_chart.png"
            )

            print("Saved :", file)

        if show:

            plt.show()

        else:

            plt.close()


# -------------------------------------------------
# Test
# -------------------------------------------------

if __name__ == "__main__":

    chart = ChartManager()

    chart.category_bar_chart()
    
        # -------------------------------------------------
    # Category Expense Pie Chart
    # -------------------------------------------------

    def category_pie_chart(
        self,
        start_date=None,
        end_date=None,
        save=True,
        show=True
    ):

        data = self.report.category_summary(
            start_date,
            end_date
        )

        if len(data) == 0:

            print("No expense data available.")

            return

        labels = []
        values = []

        for item in data:

            labels.append(
                item["category"]
            )

            values.append(
                item["total"]
            )

        plt.figure(figsize=(8, 8))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Category-wise Expense Distribution")

        plt.axis("equal")

        if save:

            file = self.save_chart(
                "category_pie_chart.png"
            )

            print("Saved :", file)

        if show:

            plt.show()

        else:

            plt.close()
            
                # -------------------------------------------------
    # Payment Method Pie Chart
    # -------------------------------------------------

    def payment_method_pie_chart(
        self,
        start_date=None,
        end_date=None,
        save=True,
        show=True
    ):

        data = self.report.payment_method_summary(
            start_date,
            end_date
        )

        if len(data) == 0:

            print("No payment data available.")

            return

        labels = []
        values = []

        for item in data:

            labels.append(
                item["payment_method"]
            )

            values.append(
                item["total"]
            )

        plt.figure(figsize=(8, 8))

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Payment Method Distribution")

        plt.axis("equal")

        if save:

            file = self.save_chart(
                "payment_method_pie_chart.png"
            )

            print("Saved :", file)

        if show:

            plt.show()

        else:

            plt.close()

    # -------------------------------------------------
    # Monthly Expense Trend
    # -------------------------------------------------

    def monthly_trend_chart(
        self,
        year=None,
        save=True,
        show=True
    ):

        if year is None:

            from datetime import datetime

            year = datetime.now().year

        summary = self.report.monthly_summary(year)

        months = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ]

        values = []

        for month in range(1, 13):
            values.append(summary.get(month, 0.0))

        plt.figure(figsize=(11, 5))

        plt.plot(
            months,
            values,
            marker="o",
            linewidth=2
        )

        plt.title(f"Monthly Expense Trend ({year})")

        plt.xlabel("Month")

        plt.ylabel("Expense Amount")

        plt.grid(True)

        if save:

            file = self.save_chart(
                f"monthly_trend_{year}.png"
            )

            print("Saved :", file)

        if show:

            plt.show()

        else:

            plt.close()
            
                # -------------------------------------------------
    # Monthly Budget vs Expense Bar Chart
    # -------------------------------------------------

    def budget_vs_expense_chart(
        self,
        year=None,
        save=True,
        show=True
    ):

        from datetime import datetime

        if year is None:
            year = datetime.now().year

        months = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ]

        budget_values = []
        expense_values = []

        for month in range(1, 13):

            budget = self.report.budget_utilization(
                month,
                year
            )

            budget_values.append(
                budget["budget"]
            )

            expense_values.append(
                budget["spent"]
            )

        import numpy as np

        x = np.arange(len(months))

        width = 0.35

        plt.figure(figsize=(12, 6))

        plt.bar(
            x - width / 2,
            budget_values,
            width,
            label="Budget"
        )

        plt.bar(
            x + width / 2,
            expense_values,
            width,
            label="Expense"
        )

        plt.xticks(
            x,
            months
        )

        plt.title(
            f"Monthly Budget vs Expense ({year})"
        )

        plt.xlabel("Month")

        plt.ylabel("Amount")

        plt.legend()

        plt.grid(
            axis="y",
            linestyle="--",
            alpha=0.5
        )

        if save:

            file = self.save_chart(
                f"budget_vs_expense_{year}.png"
            )

            print("Saved :", file)

        if show:

            plt.show()

        else:

            plt.close()
            
                # -------------------------------------------------
    # Dashboard Summary
    # -------------------------------------------------

    def dashboard_summary(self):

        print("=" * 50)
        print("DailyExpense Dashboard")
        print("=" * 50)

        print(f"Total Expense      : ₹ {self.report.total_expense():,.2f}")
        print(f"Transactions       : {self.report.total_transactions()}")

        from datetime import datetime

        today = datetime.today()

        budget = self.report.budget_utilization(
            today.month,
            today.year
        )

        print(f"Current Budget     : ₹ {budget['budget']:,.2f}")
        print(f"Spent              : ₹ {budget['spent']:,.2f}")
        print(f"Remaining          : ₹ {budget['remaining']:,.2f}")
        print(f"Budget Used        : {budget['percentage_used']:.2f}%")
        print(f"Status             : {budget['status']}")

    # -------------------------------------------------
    # Generate All Charts
    # -------------------------------------------------

    def generate_all_charts(
        self,
        year=None
    ):

        print("\nGenerating Charts...\n")

        self.category_bar_chart(
            save=True,
            show=False
        )

        self.category_pie_chart(
            save=True,
            show=False
        )

        self.payment_method_pie_chart(
            save=True,
            show=False
        )

        self.monthly_trend_chart(
            year=year,
            save=True,
            show=False
        )

        self.budget_vs_expense_chart(
            year=year,
            save=True,
            show=False
        )

        print("\nAll charts generated successfully.")
        print("Location :", self.chart_folder)


# -------------------------------------------------
# Test Program
# -------------------------------------------------

if __name__ == "__main__":

    chart = ChartManager()

    chart.dashboard_summary()

    chart.generate_all_charts()

    print("\nDone.")