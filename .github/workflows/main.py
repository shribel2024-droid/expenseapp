"""
=========================================================
DailyExpense Manager
main.py

Main Application

Compatible with:
- Python 3.11
- Pydroid 3
- Kivy 2.3
=========================================================
"""

import sys
from kivy.utils import platform

# Apply fixed window dimensions ONLY on Desktop systems.
# Forcing fixed dimensions on Android/Pydroid 3 causes SDL2 window creation crashes.
if platform not in ("android", "ios"):
    from kivy.config import Config
    Config.set("graphics", "width", "420")
    Config.set("graphics", "height", "760")
    Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    FadeTransition
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

# =========================================================
# Safe Imports (Prevents Instant Crashes if Modules Missing)
# =========================================================

try:
    from expense import ExpenseManager
except ImportError:
    class ExpenseManager:
        def add_expense(self, c, d, a, p): pass
        def search_expenses(self, k): return []

try:
    from report import ReportManager
except ImportError:
    class ReportManager:
        def total_expense(self): return 0.0
        def total_transactions(self): return 0
        def daily_report_text(self): return "Daily Report: Module not found."
        def monthly_report_text(self): return "Monthly Report: Module not found."
        def yearly_report_text(self): return "Yearly Report: Module not found."
        def category_summary_text(self): return "Category Summary: Module not found."
        def payment_summary_text(self): return "Payment Summary: Module not found."
        def budget_summary_text(self): return "Budget Summary: Module not found."

try:
    from charts import ChartManager
except ImportError:
    class ChartManager:
        def category_bar_chart(self): pass
        def category_pie_chart(self): pass
        def payment_method_pie_chart(self): pass
        def monthly_trend_chart(self): pass
        def budget_vs_expense_chart(self): pass
        def generate_all_charts(self): pass

try:
    from backup import BackupManager
except ImportError:
    class BackupManager:
        def create_backup(self): return False, "Backup module not found."
        def create_zip_backup(self): return False, "Backup module not found."
        def restore_latest_backup(self): return False, "Backup module not found."
        def list_backups(self): return []
        def backup_statistics(self): return {"Status": "Module missing"}
        def cleanup_old_backups(self, keep_latest=10): return []

try:
    from settings import SettingsManager
except ImportError:
    class SettingsManager:
        def get_setting(self, key): return ""
        def get_settings(self): return [0, "Dark", "₹", "UPI", "YYYY-MM-DD", 1, "Daily", "exports"]
        def update_setting(self, key, val): pass
        def reset_defaults(self): pass


# =========================================================
# Dashboard Screen
# =========================================================

class DashboardScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.report = ReportManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="DailyExpense Manager",
            font_size=24,
            size_hint=(1, 0.1)
        )

        root.add_widget(title)

        self.summary = Label(
            text="Loading...",
            halign="left",
            valign="top"
        )

        root.add_widget(self.summary)

        buttons = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )

        buttons.bind(
            minimum_height=buttons.setter("height")
        )

        menu = [
            ("Add Expense", "add"),
            ("Search", "search"),
            ("Reports", "reports"),
            ("Charts", "charts"),
            ("Budget", "budget"),
            ("Backup", "backup"),
            ("Settings", "settings"),
            ("Exit", "exit")
        ]

        for text, action in menu:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=60
            )
            btn.bind(on_release=self.button_click)
            buttons.add_widget(btn)

        scroll = ScrollView()
        scroll.add_widget(buttons)
        root.add_widget(scroll)

        self.add_widget(root)

        Clock.schedule_once(self.load_dashboard, 0.2)

    def on_pre_enter(self, *args):
        self.load_dashboard()

    def load_dashboard(self, *args):
        try:
            total = self.report.total_expense()
            count = self.report.total_transactions()
            self.summary.text = (
                f"Total Expense : ₹ {total:,.2f}\n\n"
                f"Transactions : {count}"
            )
        except Exception as e:
            self.summary.text = f"Error loading summary: {str(e)}"

    def button_click(self, button):
        action_map = {
            "Add Expense": "add",
            "Search": "search",
            "Reports": "reports",
            "Charts": "charts",
            "Budget": "budget",
            "Backup": "backup",
            "Settings": "settings"
        }
        text = button.text
        if text == "Exit":
            App.get_running_app().stop()
        elif text in action_map:
            self.manager.current = action_map[text]


# =========================================================
# Add Expense Screen
# =========================================================

class AddExpenseScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.expense_db = ExpenseManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="Add Expense",
            font_size=24,
            size_hint=(1, .1)
        )
        root.add_widget(title)

        self.category = TextInput(hint_text="Category", multiline=False)
        root.add_widget(self.category)

        self.description = TextInput(hint_text="Description", multiline=False)
        root.add_widget(self.description)

        self.amount = TextInput(
            hint_text="Amount",
            input_filter="float",
            multiline=False
        )
        root.add_widget(self.amount)

        self.payment = TextInput(hint_text="Payment Method", multiline=False)
        root.add_widget(self.payment)

        save = Button(text="Save Expense", size_hint=(1, .1))
        save.bind(on_release=self.save_expense)
        root.add_widget(save)

        home = Button(text="Back to Dashboard", size_hint=(1, .1))
        home.bind(on_release=self.go_home)
        root.add_widget(home)

        self.add_widget(root)

    def popup(self, title, message):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        content.add_widget(Label(text=message))

        btn = Button(text="OK", size_hint=(1, .3))
        popup = Popup(title=title, content=content, size_hint=(.8, .4))
        btn.bind(on_release=popup.dismiss)

        content.add_widget(btn)
        popup.open()

    def save_expense(self, instance):
        try:
            category = self.category.text.strip()
            description = self.description.text.strip()
            amount_text = self.amount.text.strip()
            payment = self.payment.text.strip()

            if not category:
                self.popup("Error", "Category required.")
                return

            if not amount_text:
                self.popup("Error", "Amount required.")
                return

            amount = float(amount_text)

            self.expense_db.add_expense(
                category,
                description,
                amount,
                payment
            )

            self.popup("Success", "Expense saved successfully.")

            self.category.text = ""
            self.description.text = ""
            self.amount.text = ""
            self.payment.text = ""

        except Exception as e:
            self.popup("Error", str(e))

    def go_home(self, instance):
        self.manager.current = "dashboard"


# =========================================================
# Search Expense Screen
# =========================================================

class SearchExpenseScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.manager_db = ExpenseManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="Search Expenses",
            font_size=24,
            size_hint=(1, .1)
        )
        root.add_widget(title)

        self.keyword = TextInput(
            hint_text="Enter Category / Description / Payment Method",
            multiline=False
        )
        root.add_widget(self.keyword)

        search = Button(text="Search", size_hint=(1, .1))
        search.bind(on_release=self.search_expense)
        root.add_widget(search)

        self.result = Label(
            text="",
            valign="top",
            halign="left",
            size_hint_y=None
        )
        self.result.bind(texture_size=lambda instance, val: setattr(instance, 'height', val[1]))
        self.result.bind(width=lambda instance, val: setattr(instance, 'text_size', (val, None)))

        scroll = ScrollView()
        scroll.add_widget(self.result)
        root.add_widget(scroll)

        home = Button(text="Back to Dashboard", size_hint=(1, .1))
        home.bind(on_release=self.go_home)
        root.add_widget(home)

        self.add_widget(root)

    def search_expense(self, instance):
        keyword = self.keyword.text.strip()

        if not keyword:
            self.result.text = "Please enter a search keyword."
            return

        try:
            rows = self.manager_db.search_expenses(keyword)

            if not rows:
                self.result.text = "No matching records found."
                return

            text = ""
            for row in rows:
                text += (
                    f"ID : {row['id']}\n"
                    f"Date : {row['date']}\n"
                    f"Category : {row['category']}\n"
                    f"Description : {row['description']}\n"
                    f"Amount : ₹ {row['amount']:.2f}\n"
                    f"Payment : {row['payment_method']}\n"
                    "------------------------------\n"
                )

            self.result.text = text

        except Exception as e:
            self.result.text = str(e)

    def go_home(self, instance):
        self.manager.current = "dashboard"


# =========================================================
# Reports Screen
# =========================================================

class ReportsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.report = ReportManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="Reports",
            font_size=24,
            size_hint=(1, .1)
        )
        root.add_widget(title)

        menu = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        menu.bind(minimum_height=menu.setter("height"))

        buttons = [
            "Daily Report",
            "Monthly Report",
            "Yearly Report",
            "Category Summary",
            "Payment Summary",
            "Budget Status"
        ]

        for item in buttons:
            btn = Button(text=item, size_hint_y=None, height=60)
            btn.bind(on_release=self.show_report)
            menu.add_widget(btn)

        scroll = ScrollView()
        self.output = Label(
            text="Select a report",
            halign="left",
            valign="top",
            size_hint_y=None
        )
        self.output.bind(texture_size=lambda instance, val: setattr(instance, 'height', val[1]))
        self.output.bind(width=lambda instance, val: setattr(instance, 'text_size', (val, None)))

        scroll.add_widget(self.output)

        root.add_widget(menu)
        root.add_widget(scroll)

        home = Button(text="Back to Dashboard", size_hint=(1, .1))
        home.bind(on_release=self.go_home)
        root.add_widget(home)

        self.add_widget(root)

    def show_report(self, button):
        name = button.text
        try:
            if name == "Daily Report":
                text = self.report.daily_report_text()
            elif name == "Monthly Report":
                text = self.report.monthly_report_text()
            elif name == "Yearly Report":
                text = self.report.yearly_report_text()
            elif name == "Category Summary":
                text = self.report.category_summary_text()
            elif name == "Payment Summary":
                text = self.report.payment_summary_text()
            elif name == "Budget Status":
                text = self.report.budget_summary_text()
            else:
                text = "Unknown Report"

            self.output.text = text

        except Exception as e:
            self.output.text = str(e)

    def go_home(self, instance):
        self.manager.current = "dashboard"


# =========================================================
# Charts Screen
# =========================================================

class ChartsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.chart = ChartManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="Charts",
            font_size=24,
            size_hint=(1, .1)
        )
        root.add_widget(title)

        menu = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        menu.bind(minimum_height=menu.setter("height"))

        chart_buttons = [
            "Category Bar",
            "Category Pie",
            "Payment Pie",
            "Monthly Trend",
            "Budget vs Expense",
            "Generate All"
        ]

        for item in chart_buttons:
            btn = Button(text=item, size_hint_y=None, height=60)
            btn.bind(on_release=self.generate_chart)
            menu.add_widget(btn)

        root.add_widget(menu)

        self.status = Label(
            text="Select a chart to generate.",
            size_hint=(1, .2)
        )
        root.add_widget(self.status)

        home = Button(text="Back to Dashboard", size_hint=(1, .1))
        home.bind(on_release=self.go_home)
        root.add_widget(home)

        self.add_widget(root)

    def generate_chart(self, button):
        try:
            if button.text == "Category Bar":
                self.chart.category_bar_chart()
                self.status.text = "Category Bar Chart Generated."
            elif button.text == "Category Pie":
                self.chart.category_pie_chart()
                self.status.text = "Category Pie Chart Generated."
            elif button.text == "Payment Pie":
                self.chart.payment_method_pie_chart()
                self.status.text = "Payment Method Pie Chart Generated."
            elif button.text == "Monthly Trend":
                self.chart.monthly_trend_chart()
                self.status.text = "Monthly Trend Chart Generated."
            elif button.text == "Budget vs Expense":
                self.chart.budget_vs_expense_chart()
                self.status.text = "Budget vs Expense Chart Generated."
            elif button.text == "Generate All":
                self.chart.generate_all_charts()
                self.status.text = "All Charts Generated Successfully."

        except Exception as e:
            self.status.text = str(e)

    def go_home(self, instance):
        self.manager.current = "dashboard"


# =========================================================
# Budget Screen
# =========================================================

class BudgetScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = SettingsManager()
        self.report = ReportManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="Monthly Budget",
            font_size=24,
            size_hint=(1, .1)
        )
        root.add_widget(title)

        self.budget_input = TextInput(
            hint_text="Enter Monthly Budget",
            input_filter="float",
            multiline=False
        )

        current = self.settings.get_setting("monthly_budget")
        if current:
            self.budget_input.text = str(current)

        root.add_widget(self.budget_input)

        save = Button(text="Save Budget", size_hint=(1, .1))
        save.bind(on_release=self.save_budget)
        root.add_widget(save)

        refresh = Button(text="Refresh Budget Status", size_hint=(1, .1))
        refresh.bind(on_release=self.refresh_status)
        root.add_widget(refresh)

        self.status = Label(
            text="",
            halign="left",
            valign="top"
        )
        root.add_widget(self.status)

        home = Button(text="Back to Dashboard", size_hint=(1, .1))
        home.bind(on_release=self.go_home)
        root.add_widget(home)

        self.add_widget(root)
        self.refresh_status()

    def save_budget(self, instance):
        try:
            val = self.budget_input.text.strip()
            if val:
                self.settings.update_setting("monthly_budget", val)
                self.refresh_status()
                self.status.text = f"Budget saved: ₹ {float(val):,.2f}\n\n" + self.status.text
        except Exception as e:
            self.status.text = f"Error saving budget: {str(e)}"

    def refresh_status(self, *args):
        try:
            text = self.report.budget_summary_text()
            self.status.text = text
        except Exception as e:
            self.status.text = f"Error loading budget status: {str(e)}"

    def go_home(self, instance):
        self.manager.current = "dashboard"


# =========================================================
# Backup Screen
# =========================================================

class BackupScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.backup = BackupManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="Database Backup",
            font_size=24,
            size_hint=(1, .1)
        )
        root.add_widget(title)

        buttons = [
            "Create Backup",
            "Create ZIP Backup",
            "Restore Latest",
            "List Backups",
            "Statistics",
            "Cleanup"
        ]

        grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter("height"))

        for text in buttons:
            btn = Button(text=text, size_hint_y=None, height=60)
            btn.bind(on_release=self.execute_action)
            grid.add_widget(btn)

        root.add_widget(grid)

        self.output = Label(
            text="Backup Manager Ready",
            halign="left",
            valign="top",
            size_hint_y=None
        )
        self.output.bind(texture_size=lambda instance, val: setattr(instance, 'height', val[1]))
        self.output.bind(width=lambda instance, val: setattr(instance, 'text_size', (val, None)))

        scroll = ScrollView()
        scroll.add_widget(self.output)
        root.add_widget(scroll)

        home = Button(text="Back to Dashboard", size_hint=(1, .1))
        home.bind(on_release=self.go_home)
        root.add_widget(home)

        self.add_widget(root)

    def execute_action(self, button):
        try:
            if button.text == "Create Backup":
                ok, msg = self.backup.create_backup()
                self.output.text = msg
            elif button.text == "Create ZIP Backup":
                ok, msg = self.backup.create_zip_backup()
                self.output.text = msg
            elif button.text == "Restore Latest":
                ok, msg = self.backup.restore_latest_backup()
                self.output.text = msg
            elif button.text == "List Backups":
                files = self.backup.list_backups()
                if not files:
                    self.output.text = "No backups available."
                else:
                    self.output.text = "\n".join(files)
            elif button.text == "Statistics":
                stats = self.backup.backup_statistics()
                text = ""
                for key, value in stats.items():
                    text += f"{key} : {value}\n"
                self.output.text = text
            elif button.text == "Cleanup":
                removed = self.backup.cleanup_old_backups(keep_latest=10)
                if removed:
                    self.output.text = "Deleted:\n\n" + "\n".join(removed)
                else:
                    self.output.text = "No old backups to delete."

        except Exception as e:
            self.output.text = str(e)

    def go_home(self, instance):
        self.manager.current = "dashboard"


# =========================================================
# Settings Screen
# =========================================================

class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = SettingsManager()

        root = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        title = Label(
            text="Application Settings",
            font_size=24,
            size_hint=(1, .1)
        )
        root.add_widget(title)

        self.theme = TextInput(hint_text="Theme (Light/Dark)", multiline=False)
        root.add_widget(self.theme)

        self.currency = TextInput(hint_text="Currency (₹,$,€,£)", multiline=False)
        root.add_widget(self.currency)

        self.payment = TextInput(hint_text="Default Payment Method", multiline=False)
        root.add_widget(self.payment)

        self.date_format = TextInput(hint_text="Date Format", multiline=False)
        root.add_widget(self.date_format)

        self.backup_status = TextInput(
            hint_text="Auto Backup (1=ON,0=OFF)",
            multiline=False,
            input_filter="int"
        )
        root.add_widget(self.backup_status)

        self.backup_frequency = TextInput(
            hint_text="Backup Frequency (Daily/Weekly)",
            multiline=False
        )
        root.add_widget(self.backup_frequency)

        self.export_folder = TextInput(hint_text="Export Folder", multiline=False)
        root.add_widget(self.export_folder)

        save = Button(text="Save Settings", size_hint=(1, .1))
        save.bind(on_release=self.save_settings)
        root.add_widget(save)

        reset = Button(text="Reset Settings", size_hint=(1, .1))
        reset.bind(on_release=self.reset_settings)
        root.add_widget(reset)

        home = Button(text="Back to Dashboard", size_hint=(1, .1))
        home.bind(on_release=self.go_home)
        root.add_widget(home)

        self.add_widget(root)

        Clock.schedule_once(self.load_settings, 0.2)

    def load_settings(self, *args):
        try:
            data = self.settings.get_settings()
            if data and len(data) >= 8:
                self.theme.text = str(data[1])
                self.currency.text = str(data[2])
                self.payment.text = str(data[3])
                self.date_format.text = str(data[4])
                self.backup_status.text = str(data[5])
                self.backup_frequency.text = str(data[6])
                self.export_folder.text = str(data[7])
        except Exception:
            pass

    def save_settings(self, instance):
        try:
            self.settings.update_setting("theme", self.theme.text)
            self.settings.update_setting("currency", self.currency.text)
            self.settings.update_setting("payment_method", self.payment.text)
            self.settings.update_setting("date_format", self.date_format.text)
            self.settings.update_setting("auto_backup", int(self.backup_status.text or 0))
            self.settings.update_setting("backup_frequency", self.backup_frequency.text)
            self.settings.update_setting("export_folder", self.export_folder.text)

            self.popup("Success", "Settings Saved")
        except Exception as e:
            self.popup("Error", str(e))

    def reset_settings(self, instance):
        self.settings.reset_defaults()
        self.load_settings()
        self.popup("Reset", "Settings restored to default")

    def popup(self, title, message):
        box = BoxLayout(orientation="vertical", spacing=10, padding=10)
        box.add_widget(Label(text=message))

        btn = Button(text="OK")
        popup = Popup(title=title, content=box, size_hint=(.8, .4))
        btn.bind(on_release=popup.dismiss)

        box.add_widget(btn)
        popup.open()

    def go_home(self, instance):
        self.manager.current = "dashboard"


# =========================================================
# Application Runner
# =========================================================

class DailyExpenseApp(App):

    def build(self):
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(AddExpenseScreen(name="add"))
        sm.add_widget(SearchExpenseScreen(name="search"))
        sm.add_widget(ReportsScreen(name="reports"))
        sm.add_widget(ChartsScreen(name="charts"))
        sm.add_widget(BudgetScreen(name="budget"))
        sm.add_widget(BackupScreen(name="backup"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm


if __name__ == "__main__":
    DailyExpenseApp().run()
