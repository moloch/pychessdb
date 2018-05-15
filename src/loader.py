import chess.pgn
import hashlib
from src.models import Game, Position, PositionGame
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
        node = game
        while not node.is_end():
            next_node = node.variations[0]
            fen = node.board().fen()
            hash_key = hashlib.md5(fen.encode()).hexdigest()
            position_result = (Position.select().where(Position.hash == hash_key).execute())
            if not position_result:
                position_id = [x for x in (Position.insert(hash=hash_key).returning(Position.id)).execute()][0][0]
            else:
                position_id = position_result[0].id
            PositionGame.insert(position_id=position_id, game_id=game_id).execute()
            node = next_node
        return game
