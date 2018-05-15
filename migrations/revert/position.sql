-- Revert chessdb:positions from pg

BEGIN;

DROP TABLE position;

COMMIT;
