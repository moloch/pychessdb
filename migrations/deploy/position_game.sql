-- Deploy chessdb:position_game to pg

BEGIN;

CREATE TABLE position_game(
    position_id BIGINT REFERENCES position,
    game_id BIGINT REFERENCES game,
    PRIMARY KEY(position_id, game_id)
);

COMMIT;
