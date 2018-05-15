from decouple import config
from peewee import *

db = PostgresqlDatabase(
    config('DB_SCHEMA'),
    user=config('DB_USER'),
    password=config('DB_PASSWD'),
    host=config('DB_HOST'),
    port=config('DB_PORT')
)


class BaseModel(Model):
    class Meta:
        database = db


class Game(BaseModel):
    id = PrimaryKeyField()
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


class Position(BaseModel):
    id = PrimaryKeyField()
    hash = FixedCharField(max_length=32)


class PositionGame(BaseModel):
    position_id = ForeignKeyField(Position)
    game_id = ForeignKeyField(Game)

    class Meta:
        table_name = 'position_game'
