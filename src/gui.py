from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from loader import PGNLoader

import os
import sys


class GamesTableModel(QAbstractTableModel):
    def rowCount(self, parent=None, *args, **kwargs):
        return 10

    def columnCount(self, parent=None, *args, **kwargs):
        return 12

    def data(self, QModelIndex, role=None):
        return 'ciao'


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.table_view = QTableView(self)
        self.table_view.setModel(GamesTableModel())

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.table_view.setFont(fixedfont)

        self.path = None

        layout.addWidget(self.table_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction("Import games...", self)
        open_file_action.setStatusTip("Import games from PGN")
        open_file_action.triggered.connect(self.file_open)

        open_db_action = QAction("Open database...", self)
        open_db_action.setStatusTip("Open game database")
        open_db_action.triggered.connect(self.load_database)

        file_menu.addAction(open_file_action)

        self.update_title()
        self.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import games from PGN", "", "PGN files (*.pgn);All files (*.*)")

        try:
            loader = PGNLoader()
            loader.load(path)
            self.path = path
            self.update_title()
        except FileNotFoundError:
            pass

    def load_database(self):
        pass

    def update_title(self):
        self.setWindowTitle("%s - PyChessDB" % (os.path.basename(self.path) if self.path else "Untitled"))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("PyChessDB")

    window = MainWindow()
    app.exec_()