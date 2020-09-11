import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.data.data_scraping import get_raw_players, get_raw_games, get_last_commit_sha, get_file_changes


@pytest.mark.slow
def test_get_raw_players(sample_players):

    assert len(sample_players) == 5
    assert isinstance(sample_players, pd.DataFrame)


@pytest.mark.slow
def test_get_raw_games(sample_games):

    assert len(sample_games) == 5
    assert isinstance(sample_games, pd.DataFrame)
    # ensure first and last row's date correct year
    assert datetime.strptime(str(sample_games.loc[0, 'tourney_date']), '%Y%m%d').year == 2020
    assert datetime.strptime(str(sample_games.loc[sample_games.index[-1], 'tourney_date']), '%Y%m%d').year == 2020


@pytest.mark.slow
def test_get_last_commit_sha():
    assert isinstance(get_last_commit_sha(), str)


@pytest.mark.slow
def test_get_file_changes():
    expected_files = ["wta_matches_2020.csv", "wta_matches_1999.csv",
                      "wta_matches_1998.csv", "wta_matches_1991.csv", "wta_matches_1984.csv"]

    changes = {file_name: patch for file_name, patch in
               get_file_changes('ca6476a75d180758723ac892c56bf334343053ab',
                                'c6b74fbccd7a0eae5604a2a9e06da2e3d79a2c65')}

    assert np.isin(list(changes.keys()), expected_files).all()
