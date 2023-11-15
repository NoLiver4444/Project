from PyQt5.QtWidgets import QMainWindow

import pyqtgraph


class graphik_time_window(QMainWindow):
    def __init__(self, db, days, parent=None):
        super().__init__(parent)
        self.db = db
        self.days = days
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graphik time")
        self.plot_graph = pyqtgraph.PlotWidget()
        self.plot_graph.resize(600, 250)
        self.plot_graph.move(100, 110)
        self.plot_graph.setTitle("График времени работы", color="w", size="20pt")
        self.plot_graph.setLabel(
            "left",
            '<span style="color: green; font-size: 18px">Время(в часах)</span>'
        )
        self.plot_graph.setLabel(
            "bottom",
            '<span style="color: green; font-size: 18px">Дни</span>'
        )
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.addLegend()
        self.setCentralWidget(self.plot_graph)
        days = [i + 1 for i in range(0, self.days)]
        number = [round(int(i[0]) / 3600, 2) for i in self.db.cursor().execute("select time from days").fetchall()]
        self.plot_graph.plot(days, number, name="Время", pen=pyqtgraph.mkPen(color=(0, 255, 0)), symbol="o",
                             symbolSize=5, symbolBrush="w")
