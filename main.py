from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from pages.home import HomePage
from pages.patient import PatientPage

from db import DB

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.init_ui()
        
    def init_ui(self):
        uic.loadUi('./ui/main.ui', self)  # Load your main UI file which contains the QStackedWidget
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        
        if self.stackedWidget is None:
            raise Exception("QStackedWidget not found. Make sure the object name is correct in the UI file.")
        
        self.home_page = HomePage(self.db)
        self.patient_page = PatientPage(self.db)
        
        self.stackedWidget.addWidget(self.home_page)
        self.stackedWidget.addWidget(self.patient_page)
        
        self.home_page.change_btn.clicked.connect(self.go_to_patient)
        self.patient_page.change_btn.clicked.connect(self.go_to_home)
        
    def go_to_home(self):
        self.stackedWidget.setCurrentWidget(self.home_page)
        
    def go_to_patient(self):
        self.stackedWidget.setCurrentWidget(self.patient_page)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
