import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.constants import PLAYER_COLS, TOURNAMENT_COLS, GAME_COLS, PERFORMANCE_COLS

from src.data.data_scraping import get_raw_players, get_raw_games, get_last_commit_sha, get_file_changes
from src.data.data_cleaning import to_datetime


@pytest.mark.slow
def test_get_raw_players(sample_players):
    assert isinstance(sample_players, pd.DataFrame)
    # these columns are expected to extract player details
    assert np.isin(sample_players.columns, list(PLAYER_COLS.values())).all()


@pytest.mark.slow
def test_get_raw_games(sample_games):
    assert isinstance(sample_games, pd.DataFrame)
    # ensure all expected year (conftest.py sets year)
    assert all(to_datetime(sample_games[TOURNAMENT_COLS["start_date"]]).dt.year == 2020)

    # columns required to extract tournament details from csv
    assert np.isin(list(TOURNAMENT_COLS.values()), sample_games.columns).all()
    # columns required to extract game details from csv
    assert np.isin(list(GAME_COLS.values()), sample_games.columns).all()

    # winner and loser performance columns have a prefix thus we remove said prefix before ensuring cols present
    cols_without_prefix = [col[2:] for col in sample_games.columns]
    # columns required to extract winner and loser performance details from csv
    assert np.isin(list(PERFORMANCE_COLS.values()), cols_without_prefix).all()


@ pytest.mark.slow
def test_get_last_commit_sha():
    assert isinstance(get_last_commit_sha(), str)


@ pytest.mark.slow
def test_get_file_changes():
    expected_files = ["wta_matches_2020.csv", "wta_matches_1999.csv",
                      "wta_matches_1998.csv", "wta_matches_1991.csv", "wta_matches_1984.csv"]

    changes = {file_name: patch for file_name, patch in
               get_file_changes('ca6476a75d180758723ac892c56bf334343053ab',
                                'c6b74fbccd7a0eae5604a2a9e06da2e3d79a2c65')}

    assert np.isin(list(changes.keys()), expected_files).all()
