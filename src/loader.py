import chess.pgn
import hashlib
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
        game_id = [x for x in (Game.insert(pgn=pgn_string, **game_headers).returning(Game.id)).execute()][0][0]
        print(game_id)
        node = game
        while not node.is_end():
            next_node = node.variations[0]
            fen = node.board().fen()
            hash_key=hashlib.md5(fen.encode()).hexdigest()
            #save FEN + game ID in dedicated table called positions
            node = next_node
        return game
