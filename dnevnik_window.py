from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton

from datetime import datetime

from Modal import Modal


class dnevnik_window(QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        uic.loadUi('UI/dnevnik.ui', self)
        self.db = db
        self.data = self.db.cursor().execute("""SELECT name FROM events""").fetchall()
        self.buttons_complete = []
        self.buttons_not_complete = []
        self.events = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dnevnik")
        x, y = 10, 10
        for i in self.data:
            self.events.append(i[0])

            self.label = QLabel('<h2 style="color: rgb(255, 255, 255);">' + i[0] + '</h2>', self)
            self.label.resize(470, 60)
            self.label.move(x, y)

            self.complete_button = QPushButton("Выполнено", self)
            self.complete_button.setStyleSheet('QPushButton {background-color: rgb(0, 255, 0);}')
            self.complete_button.resize(130, 60)
            self.complete_button.move(500, y)
            self.complete_button.clicked.connect(self.complete)

            self.buttons_complete.append(self.complete_button)

            self.not_complete_button = QPushButton("Не выполнено", self)
            self.not_complete_button.setStyleSheet('QPushButton {background-color: rgb(255, 0, 0);}')
            self.not_complete_button.resize(130, 60)
            self.not_complete_button.move(650, y)
            self.not_complete_button.clicked.connect(self.not_complete)

            self.buttons_not_complete.append(self.not_complete_button)

            y = y + 100

        self.add_button = QPushButton("Добавить", self)
        self.add_button.resize(150, 60)
        self.add_button.setStyleSheet('QPushButton {background-color: rgb(200, 200, 200);}')
        self.add_button.move(325, y)
        self.add_button.clicked.connect(self.push)

    def push(self):
        self.modal = Modal(self.db)
        self.modal.show()

    def complete(self):
        index = self.buttons_complete.index(self.sender())

        self.db.cursor().execute("DELETE from events where name = '" + self.events[index] + "'")

        file = open("files/check.txt", 'r+')
        text = str(int(file.read().split()[1]) + 1)
        number = int(
            self.db.cursor().execute("select number from days where day = " + str(datetime.now().day)).fetchall()[0][
                0]) + 1

        self.db.cursor().execute("update days set number = " + str(number) + " where day = " + str(datetime.now().day))

        self.db.commit()

        file.seek(0)
        file.write("1 " + text)
        file.close()

    def not_complete(self):
        index = self.buttons_not_complete.index(self.sender())

        self.db.cursor().execute("DELETE from events where name = '" + self.events[index] + "'")
        self.db.commit()

        file = open("files/check.txt", 'r+')
        text = file.read().split()[1]

        file.seek(0)
        file.write("1 " + text)
        file.close()
