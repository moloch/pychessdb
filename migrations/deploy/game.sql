-- Deploy chessdb:games to pg

BEGIN;

CREATE TABLE game(
id BIGSERIAL NOT NULL CONSTRAINT games_pk PRIMARY KEY,
event VARCHAR,
site VARCHAR,
date VARCHAR,
round VARCHAR,
white VARCHAR,
black VARCHAR,
result VARCHAR,
pgn TEXT NOT NULL,
white_title VARCHAR,
black_title VARCHAR,
white_elo VARCHAR,
black_elo VARCHAR,
white_uscf VARCHAR,
black_uscf VARCHAR,
white_na VARCHAR,
black_na VARCHAR,
white_type VARCHAR,
black_type VARCHAR,
event_date VARCHAR,
event_sponsor VARCHAR,
section VARCHAR,
stage VARCHAR,
board VARCHAR,
opening VARCHAR,
variation VARCHAR,
sub_variation VARCHAR,
eco VARCHAR,
nic VARCHAR,
time VARCHAR,
utc_time VARCHAR,
utc_date VARCHAR,
time_control VARCHAR,
set_up VARCHAR,
fen VARCHAR,
termination VARCHAR,
annotator VARCHAR,
mode VARCHAR,
ply_count VARCHAR
);

COMMIT;
