"""
=========================================================
DailyExpense Manager
utils.py

Common Utility Functions

Compatible with:
- Python 3.11
- Pydroid 3
=========================================================
"""

import os
from datetime import datetime


class Utils:

    # -------------------------------------------------
    # Current Date
    # -------------------------------------------------

    @staticmethod
    def current_date():

        return datetime.now().strftime("%d-%m-%Y")

    # -------------------------------------------------
    # Current Time
    # -------------------------------------------------

    @staticmethod
    def current_time():

        return datetime.now().strftime("%H:%M:%S")

    # -------------------------------------------------
    # Current Date Time
    # -------------------------------------------------

    @staticmethod
    def current_datetime():

        return datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    # -------------------------------------------------
    # Format Currency
    # -------------------------------------------------

    @staticmethod
    def format_currency(
        amount,
        symbol="₹"
    ):

        try:

            return f"{symbol} {float(amount):,.2f}"

        except Exception:

            return f"{symbol} 0.00"

    # -------------------------------------------------
    # Convert String to Float
    # -------------------------------------------------

    @staticmethod
    def to_float(value):

        try:

            return float(value)

        except Exception:

            return 0.0

    # -------------------------------------------------
    # Convert String to Integer
    # -------------------------------------------------

    @staticmethod
    def to_int(value):

        try:

            return int(value)

        except Exception:

            return 0

    # -------------------------------------------------
    # Check File Exists
    # -------------------------------------------------

    @staticmethod
    def file_exists(path):

        return os.path.isfile(path)

    # -------------------------------------------------
    # Check Folder Exists
    # -------------------------------------------------

    @staticmethod
    def folder_exists(path):

        return os.path.isdir(path)

    # -------------------------------------------------
    # Create Folder
    # -------------------------------------------------

    @staticmethod
    def create_folder(path):

        os.makedirs(
            path,
            exist_ok=True
        )

        return path
            # -------------------------------------------------
    # Validate Date
    # -------------------------------------------------

    @staticmethod
    def validate_date(date_string, fmt="%d-%m-%Y"):

        try:
            datetime.strptime(date_string, fmt)
            return True
        except ValueError:
            return False

    # -------------------------------------------------
    # Validate Amount
    # -------------------------------------------------

    @staticmethod
    def validate_amount(amount):

        try:
            value = float(amount)
            return value >= 0
        except Exception:
            return False

    # -------------------------------------------------
    # Validate Integer
    # -------------------------------------------------

    @staticmethod
    def validate_integer(value):

        try:
            int(value)
            return True
        except Exception:
            return False

    # -------------------------------------------------
    # Validate Float
    # -------------------------------------------------

    @staticmethod
    def validate_float(value):

        try:
            float(value)
            return True
        except Exception:
            return False

    # -------------------------------------------------
    # Validate Email Address
    # -------------------------------------------------

    @staticmethod
    def validate_email(email):

        import re

        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        return re.match(pattern, email) is not None

    # -------------------------------------------------
    # Validate Mobile Number
    # -------------------------------------------------

    @staticmethod
    def validate_mobile(number):

        import re

        number = str(number).strip()

        pattern = r'^[6-9]\d{9}$'

        return re.match(pattern, number) is not None

    # -------------------------------------------------
    # Remove Invalid Filename Characters
    # -------------------------------------------------

    @staticmethod
    def sanitize_filename(filename):

        invalid = '\\/:*?"<>|'

        for char in invalid:
            filename = filename.replace(char, "_")

        return filename.strip()

    # -------------------------------------------------
    # Human Readable File Size
    # -------------------------------------------------

    @staticmethod
    def format_file_size(size):

        size = float(size)

        units = ["Bytes", "KB", "MB", "GB", "TB"]

        index = 0

        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1

        return f"{size:.2f} {units[index]}"
            # -------------------------------------------------
    # Generate Timestamp
    # -------------------------------------------------

    @staticmethod
    def timestamp():

        return datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    # -------------------------------------------------
    # Generate UUID
    # -------------------------------------------------

    @staticmethod
    def generate_uuid():

        import uuid

        return str(uuid.uuid4())

    # -------------------------------------------------
    # Generate Random ID
    # -------------------------------------------------

    @staticmethod
    def random_id(length=8):

        import random
        import string

        chars = (
            string.ascii_uppercase +
            string.digits
        )

        return "".join(
            random.choice(chars)
            for _ in range(length)
        )

    # -------------------------------------------------
    # Generate Backup Filename
    # -------------------------------------------------

    @staticmethod
    def backup_filename(prefix="expense_backup"):

        return (
            f"{prefix}_"
            f"{Utils.timestamp()}.db"
        )

    # -------------------------------------------------
    # Generate Export Filename
    # -------------------------------------------------

    @staticmethod
    def export_filename(
        prefix="expense_report",
        extension="csv"
    ):

        return (
            f"{prefix}_"
            f"{Utils.timestamp()}."
            f"{extension}"
        )

    # -------------------------------------------------
    # Calculate Folder Size
    # -------------------------------------------------

    @staticmethod
    def folder_size(folder):

        total = 0

        if not os.path.exists(folder):
            return 0

        for root, dirs, files in os.walk(folder):

            for file in files:

                path = os.path.join(
                    root,
                    file
                )

                if os.path.isfile(path):

                    total += os.path.getsize(path)

        return total

    # -------------------------------------------------
    # Copy File
    # -------------------------------------------------

    @staticmethod
    def copy_file(source, destination):

        import shutil

        try:

            shutil.copy2(
                source,
                destination
            )

            return True

        except Exception:

            return False

    # -------------------------------------------------
    # Move File
    # -------------------------------------------------

    @staticmethod
    def move_file(source, destination):

        import shutil

        try:

            shutil.move(
                source,
                destination
            )

            return True

        except Exception:

            return False

    # -------------------------------------------------
    # Delete File
    # -------------------------------------------------

    @staticmethod
    def delete_file(filename):

        try:

            if os.path.exists(filename):

                os.remove(filename)

                return True

            return False

        except Exception:

            return False

    # -------------------------------------------------
    # Write Log
    # -------------------------------------------------

    @staticmethod
    def write_log(message, logfile="application.log"):

        try:

            with open(
                logfile,
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    f"[{Utils.current_datetime()}] "
                    f"{message}\n"
                )

            return True

        except Exception:

            return False
            
                # -------------------------------------------------
    # Calculate MD5 Hash
    # -------------------------------------------------

    @staticmethod
    def md5_hash(filename):

        import hashlib

        if not os.path.exists(filename):
            return None

        md5 = hashlib.md5()

        with open(filename, "rb") as file:

            while True:

                data = file.read(4096)

                if not data:
                    break

                md5.update(data)

        return md5.hexdigest()

    # -------------------------------------------------
    # Calculate SHA256 Hash
    # -------------------------------------------------

    @staticmethod
    def sha256_hash(filename):

        import hashlib

        if not os.path.exists(filename):
            return None

        sha = hashlib.sha256()

        with open(filename, "rb") as file:

            while True:

                data = file.read(4096)

                if not data:
                    break

                sha.update(data)

        return sha.hexdigest()

    # -------------------------------------------------
    # Database Exists
    # -------------------------------------------------

    @staticmethod
    def database_exists(db_path):

        return os.path.isfile(db_path)

    # -------------------------------------------------
    # Internet Connection Check
    # -------------------------------------------------

    @staticmethod
    def internet_available(timeout=5):

        import socket

        try:

            socket.setdefaulttimeout(timeout)

            socket.create_connection(
                ("8.8.8.8", 53)
            )

            return True

        except Exception:

            return False

    # -------------------------------------------------
    # System Information
    # -------------------------------------------------

    @staticmethod
    def system_information():

        import platform

        return {

            "Operating System":
                platform.system(),

            "OS Version":
                platform.version(),

            "Machine":
                platform.machine(),

            "Processor":
                platform.processor(),

            "Python":
                platform.python_version()

        }


# -------------------------------------------------
# Test Program
# -------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("DailyExpense Utility Module")
    print("=" * 60)

    print("\nCurrent Date :", Utils.current_date())
    print("Current Time :", Utils.current_time())

    print("\nCurrency Example")
    print(Utils.format_currency(12345.67))

    print("\nRandom ID")
    print(Utils.random_id())

    print("\nUUID")
    print(Utils.generate_uuid())

    print("\nInternet Available")
    print(Utils.internet_available())

    print("\nSystem Information")

    info = Utils.system_information()

    for key, value in info.items():

        print(f"{key:20}: {value}")

    print("\nApplication Log")

    Utils.write_log(
        "Utility Module Executed"
    )

    print("Log file updated.")

    print("\nHash Example")

    if Utils.file_exists("utils.py"):

        print("MD5")
        print(Utils.md5_hash("utils.py"))

        print()

        print("SHA256")
        print(Utils.sha256_hash("utils.py"))

    print("\nDone.")