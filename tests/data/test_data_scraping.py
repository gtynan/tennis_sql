import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.data.data_scraping import get_raw_players, get_raw_games


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
