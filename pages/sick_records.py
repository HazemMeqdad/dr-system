from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtCore import QDate
from db import DB

class SickRecordsPage(QWidget):
    def __init__(self, db: DB, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/sick_records.ui", self)

        self.db = db
        self.patient_id = None

        self.sick_records_table = self.findChild(QTableWidget, 'sick_records_table')
        self.sick_date = self.findChild(QLineEdit, 'sick_date')
        self.symptoms = self.findChild(QTextEdit, 'symptoms')

        self.add_sick_record_btn = self.findChild(QPushButton, 'add_sick_record_btn')
        self.back_btn = self.findChild(QPushButton, 'back_btn')

        self.add_sick_record_btn.clicked.connect(self.add_sick_record)
        self.back_btn.clicked.connect(self.go_back)

        # Set table headers
        headers = ["ID", "Sick Date", "Symptoms"]
        self.sick_records_table.setColumnCount(len(headers))
        self.sick_records_table.setHorizontalHeaderLabels(headers)

        # Disable the table but allow selection
        self.sick_records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sick_records_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sick_records_table.setSelectionMode(QTableWidget.SingleSelection)

    def load_sick_records(self, patient_id):
        self.patient_id = patient_id
        sick_records = self.db.get_sick_records(patient_id)
        self.populate_table(sick_records)

    def populate_table(self, data):
        self.sick_records_table.setRowCount(len(data))
        for row_idx, record in enumerate(data):
            for col_idx, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                self.sick_records_table.setItem(row_idx, col_idx, item)

    def add_sick_record(self):
        sick_date = self.sick_date.text().strip()
        symptoms = self.symptoms.toPlainText().strip()
        if not sick_date or not symptoms:
            QMessageBox.critical(self, "Validation Error", "Sick date and symptoms are required.")
            return
        self.db.add_sick_record(self.patient_id, sick_date, symptoms)
        self.load_sick_records(self.patient_id)
        self.sick_date.clear()
        self.symptoms.clear()

    def go_back(self):
        self.parentWidget().setCurrentIndex(0)  # Switch back to home page
