-- Revert chessdb:appschema from pg

BEGIN;

DROP SCHEMA chessdb;

COMMIT;
