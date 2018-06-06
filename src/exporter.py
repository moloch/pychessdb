import itertools
import chess
from chess.pgn import StringExporter


class HtmlExporter(StringExporter):

    def begin_variation(self):
        self.variation_depth += 1

        if self.variations:
            self.write_token('<br>')
            self.write_token('&nbsp;' * self.variation_depth * 4)
            self.write_token('( ')
            self.force_movenumber = True

    def end_variation(self):
        self.variation_depth -= 1

        if self.variations:
            self.write_token(') <br>')
            self.write_token('&nbsp;' * self.variation_depth * 4)
            self.force_movenumber = True

    def visit_move(self, board, move):
        if self.variations or not self.variation_depth:
            # Write the move number.
            if board.turn == chess.WHITE:
                self.write_token(str(board.fullmove_number) + ". ")
            elif self.force_movenumber:
                self.write_token(str(board.fullmove_number) + "... ")
            new_board = board.copy()
            new_board.push(move)
            self.write_token('<a href="/move/?fen={}&move={}">'.format(new_board.fen(), move.uci()))
            # Write the SAN.
            self.write_token(board.san(move) + "</a> ")

            self.force_movenumber = False
