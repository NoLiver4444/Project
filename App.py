import sqlite3
from datetime import datetime
from calendar import monthrange

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer

from graphik_time_window import graphik_time_window
from graphik_number_window import graphik_number_window
from dnevnik_window import dnevnik_window
from breaking_window import breaking_window
from file_maker import file_maker
from Halper import new_month, days_maker, make_time, obn_db_time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI/Main_window.ui', self)

        file = open("files/check.txt", "r+")
        file.seek(0)
        file.write("0 0")

        self.db = sqlite3.connect('Database.sqlite')
        self.timer_check = False
        # Чтобы проверить окно отдыха в self.time нужно написать 5399
        self.time = 0
        self.count = 0

        self.year_now = self.db.cursor().execute("""select number from checking where name = 'year'""").fetchall()[0][0]
        self.month_now = self.db.cursor().execute("""select number from checking where name = 'month'""").fetchall()[0][
            0]
        self.days = monthrange(self.year_now, self.month_now)[1]

        if self.year_now != datetime.now().year or self.month_now != datetime.now().month:
            self.days = new_month(self.db, self.days)

        self.check_month = \
            self.db.cursor().execute("""select number from checking where name = 'check_month'""").fetchall()[0][0]

        if self.check_month == 0:
            days_maker(self.db, self.days)

        self.react = QTimer(self)
        self.react.timeout.connect(self.React)
        self.react.start(1000)

        self.timer.setReadOnly(True)
        self.initUI()

    def initUI(self):
        self.bt_graphik_time.clicked.connect(self.graph_time_write)
        self.bt_graphik_number.clicked.connect(self.graph_number_write)
        self.bt_dnevnik.clicked.connect(self.dnev_write)
        self.bt_timer.clicked.connect(self.timer_push)
        self.bt_txt_file.clicked.connect(self.file_maker)

    def timer_push(self):
        if self.timer_check is True:
            self.timer_check = False
        else:
            self.timer_check = True
            if self.count == 0:
                self.ti = QTimer(self)
                self.ti.timeout.connect(self.Timer)
                self.ti.start(1000)
                self.count = 1

    def Timer(self):
        if self.timer_check is True:
            self.timer.setText(":".join(make_time(self.timer)))
            obn_db_time(self.db)
            self.time += 1
            if self.time % 1800 == 0 and (self.time // 1800) % 3 == 0:
                self.timer_check = False
                self.breaking()

    def breaking(self):
        self.breaking = breaking_window()
        self.breaking.show()

    def file_maker(self):
        self.file_maker = file_maker(self.db)
        self.file_maker.show()

    def graph_time_write(self):
        self.graphik_time = graphik_time_window(self.db, self.days)
        self.graphik_time.show()

    def graph_number_write(self):
        self.graphik_number = graphik_number_window(self.db, self.days)
        self.graphik_number.show()

    def dnev_write(self):
        self.dnevnik = dnevnik_window(self.db)
        self.dnevnik.show()

    def React(self):
        file = open("files/check.txt", "r+")
        text = file.read().split()
        self.check = text[0]
        if self.check == "1":
            file.seek(0)
            file.write("0 " + text[1])
            file.close()
            self.dnevnik.close()
            self.dnevnik = dnevnik_window(self.db)
            self.dnevnik.show()
