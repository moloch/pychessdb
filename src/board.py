#!/usr/bin/env python

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import chess
import chess.pgn

from exporter import HtmlExporter


class SquareGraphics(QGraphicsRectItem):
    def __init__(self, board_graphics, square):
        super(SquareGraphics, self).__init__()
        self.board_graphics = board_graphics
        self.square = square
        self.setAcceptDrops(True)
        self.piece_graphics = None

    #def dropEvent(self, event):
    #    game = self.board_graphics.game
    #    move = self.board_graphics.current_move
    #    move.destination = self.square.get_coords()
    #    print("Drop event with move: " + str(move))
    #    if self.square.piece is not None:
    #        move.is_take = True
    #    if game.current_player.move(move) is not False:
    #        piece_pixmap = QPixmap("img/" + self.board_graphics.moving_piece.piece.color +
    #                           "_" + self.board_graphics.moving_piece.piece.name + ".png")
    #        piece_pixmap = piece_pixmap.scaledToHeight(70, Qt.SmoothTransformation)
    #        piece_graphics = PieceGraphics(self.board_graphics, piece_pixmap, self.square.piece)
    #        x = self.rect().x()
    #        y = self.rect().y()
    #        piece_graphics.setOffset(x, y)
    #        self.board_graphics.scene.removeItem(self.board_graphics.moving_piece)
    #        if move.is_take and self.piece_graphics is not None:
    #            self.board_graphics.scene.removeItem(self.piece_graphics)
    #        self.piece_graphics = piece_graphics
    #        self.board_graphics.scene.addItem(piece_graphics)


class BoardGraphics(QGraphicsRectItem):
    def __init__(self, scene, board):
        super(BoardGraphics, self).__init__()
        self.scene = scene
        self.board = board
        self.__generate_board()
        self.moving_piece = None
        self.current_move = None

    def __generate_board(self):
        board = self.board
        for square in chess.SQUARES:
            square_graphic_item = SquareGraphics(self, square)
            y = (70 * 7) - (chess.square_rank(square) * 70)
            x = chess.square_file(square) * 70
            square_graphic_item.setRect(QRectF(x, y, 70, 70))
            if (square + chess.square_rank(square)) % 2 == 0:
                square_graphic_item.setBrush(QBrush(QColor("grey")))
            else:
                square_graphic_item.setBrush(QBrush(QColor("white")))
            self.scene.addItem(square_graphic_item)
            self.__add_piece(board.piece_at(square), x, y)

    def __add_piece(self, piece, x, y):
        if piece is not None:
            color_symbol = 'w' if chess.WHITE == piece.color else 'b'
            piece_pixmap = QPixmap("images/" + color_symbol + "_" + piece.symbol().lower() + ".png")
            piece_pixmap = piece_pixmap.scaledToHeight(70, Qt.SmoothTransformation)
            piece_graphics = PieceGraphics(self, piece_pixmap, piece)
            piece_graphics.setOffset(x, y)
            self.scene.addItem(piece_graphics)


class PieceGraphics(QGraphicsPixmapItem):
    def __init__(self, board_graphics, pixmap, piece):
        super().__init__(pixmap)
        self.board_graphics = board_graphics
        self.piece = piece

    def mousePressEvent(self, event):
        pass

    #def mouseMoveEvent(self, event):
    #    if self.piece.color is not self.board_graphics.game.current_player.color:
    #        return

    #    self.board_graphics.moving_piece = self
    #    move = Move()
    #    move.piece = self.piece.name
    #     move.source = self.piece.square.get_coords()
    #     move.color = self.piece.color
    #     self.board_graphics.current_move = move
    #     print("Mouse move event with move: " + str(move))
    #     item_data = QByteArray()
    #     buffer = QBuffer(item_data)
    #     buffer.open(QIODevice.WriteOnly)
    #     self.pixmap().save(buffer)
    #     mime_data = QMimeData()
    #     mime_data.setData('application/x-dnditemdata', item_data)
    #
    #     drag = QDrag(event.widget())
    #     drag.setMimeData(mime_data)
    #     drag.setPixmap(self.pixmap())
    #     x = self.pos().toPoint().x() + self.pixmap().width() / 2
    #     y = self.pos().toPoint().y() + self.pixmap().height() / 2
    #     drag.setHotSpot(QPoint(x, y))
    #     drag.exec_()


class BoardGraphicsView(QGraphicsView):
    def __init__(self, board):
        super(BoardGraphicsView, self).__init__()
        self.board = board
        scene = QGraphicsScene(self)
        rectangle = BoardGraphics(scene, self.board)
        rectangle.setRect(QRectF(0, 0, 560, 560))
        scene.addItem(rectangle)
        scene.setSceneRect(0, 0, 560, 560)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("Moloch Chess")


class BoardMainWindow(QMainWindow):

    def __init__(self, game):
        super(BoardMainWindow, self).__init__()

        self.game = game

        self.layout = QHBoxLayout()
        self.board_graphics_view = BoardGraphicsView(self.game.board().copy())
        self.pgn_editor = QTextBrowser(self)
        self.pgn_editor.anchorClicked.connect(self.on_anchor_clicked)
        pgn_exporter = HtmlExporter(headers=False, comments=False)
        self.pgn_editor.setAcceptRichText(True)
        game_text = game.accept(pgn_exporter)
        print(game_text)
        self.pgn_editor.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.pgn_editor.setHtml(game_text)

        self.layout.addWidget(self.board_graphics_view)
        self.layout.addWidget(self.pgn_editor)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.show()

    def on_anchor_clicked(self, url):
        self.pgn_editor.setSource(QUrl())
        query_params = QUrlQuery(url)
        fen = query_params.queryItemValue('fen')
        move = query_params.queryItemValue('move')
        new_board = chess.Board(fen=fen)
        new_board.push(chess.Move.from_uci(move))
        self.board_graphics_view.hide()
        board_view = BoardGraphicsView(new_board)
        self.layout.replaceWidget(self.board_graphics_view, board_view)
        self.board_graphics_view = board_view
