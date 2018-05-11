-- Revert chessdb:games from pg

BEGIN;

DROP TABLE games;

COMMIT;
