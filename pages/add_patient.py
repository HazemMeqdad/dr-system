from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QDateEdit, QTextEdit, QComboBox, QMessageBox
from PyQt5.QtCore import QDate, pyqtSignal
from db import DB

class AddPatientPage(QWidget):
    patient_added = pyqtSignal()  # Define the signal

    def __init__(self, db: DB, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/add_patient.ui", self)
        
        self.db = db
        
        self.first_name = self.findChild(QLineEdit, 'first_name')
        self.last_name = self.findChild(QLineEdit, 'last_name')
        self.age = self.findChild(QLineEdit, 'age')
        self.gender = self.findChild(QComboBox, 'gender')
        self.identification_card = self.findChild(QLineEdit, 'identification_card')
        self.address = self.findChild(QLineEdit, 'address')
        self.phone = self.findChild(QLineEdit, 'phone')
        self.date = self.findChild(QDateEdit, 'date')
        self.date.setDisplayFormat("dd/MM/yyyy")
        self.description = self.findChild(QTextEdit, 'description')
        self.prescription = self.findChild(QTextEdit, 'prescription')
        
        self.submit_btn = self.findChild(QPushButton, 'submit_btn')
        self.cancel_btn = self.findChild(QPushButton, 'cancel_btn')
        
        self.submit_btn.clicked.connect(self.add_patient)
        self.cancel_btn.clicked.connect(self.go_back)
    
    def validate_fields(self):
        if not self.first_name.text().strip():
            return False, "First Name is required."
        if not self.last_name.text().strip():
            return False, "Last Name is required."
        if not self.age.text().strip().isdigit() or int(self.age.text().strip()) <= 0:
            return False, "Age must be a positive number."
        if self.gender.currentText().strip() not in ['Male', 'Female']:
            return False, "Gender must be Male or Female."
        if not self.identification_card.text().strip():
            return False, "Identification Card is required."
        if not self.address.text().strip():
            return False, "Address is required."
        if not self.phone.text().strip():
            return False, "Phone is required."
        if not self.date.date().isValid():
            return False, "Date is invalid."
        if not self.description.toPlainText().strip():
            return False, "Description is required."
        if not self.prescription.toPlainText().strip():
            return False, "Prescription is required."
        return True, ""

    def show_error_message(self, message):
        QMessageBox.critical(self, "Validation Error", message)

    def add_patient(self):
        valid, message = self.validate_fields()
        if not valid:
            self.show_error_message(message)
            return

        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        age = int(self.age.text().strip())
        gender = self.gender.currentText().strip()
        identification_card = self.identification_card.text().strip()
        address = self.address.text().strip()
        phone = self.phone.text().strip()
        date = self.date.date().toString("dd/MM/yyyy")
        description = self.description.toPlainText().strip()
        prescription = self.prescription.toPlainText().strip()
        
        self.db.add_patient_record(first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription)
        self.clear_fields()
        self.patient_added.emit()  # Emit the signal
        self.parentWidget().setCurrentIndex(0)  # Switch back to home page
    
    def clear_fields(self):
        self.first_name.clear()
        self.last_name.clear()
        self.age.clear()
        self.gender.setCurrentIndex(0)  # Reset to first item
        self.identification_card.clear()
        self.address.clear()
        self.phone.clear()
        self.date.setDate(QDate.currentDate())
        self.description.clear()
        self.prescription.clear()
    
    def go_back(self):
        self.parentWidget().setCurrentIndex(0)  # Switch back to home page
