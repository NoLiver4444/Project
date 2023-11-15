from PyQt5.QtWidgets import QMainWindow

import pyqtgraph


class graphik_number_window(QMainWindow):
    def __init__(self, db, days, parent=None):
        super().__init__(parent)
        self.db = db
        self.days = days
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graphik numbers")
        self.plot_graph = pyqtgraph.PlotWidget()
        self.plot_graph.resize(600, 250)
        self.plot_graph.move(100, 110)
        self.plot_graph.setTitle("График выполненых задач", color="w", size="20pt")
        self.plot_graph.setLabel(
            "left",
            '<span style="color: blue; font-size: 18px">Задачи(в количестве)</span>'
        )
        self.plot_graph.setLabel(
            "bottom",
            '<span style="color: blue; font-size: 18px">Дни</span>'
        )
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.addLegend()
        self.setCentralWidget(self.plot_graph)
        days = [i + 1 for i in range(0, self.days)]
        number = [int(i[0]) for i in self.db.cursor().execute("select number from days").fetchall()]
        self.plot_graph.plot(days, number, name="Задачи", pen=pyqtgraph.mkPen(color=(0, 0, 255)), symbol="o",
                             symbolSize=5, symbolBrush="w")
