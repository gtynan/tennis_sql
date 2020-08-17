import pytest
import pandas as pd
import numpy as np

from src.data.data_scraping import get_raw_players
from src.constants import player_csv_map, game_csv_map, tournament_csv_map


@pytest.mark.slow
def test_get_raw_players(sample_players):
    expected_columns = list(player_csv_map.values())

    assert len(sample_players) == 5
    assert isinstance(sample_players, pd.DataFrame)
    assert np.isin(expected_columns, sample_players.columns).all()


@pytest.mark.slow
def test_get_raw_games(sample_games):
    raw_games = sample_games
    expected_columns = list(game_csv_map.values()) + \
        list(tournament_csv_map.values())

    assert len(sample_games) == 5
    assert isinstance(sample_games, pd.DataFrame)
    assert np.isin(expected_columns, sample_games.columns).all()
