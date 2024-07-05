from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtCore import Qt
from db import DB

class HomePage(QWidget):
    def __init__(self, db: DB, main_window, *args, **kwargs) -> None:
        self.db = db
        self.main_window = main_window
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/home.ui", self)

        self.change_btn = self.findChild(QPushButton, 'change_btn')
        self.add_patient_btn = self.findChild(QPushButton, 'change_btn_2')
        self.sick_records_btn = self.findChild(QPushButton, 'sick_records_btn')
        self.patient_table = self.findChild(QTableWidget, 'patient_table')
        self.search_bar = self.findChild(QLineEdit, 'search_bar')

        self.search_bar.textChanged.connect(self.filter_table)

        # Set table headers
        headers = ["ID", "First Name", "Last Name", "Age", "Gender", "Address", "Phone", "Date", "Description", "Prescription"]
        self.patient_table.setColumnCount(len(headers))
        self.patient_table.setHorizontalHeaderLabels(headers)

        # Disable the table but allow selection
        self.patient_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.patient_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.patient_table.setSelectionMode(QTableWidget.SingleSelection)

        self.load_patients()

        self.sick_records_btn.clicked.connect(self.view_sick_records)

    def load_patients(self):
        self.patients = self.db.get_all_patients()
        self.populate_table(self.patients)

    def populate_table(self, data):
        self.patient_table.setRowCount(len(data))
        for row_idx, patient in enumerate(data):
            for col_idx, value in enumerate(patient):
                item = QTableWidgetItem(str(value))
                self.patient_table.setItem(row_idx, col_idx, item)

    def filter_table(self):
        filter_text = self.search_bar.text().lower()
        filtered_data = [
            patient for patient in self.patients
            if any(filter_text in str(value).lower() for value in patient)
        ]
        self.populate_table(filtered_data)

    def get_selected_patient(self):
        selected_row = self.patient_table.currentRow()
        if selected_row >= 0:
            return self.patients[selected_row]
        return None

    def view_sick_records(self):
        selected_patient = self.get_selected_patient()
        if selected_patient:
            self.main_window.view_sick_records(selected_patient[0])
