import chess.pgn
from peewee import *
from decouple import config
from src.pgn_tags import pgn_to_columns

db = PostgresqlDatabase(
    config('DB_SCHEMA'),
    user=config('DB_USER'),
    password=config('DB_PASSWD'),
    host=config('DB_HOST'),
    port=config('DB_PORT')
)


class Game(Model):
    id = BigAutoField(primary_key=True, unique=True)
    event = CharField()
    site = CharField()
    date = CharField()
    round = CharField()
    white = CharField()
    black = CharField()
    result = CharField()
    white_title = CharField()
    black_title = CharField()
    white_elo = CharField()
    black_elo = CharField()
    white_uscf = CharField()
    black_uscf = CharField()
    white_na = CharField()
    black_na = CharField()
    white_type = CharField()
    black_type = CharField()
    event_date = CharField()
    event_sponsor = CharField()
    section = CharField()
    stage = CharField()
    board = CharField()
    opening = CharField()
    variation = CharField()
    sub_variation = CharField()
    eco = CharField()
    nic = CharField()
    time = CharField()
    utc_time = CharField()
    utc_date = CharField()
    time_control = CharField()
    set_up = CharField()
    fen = CharField()
    termination = CharField()
    annotator = CharField()
    mode = CharField()
    ply_count = CharField()
    pgn = TextField()

    class Meta:
        database = db


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
