from src.loader import Loader
import os.path
from unittest.mock import MagicMock

curr_path = os.path.abspath(os.path.dirname(__file__))
test_pgn_path = os.path.join(curr_path, 'pgn_files/game_000.pgn')


def test_loader(mocker):
    mocker.patch('peewee.Model.save', new=MagicMock())
    loader = Loader()
    game = loader.load_single_file(test_pgn_path)
    assert game.headers['ECO'] == "D02"
    assert game.headers['Result'] == "1-0"
