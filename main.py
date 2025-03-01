from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QAction, QFileDialog, QMessageBox
from pages.home import HomePage
from pages.patient import PatientPage
from pages.add_patient import AddPatientPage
from pages.sick_records import SickRecordsPage
from db import DB

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('ui/main.ui', self)
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')

        if self.stackedWidget is None:
            raise Exception("QStackedWidget not found. Make sure the object name is correct in the UI file.")

        self.home_page = HomePage(self.db, self)
        self.patient_page = PatientPage(self.db)
        self.add_patient_page = AddPatientPage(self.db)
        self.sick_records_page = SickRecordsPage(self.db)

        self.stackedWidget.addWidget(self.home_page)
        self.stackedWidget.addWidget(self.patient_page)
        self.stackedWidget.addWidget(self.add_patient_page)
        self.stackedWidget.addWidget(self.sick_records_page)

        self.home_page.change_btn.clicked.connect(self.home_page.view_patient_details)
        self.patient_page.change_btn.clicked.connect(self.go_to_home)
        self.home_page.add_patient_btn.clicked.connect(self.go_to_add_patient)
        self.add_patient_page.patient_added.connect(self.refresh_home_page)

        self.actionBackup = self.findChild(QAction, 'actionBackup')
        self.actionRestore = self.findChild(QAction, 'actionRestore')

        self.actionBackup.triggered.connect(self.backup_database)
        self.actionRestore.triggered.connect(self.restore_database)

    def go_to_home(self):
        self.stackedWidget.setCurrentWidget(self.home_page)

    def go_to_patient(self):
        self.stackedWidget.setCurrentWidget(self.patient_page)

    def go_to_add_patient(self):
        self.stackedWidget.setCurrentWidget(self.add_patient_page)

    def refresh_home_page(self):
        self.home_page.load_patients()
        self.go_to_home()

    def show_patient_details(self, selected_patient):
        self.patient_page.display_patient_details(selected_patient)
        self.go_to_patient()

    def view_sick_records(self, patient_id):
        self.sick_records_page.load_sick_records(patient_id)
        self.stackedWidget.setCurrentWidget(self.sick_records_page)

    def backup_database(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Backup", "", "Database Files (*.db);;All Files (*)", options=options)
        if file_name:
            self.db.backup_database(file_name)
            QMessageBox.information(self, "Backup", "Backup successful")

    def restore_database(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Backup", "", "Database Files (*.db);;All Files (*)", options=options)
        if file_name:
            self.db.restore_database(file_name)
            self.refresh_home_page()
            QMessageBox.information(self, "Restore", "Restore successful")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()  # Show the window maximized by default
    app.exec_()
