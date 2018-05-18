from loader import PGNLoader
import os.path
from unittest.mock import MagicMock

curr_path = os.path.abspath(os.path.dirname(__file__))
test_pgn_path = os.path.join(curr_path, 'pgn_files/game_001.pgn')


def test_loader(mocker):
    #mocker.patch('peewee.Model.save', new=MagicMock())
    loader = PGNLoader()
    game = loader.load(test_pgn_path)
