"""
=========================================================
DailyExpense Manager
settings.py

Application Settings Manager

Compatible with:
- Python 3.11
- Pydroid 3
=========================================================
"""

import sqlite3
from database import DB_PATH


class SettingsManager:

    def __init__(self):

        self.db = DB_PATH

        self.create_settings_table()

        self.create_default_settings()

    # -------------------------------------------------
    # Database Connection
    # -------------------------------------------------

    def connect(self):

        return sqlite3.connect(self.db)

    # -------------------------------------------------
    # Create Settings Table
    # -------------------------------------------------

    def create_settings_table(self):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS settings
        (
            setting_key TEXT PRIMARY KEY,
            setting_value TEXT
        )
        """)

        conn.commit()

        conn.close()

    # -------------------------------------------------
    # Create Default Settings
    # -------------------------------------------------

    def create_default_settings(self):

        defaults = {

            "currency": "₹",

            "theme": "Light",

            "date_format": "%d-%m-%Y",

            "default_payment": "Cash",

            "monthly_budget": "0",

            "backup_folder": "backups",

            "export_folder": "exports",

            "chart_folder": "charts",

            "auto_backup": "Yes",

            "backup_interval": "Daily",

            "keep_backups": "10"

        }

        conn = self.connect()

        cur = conn.cursor()

        for key, value in defaults.items():

            cur.execute("""

            INSERT OR IGNORE INTO settings

            (setting_key, setting_value)

            VALUES (?,?)

            """, (key, value))

        conn.commit()

        conn.close()

    # -------------------------------------------------
    # Load All Settings
    # -------------------------------------------------

    def load_settings(self):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""

        SELECT

            setting_key,

            setting_value

        FROM settings

        ORDER BY setting_key

        """)

        rows = cur.fetchall()

        conn.close()

        data = {}

        for key, value in rows:

            data[key] = value

        return data
            # -------------------------------------------------
    # Get Single Setting
    # -------------------------------------------------

    def get_setting(self, key):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""

        SELECT setting_value

        FROM settings

        WHERE setting_key=?

        """, (key,))

        row = cur.fetchone()

        conn.close()

        if row:

            return row[0]

        return None

    # -------------------------------------------------
    # Check Setting Exists
    # -------------------------------------------------

    def setting_exists(self, key):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""

        SELECT COUNT(*)

        FROM settings

        WHERE setting_key=?

        """, (key,))

        exists = cur.fetchone()[0]

        conn.close()

        return exists > 0

    # -------------------------------------------------
    # Save New Setting
    # -------------------------------------------------

    def save_setting(self, key, value):

        if self.setting_exists(key):

            return False

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""

        INSERT INTO settings

        (setting_key, setting_value)

        VALUES (?,?)

        """, (key, str(value)))

        conn.commit()

        conn.close()

        return True

    # -------------------------------------------------
    # Update Existing Setting
    # -------------------------------------------------

    def update_setting(self, key, value):

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""

        UPDATE settings

        SET setting_value=?

        WHERE setting_key=?

        """, (str(value), key))

        conn.commit()

        conn.close()

        return True

    # -------------------------------------------------
    # Set Setting
    # Creates new or updates existing
    # -------------------------------------------------

    def set_setting(self, key, value):

        if self.setting_exists(key):

            return self.update_setting(
                key,
                value
            )

        return self.save_setting(
            key,
            value
        )

    # -------------------------------------------------
    # Delete Setting
    # -------------------------------------------------

    def delete_setting(self, key):

        if not self.setting_exists(key):

            return False

        conn = self.connect()

        cur = conn.cursor()

        cur.execute("""

        DELETE FROM settings

        WHERE setting_key=?

        """, (key,))

        conn.commit()

        conn.close()

        return True
        
           # -------------------------------------------------
    # Reset All Settings to Default
    # -------------------------------------------------

    def reset_defaults(self):
        """
        Reset all application settings to their default values.
        """

        defaults = {

            "currency": "₹",

            "theme": "Light",

            "date_format": "%d-%m-%Y",

            "default_payment": "Cash",

            "monthly_budget": "0",

            "backup_folder": "backups",

            "export_folder": "exports",

            "chart_folder": "charts",

            "auto_backup": "Yes",

            "backup_interval": "Daily",

            "keep_backups": "10"

        }

        conn = self.connect()

        cur = conn.cursor()

        try:

            # Remove all existing settings
            cur.execute("DELETE FROM settings")

            # Insert default settings
            for key, value in defaults.items():

                cur.execute("""

                INSERT INTO settings
                (setting_key, setting_value)
                VALUES (?,?)

                """, (key, str(value)))

            conn.commit()

            return (
                True,
                "Settings restored to default values."
            )

        except Exception as e:

            conn.rollback()

            return (
                False,
                str(e)
            )

        finally:

            conn.close()
                # -------------------------------------------------
    # Export Settings to JSON
    # -------------------------------------------------

    def export_settings(self, filename="settings.json"):
        """
        Export all application settings to a JSON file.
        """

        import json

        try:

            settings = self.load_settings()

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    settings,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return (
                True,
                filename
            )

        except Exception as e:

            return (
                False,
                str(e)
            )

    # -------------------------------------------------
    # Import Settings from JSON
    # -------------------------------------------------

    def import_settings(self, filename):
        """
        Import settings from a JSON file.
        Existing settings are updated automatically.
        """

        import json
        import os

        if not os.path.exists(filename):

            return (
                False,
                "Settings file not found."
            )

        try:

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as file:

                settings = json.load(file)

            for key, value in settings.items():

                self.set_setting(
                    key,
                    value
                )

            return (
                True,
                "Settings imported successfully."
            )

        except Exception as e:

            return (
                False,
                str(e)
            )

    # -------------------------------------------------
    # Print Settings
    # -------------------------------------------------

    def print_settings(self):

        settings = self.load_settings()

        print("=" * 60)
        print("APPLICATION SETTINGS")
        print("=" * 60)

        for key in sorted(settings.keys()):

            print("{:<25} {}".format(
                key,
                settings[key]
            ))

        print("=" * 60)
        