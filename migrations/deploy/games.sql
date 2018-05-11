-- Deploy chessdb:games to pg

BEGIN;

CREATE TABLE games(
id BIGSERIAL NOT NULL CONSTRAINT games_pk PRIMARY KEY,
event VARCHAR,
site VARCHAR,
date VARCHAR,
round VARCHAR,
white VARCHAR,
black VARCHAR,
result VARCHAR,
pgn TEXT NOT NULL
);

COMMIT;
