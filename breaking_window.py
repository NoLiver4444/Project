from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from random import choice


class breaking_window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pictures = ["anime/1.png", "anime/2.png", "anime/3.png", "anime/4.png", "anime/5.png", "anime/6.png",
                         "anime/7.png", "anime/8.png", "anime/9.png", "anime/10.png", "anime/11.png", "anime/12.png",
                         "anime/13.png", "anime/14.png", "anime/15.png", "anime/16.png", "anime/17.png", "anime/18.png",
                         "anime/19.png", "anime/20.png", "anime/21.png", "anime/22.png"]
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Breaking window")
        self.setGeometry(300, 200, 800, 600)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")

        self.label = QLabel('<h2 style="color: rgb(255, 255, 255); font-size: 32px;">Нужно отдохнуть)</h2>', self)
        self.label.resize(250, 50)
        self.label.move(100, 125)

        self.picture = QPixmap(choice(self.pictures))
        self.image = QLabel(self)
        self.image.move(400, 0)
        self.image.resize(600, 600)
        self.image.setPixmap(self.picture)
