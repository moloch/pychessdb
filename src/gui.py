from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from loader import PGNLoader
from models import Game

import os
import sys


class GamesTableModel(QAbstractTableModel):
    def __init__(self):
        super(GamesTableModel, self).__init__()
        self.headers = {0: 'white', 1: 'black', 2: 'pgn'}
        self.games = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.games)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        game = self.games[index.row()]
        if role == Qt.DisplayRole:
            return QVariant(getattr(game, self.headers[index.column()]))

    def headerData(self, index, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return QVariant(self.headers[index])
        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return QVariant(index)

    def add_game(self, game):
        self.beginResetModel()
        self.games.append(game)
        self.endResetModel()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.table_view = QTableView(self)
        self.table_view.setModel(GamesTableModel())
        self.table_view.horizontalHeader().setStretchLastSection(QHeaderView.Stretch)

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
        file_menu.addAction(open_db_action)

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
        games_model = self.table_view.model()
        games = Game.select().paginate(1, 10)
        for game in games:
            games_model.add_game(game)

    def update_title(self):
        self.setWindowTitle("%s - PyChessDB" % (os.path.basename(self.path) if self.path else "Untitled"))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("PyChessDB")

    window = MainWindow()
    app.exec_()
