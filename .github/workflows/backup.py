"""
=========================================================
DailyExpense Manager
backup.py

Database Backup & Restore Manager

Compatible with:
- Python 3.11
- Pydroid 3
=========================================================
"""

import os
import shutil
import sqlite3
import zipfile

from datetime import datetime

from database import DB_PATH


class BackupManager:

    def __init__(self):

        self.database = DB_PATH

        self.backup_folder = "backups"

        os.makedirs(
            self.backup_folder,
            exist_ok=True
        )

    # -------------------------------------------------
    # Generate Timestamp
    # -------------------------------------------------

    def timestamp(self):

        return datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    # -------------------------------------------------
    # Database Exists
    # -------------------------------------------------

    def database_exists(self):

        return os.path.exists(
            self.database
        )

    # -------------------------------------------------
    # Backup Exists
    # -------------------------------------------------

    def backup_exists(self, filename):

        return os.path.exists(
            os.path.join(
                self.backup_folder,
                filename
            )
        )

    # -------------------------------------------------
    # Create SQLite Backup
    # -------------------------------------------------

    def create_backup(self):

        if not self.database_exists():

            return (
                False,
                "Database not found."
            )

        filename = (
            "expense_backup_"
            + self.timestamp()
            + ".db"
        )

        destination = os.path.join(
            self.backup_folder,
            filename
        )

        try:

            shutil.copy2(
                self.database,
                destination
            )

            return (
                True,
                destination
            )

        except Exception as e:

            return (
                False,
                str(e)
            )

    # -------------------------------------------------
    # List Backups
    # -------------------------------------------------

    def list_backups(self):

        files = []

        for file in os.listdir(
            self.backup_folder
        ):

            if file.endswith(".db"):

                files.append(file)

        files.sort(reverse=True)

        return files

    # -------------------------------------------------
    # Backup Information
    # -------------------------------------------------

    def backup_information(self):

        backups = self.list_backups()

        info = []

        for file in backups:

            path = os.path.join(
                self.backup_folder,
                file
            )

            size = os.path.getsize(path)

            modified = datetime.fromtimestamp(
                os.path.getmtime(path)
            )

            info.append({

                "file": file,

                "size_kb":
                    round(size / 1024, 2),

                "modified":
                    modified.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )

            })

        return info
            # -------------------------------------------------
    # Restore Database
    # -------------------------------------------------

    def restore_backup(self, backup_file):
        """
        Restore the SQLite database from a backup.

        Parameters
        ----------
        backup_file : str
            Backup filename (inside backups folder)
            or full file path.

        Returns
        -------
        (True, message) on success
        (False, error) on failure
        """

        # Determine source file
        if os.path.isabs(backup_file):
            source = backup_file
        else:
            source = os.path.join(
                self.backup_folder,
                backup_file
            )

        # Check backup exists
        if not os.path.exists(source):
            return (
                False,
                "Backup file not found."
            )

        try:

            # Verify SQLite file
            conn = sqlite3.connect(source)
            conn.execute("PRAGMA integrity_check;")
            conn.close()

            # Restore database
            shutil.copy2(
                source,
                self.database
            )

            return (
                True,
                "Database restored successfully."
            )

        except sqlite3.DatabaseError:

            return (
                False,
                "Invalid SQLite backup file."
            )

        except Exception as e:

            return (
                False,
                str(e)
            )

    # -------------------------------------------------
    # Restore Latest Backup
    # -------------------------------------------------

    def restore_latest_backup(self):

        backups = self.list_backups()

        if len(backups) == 0:

            return (
                False,
                "No backup available."
            )

        latest = backups[0]

        return self.restore_backup(latest)
            # -------------------------------------------------
    # Create ZIP Backup
    # -------------------------------------------------

    def create_zip_backup(self):
        """
        Create a compressed ZIP backup of the database.
        """

        if not self.database_exists():

            return (
                False,
                "Database not found."
            )

        filename = (
            "expense_backup_"
            + self.timestamp()
            + ".zip"
        )

        zip_path = os.path.join(
            self.backup_folder,
            filename
        )

        try:

            with zipfile.ZipFile(
                zip_path,
                "w",
                zipfile.ZIP_DEFLATED
            ) as zipf:

                zipf.write(
                    self.database,
                    arcname=os.path.basename(self.database)
                )

            return (
                True,
                zip_path
            )

        except Exception as e:

            return (
                False,
                str(e)
            )

    # -------------------------------------------------
    # Restore ZIP Backup
    # -------------------------------------------------

    def restore_zip_backup(self, zip_file):
        """
        Restore database from ZIP backup.
        """

        if os.path.isabs(zip_file):
            source = zip_file
        else:
            source = os.path.join(
                self.backup_folder,
                zip_file
            )

        if not os.path.exists(source):

            return (
                False,
                "ZIP backup not found."
            )

        try:

            with zipfile.ZipFile(source, "r") as zipf:

                db_files = [
                    f for f in zipf.namelist()
                    if f.endswith(".db")
                ]

                if not db_files:
                    return (
                        False,
                        "No database found in ZIP."
                    )

                temp_db = db_files[0]

                zipf.extract(
                    temp_db,
                    self.backup_folder
                )

                extracted = os.path.join(
                    self.backup_folder,
                    temp_db
                )

                shutil.copy2(
                    extracted,
                    self.database
                )

                os.remove(extracted)

            return (
                True,
                "ZIP backup restored successfully."
            )

        except Exception as e:

            return (
                False,
                str(e)
            )

    # -------------------------------------------------
    # Delete Backup
    # -------------------------------------------------

    def delete_backup(self, backup_file):
        """
        Delete a backup (.db or .zip).
        """

        if os.path.isabs(backup_file):
            file_path = backup_file
        else:
            file_path = os.path.join(
                self.backup_folder,
                backup_file
            )

        if not os.path.exists(file_path):

            return (
                False,
                "Backup file not found."
            )

        try:

            os.remove(file_path)

            return (
                True,
                "Backup deleted successfully."
            )

        except Exception as e:

            return (
                False,
                str(e)
            )
                # -------------------------------------------------
    # Verify Backup
    # -------------------------------------------------

    def verify_backup(self, backup_file):
        """
        Verify whether a backup is a valid SQLite database.
        """

        if os.path.isabs(backup_file):
            file_path = backup_file
        else:
            file_path = os.path.join(
                self.backup_folder,
                backup_file
            )

        if not os.path.exists(file_path):
            return False, "Backup file not found."

        try:
            conn = sqlite3.connect(file_path)
            result = conn.execute(
                "PRAGMA integrity_check;"
            ).fetchone()[0]
            conn.close()

            if result.lower() == "ok":
                return True, "Backup verified successfully."

            return False, result

        except Exception as e:
            return False, str(e)

    # -------------------------------------------------
    # Cleanup Old Backups
    # -------------------------------------------------

    def cleanup_old_backups(self, keep_latest=10):
        """
        Keep only the latest 'keep_latest' backups.
        Deletes older .db and .zip backup files.
        """

        files = []

        for file in os.listdir(self.backup_folder):

            if file.endswith(".db") or file.endswith(".zip"):

                path = os.path.join(
                    self.backup_folder,
                    file
                )

                files.append((
                    os.path.getmtime(path),
                    path
                ))

        files.sort(reverse=True)

        removed = []

        for _, path in files[keep_latest:]:

            try:
                os.remove(path)
                removed.append(os.path.basename(path))
            except Exception:
                pass

        return removed

    # -------------------------------------------------
    # Backup Statistics
    # -------------------------------------------------

    def backup_statistics(self):

        db_count = 0
        zip_count = 0
        total_size = 0

        for file in os.listdir(self.backup_folder):

            path = os.path.join(
                self.backup_folder,
                file
            )

            if file.endswith(".db"):
                db_count += 1

            elif file.endswith(".zip"):
                zip_count += 1

            total_size += os.path.getsize(path)

        return {
            "database_backups": db_count,
            "zip_backups": zip_count,
            "total_backups": db_count + zip_count,
            "total_size_mb": round(
                total_size / (1024 * 1024),
                2
            )
        }


# -------------------------------------------------
# Test Program
# -------------------------------------------------

if __name__ == "__main__":

    backup = BackupManager()

    print("=" * 60)
    print("DailyExpense Backup Manager")
    print("=" * 60)

    success, message = backup.create_backup()

    print("\nCreate Backup")
    print(success, message)

    success, message = backup.create_zip_backup()

    print("\nCreate ZIP Backup")
    print(success, message)

    print("\nAvailable Backups")

    for file in backup.list_backups():

        print(" -", file)

    print("\nStatistics")

    stats = backup.backup_statistics()

    for key, value in stats.items():

        print(f"{key:20}: {value}")

    removed = backup.cleanup_old_backups(
        keep_latest=10
    )

    print("\nRemoved Old Backups")

    if removed:

        for item in removed:
            print(" -", item)

    else:
        print("None")

    print("\nBackup Manager Ready.")