from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton
import typing as t
from db import DB


class PatientPage(QWidget):
    def __init__(self, db: DB, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/patient.ui", self)

        self.db = db

        self.change_btn = self.findChild(QPushButton, 'change_btn')
        if self.change_btn is None:
            raise Exception("change_btn not found. Make sure the object name is correct in the UI file.")
