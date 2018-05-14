from src.loader import Loader
import os.path

curr_path = os.path.abspath(os.path.dirname(__file__))
test_pgn_path = os.path.join(curr_path, 'pgn_files/game_000.pgn')


def test_loader():
    loader = Loader()
    game = loader.load_single_file(test_pgn_path)
    assert game.headers['Result'] == "1-0"
