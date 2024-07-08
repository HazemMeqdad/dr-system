import sqlite3
import shutil
import os
import base64

class DB:
    def __init__(self):
        self.db_path = "patient_records.db"
        self.connection = self.create_connection()
        self.create_table()  # Ensure the schema is created the tables

    def create_connection(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
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
                    identification_card TEXT,
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
                    complaint TEXT,
                    medical_history TEXT,
                    examination TEXT,
                    tests_results TEXT,
                    test_image BLOB,
                    diagnosis TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_records (id)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def remove_symptoms_column(self):
        try:
            cursor = self.connection.cursor()
            # Create a new table without the 'symptoms' column
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS new_sick_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    sick_date TEXT NOT NULL,
                    complaint TEXT,
                    medical_history TEXT,
                    examination TEXT,
                    tests_results TEXT,
                    test_image BLOB,
                    diagnosis TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patient_records (id)
                )
            ''')
            # Copy data from the old table to the new table
            cursor.execute('''
                INSERT INTO new_sick_records (id, patient_id, sick_date, complaint, medical_history, examination, tests_results, test_image, diagnosis)
                SELECT id, patient_id, sick_date, complaint, medical_history, examination, tests_results, test_image, diagnosis
                FROM sick_records
            ''')
            # Drop the old table
            cursor.execute('DROP TABLE sick_records')
            # Rename the new table to the original table name
            cursor.execute('ALTER TABLE new_sick_records RENAME TO sick_records')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error removing symptoms column: {e}")

    def get_all_patients(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT id, first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription FROM patient_records')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching patients: {e}")
            return []

    def add_patient_record(self, first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO patient_records (first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding patient: {e}")

    def update_patient(self, id_, first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE patient_records
                SET first_name = ?, last_name = ?, age = ?, gender = ?, identification_card = ?, address = ?, phone = ?, date = ?, description = ?, prescription = ?
                WHERE id = ?
            ''', (first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription, id_))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating patient: {e}")
            return False
        
    def add_sick_record(self, patient_id, sick_date, complaint, medical_history, examination, tests_results, test_image, diagnosis):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO sick_records (patient_id, sick_date, complaint, medical_history, examination, tests_results, test_image, diagnosis)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, sick_date, complaint, medical_history, examination, tests_results, test_image, diagnosis))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding sick record: {e}")

    def get_sick_records(self, patient_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT id, sick_date, complaint, medical_history, examination, tests_results, test_image, diagnosis FROM sick_records WHERE patient_id = ?', (patient_id,))
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
            self.update_schema()  # Ensure the schema is up to date after restore
            print("Restore successful")
        except Exception as e:
            print(f"Error restoring backup: {e}")
