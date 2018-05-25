import itertools
import chess
from chess.pgn import StringExporter


class HtmlExporter(StringExporter):

    def visit_move(self, board, move):
        if self.variations or not self.variation_depth:
            # Write the move number.
            if board.turn == chess.WHITE:
                self.write_token(str(board.fullmove_number) + ". ")
            elif self.force_movenumber:
                self.write_token(str(board.fullmove_number) + "... ")
            self.write_token('<a href="/move/?fen={}&move={}">'.format(board.fen(), move.uci()))
            # Write the SAN.
            self.write_token(board.san(move) + "</a> ")

            self.force_movenumber = False
