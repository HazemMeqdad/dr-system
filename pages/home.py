from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget
import typing as t
from db import DB

class HomePage(QWidget):
    def __init__(self, db: DB, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/home.ui", self)
        
        self.db = db

        self.change_btn = self.findChild(QPushButton, 'change_btn')
        if self.change_btn is None:
            raise Exception("change_btn not found. Make sure the object name is correct in the UI file.")

        self.patient_list = self.findChild(QListWidget, 'patient_list')
        if self.patient_list is None:
            raise Exception("patient_list not found. Make sure the object name is correct in the UI file.")

        # Static data for patients
        patients = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown"]
        self.patient_list.addItems(patients)
