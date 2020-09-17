import numpy as np

from src.db.models.pydantic.game import GameCreate
from src.db.models.pydantic.performance import PerformanceCreate


"""Tests pydantic's base functionality
"""


def test_create_model_comparison():
    """pydantic/base.py has comparison functions ensure this work down stream
    """
    game_object = GameCreate(id='test', round='R32', score='', circuit='wta', tournament_id='t_id')
    other_object = GameCreate(id='test_1', round='R32', score='', circuit='wta', tournament_id='t_id')

    assert game_object != other_object
    assert game_object < other_object


def test_create_model_nan_to_none():
    game_object = GameCreate(id='test', round='R32', score=np.nan, circuit='wta', tournament_id='t_id')

    assert game_object.score is None


def test_performance_model_comparison():
    w_performance = PerformanceCreate(game_id='game', player_id=1, won=True)
    l_performance = PerformanceCreate(game_id='game', player_id=2, won=False)

    assert w_performance != l_performance
    assert w_performance > l_performance
