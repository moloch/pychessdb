-- Deploy chessdb:positions to pg

BEGIN;

CREATE TABLE position(
    id BIGSERIAL NOT NULL CONSTRAINT positions_pk PRIMARY KEY,
    hash CHAR(32) UNIQUE
);

COMMIT;
