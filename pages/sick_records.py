from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap
from db import DB
import base64

class SickRecordsPage(QWidget):
    def __init__(self, db: DB, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/sick_records.ui", self)

        self.db = db
        self.patient_id = None
        self.test_image_data = None

        self.sick_records_table = self.findChild(QTableWidget, 'sick_records_table')
        self.sick_date = self.findChild(QDateEdit, 'sick_date')
        self.complaint = self.findChild(QLineEdit, 'complaint')
        self.medical_history = self.findChild(QLineEdit, 'medical_history')
        self.examination = self.findChild(QLineEdit, 'examination')
        self.tests_results = self.findChild(QLineEdit, 'tests_results')
        self.diagnosis = self.findChild(QLineEdit, 'diagnosis')
        self.image_label = self.findChild(QLabel, 'image_label')

        self.upload_image_btn = self.findChild(QPushButton, 'upload_image_btn')
        self.add_sick_record_btn = self.findChild(QPushButton, 'add_sick_record_btn')
        self.back_btn = self.findChild(QPushButton, 'back_btn')

        self.upload_image_btn.clicked.connect(self.upload_image)
        self.add_sick_record_btn.clicked.connect(self.add_sick_record)
        self.back_btn.clicked.connect(self.go_back)

        # Set table headers
        headers = ["ID", "Sick Date", "Complaint", "Medical History", "Examination", "Tests Results", "Diagnosis"]
        self.sick_records_table.setColumnCount(len(headers))
        self.sick_records_table.setHorizontalHeaderLabels(headers)

        # Disable the table but allow selection
        self.sick_records_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sick_records_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sick_records_table.setSelectionMode(QTableWidget.SingleSelection)

        # Set the default value of the sick date to the current date
        self.sick_date.setDate(QDate.currentDate())

    def load_sick_records(self, patient_id):
        self.patient_id = patient_id
        sick_records = self.db.get_sick_records(patient_id)
        self.populate_table(sick_records)

    def populate_table(self, data):
        self.sick_records_table.setRowCount(len(data))
        for row_idx, record in enumerate(data):
            for col_idx, value in enumerate(record[:7]):
                item = QTableWidgetItem(str(value))
                self.sick_records_table.setItem(row_idx, col_idx, item)
            if record[6]:  # If there is an image
                pixmap = QPixmap()
                pixmap.loadFromData(base64.b64decode(record[6]))
                self.image_label.setPixmap(pixmap.scaled(200, 200, aspectRatioMode=Qt.KeepAspectRatio))
            else:
                self.image_label.setText("No image uploaded")

    def add_sick_record(self):
        sick_date = self.sick_date.date().toString("dd/MM/yyyy")
        complaint = self.complaint.text().strip()
        medical_history = self.medical_history.text().strip()
        examination = self.examination.text().strip()
        tests_results = self.tests_results.text().strip()
        diagnosis = self.diagnosis.text().strip()

        if not sick_date or not complaint or not medical_history or not examination or not tests_results or not diagnosis:
            QMessageBox.critical(self, "Validation Error", "All fields are required.")
            return

        if self.test_image_data:
            test_image = base64.b64encode(self.test_image_data).decode('utf-8')
        else:
            test_image = None

        self.db.add_sick_record(self.patient_id, sick_date, complaint, medical_history, examination, tests_results, test_image, diagnosis)
        self.load_sick_records(self.patient_id)
        self.clear_fields()

    def clear_fields(self):
        self.sick_date.setDate(QDate.currentDate())
        self.complaint.clear()
        self.medical_history.clear()
        self.examination.clear()
        self.tests_results.clear()
        self.diagnosis.clear()
        self.test_image_data = None
        self.image_label.setText("No image uploaded")

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            with open(file_name, 'rb') as file:
                self.test_image_data = file.read()
                pixmap = QPixmap()
                pixmap.loadFromData(self.test_image_data)
                self.image_label.setPixmap(pixmap.scaled(200, 200, aspectRatioMode=Qt.KeepAspectRatio))
            QMessageBox.information(self, "Image Upload", "Image uploaded successfully.")

    def go_back(self):
        self.parentWidget().setCurrentIndex(0)  # Switch back to home page
