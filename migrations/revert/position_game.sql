-- Revert chessdb:position_game from pg

BEGIN;

DROP TABLE position_game;

COMMIT;
