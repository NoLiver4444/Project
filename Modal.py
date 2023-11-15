from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton


class Modal(QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        uic.loadUi('UI/dnevnik.ui', self)
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Modal window")
        self.event_text = QLineEdit(self)
        self.event_text.setStyleSheet(
            'color: rgb(255, 255, 255); border-style: outset; border-width: 2px; border-color: rgb(255, 255, 255);')
        self.event_text.resize(600, 60)
        self.event_text.move(100, 10)

        self.add_event_button = QPushButton("Добавить", self)
        self.add_event_button.setStyleSheet('background-color: rgb(200, 200, 200);')
        self.add_event_button.resize(150, 60)
        self.add_event_button.move(325, 90)
        self.add_event_button.clicked.connect(self.add)

    def add(self):
        if self.event_text.text() != "":
            self.db.execute("INSERT INTO events(name) values('" + self.event_text.text() + "')")
            self.db.commit()
        file = open("files/check.txt", 'r+')
        text = file.read().split()
        file.seek(0)
        file.write("1 " + text[1])
        file.close()

        self.close()
