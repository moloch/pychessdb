import chess.pgn
from src.models import Game
from src.pgn_tags import pgn_to_columns


class Loader:
    def _get_pgn_headers_columns(self, pgn_headers):
        mapping = {}
        for h in pgn_headers:
            try:
                mapping[pgn_to_columns[h]] = pgn_headers[h]
            except KeyError:
                pass
        return mapping

    def load_single_file(self, path):
        pgn = open(path)
        game = chess.pgn.read_game(pgn)
        exporter = chess.pgn.StringExporter()
        pgn_string = game.accept(exporter)
        game_headers = self._get_pgn_headers_columns(game.headers)
        Game.create(pgn=pgn_string, **game_headers)
        return game
