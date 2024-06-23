from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from pages.home import HomePage
from pages.patient import PatientPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/home.ui', self)
        # self.home_page = HomePage()
        # self.stackedWidget.addWidget(self.home_page)
        # # self.first.change_btn.clicked.connect(self.go_to_second)
        # self.patient_page = PatientPage()
        # self.stackedWidget.addWidget(self.patient_page)
        # # self.second.change_btn.clicked.connect(self.go_to_first)

    def go_to_first(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_second(self):
        self.stackedWidget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()