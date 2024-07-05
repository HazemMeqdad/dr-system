import sqlite3
import shutil
import os

class DB:
    def __init__(self):
        self.db_path = "patient_records.db"
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.create_table()
            return self.connection
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sick_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    sick_date TEXT NOT NULL,
                    symptoms TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patient_records (id)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def get_all_patients(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT id, first_name, last_name, age, gender, address, phone, date, description, prescription FROM patient_records')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching patients: {e}")
            return []

    def add_patient_record(self, first_name, last_name, age, gender, address, phone, date, description, prescription):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO patient_records (first_name, last_name, age, gender, address, phone, date, description, prescription)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, age, gender, address, phone, date, description, prescription))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding patient: {e}")

    def update_patient_record(self, id_, first_name, last_name, age, gender, address, phone, date, description, prescription):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE patient_records
                SET first_name = ?, last_name = ?, age = ?, gender = ?, address = ?, phone = ?, date = ?, description = ?, prescription = ?
                WHERE id = ?
            ''', (first_name, last_name, age, gender, address, phone, date, description, prescription, id_))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating patient: {e}")

    def add_sick_record(self, patient_id, sick_date, symptoms):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO sick_records (patient_id, sick_date, symptoms)
                VALUES (?, ?, ?)
            ''', (patient_id, sick_date, symptoms))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding sick record: {e}")

    def get_sick_records(self, patient_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT id, sick_date, symptoms FROM sick_records WHERE patient_id = ?', (patient_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching sick records: {e}")
            return []

    def backup_database(self, backup_path):
        try:
            shutil.copy(self.db_path, backup_path)
            print("Backup successful")
        except Exception as e:
            print(f"Error creating backup: {e}")

    def restore_database(self, backup_path):
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
            shutil.copy(backup_path, self.db_path)
            self.connection.close()
            self.connection = self.create_connection()
            print("Restore successful")
        except Exception as e:
            print(f"Error restoring backup: {e}")
