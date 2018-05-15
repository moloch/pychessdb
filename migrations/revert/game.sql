-- Revert chessdb:games from pg

BEGIN;

DROP TABLE game;

COMMIT;
