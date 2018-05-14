import chess.pgn as pgn_reader


class Loader:
    def __init__(self):
        pass

    def load_single_file(self, path):
        pgn = open(path)
        game = pgn_reader.read_game(pgn)
        return game
