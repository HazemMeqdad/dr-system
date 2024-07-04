import sqlite3

class DB:
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        try:
            self.connection = sqlite3.connect("patient_records.db")
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
