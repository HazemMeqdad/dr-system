from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QDateEdit, QTextEdit, QComboBox
from PyQt5.QtCore import QDate
from db import DB

class PatientPage(QWidget):
    def __init__(self, db: DB, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/patient.ui", self)

        self.db = db

        self.change_btn = self.findChild(QPushButton, 'change_btn')
        self.save_btn = self.findChild(QPushButton, 'save_btn')

        self.id_edit = self.findChild(QLineEdit, 'id_edit')
        self.first_name_edit = self.findChild(QLineEdit, 'first_name_edit')
        self.last_name_edit = self.findChild(QLineEdit, 'last_name_edit')
        self.age_edit = self.findChild(QLineEdit, 'age_edit')
        self.gender_edit = self.findChild(QComboBox, 'gender_edit')
        self.identification_card_edit = self.findChild(QLineEdit, 'identification_card_edit')
        self.address_edit = self.findChild(QLineEdit, 'address_edit')
        self.phone_edit = self.findChild(QLineEdit, 'phone_edit')
        self.date_edit = self.findChild(QDateEdit, 'date_edit')
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.description_edit = self.findChild(QTextEdit, 'description_edit')
        self.prescription_edit = self.findChild(QTextEdit, 'prescription_edit')

        self.change_btn.clicked.connect(self.go_back)
        self.save_btn.clicked.connect(self.save_patient_details)

    def display_patient_details(self, patient):
        self.id_edit.setText(str(patient[0]))
        self.first_name_edit.setText(patient[1])
        self.last_name_edit.setText(patient[2])
        self.age_edit.setText(str(patient[3]))
        gender = patient[4]
        gender_index = self.gender_edit.findText(gender)
        if gender_index != -1:
            self.gender_edit.setCurrentIndex(gender_index)
        self.identification_card_edit.setText(patient[5])
        self.address_edit.setText(patient[6])
        self.phone_edit.setText(patient[7])
        self.date_edit.setDate(QDate.fromString(patient[8], "dd/MM/yyyy"))
        self.description_edit.setText(patient[9])
        self.prescription_edit.setText(patient[10])

    def save_patient_details(self):
        id_ = int(self.id_edit.text())
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        age = int(self.age_edit.text())
        gender = self.gender_edit.currentText().strip()
        identification_card = self.identification_card_edit.text().strip()
        address = self.address_edit.text()
        phone = self.phone_edit.text()
        date = self.date_edit.date().toString("dd/MM/yyyy")
        description = self.description_edit.toPlainText()
        prescription = self.prescription_edit.toPlainText()

        self.db.update_patient_record(id_, first_name, last_name, age, gender, identification_card, address, phone, date, description, prescription)
        self.go_back()

    def go_back(self):
        self.parentWidget().setCurrentIndex(0)  # Switch back to home page
