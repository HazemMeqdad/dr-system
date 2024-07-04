from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
import typing as t
from db import DB

class HomePage(QWidget):
    def __init__(self, db: DB, *args, **kwargs) -> None:
        self.db = db
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/home.ui", self)

        self.change_btn = self.findChild(QPushButton, 'change_btn')
        if self.change_btn is None:
            raise Exception("change_btn not found. Make sure the object name is correct in the UI file.")

        self.patient_table = self.findChild(QTableWidget, 'patient_table')
        if self.patient_table is None:
            raise Exception("patient_table not found. Make sure the object name is correct in the UI file.")

        self.search_bar = self.findChild(QLineEdit, 'search_bar')
        if self.search_bar is None:
            raise Exception("search_bar not found. Make sure the object name is correct in the UI file.")

        self.search_bar.textChanged.connect(self.filter_table)

        # Set table headers
        headers = ["ID", "First Name", "Last Name", "Age", "Gender", "Address", "Phone"]
        self.patient_table.setColumnCount(len(headers))
        self.patient_table.setHorizontalHeaderLabels(headers)

        # Static data for patients
        self.patients = [
            [1, "John", "Doe", 30, "Male", "123 Elm St", "123-456-7890"],
            [2, "Jane", "Smith", 25, "Female", "456 Oak St", "234-567-8901"],
            [3, "Alice", "Johnson", 28, "Female", "789 Pine St", "345-678-9012"],
            [4, "Bob", "Brown", 35, "Male", "101 Maple St", "456-789-0123"],
        ]
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
