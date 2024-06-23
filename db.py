import sqlite3
import os
import shutil
import pandas as pd

class DB:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect("patient_records.db")
            print(f"Connected to SQLite version {sqlite3.version}")
            return connection
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return connection

    def create_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patient_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    address TEXT,
                    phone TEXT,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    prescription TEXT NOT NULL
                )
            ''')
            self.connection.commit()
            print("Table created successfully")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_patient_record(self, first_name, last_name, age, gender, address, phone, date, description, prescription):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO patient_records (first_name, last_name, age, gender, address, phone, date, description, prescription)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, age, gender, address, phone, date, description, prescription))
            self.connection.commit()
            print("Patient record added successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error adding patient record: {e}")
            return False

    def update_patient_record(self, selected_record, first_name, last_name, age, gender, address, phone, date, description, prescription):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE patient_records
                SET first_name=?, last_name=?, age=?, gender=?, address=?, phone=?, date=?, description=?, prescription=?
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            ''', (first_name, last_name, age, gender, address, phone, date, description, prescription, f'%{selected_record}%', f'%{selected_record}%'))
            self.connection.commit()
            print("Patient record updated successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error updating patient record: {e}")
            return False

    def search_patient_record(self, search_query):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM patient_records
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            ''', (f'%{search_query}%', f'%{search_query}%'))
            records = cursor.fetchall()
            return records
        except sqlite3.Error as e:
            print(f"Error searching patient records: {e}")
            return []

    def delete_patient_record(self, selected_record):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                DELETE FROM patient_records
                WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?
            ''', (f'%{selected_record}%', f'%{selected_record}%'))
            self.connection.commit()
            print("Patient record deleted successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error deleting patient record: {e}")
            return False

    def update_backup(self):
        try:
            backup_folder = "backup"
            os.makedirs(backup_folder, exist_ok=True)
            backup_db_path = os.path.join(backup_folder, "patient_records_backup.db")
            backup_excel_path = os.path.join(backup_folder, "patient_records_backup.xlsx")

            shutil.copy2("patient_records.db", backup_db_path)

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM patient_records")
            records = cursor.fetchall()

            df = pd.DataFrame(records, columns=["ID", "First Name", "Last Name", "Age", "Gender", "Address", "Phone", "Date", "Description", "Prescription"])
            df.to_excel(backup_excel_path, index=False)
            print("Backup updated successfully")
            return True
        except Exception as e:
            print(f"Failed to update backup: {e}")
            return False

    def import_data(self, import_file_path):
        try:
            connection = self.create_connection()
            if connection:
                df = pd.read_excel(import_file_path)

                cursor = connection.cursor()
                cursor.execute("DELETE FROM patient_records")

                for _, row in df.iterrows():
                    cursor.execute('''
                        INSERT INTO patient_records (first_name, last_name, age, gender, address, phone, date, description, prescription)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (row["First Name"], row["Last Name"], row["Age"], row["Gender"], row["Address"], row["Phone"], row["Date"], row["Description"], row["Prescription"]))

                connection.commit()
                connection.close()
                print("Data imported successfully")
                return True
        except Exception as e:
            print(f"Failed to import data: {e}")
            return False
