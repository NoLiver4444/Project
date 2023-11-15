from PyQt5.QtWidgets import QMainWindow, QInputDialog
from datetime import datetime


class file_maker(QMainWindow):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle("File maker")
        name, ok_pressed = QInputDialog.getText(self, "Ввод имени", "ведите ваше полное имя:")

        if ok_pressed:
            file = open("files/work.txt", "r+", encoding="utf-8")
            file.seek(0)
            time_work = \
                self.db.cursor().execute("select * from days where day = " + str(datetime.now().day)).fetchall()[0]
            hours = str(time_work[2] // 3600)
            minutes = str((time_work[2] - int(hours) * 3600) // 60)
            seconds = str((time_work[2] - int(hours) * 3600 - int(minutes) * 60))
            file.write("Работник: " + name + "\n")
            file.write("Время работы: " + hours + " часов " + minutes + " минут " + seconds + " секунд " + "\n")
            file.write("Количество выполненных задач: " + str(time_work[1]) + "\n")
            file.close()
